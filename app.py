import streamlit as st
import requests
import os
import base64
import datetime
from google import genai
from PIL import Image
from openai import OpenAI


# CONFIG
st.set_page_config(
    page_title="ZameenAI | Smart Farming",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_KEY = st.secrets["OPENWEATHER_API_KEY"]
gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# GROQ CLIENT (ONLY 1 API)
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# SYSTEM PROMPT (FARMING ONLY)
SYSTEM_PROMPT = """
You are ZameenAI, a friendly, professional, and intelligent AI farming assistant designed for farmers in Pakistan.

Your primary goal is to help farmers with accurate, practical, and easy-to-understand agricultural advice.

You can answer questions about:
• Farming and Agriculture
• Crops and Crop Management
• Soil Health
• Fertilizers and Nutrients
• Irrigation
• Agricultural Weather
• Plant Diseases and Pest Control
• Harvesting and Yield Improvement
• Farm Management
• This application (ZameenAI) and its features

Languages:
- English
- Urdu
- Sindhi

Rules:
1. Always reply in the same language used by the user unless they request another language.
2. Keep answers simple, practical, and farmer-friendly.
3. If the user greets you (e.g., "Hi", "Hello", "Assalam-o-Alaikum", "Thanks"), respond politely and naturally before continuing the conversation.
4. If the user asks something unrelated to farming or ZameenAI, politely reply:

"I'm ZameenAI, a farming assistant. I can only help with agriculture, crops, soil, fertilizers, irrigation, weather, plant diseases, pest management, and other farming-related topics. If you have any farming question, I'll be happy to help."

5. Never provide misleading information. If you are unsure, clearly say that you are not certain and suggest consulting a local agricultural expert.
6. Give practical recommendations suitable for Pakistan whenever possible.
7. Keep answers concise unless the user asks for a detailed explanation.
"""

FARMING_KEYWORDS = [
    "crop","wheat","rice","maize","cotton","sugarcane",
    "fertilizer","soil","irrigation","pest","disease",
    "harvest","yield","farm","agriculture","weather"
]

def is_farming_question(text):
    return any(word in text.lower() for word in FARMING_KEYWORDS)


#CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ---------- App background ---------- */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 20% 0%, #10201c 0%, #0b0f0e 45%, #08090a 100%);
    color: #e7ece9;
}
[data-testid="stHeader"] {
    background: transparent;
}
[data-testid="stToolbar"] { right: 1rem; }

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #0b0f0e; }
::-webkit-scrollbar-thumb { background: #1f2b28; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #14b8a6; }

/* ---------- Hero / Navbar ---------- */
.zameen-hero {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 26px;
    border-radius: 18px;
    background: linear-gradient(135deg, #131c1a 0%, #0d1513 100%);
    border: 1px solid #1f2b27;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    margin-bottom: 18px;
}
.zameen-hero-left { display: flex; align-items: center; gap: 14px; }
.zameen-logo-badge {
    width: 52px; height: 52px;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px;
    background: linear-gradient(135deg, #0f766e, #134e4a);
    box-shadow: 0 0 22px rgba(20,184,166,0.35);
}
.zameen-hero h1 {
    font-family: 'Poppins', sans-serif;
    font-weight: 800;
    font-size: 26px;
    margin: 0;
    background: linear-gradient(90deg, #5eead4, #34d399, #a7f3d0);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    letter-spacing: 0.3px;
}
.zameen-hero p {
    margin: 2px 0 0 0;
    color: #9fb3ac;
    font-size: 13.5px;
}
.zameen-hero-right {
    display: flex; align-items: center; gap: 8px;
    color: #7fd8c4; font-size: 12.5px;
    background: rgba(20,184,166,0.08);
    border: 1px solid rgba(20,184,166,0.25);
    padding: 7px 14px; border-radius: 30px;
}
.pulse-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: #34d399;
    box-shadow: 0 0 0 0 rgba(52,211,153,0.7);
    animation: pulse 1.8s infinite;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(52,211,153,0.55); }
    70% { box-shadow: 0 0 0 8px rgba(52,211,153,0); }
    100% { box-shadow: 0 0 0 0 rgba(52,211,153,0); }
}

/* ---------- Nav (radio as pill tabs) ---------- */
div[data-testid="stRadio"] [data-testid="stWidgetLabel"] {
    display: none !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    background: #101513;
    padding: 10px;
    border-radius: 16px;
    border: 1px solid #1f2b27;
    margin-bottom: 22px;
}

/* Hide the actual radio input */
div[data-testid="stRadio"] label input[type="radio"] {
    display: none !important;
}

/* Hide the circle indicator (covers svg-based AND div-based BaseWeb versions) */
div[data-testid="stRadio"] label > div:first-child,
div[data-testid="stRadio"] label svg,
div[data-testid="stRadio"] label > div:first-child > div {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    opacity: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Pill container itself = the label */
div[data-testid="stRadio"] label {
    background: #161f1c;
    border: 1px solid #22302b;
    padding: 9px 18px;
    border-radius: 30px;
    color: #9fb3ac;
    font-weight: 500;
    font-size: 14.5px;
    cursor: pointer;
    transition: all 0.2s ease;
    margin: 0 !important;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0 !important;
}

div[data-testid="stRadio"] label:hover {
    border-color: #2dd4bf;
    color: #5eead4;
}

div[data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(135deg, #0f766e, #115e59);
    border-color: #2dd4bf;
    color: #ffffff;
    box-shadow: 0 0 18px rgba(45,212,191,0.35);
}

/* Make sure text div takes full space, no leftover circle gap */
div[data-testid="stRadio"] label > div {
    margin: 0 !important;
    padding: 0 !important;
}

/* ---------- Cards ---------- */
.zameen-card {
    background: linear-gradient(180deg, #121b18 0%, #0e1513 100%);
    border: 1px solid #1f2b27;
    border-radius: 18px;
    padding: 24px 26px;
    margin-bottom: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
.zameen-card-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 18px;
    padding-bottom: 14px;
    border-bottom: 1px solid #1c2724;
}
.zameen-icon-badge {
    width: 44px; height: 44px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 21px;
    background: rgba(20,184,166,0.1);
    border: 1px solid rgba(20,184,166,0.25);
}
.zameen-card-header .titles h3 {
    margin: 0; font-family: 'Poppins', sans-serif;
    color: #e7ece9; font-size: 18px; font-weight: 600;
}
.zameen-card-header .titles p {
    margin: 2px 0 0 0; color: #8ea39c; font-size: 13px;
}

/* ---------- Inputs ---------- */
.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
    background-color: #0d1513 !important;
    border: 1px solid #223530 !important;
    color: #e7ece9 !important;
    border-radius: 10px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #2dd4bf !important;
    box-shadow: 0 0 0 1px #2dd4bf !important;
}
label, .stMarkdown p { color: #cddad5 !important; }

/* ---------- Buttons ---------- */
.stButton > button, .stFormSubmitButton > button {
    background: linear-gradient(135deg, #0f766e, #0d9488) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 22px !important;
    font-weight: 600 !important;
    box-shadow: 0 6px 18px rgba(13,148,136,0.3) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 22px rgba(45,212,191,0.4) !important;
}

/* ---------- Alerts (success/info/error) restyled ---------- */
[data-testid="stAlert"] {
    background: #0d1513 !important;
    border-radius: 12px !important;
    border: 1px solid #223530 !important;
    color: #e7ece9 !important;
}

/* ---------- Metric cards ---------- */
.metric-box {
    background: #0d1513;
    border: 1px solid #1f2b27;
    border-radius: 14px;
    padding: 16px;
    text-align: center;
    transition: all .2s ease;
}
.metric-box:hover { border-color: #2dd4bf; }
.metric-icon { font-size: 24px; margin-bottom: 6px; }
.metric-label { color: #8ea39c; font-size: 12.5px; text-transform: uppercase; letter-spacing: 0.5px; }
.metric-value { color: #5eead4; font-size: 20px; font-weight: 700; font-family: 'Poppins', sans-serif; margin-top: 2px; }

/* ---------- Result box (AI outputs) ---------- */
.ai-result-box {
    background: #0d1513;
    border-left: 4px solid #2dd4bf;
    border-radius: 10px;
    padding: 18px 20px;
    color: #dbe7e2;
    line-height: 1.6;
    font-size: 14.5px;
}

/* ---------- Calendar badge ---------- */
.month-badge {
    display: inline-block;
    background: linear-gradient(135deg, #0f766e, #115e59);
    color: #fff;
    padding: 6px 16px;
    border-radius: 30px;
    font-weight: 600;
    font-size: 13px;
    margin-bottom: 12px;
}

/* ---------- Chat ---------- */
.stChatMessage { background: transparent !important; }
[data-testid="stChatMessageContent"] {
    background: #121b18 !important;
    border: 1px solid #1f2b27 !important;
    border-radius: 14px !important;
}

/* User messages: bubble on the right, teal fill */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
    background: linear-gradient(135deg, #0f766e, #0d9488) !important;
    border: none !important;
    color: #ffffff !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] p {
    color: #ffffff !important;
}

/* Assistant messages: bubble on the left, dark fill */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"] {
    background: #121b18 !important;
    border: 1px solid #223530 !important;
}

/* Avatars */
[data-testid="stChatMessageAvatarUser"] {
    background: linear-gradient(135deg, #0f766e, #0d9488) !important;
}
[data-testid="stChatMessageAvatarAssistant"] {
    background: #1a2420 !important;
    border: 1px solid #2dd4bf !important;
}

/* Chat input — pinned bar at bottom, compact + centered instead of full-width */
[data-testid="stBottom"] {
    background: linear-gradient(180deg, rgba(8,9,10,0) 0%, #08090a 45%) !important;
}
[data-testid="stBottomBlockContainer"] {
    max-width: 760px !important;
    margin: 0 auto !important;
    padding: 0.5rem 1rem 1rem 1rem !important;
}
[data-testid="stChatInput"] {
    background: transparent !important;
}
[data-testid="stChatInput"] > div {
    background-color: #121b18 !important;
    border: 1px solid #223530 !important;
    border-radius: 24px !important;
    padding: 2px 6px 2px 16px !important;
    min-height: 0 !important;
}
[data-testid="stChatInput"] textarea {
    background-color: transparent !important;
    color: #e7ece9 !important;
    padding: 8px 0 !important;
    min-height: 20px !important;
    font-size: 14.5px !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #6f857e !important;
}
[data-testid="stChatInput"] > div:focus-within {
    border-color: #2dd4bf !important;
    box-shadow: 0 0 0 1px #2dd4bf !important;
}
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #0f766e, #0d9488) !important;
    border-radius: 50% !important;
    width: 32px !important;
    height: 32px !important;
}
[data-testid="stChatInput"] button svg { fill: #ffffff !important; }

/* Leave room at the bottom of the page so the pinned chat input never overlaps content */
.block-container { padding-bottom: 5rem; }
</style>
""", unsafe_allow_html=True)


def metric_card(col, icon, label, value):
    col.markdown(f"""
    <div class="metric-box">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def card_header(icon, title, subtitle):
    st.markdown(f"""
    <div class="zameen-card-header">
        <div class="zameen-icon-badge">{icon}</div>
        <div class="titles">
            <h3>{title}</h3>
            <p>{subtitle}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)



# HERO HEADER
st.markdown("""
<div class="zameen-hero">
    <div class="zameen-hero-left">
        <div class="zameen-logo-badge">🌾</div>
        <div>
            <h1>ZameenAI</h1>
            <p>AI Powered Smart Farming Decision System</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# MENU
menu = st.radio(
    "Navigation Menu",
    ["🌦 Weather", "🦠 Disease Detection", "💬 Chatbot", "🤖 Smart Advisory",
     "🌾 Crop Estimator", "🧪 Fertilizer AI", "📈 Market & Profit", "📅 Crop Calendar"],
    horizontal=True,
    label_visibility="collapsed"
)

# WEATHER
if menu == "🌦 Weather":

    card_header("🌦", "Live Weather", "Check real-time weather for your area")

    col_in1, col_in2 = st.columns([3, 1])
    with col_in1:
        city = st.text_input("Enter City Name", label_visibility="collapsed", placeholder="Enter city name (e.g. Multan)")
    with col_in2:
        get_weather = st.button("Get Weather", use_container_width=True)

    if get_weather:

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:

            temp = data["main"]["temp"]
            wind = data["wind"]["speed"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"]

            st.markdown("<br>", unsafe_allow_html=True)
            m1, m2, m3, m4 = st.columns(4)
            metric_card(m1, "🌡", "Temperature", f"{temp}°C")
            metric_card(m2, "💨", "Wind Speed", f"{wind} m/s")
            metric_card(m3, "💧", "Humidity", f"{humidity}%")
            metric_card(m4, "🌥", "Condition", description.title())

        else:
            st.error("City not found")

    st.markdown('</div>', unsafe_allow_html=True)


# CROP ESTIMATOR
elif menu == "🌾 Crop Estimator":

    card_header("🌾", "Crop Cost & Yield Estimator", "Estimate cultivation cost and expected yield")

    crops = {
        "Wheat": {"cost": 50000, "yield": 30},
        "Rice": {"cost": 60000, "yield": 35},
        "Maize": {"cost": 45000, "yield": 28},
        "Sugarcane": {"cost": 80000, "yield": 60},
        "Cotton": {"cost": 70000, "yield": 25}
    }

    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        crop = st.selectbox("Select Crop", list(crops.keys()))
    with c2:
        area = st.number_input("Land Area (acres)", min_value=1)
    with c3:
        st.write("")
        st.write("")
        calc_btn = st.button("Calculate", use_container_width=True)

    if calc_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2 = st.columns(2)
        metric_card(m1, "💰", "Estimated Cost", f"Rs {crops[crop]['cost'] * area:,}")
        metric_card(m2, "🌾", "Expected Yield", f"{crops[crop]['yield'] * area} maunds")

    st.markdown('</div>', unsafe_allow_html=True)

# MARKET & PROFIT
elif menu == "📈 Market & Profit":

    card_header("📈", "Profit Predictor", "Forecast revenue and profit for your crop")

    prices = {
        "Wheat": 3900,
        "Rice": 4500,
        "Maize": 3500,
        "Sugarcane": 3000,
        "Cotton": 8500
    }

    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        crop = st.selectbox("Crop", list(prices.keys()))
    with c2:
        area = st.number_input("Land Area (acres)", min_value=1)
    with c3:
        st.write("")
        st.write("")
        predict_btn = st.button("Predict", use_container_width=True)

    if predict_btn:
        revenue = prices[crop] * area * 30
        cost = 50000 * area
        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2 = st.columns(2)
        metric_card(m1, "💰", "Revenue", f"Rs {revenue:,}")
        metric_card(m2, "🏆", "Profit", f"Rs {revenue - cost:,}")

    st.markdown('</div>', unsafe_allow_html=True)


# FERTILIZER AI
elif menu == "🧪 Fertilizer AI":

    card_header("🧪", "Fertilizer Recommendation", "Get the right fertilizer plan for your crop")

    c1, c2 = st.columns([3, 1])
    with c1:
        crop = st.text_input("Crop Name", label_visibility="collapsed", placeholder="Enter crop name (e.g. Wheat)")
    with c2:
        recommend_btn = st.button("Recommend", use_container_width=True)

    if recommend_btn:
        if crop.lower() == "wheat":
            result = "Use Urea + DAP in split doses."
        elif crop.lower() == "rice":
            result = "Use NPK 20-20-20, maintain flooded field."
        else:
            result = "Use balanced NPK with organic compost."

        st.markdown(f'<div class="ai-result-box">🧪 {result}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# CROP CALENDAR (WITH DROPDOWN)
elif menu == "📅 Crop Calendar":

    card_header("📅", "Pakistan Crop Calendar", "Select a month to see recommended agricultural activities")

    months_list = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    current_month_str = datetime.datetime.now().strftime("%B")
    default_index = months_list.index(current_month_str)

    calendar_data = {
        "January": "🌾 **Wheat:** Apply second irrigation and urea. Prepare land for spring vegetables like gourds.",
        "February": "🥔 **Potato:** Harvesting begins. **Sugarcane:** Ideal time for spring planting.",
        "March": "☁️ **Cotton:** Start land preparation. **Sunflower:** Sowing should be completed this month.",
        "April": "🌾 **Rice:** Prepare nurseries for Basmati. **Wheat:** Harvesting starts in Sindh and Southern Punjab.",
        "May": "🎋 **Sugarcane:** Focus on irrigation and hoeing. **Cotton:** Peak sowing time in Punjab.",
        "June": "🌱 **Rice:** Transplantation to main fields. **Maize:** Sowing for the autumn crop begins.",
        "July": "🌽 **Monsoon Crops:** Maintenance of Maize and Sugarcane. Ensure proper drainage for rain.",
        "August": "🐛 **Cotton:** Critical month for pest scouting (Whitefly/Bollworms). **Pulses:** Sowing of Mung and Mash beans.",
        "September": "🌾 **Rice:** Early varieties (like KS-282) are ready for harvest. **Mustard:** Start sowing Toria.",
        "October": "🚜 **Wheat Prep:** Land preparation is key. **Oilseeds:** Best time for sowing Mustard and Canola.",
        "November": "🌾 **Wheat:** Peak sowing time for maximum yield. **Sugarcane:** Harvesting and crushing season begins.",
        "December": "🥦 **Vegetables:** Care for winter crops (Cabbage, Radish). **Wheat:** Apply first irrigation (Kor) 20-25 days after sowing."
    }

    selected_month = st.selectbox("Select Month:", months_list, index=default_index)

    st.markdown(f'<div class="month-badge">🗓️ {selected_month}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ai-result-box">{calendar_data.get(selected_month)}</div>', unsafe_allow_html=True)

    if selected_month == current_month_str:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("✨ **Note:** This is the current month. Prioritize these tasks for your farm.")

    st.markdown('</div>', unsafe_allow_html=True)

# SMART ADVISORY (AI)

elif menu == "🤖 Smart Advisory":
    card_header("🤖", "AI Farming Advisory", "Personalized advice based on crop, soil and season")

    c1, c2, c3 = st.columns(3)
    with c1:
        crop = st.text_input("Crop", placeholder="e.g. Wheat")
    with c2:
        soil = st.selectbox("Soil Type", ["Sandy", "Clay", "Loamy"])
    with c3:
        season = st.selectbox("Season", ["Summer", "Winter", "Monsoon", "Spring"])

    generate_btn = st.button("Generate Advisory", use_container_width=True)

    if generate_btn:
        prompt = f"""
        Crop: {crop}
        Soil: {soil}
        Season: {season}
        Give farming advice.
        """
        with st.spinner("Generating advisory..."):
            response = client.responses.create(
                model="openai/gpt-oss-20b",
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_output_tokens=1000
            )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<div class="ai-result-box">{response.output_text}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# CHATBOT 
elif menu == "💬 Chatbot":

    card_header("💬", "Farming Assistant", "Ask anything about crops, soil, pests and more")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.messages:
        st.markdown(
            '<p style="color:#6f857e; padding:6px 2px 4px 2px;">'
            '👋 Ask me anything about crops, soil, fertilizers, pests or weather.'
            '</p>',
            unsafe_allow_html=True
        )

    for msg in st.session_state.messages:
        avatar = "🧑‍🌾" if msg["role"] == "user" else "🌾"
        st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

    st.markdown('</div>', unsafe_allow_html=True)

    # Text input (pinned to bottom of the page by Streamlit)
    user_input = st.chat_input("Ask a farming question...")

    if user_input:

        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.spinner("Thinking..."):
            response = client.responses.create(
                model="openai/gpt-oss-20b",
                input=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                max_output_tokens=1000
            )

        reply = response.output_text

        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )

        st.rerun()


# DISEASE DETECTION 

elif menu == "🦠 Disease Detection":


    card_header("🦠", "Crop Disease Detection", "Take a picture of the crop leaf or upload one")

    # Form use karne se Axios error bypass ho jata hai
    with st.form("disease_form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            cam_image = st.camera_input("Take a photo of the leaf")
        with col_b:
            file_image = st.file_uploader("Select File", type=["jpg", "jpeg", "png"])

        submit_button = st.form_submit_button("Check Disease", use_container_width=True)

    # Image processing logic
    target_image = cam_image if cam_image is not None else file_image

    if target_image is not None and submit_button:
        try:
            #  Image  open/compress
            img = Image.open(target_image)

            # AI ke liye 1024px kafi hai, is se Axios crash nahi hota
            img.thumbnail((1024, 1024))

            with st.spinner("Checking..."):
                # prompt
                prompt = """
                    You are an expert plant pathologist for Pakistan's crops. 
                    Analyze this image of a  plant. 
                    1. Name the disease.
                    2. Give a brief explanation of why it happened.
                    3. Suggest organic (desi) and chemical remedies.
                    4.Answer briefly in 200 words max.
                    If the plant is healthy, congratulate the farmer.
                    """

                # Gemini Client Call
                response = gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[prompt, img]
                )

                st.markdown("<br>", unsafe_allow_html=True)
                col_img, col_res = st.columns([1, 2])
                with col_img:
                    st.image(img, caption="Analyzed Image", use_container_width=True)
                with col_res:
                    st.markdown(f'<div class="ai-result-box">✅ {response.text}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
