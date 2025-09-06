import streamlit as st
import pandas as pd
import apps.theme as th
import os

DATA_FILE = "moods.csv"

def app():
    th.apply_custom_theme()
    st.title("Settings")
    st.write(" ")
    st.markdown(
        "I hope you like this app I made for the **Athena Awards hackathon**."
        "Check out the source code below!"
        )
    st.link_button("Github repo", "") # add link to the repo

    st.subheader("Privacy & Data Security")
    st.markdown(
        """
        - This app does **not** send your period or mood data to any sever.
        - You are responsible for saving and uploading you own data files.
        - The chatbot (*Auntie Alade*) is based on **DeepSeek v3.1 via OpenRouter**.
          Check [OpenRouter's policy](https://openrouter.ai/docs/features/privacy-and-logging) for details on data privacy
        """
    )

    st.divider()
    
    # theme toggle
    st.subheader("Change appearance")
    if st.button("Toggle themes"):
        if st.session_state["theme"] == "light":
            st.session_state["theme"] = "dark"
        else:
            st.session_state["theme"] = "light"
        
        # to stay on the settings page after reruning
        st.session_state["current_page"] = "Settings"
        st.rerun()


    # export data
    st.subheader(" Data Management")
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        st.download_button(
            label= "Download mood data as a CSV",
            data = df.to_csv(index=False).encode("UTF-8"),
            file_name="mood_data.csv",
            mime="text/csv"
        )
    else:
        st.info("No mood data available yet to export.")

    
    # Reset data
    if st.button("Reset All mood data"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            st.success("Mood data has veed reset.")
        else:
            st.info("No mood data file fount to reset.")
    
