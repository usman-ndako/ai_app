from fastapi import FastAPI, Query
from typing import List
import pandas as pd
import joblib

# Load the trained model and items data only once at startup
model = joblib.load("model_svd.pkl")
items = pd.read_csv("your_items.csv")

app = FastAPI(
    title="E-commerce Recommendation API",
    description="Personalized AI-powered recommendations using a trained SVD model.",
    version="1.0.0",
)

@app.get("/recommend/", summary="Get personalized product recommendations")
def recommend(user_id: int, n: int = 5, category: str = None):
    """
    Returns top-N recommended products for a given user.
    Optional: Filter recommendations by category.
    """
    movie_ids = [str(i) for i in items['item_id']]
    predicted_ratings = [(mid, model.predict(str(user_id), mid).est) for mid in movie_ids]
    # Sort by predicted score
    top_n = sorted(predicted_ratings, key=lambda x: x[1], reverse=True)
    top_n_ids = [int(x[0]) for x in top_n[:n*2]]  # get a few extra in case of filtering
    
    recommendations = items[items['item_id'].isin(top_n_ids)]
    if category:
        recommendations = recommendations[recommendations['category'].str.lower() == category.lower()]
    recommendations = recommendations.head(n)

    results = recommendations[['item_id', 'title', 'price', 'margin', 'category']].to_dict('records')
    return {"user_id": user_id, "recommendations": results}

# Optional: Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the E-commerce Recommendation API!"}
