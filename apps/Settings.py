import streamlit as st
import pandas as pd
import os

DATA_FILE = "moods.csv"

def apply_custom_theme():
    theme = st.session_state.get("theme", "light")

    if theme == "Dark":
        st.markdown(
            """
            <style>
                body {
                    background-color: #1e1e1e;
                    color: #f0f0f0;
                }

                .stApp {
                    background-color: #1e1e1e;
                }

                .stButton>button {
                    background-color: #DEABDE;
                    color: black;

                }
            </style>
            """,
            unsafe_allow_html= True
        )
    else:
        st.markdown(
            """
            <style>
                body{
                    background-color: #F7DFF7;
                    color: black;

                }
                .stApp{
                    background-color: #F7DFF7;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

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
