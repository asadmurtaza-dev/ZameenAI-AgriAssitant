# 🌾 ZameenAI

> **AI-Powered Smart Farming Decision System for Pakistan**

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLM-green)
![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-orange)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

---

## 🌱 Overview

**ZameenAI** is an AI-powered smart farming assistant built to help farmers make better agricultural decisions.

The platform combines multiple AI technologies into a single application, allowing farmers to:

- Detect crop diseases using AI Vision
- Get personalized farming advice
- Check live weather
- Estimate crop yield and profit
- Receive fertilizer recommendations
- View Pakistan crop calendar
- Chat with an AI farming assistant
- Interact using voice and multiple languages

Our goal is to make modern agricultural knowledge accessible to every farmer.

---

# ✨ Features

## 🌦 Live Weather

- Real-time weather
- Temperature
- Humidity
- Wind Speed
- Weather Conditions

---

## 🦠 AI Disease Detection

Upload or capture a crop image.

AI automatically:

- Detects disease
- Explains the cause
- Suggests organic remedies
- Suggests chemical treatments

Powered by **Google Gemini 2.5 Flash Vision**

---

## 💬 AI Farming Chatbot

Ask any farming-related question.

Supports:

- English
- Urdu
- Sindhi

Powered by **Groq GPT-OSS-20B**

---

## 🎤 Voice Support

Farmers can interact using voice instead of typing.

---

## 🤖 Smart Advisory

Provides personalized recommendations based on:

- Crop
- Soil Type
- Season

---

## 🌾 Crop Yield Estimator

Estimate:

- Cost
- Expected Yield

---

## 📈 Market & Profit Prediction

Estimate:

- Revenue
- Profit

---

## 🧪 Fertilizer Recommendation

AI recommends fertilizers according to crop type.

---

## 📅 Pakistan Crop Calendar

Monthly agricultural activities for Pakistan.

---

# 🛠 Tech Stack

| Technology | Usage |
|------------|-------|
| Python | Backend |
| Streamlit | Frontend |
| Groq GPT-OSS-20B | AI Chatbot |
| Gemini 2.5 Flash | Disease Detection |
| OpenWeather API | Live Weather |
| Pillow | Image Processing |
| Requests | API Calls |

---

# 📂 Project Structure

```
ZameenAI/

│

├── app.py

├── requirements.txt

├── README.md

├── .streamlit/

│   └── secrets.toml

```

---

# 🚀 Installation

Clone repository

```bash
git clone https://github.com/asadmurtaza-dev/ZameenAI-AgriAssitant.git

cd ZameenAI
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
streamlit run app.py
```

---

# 🔑 Environment Variables

## Streamlit Secrets

Create

```
.streamlit/secrets.toml
```

Add

```toml
OPENWEATHER_API_KEY="YOUR_KEY"
```

Environment Variables

```text
GROQ_API_KEY=YOUR_GROQ_KEY

GEMINI_API_KEY=YOUR_GEMINI_KEY
```

---

# 🌍 Deployment

Deploy easily on **Streamlit Community Cloud**

1. Push project to GitHub

2. Login to Streamlit Cloud

3. Create New App

4. Select repository

5. Add Secrets

```toml
OPENWEATHER_API_KEY="..."

```

Environment Variables

```
GROQ_API_KEY

GEMINI_API_KEY
```

6. Click **Deploy**


---

# 🌍 Supported Languages

- 🇬🇧 English
- 🇵🇰 Urdu
- 🌾 Sindhi

---

# 💡 Future Improvements

- Satellite Crop Monitoring
- AI Pest Prediction
- Soil Analysis
- Offline Mode
- Mobile Application
- Government Scheme Recommendations
- Farmer Community
- Voice Responses
- Market Price Forecasting

---

# 👨‍💻 Team

- Sayed Asad Murtiza
-Anha Alishba

---

# ❤️ Acknowledgements

- Google Gemini
- Groq
- OpenWeather
- Streamlit

---

# 📜 License

This project is licensed under the MIT License.

---

## ⭐ If you like this project, don't forget to star the repository!
