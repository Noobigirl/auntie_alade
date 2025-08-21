import ollama

# creating the ollama client
client = ollama.Client()

model = "auntie_alade"

# conversation history
history = []


def get_prompt():
    global history
    while True: 
        user_prompt = input("Say something to auntie Alade: ")
        # stoping the chat if no prompt
        if user_prompt.strip == "":
            
            return
        # adding user input to history
        history.append({"role":"user", "content": user_prompt})
        display_response()

def display_response():
    global history

    # sending full conversation history to the model
    model_response = client.chat(model = model, messages= history)
    reply = model_response["message"]["content"]

    # adding auntie's reply to history
    history.append({"role": "assitant", "content": reply})
    print("Auntie says: ")
    print(reply) 




get_prompt()


