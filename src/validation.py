# src/validation.py
from fastapi import HTTPException

def recommend_similar_movies(title, movie_user_matrix, ratings_sparse, knn_model, movies_df, top_n=10):
    """
    Return top_n similar movies with similarity score and genres.
    """
    if title not in movie_user_matrix.index:
        raise HTTPException(status_code=404, detail=f"Movie '{title}' not found.")

    idx = movie_user_matrix.index.get_loc(title)
    distances, indices = knn_model.kneighbors(ratings_sparse[idx], n_neighbors=min(top_n+1, len(movie_user_matrix)))

    out = []
    for i in range(1, len(indices[0])):  # skip itself
        rec = movie_user_matrix.index[indices[0][i]]
        sim = 1 - float(distances[0][i])
        g = movies_df.loc[movies_df["title"] == rec, "genres"].values
        out.append({
            "title": rec,
            "similarity": round(sim, 4),
            "genres": g[0] if len(g) else ""
        })
    return out[:top_n]
