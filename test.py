from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  extra_body={},
  model="deepseek/deepseek-r1:free",
  messages=[
    {
      "role": "user",
      "content": "fuck you?"
    }
  ]
)
print(completion.choices[0].message.content)

# creating and naming a new ChatterBot instance
chatbot = ChatBot("Auntie Alade",
storage_adapter="chatterbot.storage.SQLStorageAdapter",
database_uri="sqlite:///auntie_alade.sqlite3"  # creates file locally

) 

"""The storage adapter is the part of the chatbot that decides how
and where conversations and training data are stored
"""

# training the chatBot with a list of statement
conversation = [
    "Hello there",
    "Hi",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome.",
    "fuck you"
]

trainer = ListTrainer(chatbot)
trainer.train(conversation)


# getting a response:

# response = chatbot.get_response("Hello friend")
# print(response)

