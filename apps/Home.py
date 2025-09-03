from streamlit_cookies_controller import CookieController # some user data will be saved in a cookie
from streamlit_option_menu import option_menu
from datetime import date
import streamlit as st 
import pandas as pd 
import altair as alt
import os


def app():
    cookies = CookieController()
    sucess_save = False 

    st.title("Period tracker")


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

        if not st.session_state.on_period: # not currently on period

            if st.button("Start period"):
                st.session_state.on_period = True
                st.session_state.current_start = str(date.today())
                st.success(f"Period started on {st.session_state.current_start}")

        else:
            st.info(f"Period ongoing since {st.session_state.current_start}")

            if st.button("End Period"):
                df = pd.read_csv(saved_file_path)
                end_date = df.iloc[-1]["date"]
                cycle_lenght = (pd.to_datetime(end_date)- pd.to_datetime(st.session_state.current_start)).days
                st.success(f"Your period ended on {end_date}")

                # saving the cycle
                st.session_state.cycles.append({
                    "start": st.session_state.current_start,
                    "end": end_date,
                    "length": cycle_lenght
                }
                )

                # going back to start period button
                st.session_state.on_period = False

            # recording period data
            st.session_state.period_date = str(st.date_input("Today's date"))
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
                st.session_state.current_start = None

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
        
        # Showing chart if we have cycles

        if st.session_state.cycles:
            cycle_df = pd.DataFrame(st.session_state.cycles)
            cycle_df["year"] = pd.to_datetime(cycle_df["start"]).dt.year
            cycle_df["month"] = pd.to_datetime(cycle_df["start"]).dt.month_name()

            years = st.multiselect("Filter by year: ", options=cycle_df["year"].unique(), default=cycle_df["year"].unique())
            months = st.multiselect("Filter by month: ", options=cycle_df["month"].unique(), default=cycle_df["month"].unique())

            filtered_df = cycle_df[(cycle_df["year"].isin(years)) & (cycle_df["month"].isin(months))]

            chart = (
                alt.Chart(filtered_df)
                .mark_bar(color="#BA5DBA", size= 50)
                .encode(
                    x= alt.X("start:T", title="Cycle Start Date"),
                    y= alt.Y("length:Q", title="Cycle Length (days)"),
                    tooltip= ["start", "end", "length"]
                )
            )

            st.altair_chart(chart, use_container_width= True)

            # predicting the next period
            if len(cycle_df) > 1:
                avg_cycle = int(cycle_df["length"].mean())
                last_end = pd.to_datetime(cycle_df["end"].iloc[-1])
                predicted_date = last_end + pd.timedelta(days=avg_cycle)

                st.subheader("Next Period Prediction")
                st.write(f"Your average cycle length is **{avg_cycle} days**")
                st.success(f"Expected next period: **{predicted_date.date()}**")
            else:
                st.info("Not enough cycle data to predict the next period yet.")
