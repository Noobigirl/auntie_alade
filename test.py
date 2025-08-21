from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
chatbot = ChatBot("Auntie Alade") # creating and naming a new ChatterBot instance


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

response = chatbot.get_response("Hello friend")
print(response)