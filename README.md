[![Athena Award Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Faward.athena.hackclub.com%2Fapi%2Fbadge)](https://award.athena.hackclub.com?utm_source=readme)

# Auntie Alade  

Auntie Alade is a **period & mood tracking web app** powered by **Streamlit** and **Supabase**.  
It combines a **chatbot** (Auntie Alade herself 💜) with tools for **tracking, visualizing, and managing personal data**, all while keeping **user privacy** as the top priority.  

---

## 🌸 Why Auntie Alade  
As a Python enthusiast, I’ve always wanted to create a bot that felt personal and supportive.  
I took inspiration from my Nigerian friend's mom. She is always caring and give advices about everything and anything.

From that idea, Auntie Alade was born:  
- A **chatbot companion** powered by a free [OpenRouter](https://openrouter.ai/) model (DeepSeek v3.1).  
- A **period tracker**, with all data stored privately in the user’s Supabase account.   

---

## ✨ Features  
- 🗨️ **Chat with Auntie Alade** (friendly bot powered via API).   
- 🌙 **Light/Dark theme toggle** with custom styling.  
- 📂 **Secure data storage** using [Supabase](https://supabase.com/):  
  - Each user has their **own private folder**.  
  - Users can **download or delete** their files anytime.  
- 🔐 **Authentication** (username + password via Supabase Auth).  
- ⚙️ **Settings page** to manage privacy, data, and app appearance.  

---
## Known Issues 

Auntie Alade is a work in progress, and there are a few quirks to be aware of:

- Chat history mix-ups: Early on, new users can somehow see someone else’s conversation. I am stil working on that, but for now I would not recommend to talk about anything too personal

- Period tracking for new users: If a new user hasn’t clicked “start period,” the app might think their period has already begun.

-Data management: Files live in Supabase Storage, so losing them means there’s no backup unless the user downloads a copy. The app expects each file to follow a specific naming pattern (user_id/period_data.csv)

- User experience quirks: Changing themes reloads the page, which  resets inputs. 

## 🛡️ Privacy & Security  
- Your mood & period data is **never shared** with any server besides Superbase.  
- Row-level security policies ensure only **you** can access your files.  
- Auntie Alade (chatbot) runs via **OpenRouter API**, so check their [privacy policy](https://openrouter.ai/docs/features/privacy-and-logging) for more details.  

---

## 🚀 Tech Stack  
- **Python**  and**Streamlit** (frontend)  
- **Altair** and **pandas** (data visualization)  
- **Supabase** (authentication + storage)  
- **OpenRouter API** (chatbot)  

---
[Link to the app](https://auntiealade-m5gguappoxhscggbfvukn3g.streamlit.app/)