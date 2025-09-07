import streamlit as st
import pandas as pd
import apps.theme as th
from login import (
    user_is_logged_in,
    st,
    upload_user_files,
    download_user_files,
    delete_user_file,
    list_user_files,
)

DATA_FILENAME = "period_data.csv"  # the main file every user has

# Supabase configuration
supabase = None
user_id = None
BUCKET = "user-files"

def get_client(baseclient):
    global supabase
    supabase = baseclient

def get_user_id(iduser):
    global user_id
    user_id = iduser


def app():
    th.apply_custom_theme()
    st.title("Settings")
    st.write(" ")
    st.markdown(
        "I hope you like this app I made with love"
        "Check out the source code below!"
        )
    st.link_button("Github repo", "https://github.com/Noobigirl/auntie_alade") # add link to the repo

    st.subheader("Privacy & Data Security")
    st.markdown(
        """
        - This app does **not** send your period or mood data to any sever.
        - You are responsible for saving and uploading you own data files.
        - The chatbot (*Auntie Alade*) is based on **DeepSeek v3.1 via OpenRouter**.
          Check [OpenRouter's policy](https://openrouter.ai/docs/features/privacy-and-logging) for details on data privacy
        """
    )

    st.divider()
    
    # theme toggle
    st.subheader("Change appearance")
    if st.button("Toggle themes"):
        if st.session_state["theme"] == "light":
            st.session_state["theme"] = "dark"
        else:
            st.session_state["theme"] = "light"
        
        # to stay on the settings page after reruning
        st.session_state["current_page"] = "Settings"
        st.rerun()




    st.subheader("Data Management")

    if not user_is_logged_in():
        st.warning("You need to be logged in to manage your data.")
        return
    # Check if user has any files

    files = list_user_files(user_id)
    if not files or DATA_FILENAME not in [f["name"] for f in files]:
        st.info("No data file found for your account.")
        return
    
    # Download button
    file_bytes = download_user_files(user_id, DATA_FILENAME)
    st.download_button(
        label="Download my data",
        data=file_bytes,
        file_name=DATA_FILENAME,
        mime="text/csv"
    )

    # Delete button with confirmation
    st.write("")  # spacing
    if st.button("Delete my data from Supabase"):
        confirm = st.checkbox("I confirm that I want to permanently delete my data")
        if confirm:
            delete_user_file(user_id, DATA_FILENAME)
            st.success("Your data has been deleted from Supabase.")

        

    
