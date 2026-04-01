import pickle
import pandas as pd

# Load saved data
movies = pickle.load(open('model/movies.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))


def recommend(movie, top_n=5):
    # Convert titles to lowercase for matching
    movie = movie.lower()
    movies['title_lower'] = movies['title'].str.lower()

    # Check if movie exists
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


if __name__ == "__main__":
    print(recommend("Avatar"))
