from streamlit_cookies_controller import CookieController # some user data will be saved in a cookie
from streamlit_option_menu import option_menu
from datetime import date
import streamlit as st 
import pandas as pd 
import altair as alt
import os


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


# --- page config
st.set_page_config(
    page_title= "Auntie Alade",
    #page icon = (I'll add it later)
    initial_sidebar_state= "expanded" # making the sidebar open by default
)

page_header = st.empty() # used to erase and replace page header
cookies = CookieController()

sucess_save = False 

# --- Helper functions

# to change the header
def change_header(new_header: str) -> None:
    global page_header
    page_header.empty() # erasing the previous header
    page_header.header(new_header) # adding the new one

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
    global sucess_save
    try:
        df = pd.read_csv(file_path)

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index= True)
        df.drop_duplicates(inplace=True, keep= "last", subset=["date"])
     
    except FileNotFoundError:
        st.write("file not found")
        # creating a new data frame if no file exists
        df = pd.DataFrame([new_row])

    df.to_csv(file_path, index= False)
    sucess_save = True
   



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


# --- tracking ongoing cycle state

if "on_period" not in st.session_state:
    st.session_state.on_period = False

if "current_start" not in st.session_state:
    st.session_state.current_start = None

if "cycles" not in st.session_state: # recording cycle
    st.session_state.cycles = []

if "period_date" not in st.session_state:
    st.session_state.period_date = None

period_end = False        
data_recorded = False

# --- period data input
if saved_file_path:

    if not st.session_state.on_period: 

        if st.button("Start period"):
            st.session_state.on_period = True
            st.session_state.current_start = str(date.today())
            st.success(f"Period started on {st.session_state.current_start}")


            # recording period data
            st.session_state.period_date = st.session_state.current_start
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
            data_recorded = True

    else:
        st.info(f"Period ongoing since {st.session_state.current_start}")


        if st.button("End Period"):
            end_date = date.today()
            df = pd.read_csv(saved_file_path)
            cycle_lenght = (pd.to_datetime(end_date) - pd.to_datetime(st.session_state.current_start)).days
            st.success(f"Period ended on {end_date}")

            # saving the cycle
            st.session_state.cycle.append(
                {
                    "start": st.session_state.current_start,
                    "end": end_date,
                    "length": cycle_lenght
                }
            )

            # reseting everything for the next cycle
            st.session_state.on_period = False
            st.session_state.current_start = None
       
        st.session_state.period_date = str(st.date_input("Today's date") )
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
        
        data_recorded = True

    if st.session_state.period_date :
        data_already_entered = st.session_state.period_date in df["date"].tolist()
        st.write(data_already_entered)
    else:
        data_already_entered = False

    if "change_message" not in st.session_state:
        # flag to know when to change the message
        st.session_state.change_message = False 

    if st.button("Save period data", disabled= data_already_entered):
        new_row = {
        "date": st.session_state.period_date ,
        "has_period_started": "Yes",
        "flow": st.session_state.flow,
        "pain": st.session_state.pain,
        "mood": st.session_state.mood
        }
        save_info(new_row, saved_file_path)
        st.session_state.change_message = not st.session_state.change_message
    
    if st.session_state.change_message:
        st.success("Your period data has been saved!")
    else:
            if sucess_save:
                st.info("You already recorded your period data")
            elif data_already_entered:
                st.info("You already recorded your period data")

    # showing chart if we have at least one cycle
    if st.session_state.cycles:
        cycle_df = pd.DataFrame(st.session_state.cycles)

        # getting months and years for filtering
        cycle_df["year"] = pd.to_datetime(cycle_df["start"]).dt.year
        cycle_df["month"] = pd.to_datetime(df["start"]).dt.month_name()

        # filtering options
        years = st.multiselect("Filter by year:", options= cycle_df["year"].unique(), default= cycle_df["year"].unique())
        months = st.multiselect("Filter by month:", options= cycle_df["month"].unique(), default= cycle_df["month"].unique())

        # bar chart
        chart = (
            alt.Chart(filtered_df)
            .mark_bar()
            .encode(
                x=alt.X("start:T", title="Cycle Start Date"),
                y= alt.Y("length:Q", title="Cycle Length (days)"),
                tooltip= ["start", "end", "lenght"]
            
            )
        )

        st.altair_chart(chart, use_container_width=True)

    if st.session_state.current_start is None:
        if st.button("Start New Period"):
            st.session_state.current_start = date.today()
    
        
# periods = df["date"].tolist()

# dates = pd.to_datetime(periods)

# cycle_df = pd.DataFrame({
#     "Start Date": dates,
#     "Cycle Length (days)": dates.to_series().diff().dt.days
# })

# st.write(" ")
# st.subheader("Cycle length")
# st.write(" ")
# # line chart of cycle lenghts
# st.line_chart(cycle_df.set_index("Start Date")["Cycle Length (days)"])