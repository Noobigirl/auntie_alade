from streamlit_option_menu import option_menu
import streamlit as st 
import apps.Home as Home
import apps.Auntie as Auntie
import apps.MoodTracker as mood
import apps.Settings as settings
from apps.theme import apply_custom_theme


# --- custom page styling
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"

st.markdown(   
    """
    <style>

    /* Change button focus color */ 
    button:focus, button: focus-visible {
        outline : none !important;
        box-shadow: 0 0 0 3px #FF5733 !important;
    }

 
    /* Changing header */
    h1, h2{
        border-bottom: 3px solid #DEABDE;
        padding-bottom: 0.3rem;
        margin-bottom: 1rem
    }

    p {
        font-size: 1.2rem !important;
        line-heigt: 1.6;
    }

    </style>
    """, 
    unsafe_allow_html= True
)


# --- page config
st.set_page_config(
    page_title= "Auntie Alade",
    #page icon = (I'll add it later)
    initial_sidebar_state= "expanded" # making the sidebar open by default
)


# --- App UI 

main_page_content = st.empty()
# sidebar menu
theme = st.session_state["theme"]
menu_styles = apply_custom_theme()
with st.sidebar: # everything that goes inside the sidebar

    selected_page = option_menu(
        menu_title = "Menu",
        menu_icon= "bi bi-three-dots-vertical",
        options = ["Home", "Mood tracker", "Talk to Auntie", "Settings"],
        icons = ["bi bi-house-door-fill",  # got the icons from bootstrap
                "bi bi-emoji-laughing", 
                "bi bi-heart", 
                "bi bi-gear-wide-connected"
                ],
        default_index = ["Home", "Mood tracker", "Talk to Auntie", "Settings"].index(st.session_state["current_page"]), # selects "Home" as the default page,,
        styles= menu_styles
    
    )


# --- page handling
if selected_page == "Home":
   Home.app()
elif selected_page == "Mood tracker":
   mood.app()
elif selected_page == "Talk to Auntie":
    Auntie.app()
else:
   settings.app()

