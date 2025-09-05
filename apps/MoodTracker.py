import streamlit as st
import pandas as pd 
import altair as alt
import apps.theme as th
from datetime import datetime
import os 

# test file
MOOD_FILE = "moods.csv"

def load_moods():
    if os.path.exists(MOOD_FILE):
        return pd.read_csv(MOOD_FILE)
    else:
        return pd.DataFrame(columns= ["date", "mood", "notes"])

def save_mood(mood, notes) -> None:
    df = load_moods()
    new_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mood": mood,
        "notes": notes
    }

    df =  pd.concat([df, pd.DataFrame([new_entry])], ignore_index= True)
    df.to_csv(MOOD_FILE, index=False)

def app() -> None:

    st.title("Mood Tracker")
    st.write("")
    mood_options = ["😊 Happy", "😢 Sad", "😡 Angry", "😌 Calm", "😰 Anxious", "🤩 Excited"]
    mood = st.selectbox("How do you feel right now?", mood_options)

    notes = st.text_area("Any thoughts you want to add?", "")

    if st.button("Save Mood"):
        save_mood(mood, notes)
        st.success("Your mood has been saved!")
    
    # Show mood history
    # st.subheader("Mood History")
    df = load_moods()

    st.write(" ")
    st.write(" ")
    if not df.empty:
       # st.dataframe(df.tail(10)) # Show last 10 entries

        # converting date column
        df["date"] = pd.to_datetime(df["date"])

        max_count = int(df["mood"].value_counts().max())
        tick_vals = list(range(0, max_count+1))

        chart = (
            alt.Chart(df)
            .mark_bar(color = "#BA5DBA", size= 50)
            .encode(
                x= alt.X(
                    "mood:N", 
                    title= "Mood",
                    axis= alt.Axis(labelAngle= 0),
                    ),
                y= alt.Y(
                    "count():Q", 
                    title= "Frequency",
                    axis=alt.Axis(values= tick_vals, format ="d"),
                    scale= alt.Scale(domain=[0, max_count])
                    ),
            
                tooltip=["mood", "count()"]
            )
            .properties(title="Mood Frequency", width="container")
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No moods logged yet. Start tracking today!")