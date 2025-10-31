# src/train.py
from sklearn.neighbors import NearestNeighbors

def train_knn(ratings_sparse):
    """
    Train a KNN model for collaborative filtering
    """
    knn = NearestNeighbors(metric="cosine", algorithm="brute")
    knn.fit(ratings_sparse)
    return knn
