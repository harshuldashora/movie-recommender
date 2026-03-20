import pickle

# Load dataset
movies = pickle.load(open('model/movies.pkl', 'rb'))


def filter_movies(duration=None, language=None, min_rating=None):
    df = movies.copy()

    # Duration filter
    if duration == "short":
        df = df[df['runtime'] < 90]

    elif duration == "medium":
        df = df[(df['runtime'] >= 90) & (df['runtime'] <= 120)]

    elif duration == "long":
        df = df[df['runtime'] > 120]

    # Language filter
    if language:
        df = df[df['original_language'] == language]

    # Rating filter
    if min_rating:
        df = df[df['vote_average'] >= min_rating]

    # Sort by rating (important)
    df = df.sort_values(by='vote_average', ascending=False)

    return df['title'].head(10).tolist()


if __name__ == "__main__":
    print(filter_movies(duration="short", language="en", min_rating=7))