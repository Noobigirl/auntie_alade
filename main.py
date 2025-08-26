import streamlit as st 
from streamlit_option_menu import option_menu

page_header = st.empty()

# --- helper function 
def change_header(new_header: str) -> None:
    global page_header
    page_header.empty() # erasing the previous header
    page_header.header(new_header) # adding the new one


# sidebar menu
with st.sidebar: # everything that goes insid the sidebar

    selected_page = option_menu(
        menu_title = "Menu",
        options = ["Home", "Mood tracker", "Talk to Auntie", "Settings"],
        # icons  to add later (bootstrap)
        default_index=0 # selects "Home" as the default page
    )


# main page
if selected_page == "Home" :
    change_header("Home Page")
else:
   change_header("Random Page")

# st.header ("Menu")
# page = st.radio("Go to", ["Home", "Mood tracker", "Talk to Auntie", "Settings"])