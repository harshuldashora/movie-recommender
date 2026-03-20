from src.recommender import recommend
from src.filter_engine import filter_movies
from src.emotion_model import recommend_by_emotion
from src.random_engine import random_movies


def hybrid_recommend(movie=None, emotion=None,
                     duration=None, language=None,
                     min_rating=None, random_choice=False):

    # 1. Random mode
    if random_choice:
        return random_movies(5)

    # 2. Get results
    sim_results = recommend(movie) if movie else []
    emo_results = recommend_by_emotion(emotion) if emotion else []

    # 3. Combine
    if movie and emotion:
        results = list(set(sim_results) & set(emo_results))
    else:
        results = sim_results if sim_results else emo_results

    # 4. If too few → relax to similarity
    if len(results) < 5:
        results = sim_results if sim_results else emo_results

    # 5. Apply filters SMARTLY
    if duration or language or min_rating:
        filtered = filter_movies(duration, language, min_rating)

        filtered_results = [m for m in results if m in filtered]

        # If filter too strict → don’t kill results
        if len(filtered_results) >= 3:
            results = filtered_results

    # 6. Final fallback
    if len(results) == 0:
        return random_movies(5)

    return results[:5]