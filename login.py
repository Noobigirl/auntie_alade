import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os
import pandas as pd
import io
import re

load_dotenv()
# configuring supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET = "user-files" # don't forget to fix the bucket issues

# -- helper functions
def username_to_email(username: str):
    """ create a fake email so we can use superbase with auth"""

    username = username.strip().lower()
    username = re.sub(r"[^a-z0-9_\-]", "_", username)
    return f"{username}@auntie.local"

def create_default_csv_bytes():
    """ Retunr bytes of the default CSV the user should start with"""
    df = pd.DataFrame(columns=["date", "has_period_started", "flow", "pain", "mood"])
    csv_bytes = df.to_csv(index=False).encode("UTF-8")
    return csv_bytes


def upload_user_files(user_id: str, filename: str, file_bytes: bytes):
    """ upload bytes to supabase storage under user_id/filename"""
    path = f"{user_id}/{filename}"    
    res = supabase.storage.from_(BUCKET).upload(path, file_bytes, {"upsert": True})
    return res

def user_is_logged_in():
    return "user_id" in st.session_state and st.session_state["user_id"]

def get_user_id_from_auth_respons(resp):

    if isinstance(resp, dict):
        if "user" in resp and resp["user"] and "id" in resp["user"]:
            return resp["user"]["id"]
        if "data" in resp and isinstance(resp["data"], dict) and "user" in resp["data"] and resp["data"]["user"]:
            return resp["data"]["user"].get("id")
    
    try:
        user = getattr(resp, "user", None)
        if user and hasattr(user, "id"):
            return user.id
    except Exception:
        pass

    return None


# --- Streamlit app UI

def app():
    st.title("Sign up/ Login")

    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None
    
    st.write("")
    tabs = st.tabs(["Sign up", "Login"])
    signup_tab, login_tab = tabs

    with signup_tab:
        st.subheader("Create an account")
        username = st.text_input("Enter a username", key= "signup_username")
        password = st.text_input("Create a password", type="password", key="signup_password")

        if st.button("Sign up"):
            if not username or not password:
                st.error("Please enter both username and password.")
            else:
                email = username_to_email(username)

                # Create usr with Supabase Auth
                try:
                    resp = supabase.auth.sign_up({"email": email, "password": password})
                except Exception as e:
                    st.error(f"Sign up failed: {e}")  
                    resp = None 
                
                if user_id:
                    st.success("Account created")

                    csv_bytes = create_default_csv_bytes()

                    try:
                        upload_user_file(user_id, "period_data.csv", csv_bytes)
                        st.success("Your data file was created in storage.")
                    except Exception as e:
                        st.warning("Account created but initial file upload failed: " + str(e))

                    # saving the session
                    st.session_state["user_id"] = user_id
                    st.session_state["username"] = username
                    st.session_state["supabase_session"] = resp.get("session")
                else:
                    st.error("Could not create account")

    with login_tab:
        st.subheader("Login with your username and password")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if not username or not password:
                st.error("Please enter both fields")
            else:
                email = username_to_email(username)

                try:
                    resp = supabase.auth.sign_in_with_password({"email": email, "password": password})

                except Exception as e:
                    st.error(f"Login failed: {e}")
                    resp = None

                user_id = get_user_id_from_auth_response(resp)
                if user_id:
                    st.success("Logged in!")
                    st.session_state["user_id"] = user_id
                    st.session_state["username"] = username
                else:
                    st.error("Login failed - wrong username/password")



