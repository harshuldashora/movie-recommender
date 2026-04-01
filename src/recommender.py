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
# Google Drive Direct Links
# ==============================
MOVIES_URL = "https://drive.google.com/uc?id=1k3TuuEdfjlifTiroEbOWK0-S1gFDlUEA"
SIMILARITY_URL = "https://drive.google.com/uc?id=1VnJsEN_RJ4iF9JlSJkeULmCL4djgjEW_"


# ==============================
# Download Function (robust)
# ==============================
def download_file(path, url):
    os.makedirs("model", exist_ok=True)

    # Re-download if file missing or corrupted
    if not os.path.exists(path) or os.path.getsize(path) < 5_000_000:
        print(f"Downloading {path}...")

        if os.path.exists(path):
            os.remove(path)

        gdown.download(url, path, quiet=False)

        # Validate file size
        size = os.path.getsize(path)
        print(f"{path} size: {size}")

        if size < 5_000_000:
            raise Exception(f"{path} download failed or corrupted.")

        print(f"{path} downloaded successfully!")


# ==============================
# Download files
# ==============================
download_file(MOVIES_PATH, MOVIES_URL)
download_file(SIMILARITY_PATH, SIMILARITY_URL)


# ==============================
# Load Data
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
# Test
# ==============================
if __name__ == "__main__":
    print(recommend("Avatar"))
