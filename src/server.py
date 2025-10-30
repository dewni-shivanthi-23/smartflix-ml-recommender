from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from rapidfuzz import process, fuzz  # faster than fuzzywuzzy

# ---- paths: update if your CSVs are elsewhere
MOVIES_CSV  = r"./notebooks/FC212024_R.G.V.Dilsara/movies.csv"
RATINGS_CSV = r"./notebooks/FC212024_R.G.V.Dilsara/ratings.csv"
MIN_COUNT   = 50

# ---- load + fit once
movies  = pd.read_csv(MOVIES_CSV)
ratings = pd.read_csv(RATINGS_CSV)

movie_data   = pd.merge(ratings, movies, on="movieId")
popular      = movie_data["title"].value_counts()
popular_list = popular[popular >= MIN_COUNT].index.tolist()
filtered     = movie_data[movie_data["title"].isin(popular_list)]

movie_user_matrix = filtered.pivot_table(index="title", columns="userId", values="rating").fillna(0)
ratings_sparse    = csr_matrix(movie_user_matrix.values)

knn = NearestNeighbors(metric="cosine", algorithm="brute")
knn.fit(ratings_sparse)

def recommend_single(title: str, top_n: int = 10):
    if title not in movie_user_matrix.index:
        guess, score, _ = process.extractOne(title, movie_user_matrix.index.tolist(), scorer=fuzz.WRatio)
        raise HTTPException(status_code=404, detail=f"'{title}' not found. Did you mean '{guess}'?")
    idx = movie_user_matrix.index.get_loc(title)
    distances, indices = knn.kneighbors(ratings_sparse[idx], n_neighbors=min(top_n+1, len(movie_user_matrix)))
    out = []
    for i in range(1, len(indices[0])):  # skip itself
        rec = movie_user_matrix.index[indices[0][i]]
        sim = 1 - float(distances[0][i])
        g = movies.loc[movies["title"] == rec, "genres"].values
        out.append({"title": rec, "similarity": round(sim, 4), "genres": g[0] if len(g) else ""})
    return out[:top_n]
# after building movie_user_matrix
AVAILABLE_TITLES = set(movie_user_matrix.index)

def search_titles(q: str, limit: int = 20):
    q = q.strip()
    df = movies[movies["title"].isin(AVAILABLE_TITLES)]  # << filter to indexable titles
    if q.isdigit() and len(q) == 4:
        m = df[df["title"].str.contains(rf"\({q}\)", regex=True, case=False, na=False)]
    else:
        m = df[df["title"].str.contains(q, case=False, na=False)]
    m = m[["title", "genres"]].drop_duplicates().head(limit)
    return [{"title": r.title, "genres": r.genres} for r in m.itertuples(index=False)]


class RecommendBody(BaseModel):
    title: str
    top_n: int = 10

class RecommendBatchBody(BaseModel):
    titles: list[str]
    top_n: int = 10

app = FastAPI(title="SmartFlix API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health(): return {"ok": True}

@app.get("/search")
def search(query: str, limit: int = 20): return {"items": search_titles(query, limit)}

@app.post("/recommend")
def recommend(body: RecommendBody): return {"items": recommend_single(body.title, body.top_n), "base": body.title}

@app.post("/recommend_batch")
def recommend_batch(body: RecommendBatchBody):
    pool = {}
    for t in body.titles:
        try:
            for r in recommend_single(t, body.top_n):
                pool[r["title"]] = max(pool.get(r["title"], 0.0), r["similarity"])
        except HTTPException:
            continue
    items = [{"title": k, "similarity": round(v, 4),
              "genres": movies.loc[movies["title"] == k, "genres"].values[0]}
             for k, v in pool.items() if k not in set(body.titles)]
    items.sort(key=lambda x: x["similarity"], reverse=True)
    return {"items": items[:body.top_n], "base": body.titles}
