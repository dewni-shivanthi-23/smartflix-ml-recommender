# src/utils.py
import pandas as pd
from scipy.sparse import csr_matrix
from pathlib import Path

def get_default_csv_paths():
    """
    Auto-detect CSV paths inside notebooks/FC212024_R.G.V.Dilsara folder.
    Returns (movies_csv, ratings_csv)
    """
    base_dir = Path(__file__).resolve().parent.parent  # project root
    notebook_dir = base_dir / "notebooks" / "FC212024_R.G.V.Dilsara"
    movies_csv = notebook_dir / "movies.csv"
    ratings_csv = notebook_dir / "ratings.csv"

    if not movies_csv.exists() or not ratings_csv.exists():
        raise FileNotFoundError(f"CSV files not found in {notebook_dir}")
    return str(movies_csv), str(ratings_csv)


def load_data(movies_path=None, ratings_path=None, min_count=50):
    """
    Load movies and ratings CSVs, filter popular movies, and return
    movies_df, ratings_df, movie_user_matrix, ratings_sparse
    """
    if movies_path is None or ratings_path is None:
        movies_path, ratings_path = get_default_csv_paths()

    movies = pd.read_csv(movies_path)
    ratings = pd.read_csv(ratings_path)

    movie_data = pd.merge(ratings, movies, on="movieId")
    popular = movie_data["title"].value_counts()
    popular_list = popular[popular >= min_count].index.tolist()
    filtered = movie_data[movie_data["title"].isin(popular_list)]

    movie_user_matrix = filtered.pivot_table(
        index="title", columns="userId", values="rating"
    ).fillna(0)

    ratings_sparse = csr_matrix(movie_user_matrix.values)

    return movies, ratings, movie_user_matrix, ratings_sparse


def search_movies(movies_df, query, available_titles=None):
    """
    Search for movies by title or year.
    Optionally filter to available_titles (e.g., popular movies)
    """
    query = query.strip()
    df = movies_df
    if available_titles is not None:
        df = movies_df[movies_df["title"].isin(available_titles)]

    if query.isdigit() and len(query) == 4:
        df = df[df["title"].str.contains(rf"\({query}\)", regex=True, case=False)]
    else:
        df = df[df["title"].str.contains(query, case=False, na=False)]

    return df[["title", "genres"]].drop_duplicates()
