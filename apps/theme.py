
import streamlit as st

if "theme" not in st.session_state:
    st.session_state["theme"] = "light" #default light

def apply_custom_theme():
    theme = st.session_state.get("theme", "light").lower() #default light

    if theme.lower() == "dark":
        st.markdown(
            """
            <style>

                header[data-testid="stHeader"] {
                    background-color: #BA68A0 !important;
                }
                body {
                    background-color: #BA68A0;
                    color: #EAEAEA;
                }

                .stApp{
                    background-color: #BA68A0
                }
                .stRadio label, .stMarkdown, .stButton label, h1, h2, h3{
                    color: #EAEAEA !important;
                }

                .css-1d391kg, .stTextInput, .stSelectbox, .stFileUploader {
                    background-color: #BA68A0!important;
                    color: #EAEAEA !important;
                }

                label, .stFrileUploader label, .stTextInput label, .stSelectbox label, .stSlider label {
                    color: #EAEAEA !important
                }

                .stButton button {
                    background-color: #DBA7C9 !important;
                    color: #EAEAEA !important;
                    border: none;
                }

                div[data-testid="stFileUploader"] section button {
                    background-color: #DBA7C9 !important;
                    color: #EAEAEA !important;
                }
 
                div[data-testid="stChatInput"]{
                    background-color: #BA68A0 !important;
                }

                .stButton buttoh:hover{
                    background-color: #9a459a !important;
                }

                .stSidebar{
                    background-color: #914377 !important;
                }

                foot{
                    background-color: #BA68A0
                }
                
            </style>
            """,
            unsafe_allow_html= True
        )

        return {
            "container": {"padding": "5px", "background-color": "#BA68A0"},
            "nav-link-selected": {"background-color": "#DBA7C9", "color":"white"},
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