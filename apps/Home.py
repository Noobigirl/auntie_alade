import theme
from datetime import date, timedelta, datetime
import streamlit as st
import pandas as pd
import altair as alt
import io 
import calendar
from supabase import create_client
import os
from dotenv import load_dotenv


# Supabase configuration
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
BUCKET = "user-files"

# Helper functions for Subapase storage

def upload_user_file(user_id: str, filename: str, file_bytes: bytes):
    """Upload bytes to supabase storage under user_id/filename"""
    path = f"{user_id}/{filename}"
    res = supabase.storage.from_(BUCKET).upload(path,
                                                file_bytes,
                                                {"content-type":"text/csv", "upsert":"true"}

    )
    return res

def download_user_files(user_id: str, filename: str):
    """Download file bytes from supabase storage"""
    path = f"{user_id}/{filename}"
    try:
        res = supabase.storage.from_(BUCKET).download(path)
        return res
    except Exception as e:
        return None

def create_prediction_calendar(predicted_dates):
    """ Create a calendar view with predicted period dates highlighted"""
    if not predicted_dates:
        st.info("No prediction available yet - track a few cycles to see predictions!")
        return
    
    # get current date and the prediction month
    today = datetime.now()
    pred_date = predicted_dates[0]

    # creating a calendar for the prediction month
    cal = calendar.monthcalendar(pred_date.year, pred_date.month)
    month_name = calendar.month_name[pred_date.month]

    st.subheader(f"Perido Prediction calendar - {month_name} {pred_date.year}")

    # creating calendar HTML

    calendar_html - f"""

    <sytle>
    .calendar{{
        display: grid;
        grip-templates-columns: repeat(7, 1fr);
        gap: 10px;
        max-width: 700px;
        margin: 20px 0;
    }}
    .day{{
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #ddd;
        border-radius: 8px;
        color: #333;
        font-weight: 500;
    }}
    .day-header {{
        font-weight: bold;
        background: #f0f2f6;
        color: #262730;
    }}
    .predicted {{
        background: #ff69b4 !important;
        color: white !important;
        font-weight: bold;
        border: 2px solid #e91e63;
    }}
    .today {{
        background: #4CAF50 !important;
        color: white !important;
        font-weight; bold;
    }}
    .empty {{
        border: none;
        background: transparent;
    }}
    </style>
    <div class="calendar">
    """
    
    #day headers

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for day in days:
        calendar_html += f'<div class="day day-header">{day}</div>'

    # Calendar days
    for week in cal;
        for day in week:
            if day == 0:
                calendar_html +='<div class="day empty"></div>'
            else:
                day_date = datetime(pred_date.year, pred_date.month, day)
                css_class = "day"
            
                # checking if it's today
                if day_date.date() == today.date():
                    css_class += " today"
                #check if it's a predicted period day
                elif any(abs((day_date.date()- p.date())).days)
                    css_class += " predicted"

                calendar_html += f'<div class="{css_class}">{day}</div>'

    calendar_html += "</div>"

    # legend
    calendar_html += """
    <div style ="margin-top: 20px;">
        <p>🟢 <span style="color: #4CAF50;"> Today</span> |
           💗 <span style="color: #ff69b4;"> Predicted Period (+-2days)</span></p>
    </div>
    """

    st.components.v1.html(calendar_html, height = 400)




def app():
    success_save = False

    st.title("Period tracker")
    st.write("")

    # Get current user ID
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("Please log in to access the period tracker.")
        return
    
    PERIOD_FILENAME = "period_data.csv"

    # loading userfile data
    
    def load_user_data():

        try:
            file_bytes = download_user_file(user_id, PERIOD_FILENAME)
            if file_bytes:
                # converting bytes to DataFrame
                csv_string = file_bytes.decode("utf-8")
                df = pd.read_csv(io.StringIO(csv_string))
                return df
            else:
                return None
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None
        
    # saving the entered data to supabase

    def save_info(new_row):
        global success_save
        try:
            # loading existing data
            df = load_user_data()

            if df is not None:
                # adding a new row and removing dupicates
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.drop_duplicates(inplace=True, keep="last", subset=["date"])
            else:
                # creating a new datframe if no existing data
                df = pd.DataFrame([new_row])
            
            # Save back to supabasae
            csv_bytes = df.to_csv(index=False).encode('utf-8')
            upload_user_file(user_id, PERIOD_FILENAME, csv_bytes)
            success_save= True

        except Exception as e:
            st.error(f"Failed to save data: {e}")
            success_save = False

    # -- loading period data from supabase

    df = load_user_data()

    if df is not None and not df.empty:
        st.success("Using you saved period data")
    else:
        st.error("No period data found. This should not happen since your file was created at sign up")

    
    # -- Tracking ongoing cycle state

    if "on_period" not in st.session_state:
        st.session_state.on_period = False

    if "current_start" not in st.session_state:
        st.session_state.current_start = None

    if "cycles" not in st.session_state:
        st.session_state.current_start = None

    if "period_date" not in st.session_state:
        st.session_state.period_date = None

    
    # period data input:

    if df is not None:
        if not st.session_state.on_period: # not currently on period
            if st.button("Start period"):
                st.session_state.on_period = True
                st.session_state.current_start = str(date.today())
                st.success(f"Period started on {st.session_state.current_start}")
        else:
            st.info(f"Period ongoing since {st.session_state.current_start}")

            if st.button("End period"):
                current_df= load_user_data()
            if currentdf is not None and not current_df.empty:
                end_date = current_df.iloc[-1]["date"]
                cycle_length = (pd.to_datetime(end_date) - pd.to_datetime(st.session_state.current_start)).days
                st.success(f"your period ended on {end_date}")

                # saving the cycle
                st.session_stae.cycles.append({
                    "start": st.session_state.current_start,
                    "end": end_date,
                    "length": cycle_length
                })

                # reseting period state
                st.session_state.on_period = False

        # Recording period data
        st.session_state.period_date = str(st.date_input("Today's date"))
        st.session_state.pain = st.slider("Pain level (0= none, 10 = severe)", 0, 10, 5)
        st.session_state.flow = st.selectbox(
            "How heavy is your period: ",
            ["light", "normal", "heavy", "I'm BLEEDING"]
        )

        st.session_state.mood = st.selectbox(
            "How do you feel?",
            ["Happy", "Sad", "Normal", "Angry", "Other"]
        )

        if st.session_state.mood == "Other":
            custom_mood = st.text_input("Tell auntie your mood")
            st.session_state.mood = custom_mood if custom_mood else "Other"

        # checking if data already entered for today
        data_already_entered = False
        if st.session_state.period_date and df is not None:
            data_already_entered = st.session_state.period_date in df["date"]

        if "change_message" not in st.session_state:
            st.session_state.change_message = False

        if st.button("Save period data", disabled= data_already_entered):
            new_row = {
                "date": st.session_state.period_date,
                "has_period_started": "Yes",
                "flow": st.session_state.flow,
                "pain": st.session_state.pain,
                "mood": st.session_state.mood
            }

            save_info(new_row)
            st.session_state.change_message = not st.session_state.change.message

            if st.session_state.change_message:
                st.success("Your period data has been saved!")
            else:
                if success_save:
                    st.info("Your data has beed updated!")
                elif data_already_entered:
                    st.info("You already recorded your period data for today")
        
        # Showing chart if we have cycles:
            if st.session_state.cycles:
                cycle_df = pd.DataFrame(st.session_state.cycles)
                cycle_df["year"] = pd.DataFrame(st.session_state.cycles["start"]).dt.year
                cycle_df["month"] = pd.to_datetime(cycle_df["start"].dt.month_name())

                years = st.multiselect("Filter by year:", options=cycle_df["year"].unique() , default=cycle_df["year"].unique())
                months = st.multiselect("Filter by month: ", options=cycle_df["month"].unique(), default =cycle_df["month"].unique())

                filtered_df = cycle_df[(cycle_df["year"].isin(years)) & (cycle_df["month"].isin(months))]

                chart = (
                    alt.Chart(filtered_df)
                    .mark_bar(color="#BA5DBA", size=50)
                    .encode(
                        x=alt.X("start:T", title="Cycle Start Date"),
                        y=alt.Y("length:Q", title="Cycle Length (days)"),
                        tooltip= ["start", "end", "length"]
                    )
                )
                st.altair_chart(chart, use_container_width = True)

                # Predicting the next period
                if len(cycle_df) > 1:
                    avg_cycle = int(cycle_df["length"].mean())
                    last_end = pd.to_datetime(cycle_df["end"].iloc[-1])
                    predicted_date = last_end + pd.timedelta(days=avg_cycle)
                    





