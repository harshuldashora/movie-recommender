import streamlit as st
import sys
import os
import base64

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.hybrid_recommender import hybrid_recommend

# -------------------------------
# FUNCTION: Convert image to base64
# -------------------------------
def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

# Load background image
bg_image = get_base64_image("app/assets/bg.jpg")

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")

# -------------------------------
# NETFLIX STYLE CSS
# -------------------------------
st.markdown(f"""
<style>

/* 🔥 BACKGROUND (clear + sharp) */
[data-testid="stAppViewContainer"] {{
    background: url("data:image/jpg;base64,{bg_image}") no-repeat center center fixed;
    background-size: cover;
    filter: brightness(0.95) contrast(1.1);
}}

/* 🔥 SMOOTH CINEMATIC GRADIENT */
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;

    background: linear-gradient(
        to bottom,
        rgba(0,0,0,0.15) 0%,
        rgba(0,0,0,0.4) 40%,
        rgba(0,0,0,0.75) 75%,
        rgba(0,0,0,0.9) 100%
    );

    z-index: 0;
}}

/* CONTENT ABOVE BACKGROUND */
.main {{
    position: relative;
    z-index: 1;
}}

/* 🔥 PREMIUM GLASS CARD */
.block-container {{
    max-width: 520px;
    margin: auto;
    padding: 2.5rem;

    background: rgba(15, 15, 15, 0.55);
    backdrop-filter: blur(20px);

    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);

    box-shadow: 
        0 8px 32px rgba(0,0,0,0.6),
        0 0 25px rgba(229, 9, 20, 0.15);

    transition: all 0.3s ease;
}}

/* 🔥 HOVER EFFECT */
.block-container:hover {{
    transform: translateY(-5px);
    box-shadow: 
        0 12px 40px rgba(0,0,0,0.8),
        0 0 35px rgba(229, 9, 20, 0.25);
}}

/* 🔥 TITLE */
h1 {{
    color: #E50914;
    text-align: center;
    font-size: 2.6rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-shadow: 0 0 15px rgba(229, 9, 20, 0.6);
}}

/* 🔥 INPUTS */
input, .stSelectbox, .stSlider {{
    background-color: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.1);
}}

/* 🔥 BUTTON */
.stButton>button {{
    width: 100%;
    background: linear-gradient(135deg, #E50914, #ff2e2e);
    color: white;
    font-weight: bold;
    border-radius: 10px;
    padding: 12px;
    transition: all 0.3s ease;
}}

.stButton>button:hover {{
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(229, 9, 20, 0.5);
}}

/* 🔥 TEXT */
label, .stMarkdown {{
    color: white !important;
}}

</style>
""", unsafe_allow_html=True)
# -------------------------------
# UI CONTENT
# -------------------------------

st.title("Movie Recommender")

movie = st.text_input("Movie Name")

emotion = st.selectbox(
    "Mood",
    ["None", "happy", "sad", "excited", "scared", "romantic", "motivated"]
)

duration = st.selectbox(
    "Duration",
    ["None", "short", "medium", "long"]
)

language = st.selectbox(
    "Language",
    ["None", "en", "hi"]
)

rating = st.slider("Minimum Rating", 0.0, 10.0, 0.0)

random_choice = st.checkbox("Random Movies")

# -------------------------------
# BUTTON ACTION
# -------------------------------

if st.button("Recommend"):

    emotion_val = None if emotion == "None" else emotion
    duration_val = None if duration == "None" else duration
    language_val = None if language == "None" else language
    rating_val = None if rating == 0.0 else rating

    results = hybrid_recommend(
        movie=movie if movie else None,
        emotion=emotion_val,
        duration=duration_val,
        language=language_val,
        min_rating=rating_val,
        random_choice=random_choice
    )

    st.subheader("Top Recommendations")

    for i, m in enumerate(results[:5], 1):
        st.write(f"{i}. {m}")
