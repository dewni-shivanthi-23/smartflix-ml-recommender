# 🎬 SmartFlix - Movie Recommendation System

SmartFlix is a machine learning-based movie recommendation system that provides personalized suggestions based on user preferences. It uses collaborative filtering and content-based filtering techniques to suggest movies users are most likely to enjoy.

---

## 📁 Project Structure
smartflix-ml-recommender/
├── data/ # Raw and cleaned datasets
├── notebooks/ # Jupyter notebooks for EDA and experiments
├── src/ # Source code
│ ├── models/ # Model training scripts
│ ├── preprocessing/ # Data cleaning and feature engineering
│ └── utils/ # Helper functions
├── results/ # Model outputs and evaluation reports
├── requirements.txt # Project dependencies
└── README.md # Project overview                                 

---

## 🚀 Getting Started

1. **Clone the repository**
   git clone https://github.com/your-username/smartflix-ml-recommender.git
   cd smartflix-ml-recommender

2. **Install the required packages**
   
3. **Explore the data and models**  
- Use the `notebooks/` directory to begin with EDA or experiments.
- Place any datasets in the `data/` directory.

---

## 🧠 ML Techniques Used

- **Collaborative Filtering** (SVD, KNN)
- **Content-Based Filtering** (TF-IDF + Cosine Similarity)
- **Hybrid Methods** (LightFM)
- **Supervised Learning Models** (Optional: XGBoost/Random Forest)

---

## 📊 Evaluation Metrics

- Root Mean Square Error (RMSE)
- Precision@K and Recall@K
- MAP@K (Mean Average Precision)

---

## 🖥️ Deployment

- Built with **Flask** and deployed on **Heroku**
- User inputs favorite movies or genres and receives 5–10 recommendations instantly

---

## 👥 Team – SE Group 03: The ReLU Rebels

- FC110583 – D.M.A.M.D.S Andradi – Team Lead
- FC110597 – R.G.V.Dilsara – Data Handler
- FC110601 – M.S.C.Udagedara – Model Trainer
- FC110577 – P.D.K.Padukka – Deployment Lead
- FC110605 – S.K.C.Dilshika – Developer

---

## 📎 References

- MovieLens 100K: https://grouplens.org/datasets/movielens/100k/
- Scikit-learn: https://scikit-learn.org/
- Surprise: https://surpriselib.com/
- LightFM: https://making.lyst.com/lightfm/
- Flask Docs: https://flask.palletsprojects.com/

