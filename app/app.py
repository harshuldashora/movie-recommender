import streamlit as st
import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hybrid_recommender import hybrid_recommend


# -------------------------------
# UI CONFIG
# -------------------------------

st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")

st.title("🎬 AI Hybrid Movie Recommendation System")

st.markdown("Get movie suggestions based on mood, similarity, and filters")

# -------------------------------
# INPUTS
# -------------------------------

movie = st.text_input("🎥 Enter Movie Name (e.g., Avatar, Batman)")

emotion = st.selectbox(
    "😊 Select Mood",
    ["None", "happy", "sad", "excited", "scared", "romantic", "motivated"]
)

duration = st.selectbox(
    "⏱ Select Duration",
    ["None", "short", "medium", "long"]
)

language = st.selectbox(
    "🌍 Select Language",
    ["None", "en", "hi"]
)

rating = st.slider("⭐ Minimum Rating", 0.0, 10.0, 0.0)

random_choice = st.checkbox("🎲 Random Movies")

# -------------------------------
# BUTTON ACTION
# -------------------------------

if st.button("🚀 Recommend"):

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

    st.subheader("🎯 Top 5 Recommendations")

    # Show only 5 movies
    results = results[:5]

    for i, m in enumerate(results, 1):
        st.write(f"{i}. {m}")