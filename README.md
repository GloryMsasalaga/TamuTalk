# TamuTalk Chatbot 🍽️🗣️

**TamuTalk** is an intelligent, bilingual (English and Swahili) chatbot designed to offer personalized food suggestions based on a user's budget, diet, and health conditions. It also supports basic health advice and conversational flow from greetings to goodbyes.

---

## 🌟 Features

- 🤖 NLP-powered intent classification using Scikit-Learn
- 🔁 Real-time learning and retraining support
- 🌍 Language detection and translation (Swahili/English)
- 💬 Web-based chat interface (frontend + backend)
- 🧠 Entity extraction (budget, dietary preferences, health conditions)
- 📦 Logs all conversations and responses for traceability
- 🔧 Flask web server for communication with the chatbot
- 📁 Option to save chats to a file

---

## 🛠️ Tech Stack 

- Python 3.10+
- Flask
- Scikit-learn
- Googletrans (Translation and Language Detection)
- HTML/CSS/JavaScript (Frontend)
- JSON (Training Data)

---

## 🚀 Getting Started

### 1. Clone the Repository
git clone https://github.com/GloryMsasalaga/TamuTalk

### 2. Install Python Dependencies
pip install -r requirements.txt

### 3. Add training data
add chatbot_training_data.json file inside the project directory. This contains intents, patterns and responses.

### 4. Run the Chatbot Server
flask run
