import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
  base_url ="https://openrouter.ai/api/v1",
  api_key = os.getenv("OPENAI_API_KEY"),
)

messages = [
    {
        "role": "system",
        "content": (
            "You are Auntie Alade, a sassy and humorous Nigerian aunty."
            "Alwasy reply with humor, sarcasm, and African proverbs/intonations"
            "You never give technical explanations or do maths/science/litterature"
            "Keep replies relatively short, casual, and witty",
            "You give life/relationship advice."
        )
    },
    {
        "role": "user",
        "content": "Hello Auntie, how are you?"
    }
]

completion = client.chat.completions.create(
    model="deepseek/deepseek-r1:free",
    messages= messages,
    max_tokens= 100,
    temperature = 0.7
)
reply = completion.choices[0].message.content
print(reply)
