
import streamlit as st

if "theme" not in st.session_state:
    st.session_state["theme"] = "dark" #default light

def apply_custom_theme():
    theme = st.session_state.get("theme", "dark").lower() #default light

    if theme.lower() == "dark": # default light
        st.markdown(
            """
            <style>
                body {
                    background-color: #914479;
                    color: #EAEAEA;
                }

                .stApp{
                    background-color: #914479
                }
                .stRadio label, .stMarkdown, .stButton label, h1, h2, h3{
                    color: #EAEAEA !important;
                }

                .css-1d391kg, .stTextInput, .stSelectbox, .stFileUploader {
                    background-color: #914479!important;
                    color: #EAEAEA !important;
                }

                label, .stFrileUploader label, .stTextInput label, .stSelectbox label, .stSlider label {
                    color: #EAEAEA !important
                }

                .stButton button {
                    background-color: #D481B6 !important;
                    color: #EAEAEA !important;
                    border: none;
                }

                .stInfo {
                    background-color: #121212
                }

                .stButton buttoh:hover{
                    background-color: #9a459a !important;
                }

                .stSidebar{
                    background-color: #49243E
                }
            </style>
            """,
            unsafe_allow_html= True
        )

        return {
            "container": {"padding": "5px", "background-color": "#914479"},
            "nav-link-selected": {"background-color": "#D481B6", "color":"white"},
            "nav-link": {
                "color": "#EAEAEA"
            },
            "menu-title": {
                "color": "#EAEAEA"
            }
        }
    else: # light theme
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

                .stButton button {
                    background-color: #EFD7EF !important;
                    color: black !impotant;
                }
            </style>
            """,
            unsafe_allow_html=True
        ),

        return {
            "container": {"padding": "5px", "background-color": "#F7DFF7"},
            "nav-link-selected": {"background-color": "#DEABDE", "color": "white"},
            "nav-link":{
                "color": "1E1E2F"
            }
        }