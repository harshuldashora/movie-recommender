import pickle

# Load dataset
movies = pickle.load(open('model/movies.pkl', 'rb'))


# Emotion → Genre mapping
emotion_map = {
    "happy": ["comedy", "family", "animation"],
    "sad": ["drama", "romance"],
    "excited": ["action", "adventure", "thriller"],
    "scared": ["horror", "thriller"],
    "romantic": ["romance"],
    "motivated": ["biography", "sport", "drama"]
}


def recommend_by_emotion(emotion):
    emotion = emotion.lower()

    if emotion not in emotion_map:
        return ["Emotion not recognized"]

    genres = emotion_map[emotion]

    # Filter movies based on genres in tags
    filtered = movies[movies['tags'].apply(
        lambda x: sum(g in x for g in genres) >= 2
    )]

    # Sort by rating
    filtered = filtered.sort_values(by='vote_average', ascending=False)

    return filtered['title'].head(10).tolist()


if __name__ == "__main__":
    print(recommend_by_emotion("happy"))