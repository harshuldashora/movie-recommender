import os
import pickle
import pandas as pd
import requests

# ==============================
# Paths
# ==============================
MOVIES_PATH = "model/movies.pkl"
SIMILARITY_PATH = "model/similarity.pkl"

# ==============================
# Hugging Face Links (BEST)
# ==============================
MOVIES_URL = "https://huggingface.co/harshuldashora/movie-recommender/resolve/main/movies.pkl"
SIMILARITY_URL = "https://huggingface.co/harshuldashora/movie-recommender/resolve/main/similarity.pkl"


# ==============================
# Download Function (robust)
# ==============================
def download_file(path, url):
    os.makedirs("model", exist_ok=True)

    # Download if missing or too small (corrupt)
    if not os.path.exists(path) or os.path.getsize(path) < 1_000_000:
        print(f"Downloading {path}...")

        if os.path.exists(path):
            os.remove(path)

        response = requests.get(url, stream=True)

        with open(path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        size = os.path.getsize(path)
        print(f"{path} size: {size}")

        if size < 1_000_000:
            raise Exception(f"{path} download failed.")

        print(f"{path} downloaded successfully!")


# ==============================
# Ensure files exist
# ==============================
download_file(MOVIES_PATH, MOVIES_URL)
download_file(SIMILARITY_PATH, SIMILARITY_URL)


# ==============================
# Load Data
# ==============================
movies = pickle.load(open(MOVIES_PATH, 'rb'))
similarity = pickle.load(open(SIMILARITY_PATH, 'rb'))


# ==============================
# Recommendation Function
# ==============================
def recommend(movie, top_n=5, language=None):
    movie = movie.lower()
    movies['title_lower'] = movies['title'].str.lower()

    if movie not in movies['title_lower'].values:
        return ["Movie not found in database"]

    movie_index = movies[movies['title_lower'] == movie].index[0]
    distances = similarity[movie_index]

    movie_scores = []

    for i, score in enumerate(distances):

        # ✅ LANGUAGE FILTER (MAIN FIX)
        if language and movies.iloc[i]['original_language'] != language:
            continue

        rating = movies.iloc[i]['vote_average']
        final_score = (0.7 * score) + (0.3 * (rating / 10))
        movie_scores.append((i, final_score))

    movie_scores = sorted(movie_scores, reverse=True, key=lambda x: x[1])

    recommended_movies = []

    for i in movie_scores[1:top_n+1]:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


# ==============================
# Test
# ==============================
if __name__ == "__main__":
    print(recommend("Avatar", language="en"))