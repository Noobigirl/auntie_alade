import streamlit as st
import pandas as pd
import os

DATA_FILE = "moods.csv"

def app():
    st.title("Settings")

    st.markdown(
        "I hope you like this app I made for the **Athena Awards hackathon**."
        "Check out the source code below!"
        )
    st.link_button("Github repo", "") # add link to the repo

    st.subheader("Privacy & Data Security")
    st.markdown(
        """
        - This app does **not** send your period or mood data to any sever.
        - You are responsible for saving and uploading you own data files.
        
        """
        )
