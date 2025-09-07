from openai import OpenAI
from dotenv import load_dotenv 
import apps.theme as theme
import streamlit as st
import time
import os

load_dotenv() 

# initializig openRouter client
AiClient = OpenAI(
    base_url= "https://openrouter.ai/api/v1",
    api_key= os.getenv("OPENAI_API_KEY")
)


def app() -> None:
    st.title("Talk to Auntie Alade")
    st.write("")
    
    avatars = {
        "user": "static/user.png",
        "assistant": "static/alade_head.png"
    }

    user_id = st.session_state.get("user_id")

    # Ensure messages is a dictionary
    if "messages" not in st.session_state or not isinstance(st.session_state.messages, dict):
        st.session_state.messages = {}

    # Ensure the user is logged in
    if not user_id:
        st.warning("You need to be logged in to chat with Auntie Alade.")
        return

    # Initialize chat history for this user
    if user_id not in st.session_state.messages:
        st.session_state.messages[user_id] = []

    # display messages
    for msg in st.session_state.messages[user_id]:
        with st.chat_message(msg["role"], avatar=avatars[msg["role"]]):
            st.markdown(msg["content"])

    # handle user input
    if prompt := st.chat_input("Say something to Auntie..."):
        st.session_state.messages[user_id].append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=avatars["user"]):
            st.markdown(prompt)

        # bot reply
        with st.chat_message("assistant", avatar=avatars["assistant"]):
            placeholder = st.empty()
            placeholder.markdown("Auntie is thinking...")

            response = ""
            stream = AiClient.chat.completions.create(
                model="deepseek/deepseek-chat-v3.1:free",
                messages=[
                    {"role": "system",
                     "content": "You are Auntie Alade, a nice Nigerian auntie giving friendly period and mood advice, with some tint of Nigerian English"},
                    *st.session_state.messages[user_id]
                ],
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta:
                    token = chunk.choices[0].delta.content
                    response += token
                    placeholder.markdown(response + "▌")
            
            placeholder.markdown(response)

        st.session_state.messages[user_id].append({"role": "assistant", "content": response})
