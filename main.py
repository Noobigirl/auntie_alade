from streamlit_cookies_controller import CookieController # some user data will be saved in a cookie
from streamlit_option_menu import option_menu
import streamlit as st 
import pandas as pd 
import os


# --- page config
st.set_page_config(
    page_title= "Auntie Alade",
    #page icon = (I'll add it later)
    initial_sidebar_state= "expanded" # making the sidebar open by default
)

page_header = st.empty() # used to erase and replace page header
cookies = CookieController()


CONFIG_FILE = "config.json" # to remember the CSV file path
TEST_DATA_FILE = "period_data.csv" # each user will have its how CSV for privacy




# --- Helper functions

# to change the header
def change_header(new_header: str, divider = "grey") -> None:
    global page_header
    page_header.empty() # erasing the previous header
    page_header.header(new_header, divider = divider) # adding the new one

# file handling
def upload_file():
    period_data = st.file_uploader("Upload your period data CSV", type = "csv")

    if period_data is not None:
        # saving the file
        os.makedirs("user_files", exist_ok= True)
        file_path = os.path.join("user_files", period_data.name)
        
        with open(file_path, "wb") as f:
            f.write(period_data.getbuffer())
        
        st.success(f"File uploaded and saved at {file_path}")

        # storing the file path in cookies
        cookies.set("period_file_path", file_path)
        return file_path
    return None

    
def create_file() : # creating a new csv an letting the user donwload it
    df = pd.DataFrame(columns=["has_period_started","date","pain","flow","mood"])
    csv_bytes = df.to_csv(index=False).encode("UTF-8")

    st.success("New period data file created! Please download it and keep it safe")
    st.download_button(
        label= "Download CSV",
        data= csv_bytes,
        file_name= "my_period_data.csv",
        mime="text/csv"
    )

    # saving a reference just in case
    os.makedirs("user_files", exist_ok=True)
    file_path = os.path.join("user_files", "my_period_data.csv")

    with open(file_path, "wb") as f:
        f.write(csv_bytes)
    # storing file path in cookie
    cookies.set("period_file_path", file_path)
    # creating the CSV file
    return file_path

# saving the entered data to the CSV file
def save_info(new_row, file_path):
    try:
        df = pd.read_csv(file_path)

        # checking if we already recorded the date's period

        check = (df["date"] == new_row["date"]) & (df["has_period_started"] == new_row["has_period_started"])

        if check.any():
            
            # only updating the other fields
            df.loc[check,
            ["pain", "flow", "mood"]] = [
                new_row["has_period_started"],
                new_row["pain"],
                new_row["flow"], 
                new_row["mood"]
            ]
        else:
            # adding a new row to the CSV
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index= True)

    except FileNotFoundError:
        # creating a new data frame if no file exists
        df = pd.DataFrame([new_row])

    df.to_csv(file_path, index= False)
    st.success("Your period data has been saved!")


# --- loading or creating a period data CSV file
saved_file_path = cookies.get("period_file_path")
df = None

if saved_file_path and os.path.exists(saved_file_path):

    try: # trying to read the exsisting data file
        df = pd.read_csv(saved_file_path)
        st.success(f"Using your saved period data: {saved_file_path}")

    except Exception as e: # in case it is moved or deleted
        st.error(f"Could not read saved file: {e}")
        st.warning("Please re-upload or create a new file.")

        col1, col2 = st.columns(2)
        with col1:
            new_path = upload_file()
            if new_path: saved_file_path = new_path

        with col2: 
             # just to center the button
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")

            if st.button("Create new file"):
                saved_file_path = create_file()
        # in that case, what do we do next?

else:

    st.info("No saved file found. Please upload or create one.")
    col1, col2 = st.columns(2)

    with col1:
        saved_file_path = upload_file()

    with col2:

        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")

        if st.button("Create new file", use_container_width= True):
            saved_file_path = create_file()


# --- App UI 

main_page_content = st.empty()
# sidebar menu
with st.sidebar: # everything that goes insid the sidebar

    selected_page = option_menu(
        menu_title = "Menu",
        menu_icon= "bi bi-three-dots-vertical",
        options = ["Home", "Mood tracker", "Talk to Auntie", "Settings"],
        icons = ["bi bi-house-door-fill",  # got the icons from bootstrap
                "bi bi-emoji-laughing", 
                "bi bi-heart", 
                "bi bi-gear-wide-connected"
                ],
        default_index = 0 # selects "Home" as the default page
    )


# --- main page
if selected_page == "Home" :
    change_header("Period Tracker")

elif selected_page == "Mood tracker":
   change_header("How do we feel today?")

elif selected_page == "Talk to Auntie":
    change_header("Get advice from auntie Alade")

else:
    change_header("Settings")



if "period_status" not in st.session_state:
    st.session_state.period_status = None

# user should only be able to select either or 
st.session_state.period_status = st.radio(
    "Did your period start?",
    ["Yes", "No"],
    index= None
)


# allowing input only if file exists
if saved_file_path:
    if st.session_state.period_status == "Yes":
        st.session_state.period_date = st.date_input("Select period start date") 

        st.session_state.pain = st.slider("Pain level (0= none, 10 = severe)", 0, 10, 5)
        st.session_state.flow = st.selectbox(
            "How heavy is your period: ",
            ["light", "normal", "heavy", "I'm BLEEDING"]
        )

        st.session_state.mood = st.selectbox(
            "How do you feel",
            ["Happy", "Sad", "Normal", "Angry", "Other"]
        )
        
        if st.session_state.mood == "Other":
            custom_mood = st.text_input("Tell auntie your mood")
            mood = custom_mood if custom_mood else "Other"

        # date = st.session_state.get("period_date")
        # pain = st.session_state.get("pain")
        # flow = st.session_state.get("flow")
        # mood_record = st.session_state.get("mood")
        
        if st.button("Save period data"):
            new_row = {
            "date": st.session_state.period_date ,
            "has_period_started": "Yes",
            "flow": st.session_state.flow,
            "pain": st.session_state.pain,
            "mood": st.session_state.mood
            }

            save_info(new_row, saved_file_path)
    

    elif st.session_state.period_status == "No":
        st.write("Don't forget to record your next period")
        st.write("You can talk to auntie if there is anything you need.")

        
    

    