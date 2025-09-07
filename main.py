from streamlit_option_menu import option_menu
import streamlit as st 
import supabase
from supabase import create_client
import apps.Home as Home
import apps.Auntie as Auntie
import apps.MoodTracker as mood
import apps.Settings as settings
import login
from apps.theme import apply_custom_theme
from dotenv import load_dotenv
import os


load_dotenv()
# configuring supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if "supabase" not in st.session_state:
    st.session_state.supabase= create_client(SUPABASE_URL, SUPABASE_KEY)
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

# --- custom page styling
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

if not st.session_state["user_id"]:
    login.get_client(st.session_state.supabase)
    login.app()

else:
    # --- page config
    st.set_page_config(
        page_title= "Auntie Alade",
        #page icon = (I'll add it later)
        initial_sidebar_state= "expanded" # making the sidebar open by default
    )


    # --- App UI 

    main_page_content = st.empty()
    # sidebar menu
    menu_styles = apply_custom_theme()
    with st.sidebar: # everything that goes inside the sidebar

        selected_page = option_menu(
            menu_title = "Menu",
            menu_icon= "bi bi-three-dots-vertical",
            options = ["Home", "Talk to Auntie", "Settings"],
            icons = ["bi bi-house-door-fill",  # got the icons from bootstrap
                    "bi bi-emoji-laughing", 
                    "bi bi-gear-wide-connected"
                    ],
            default_index = ["Home", "Talk to Auntie", "Settings"].index(st.session_state["current_page"]), # selects "Home" as the default page,,
            styles= menu_styles
        
        )

        # showing logged in user's info
        if st.session_state["user_id"]:
            st.write("")
            st.success(f"Welcome back, {st.session_state['username']}!")
            if st.button("Log out"):
                try:
                    supabase.auth.sign_out()
                except:
                    pass

                st.session_state["user_id"] = None
                st.session_state["username"] = None
                st.rerun()
    



    # --- page handling
    if selected_page == "Home":
        Home.get_client(st.session_state.supabase)
        Home.app()
    elif selected_page == "Talk to Auntie":
        Auntie.app()
    else:
        settings.get_user_id(st.session_state["user_id"])
        settings.get_client(st.session_state.supabase)
        settings.app()

