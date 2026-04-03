import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_similarity():
    print("Loading processed data...")

    # Load cleaned dataset
    df = pd.read_csv('data/processed/movies_cleaned.csv')

    print("Vectorizing text...")

    # Convert text to numerical vectors
    cv = TfidfVectorizer(max_features=10000, stop_words='english')
    vectors = cv.fit_transform(df['tags']).toarray()

    print("Calculating similarity matrix...")

    # Compute similarity
    similarity = cosine_similarity(vectors)

    print("Saving model files...")

    # Save dataset and similarity matrix
    pickle.dump(df, open('model/movies.pkl', 'wb'))
    pickle.dump(similarity, open('model/similarity.pkl', 'wb'))

    print("✅ Similarity model created successfully!")


if __name__ == "__main__":
    build_similarity()
