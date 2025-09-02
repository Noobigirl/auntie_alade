from openai import OpenAI
from dotenv import load_dotenv 
import streamlit as st
import time
import os

load_dotenv() 

# initializig openRouter client
AiClient = OpenAI(
    base_url= "https://openrouter.ai/api/v1",
    api_key= os.getenv("OPENAI_API_KEY")
)

# using local bot is not sustainable,
# switch to online api
def app():
    st.title("Talk to Auntie Alade")

    avatars = {
        "user": "static/user.png",
        "assistant": "static/alade_head.png"
    }

    # intitializing the chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # displaying the chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar= avatars[msg["role"]]):
            st.markdown(msg["content"])
    
    # user input
    if prompt := st.chat_input("Say somethig to auntie..."):
        #saving user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user", avatar= avatars["user"]):
            st.markdown(prompt)


        # bot reply
        with st.chat_message("assistant", avatar= avatars["assistant"]):
            # adding text typing effect like chat gpt
            placeholder = st.empty()
            placeholder.markdown("Auntie is thinking...")

            response = ""
            stream = AiClient.chat.completions.create(
                model="deepseek/deepseek-chat-v3.1:free",
                messages=[
                    {"role": "system", 
                    "content": "You are Auntie Alade, a nice Nigerian auntie giving friendly period and mood advice, with some tint of Nigerian English"},
                    *st.session_state.messages
                ],
                stream= True
            )
            for  chunk in stream:
                if chunk.choices[0].delta:
                    token = chunk.choices[0].delta.content
                    response += token
                    placeholder.markdown(response + "▌")
                    time.sleep(0.04)

            placeholder.markdown(response)

        # saving bot response
        st.session_state.messages.append({"role": "assistant", "content": response})
