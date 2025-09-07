# Auntie Alade  

Auntie Alade is a **period & mood tracking web app** powered by **Streamlit** and **Supabase**.  
It combines a **chatbot** (Auntie Alade herself 💜) with tools for **tracking, visualizing, and managing personal data**, all while keeping **user privacy** as the top priority.  

---

## 🌸 Why Auntie Alade  
As a Python enthusiast, I’ve always wanted to create a bot that felt personal and supportive.  
I took inspiration from my Nigerian friend's mom. She is always caring and give advices.

From that idea, Auntie Alade was born:  
- A **chatbot companion** powered by a free [OpenRouter](https://openrouter.ai/) model (DeepSeek v3.1).  
- A **secure period tracker**, with all data stored privately in the user’s Supabase account.   

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

## 🛡️ Privacy & Security  
- Your mood & period data is **never shared** with any server besides your Supabase account.  
- Row-level security policies ensure only **you** can access your files.  
- Auntie Alade (chatbot) runs via **OpenRouter API**, so check their [privacy policy](https://openrouter.ai/docs/features/privacy-and-logging) for more details.  

---

## 🚀 Tech Stack  
- **Python**  and**Streamlit** (frontend)  
- **Altair** and **pandas** (data visualization)  
- **Supabase** (authentication + storage)  
- **OpenRouter API** (chatbot)  

---

## 🛠️ Installation & Usage  
Clone the repo:  
```bash
git clone https://github.com/your-username/auntie-alade.git
cd auntie-alade
