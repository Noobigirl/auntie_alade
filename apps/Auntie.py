import streamlit as st
import time
import ollama

# using local bot is not sustainable,
# switch to online api
def app():
    st.title("Talk to Auntie Alade")

    # --- Initializing the ollama clietn
    client = ollama.Client()
    model = "auntie_alade" 

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


        with st.chat_message("assistant", avatar= avatars["assistant"]):
            # adding text typing effect like chat gpt
            placeholder = st.empty()
            placeholder.markdown("Auntie is thinking...")

              # ollama bot response
            stream = client.chat(
            model= model,
            messages= st.session_state.messages,
            stream = True
            )

            response = ""
            for  chunk in stream:
                if "message" in chunk:
                    token = chunk["message"]["content"]
                    response += token
                    placeholder.markdown(response + "▌")
                    time.sleep(0.04)

            placeholder.markdown(response)

        # saving bot response
        st.session_state.messages.append({"role": "assistant", "content": response})
