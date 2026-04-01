import os
import pickle
import pandas as pd
import gdown

# ==============================
# Paths
# ==============================
MOVIES_PATH = "model/movies.pkl"
SIMILARITY_PATH = "model/similarity.pkl"

# ==============================
# Google Drive Links (ORIGINAL)
# ==============================
MOVIES_URL = "https://drive.google.com/file/d/1hrhBsxABhGR2ts7gRPI7pyB6Fdn_OjkW/view"
SIMILARITY_URL = "https://drive.google.com/file/d/19lsw0YwtmgxjSojNeLeoRcywYoUevOnN/view"


# ==============================
# Download Function (using gdown)
# ==============================
def download_file(path, url):
    if not os.path.exists(path):
        os.makedirs("model", exist_ok=True)
        print(f"Downloading {path}...")

        gdown.download(url, path, quiet=False)

        print(f"{path} downloaded successfully!")


# ==============================
# Ensure Files Exist
# ==============================
download_file(MOVIES_PATH, MOVIES_URL)
download_file(SIMILARITY_PATH, SIMILARITY_URL)


# ==============================
# Load Data Safely
# ==============================
try:
    with open(MOVIES_PATH, "rb") as f:
        movies = pickle.load(f)

    with open(SIMILARITY_PATH, "rb") as f:
        similarity = pickle.load(f)

except Exception as e:
    raise RuntimeError(f"Error loading model files: {e}")


# ==============================
# Recommendation Function
# ==============================
def recommend(movie, top_n=5):
    movie = movie.lower()
    movies['title_lower'] = movies['title'].str.lower()

    if movie not in movies['title_lower'].values:
        return ["Movie not found in database"]

    movie_index = movies[movies['title_lower'] == movie].index[0]

    distances = similarity[movie_index]

    movie_scores = []

    for i, score in enumerate(distances):
        rating = movies.iloc[i]['vote_average']
        final_score = (0.7 * score) + (0.3 * (rating / 10))
        movie_scores.append((i, final_score))

    movie_scores = sorted(movie_scores, reverse=True, key=lambda x: x[1])

    recommended_movies = []

    for i in movie_scores[1:top_n+1]:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


# ==============================
# Test Run
# ==============================
if __name__ == "__main__":
    print(recommend("Avatar"))
