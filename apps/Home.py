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

# Helper functions for Supabase storage
def upload_user_file(user_id: str, filename: str, file_bytes: bytes):
    """Upload bytes to supabase storage under user_id/filename"""
    path = f"{user_id}/{filename}"
    try:
        res = supabase.storage.from_(BUCKET).upload(path,
                                                    file_bytes,
                                                    {"content-type": "text/csv"}
        )
        return res
    except Exception as e:
        st.error(f"Upload failed: {str(e)}")
        return None

def download_user_file(user_id: str, filename: str):
    """Download file bytes from supabase storage"""
    path = f"{user_id}/{filename}"
    try:
        res = supabase.storage.from_(BUCKET).download(path)
        return res
    except Exception as e:
        return None

def create_prediction_calendar(predicted_dates):
    """Create a calendar view with predicted period dates highlighted"""
    if not predicted_dates:
        return
    
    # Get current date and the prediction month
    today = datetime.now()
    pred_date = predicted_dates[0]

    # Creating a calendar for the prediction month
    cal = calendar.monthcalendar(pred_date.year, pred_date.month)
    month_name = calendar.month_name[pred_date.month]

    st.subheader(f"Period Prediction Calendar - {month_name} {pred_date.year}")

    # Creating calendar HTML
    calendar_html = f"""
    <style>
    .calendar{{
        display: grid;
        grid-template-columns: repeat(7, 1fr);
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
        background: white;
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
        animation: pulse 2s infinite;
    }}
    .today {{
        background: #4CAF50 !important;
        color: white !important;
        font-weight: bold;
    }}
    .empty {{
        border: none;
        background: transparent;
    }}
    @keyframes pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(233, 30, 99, 0.7); }}
        70% {{ box-shadow: 0 0 0 10px rgba(233, 30, 99, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(233, 30, 99, 0); }}
    }}
    </style>
    <div class="calendar">
    """
    
    # Day headers
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for day in days:
        calendar_html += f'<div class="day day-header">{day}</div>'

    # Calendar days
    for week in cal:
        for day in week:
            if day == 0:
                calendar_html += '<div class="day empty"></div>'
            else:
                day_date = datetime(pred_date.year, pred_date.month, day)
                css_class = "day"
            
                # Checking if it's today
                if day_date.date() == today.date():
                    css_class += " today"
                # Check if it's a predicted period day
                elif any(abs((day_date.date() - p.date()).days) <= 2 for p in predicted_dates):
                    css_class += " predicted"

                calendar_html += f'<div class="{css_class}">{day}</div>'

    calendar_html += "</div>"

    # Legend
    calendar_html += """
    <div style="margin-top: 20px;">
        <p><strong>Legend:</strong></p>
        <p>🟢 <span style="color: #4CAF50;">Today</span> |
           💗 <span style="color: #ff69b4;">Predicted Period (±2 days)</span></p>
    </div>
    """

    st.components.v1.html(calendar_html, height=400)

def app():
    success_save = False

    st.title("Period tracker")
    st.write("")

    # Get current user ID
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("Please log in to access the period tracker.")
        return
    
    # try:
    #     user = supabase.auth.get_user()
    #     st.write(f"DEBUG - Authenticated user: {user.user.id if user.user else 'None'}")
    #     st.write(f"DEBUG - Session user_id: {user_id}")
    # except Exception as e:
    #     st.error(f"Authentication check failed: {e}")
    
    PERIOD_FILENAME = "period_data.csv"

    # Loading user file data
    def load_user_data():
        """Load user's period data from Supabase storage"""
        try:
            file_bytes = download_user_file(user_id, PERIOD_FILENAME)
            if file_bytes:
                # Converting bytes to DataFrame
                csv_string = file_bytes.decode("utf-8")
                df = pd.read_csv(io.StringIO(csv_string))
                return df
            else:
                return None
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None
        
    # Saving the entered data to supabase
    def save_info(new_row):
        """Save new row to user's CSV in Supabase storage"""
        global success_save
        try:
            # Loading existing data
            df = load_user_data()

            if df is not None:
                # Adding a new row and removing duplicates
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.drop_duplicates(inplace=True, keep="last", subset=["date"])
            else:
                # Creating a new dataframe if no existing data
                df = pd.DataFrame([new_row])
            
            # Save back to supabase
            csv_bytes = df.to_csv(index=False).encode('utf-8')
            upload_user_file(user_id, PERIOD_FILENAME, csv_bytes)
            success_save = True

        except Exception as e:
            st.error(f"Failed to save data: {e}")
            success_save = False

    # Loading period data from supabase
    df = load_user_data()

    if df is not None and not df.empty:
        st.success("Using your saved period data")
    else:
        st.warning("No period data found. Creating a new file for you...")
        # Create empty DataFrame with correct columns
        df = pd.DataFrame(columns=["date", "has_period_started", "flow", "pain", "mood"])
        # Save empty file to Supabase
        try:
            csv_bytes = df.to_csv(index=False).encode('utf-8')
            upload_user_file(user_id, PERIOD_FILENAME, csv_bytes)
            st.success("New period data file created!")
        except Exception as e:
            st.error(f"Failed to create data file: {e}")
            return

    # Tracking ongoing cycle state
    if "on_period" not in st.session_state:
        st.session_state.on_period = False

    if "current_start" not in st.session_state:
        st.session_state.current_start = None

    if "cycles" not in st.session_state:
        st.session_state.cycles = []

    if "period_date" not in st.session_state:
        st.session_state.period_date = None
    
    # Period data input
    if df is not None:
        if not st.session_state.on_period:  # Not currently on period
            if st.button("Start period"):
                st.session_state.on_period = True
                st.session_state.current_start = str(date.today())
                st.success(f"Period started on {st.session_state.current_start}")
        else:
            st.info(f"Period ongoing since {st.session_state.current_start}")

            if st.button("End period"):
                current_df = load_user_data()
                if current_df is not None and not current_df.empty:
                    end_date = current_df.iloc[-1]["date"]
                    cycle_length = (pd.to_datetime(end_date) - pd.to_datetime(st.session_state.current_start)).days
                    st.success(f"Your period ended on {end_date}")

                    # Saving the cycle
                    st.session_state.cycles.append({
                        "start": st.session_state.current_start,
                        "end": end_date,
                        "length": cycle_length
                    })

                    # Resetting period state
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

            # Checking if data already entered for today
            data_already_entered = False
            if st.session_state.period_date and df is not None:
                data_already_entered = st.session_state.period_date in df["date"].tolist()

            if "change_message" not in st.session_state:
                st.session_state.change_message = False

            if st.button("Save period data", disabled=data_already_entered):
                new_row = {
                    "date": st.session_state.period_date,
                    "has_period_started": "Yes",
                    "flow": st.session_state.flow,
                    "pain": st.session_state.pain,
                    "mood": st.session_state.mood
                }

                save_info(new_row)
                st.session_state.change_message = not st.session_state.change_message

                if st.session_state.change_message:
                    st.success("Your period data has been saved!")
                else:
                    if success_save:
                        st.info("Your data has been updated!")
                    elif data_already_entered:
                        st.info("You already recorded your period data for today")
        
        # Chart section - Always visible
        st.subheader("📊 Cycle Analysis") 

        if st.session_state.cycles:
            cycle_df = pd.DataFrame(st.session_state.cycles)
            cycle_df["year"] = pd.to_datetime(cycle_df["start"]).dt.year
            cycle_df["month"] = pd.to_datetime(cycle_df["start"]).dt.month_name()

            years = st.multiselect("Filter by year:", options=cycle_df["year"].unique(), default=cycle_df["year"].unique())
            months = st.multiselect("Filter by month:", options=cycle_df["month"].unique(), default=cycle_df["month"].unique())

            filtered_df = cycle_df[(cycle_df["year"].isin(years)) & (cycle_df["month"].isin(months))]

            if not filtered_df.empty:
                chart = (
                    alt.Chart(filtered_df)
                    .mark_bar(color="#BA5DBA", size=50)
                    .encode(
                        x=alt.X("start:T", title="Cycle Start Date"),
                        y=alt.Y("length:Q", title="Cycle Length (days)"),
                        tooltip=["start", "end", "length"]
                    )
                )
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("No data matches your filter criteria.")
            
        else:
            st.info("No cycle data yet. Complete a few periods to see your cycle patterns!")
            # Show empty chart placeholder
            placeholder_df = pd.DataFrame({
                "start": [date.today()],
                "length": [0]
            })
            chart = (
                alt.Chart(placeholder_df)
                .mark_bar(color="#lightgray", size=50)
                .encode(
                    x=alt.X("start:T", title="Cycle Start Date"),
                    y=alt.Y("length:Q", title="Cycle Length (days)", scale=alt.Scale(domain=[0, 35])),
                )
            )
            st.altair_chart(chart, use_container_width=True)
        
        # Period Predictions Section - Always visible
        st.subheader("🔮 Period Predictions")

        if st.session_state.cycles and len(st.session_state.cycles) > 1:
            cycle_df = pd.DataFrame(st.session_state.cycles)
            avg_cycle = int(cycle_df["length"].mean())
            last_end = pd.to_datetime(cycle_df["end"].iloc[-1])
            predicted_date = last_end + pd.timedelta(days=avg_cycle)

            # Show calendar with predictions
            predicted_dates = [predicted_date]
            create_prediction_calendar(predicted_dates)
        else:
            st.info("Complete at least 2 cycles to see predictions!")
            create_prediction_calendar([])