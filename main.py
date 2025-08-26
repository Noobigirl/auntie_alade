import streamlit as st 
import os
import json
import pandas as pd 
from streamlit_option_menu import option_menu

CONFIG_FILE = "config.json" # to remember the CSV file path
TEST_DATA_FILE = "period_data.csv" # each user will have its how CSV for privacy
page_header = st.empty()


# --- Helper functions
def change_header(new_header: str, divider = "red") -> None:
    global page_header
    page_header.empty() # erasing the previous header
    page_header.header(new_header, divider= divider) # adding the new one


def save_config(csv_path):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"csv_path": csv_path}, f)


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f).get("csv_path") # getting the latest path
    return None

def create_default_csv():
    df = pd.DataFrame(columns=["date","has_period_started","flow","mood"])
    default_file = "my_period_data.csv"
    df.to_csv(default_file, index=False)
    return default_file


# --- App UI

# -- Config

csv_path = load_config()

def upload_file():
    period_data = st.file_uploader("Upload your period CSV", type = "csv")

    if period_data is not None:
        csv_path = period_data.name
        with open(csv_path, "wb") as f:
            f.write(period_data.getbuffer())
        save_config(csv_path)
        st.success("Period data uploaded and saved for next time!")
        df = pd.read_csv(csv_path)

    # if we find the path and the file is exsisting there
if csv_path and os.path.exists(csv_path):
    st.success(f"Using your saved period data: {csv_path}")
    df = pd.read_csv(csv_path)
else:
    # prompting the user to upload a file or create a new file
    upload = st.checkbox("Create a new period data file", value= False)
    create = st.checkbox("Upload period data", value= False)
    if upload:
        upload_file()
    elif create:
        csv_path = create_default_csv()
        save_config(csv_path)
        st.success(f"New data file created: {csv_path}")

        with open(csv_path, "rb") as f:
            st.download_button("Download CSV", f, file_name=csv_path)
        df = pd.read_csv(csv_path)


# page "backend" 



#load_data()
# page options
st.set_page_config(
    page_title= "Auntie Alade",
    #page icon =
    initial_sidebar_state= "expanded" # sidebar open by default
)


# sidebar menu
with st.sidebar: # everything that goes insid the sidebar

    selected_page = option_menu(
        menu_title = "Menu",
        menu_icon= "bi bi-three-dots-vertical",
        options = ["Home", "Mood tracker", "Talk to Auntie", "Settings"],
        icons = ["bi bi-house-door-fill",  # got the icons from bootstrap
                "bi bi-emoji-laughing", 
                "bi bi-heart", 
                "bi bi-gear-wide-connected"],
        default_index = 0 # selects "Home" as the default page
    )


# main page
if selected_page == "Home" :
    change_header("Period Tracker")

elif selected_page == "Mood tracker":
   change_header("How do we feel today?")

elif selected_page == "Talk to Auntie":
    change_header("Get advice from auntie Alade")

else:
    change_header("Settings")

st.date_input("Select period start date")