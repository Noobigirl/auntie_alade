import ollama

def get_prompt():
    pass

# creatign the ollama client

client = ollama.Client()

# defining the LLM model used and the prompt

model = "auntie_alade"
prompt = "hi there"

# sending the prompt to the model

model_response = client.generate(model = model, prompt = prompt)

print("Auntie says: ")

print(model_response.response) 