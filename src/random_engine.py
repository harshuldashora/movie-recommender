import pickle

# Load dataset
movies = pickle.load(open('model/movies.pkl', 'rb'))


def random_movies(n=5):
    return movies.sample(n)['title'].tolist()


if __name__ == "__main__":
    print(random_movies(5))