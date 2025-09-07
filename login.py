import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os
import pandas as pd
import io

# Supabase configuration
supabase = None
def get_client(baseclient):
    global supabase
    supabase = baseclient
BUCKET = "user-files" # don't forget to fix the bucket issues

# -- helper functions

def create_default_csv_bytes():
    """ Retunr bytes of the default CSV the user should start with"""
    df = pd.DataFrame(columns=["date", "has_period_started", "flow", "pain", "mood"])
    csv_bytes = df.to_csv(index=False).encode("UTF-8")
    return csv_bytes

def upload_user_files(user_id: str, filename: str, file_bytes: bytes):
    """ upload bytes to supabase storage under user_id/filename"""
    path = f"{user_id}/{filename}"    
    res = supabase.storage.from_(BUCKET).upload(path,
                                                 file_bytes,
                                                 {"content-type": "text/csv", "upsert":"true"}
    )
    return res

def download_user_files(user_id: str, filename: str):
    """ download file bytes from supabase storage"""
    path = f"{user_id}/{filename}"
    res = supabase.storage.from_(BUCKET).download(path)
    return res

def delete_user_file(user_id: str, filename: str):
    """ delete file from supabase storage"""
    path = f"{user_id}/{filename}"
    res = supabase.storage.from_(BUCKET).remove([path])
    return res

def list_user_files(user_id: str):
    """ list all files for a user"""
    try:
        res = supabase.storage.from_(BUCKET).list(user_id)
        return res
    except Exception as e:
        return []

    
def user_is_logged_in():
    return "user_id" in st.session_state and st.session_state["user_id"]

def get_user_id_from_auth_response(resp):
    """ Extract user ID from Supabase auth response"""
    try:
        # handling different response formats
        if hasattr(resp, "user") and resp.user and hasattr(resp.user, "id"):
            return resp.user.id
        elif isinstance(resp, dict):
            if "user" in resp and resp["user"] and "id" in resp["user"]:
                return resp["user"]["id"]
    except Exception as e:
        st.error(f"Error extracting user ID: {e}")
    return None


# --- Streamlit app UI

def app():

    st.title("Welcome to Auntie Alade")

    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None
    
    if "username" not in st.session_state:
        st.session_state["username"] = None

    st.write("")
    signup_tab, login_tab = st.tabs(["Sign up", "Login"])
    

    with signup_tab:
        st.subheader("Create an account")
        username = st.text_input("Enter a username", key= "signup_username")
        password = st.text_input("Create a password", type="password", key="signup_password")

        if st.button("Sign up"):
            if not username or not password:
                st.error("Please enter both username and password.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long.")

            else: 
                try:
                    
                    # creating email from username
                    email = f"{username}@alade.local"

                    # sign up with supabase auth
                    res = supabase.auth.sign_up({
                        "email": email,
                        "password": password
                    })

                    user_id = get_user_id_from_auth_response(res)

                    if user_id:
                        # default CSV file
                        csv_bytes = create_default_csv_bytes()

                        try: 
                            upload_user_files(user_id, "period_data.csv", csv_bytes)
                            st.success("Account created and your data file was initialized")
                        except Exception as e:
                            st.warning("Account created but initial file upload failed: " + str(e))  

                        # saving the session
                        st.session_state["user_id"] = user_id
                        st.session_state["username"] = username
                        st.rerun()
                    else:
                        st.error("Sign up failed. Please try again.")

                except Exception as e:
                    error_msg = str(e)
                    if "already registered" in error_msg.lower():
                        st.error("This username is already taken, Please choose a different one")
                    else:   
                        st.error(f"Sign up failed: {e}")  
   
    with login_tab:
        st.subheader("Login with your username and password")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if not username or not password:
                st.error("Please enter both fields")
            else:
                try: 
                    # converting username to email
                    email = f"{username}@alade.local"

                    # sign up with supabase auth
                    res = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })
                    user_id = get_user_id_from_auth_response(res)

                    if user_id:
                        st.session_state["user_id"] = user_id
                        st.session_state["username"] = username
                        st.rerun()
                    else:
                        st.error("Login failed. Please check your credentials")
                except Exception as e:
                    error_msg = str(e)
                    if "invalid" in error_msg.lower():
                        st.error("Invalid username or password.")
                    else:
                        st.error(f"Login failed: {error_msg}" )



