import pandas as pd
from utils import convert, fetch_director, clean_list


def preprocess():
    print("Loading data...")

    # Load datasets
    movies = pd.read_csv('data/raw/tmdb_5000_movies.csv')
    credits = pd.read_csv('data/raw/tmdb_5000_credits.csv')

    print("Merging datasets...")
    movies = movies.merge(credits, on='title')

    print("Selecting required columns...")
    movies = movies[['movie_id', 'title', 'overview', 'genres',
                     'keywords', 'cast', 'crew', 'runtime',
                     'original_language', 'vote_average']]

    print("Dropping missing values...")
    movies.dropna(inplace=True)

    print("Converting JSON columns...")
    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(lambda x: convert(x)[:3])
    movies['crew'] = movies['crew'].apply(fetch_director)

    print("Cleaning text...")
    movies['genres'] = movies['genres'].apply(clean_list)
    movies['keywords'] = movies['keywords'].apply(clean_list)
    movies['cast'] = movies['cast'].apply(clean_list)
    movies['crew'] = movies['crew'].apply(clean_list)

    print("Processing overview (important)...")
    # ✅ LIMIT overview to reduce noise (VERY IMPORTANT)
    movies['overview'] = movies['overview'].apply(lambda x: x.split()[:30])

    print("Creating tags (optimized for embeddings)...")

    # ❌ DO NOT include language in tags (use as filter only)

    movies['tags'] = (
        movies['overview'] +
        movies['genres'] * 2 +
        movies['keywords'] * 2 +
        movies['cast'] +
        movies['crew']
    )

    print("Converting tags to string...")
    movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))

    print("Final dataset...")
    new_df = movies[['movie_id', 'title', 'tags',
                     'runtime', 'original_language', 'vote_average']]

    print("Saving file...")
    new_df.to_csv('data/processed/movies_cleaned.csv', index=False)

    print("Preprocessing Done Successfully!")


if __name__ == "__main__":
    preprocess()
