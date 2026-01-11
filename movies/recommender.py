import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

movies_path = os.path.join(BASE_DIR, "data", "movies.csv")
ratings_path = os.path.join(BASE_DIR, "data", "ratings.csv")

movies = pd.read_csv(movies_path)
ratings = pd.read_csv(ratings_path)

# ---------------- CONTENT BASED ----------------
cv = CountVectorizer(tokenizer=lambda x: x.split('|'))
genre_matrix = cv.fit_transform(movies['genres'])
genre_similarity = cosine_similarity(genre_matrix)

def recommend_by_movie(title, n=5):
    if title not in movies['title'].values:
        return []

    idx = movies[movies['title'] == title].index[0]
    scores = list(enumerate(genre_similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    return movies.iloc[[i[0] for i in scores[1:n+1]]][
        ["movieId", "title", "genres"]
    ].to_dict(orient="records")

# ---------------- TOP RATED ----------------
def top_rated_movies(n=5):
    avg = ratings.groupby("movieId")["rating"].mean()
    top = avg.sort_values(ascending=False).head(n)

    return movies[movies["movieId"].isin(top.index)][
        ["movieId", "title", "genres"]
    ].to_dict(orient="records")

# ---------------- COLLABORATIVE ----------------
def collaborative_recommend(user_id, n=5):
    matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
    sparse = csr_matrix(matrix.values)
    user_similarity = cosine_similarity(sparse)

    if user_id not in matrix.index:
        return []

    user_idx = matrix.index.tolist().index(user_id)
    scores = user_similarity[user_idx].dot(matrix.values)

    movie_scores = pd.Series(scores, index=matrix.columns)
    rated = matrix.loc[user_id]
    movie_scores = movie_scores[rated == 0]

    top_movies = movie_scores.sort_values(ascending=False).head(n)

    return movies[movies["movieId"].isin(top_movies.index)][
        ["movieId", "title", "genres"]
    ].to_dict(orient="records")
