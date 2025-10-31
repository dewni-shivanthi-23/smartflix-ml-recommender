# src/test.py
# Example: quick test
from src.utils import load_data
movies, ratings, movie_user_matrix, ratings_sparse = load_data()
print("Movies loaded:", len(movies))
print("Users:", movie_user_matrix.shape[1])
