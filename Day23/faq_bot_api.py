# """
# AI FAQ Bot Backend
# Author: Usman Ndako
# Phase 4 — Day 23 (AI Customer Support Chatbot)
# Description:
# A FastAPI backend that uses semantic similarity to answer FAQ questions automatically.
# """

# # ------------------------------
# # 1. Imports
# # ------------------------------
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from sentence_transformers import SentenceTransformer, util
# import torch

# # ------------------------------
# # 2. Initialize App and Model
# # ------------------------------
# app = FastAPI(title="AI FAQ Bot", version="1.0")

# print("⏳ Loading embedding model...")
# model = SentenceTransformer("all-MiniLM-L6-v2")
# print("✅ Model loaded successfully!")

# # ------------------------------
# # 3. FAQ Knowledge Base
# # ------------------------------
# FAQS = [
#     {
#         "question": "How can I reset my password?",
#         "answer": "Click on 'Forgot Password' at the login page and follow the instructions."
#     },
#     {
#         "question": "How do I cancel my subscription?",
#         "answer": "Go to 'Account Settings' and select 'Cancel Subscription'."
#     },
#     {
#         "question": "Do you offer refunds?",
#         "answer": "Yes, we offer refunds within 30 days of purchase."
#     },
#     {
#         "question": "How can I contact support?",
#         "answer": "You can reach us anytime at support@yourcompany.com."
#     }
# ]

# # ------------------------------
# # 4. Precompute FAQ Embeddings
# # ------------------------------
# faq_questions = [faq["question"] for faq in FAQS]
# faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

# # ------------------------------
# # 5. Define Request Schema
# # ------------------------------
# class UserQuery(BaseModel):
#     question: str

# # ------------------------------
# # 6. Core Logic — Semantic Matching
# # ------------------------------
# @app.post("/ask")
# def ask_question(query: UserQuery):
#     try:
#         # Encode the user’s question
#         query_embedding = model.encode(query.question, convert_to_tensor=True)
        
#         # Compute cosine similarity
#         similarities = util.cos_sim(query_embedding, faq_embeddings)
        
#         # Get the best match
#         best_match_idx = torch.argmax(similarities).item()
#         best_score = float(similarities[0][best_match_idx])
#         best_faq = FAQS[best_match_idx]

#         # Optional: Confidence threshold
#         if best_score < 0.5:
#             return {
#                 "question": query.question,
#                 "answer": "I'm not sure about that. Please contact support for more details.",
#                 "similarity_score": best_score
#             }

#         # Return best match
#         return {
#             "question": query.question,
#             "matched_faq": best_faq["question"],
#             "answer": best_faq["answer"],
#             "similarity_score": best_score
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # ------------------------------
# # 7. Run Command (CLI)
# # ------------------------------
# # To start the API, run this in your terminal:
# # uvicorn faq_bot_api:app --reload


"""
AI FAQ Bot Backend (CSV/Excel Version)
Author: Boss
Phase 4 — Day 23 (Enhanced)
"""

# ------------------------------
# 1. Imports
# ------------------------------
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import torch
import pandas as pd
import os

# ------------------------------
# 2. Initialize App and Model
# ------------------------------
app = FastAPI(title="AI FAQ Bot", version="1.1")

print("⏳ Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Model loaded successfully!")

# ------------------------------
# 3. Load FAQs from CSV or Excel
# ------------------------------
def load_faq_data(file_path: str = "faqs.csv"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ FAQ file not found: {file_path}")

    # Automatically detect file type
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Use .csv or .xlsx")

    # Check for required columns
    if "question" not in df.columns or "answer" not in df.columns:
        raise ValueError("File must contain 'question' and 'answer' columns")

    faqs = df.to_dict(orient="records")
    print(f"✅ Loaded {len(faqs)} FAQ entries from {file_path}")
    return faqs

FAQS = load_faq_data("faqs.csv")

# ------------------------------
# 4. Precompute Embeddings
# ------------------------------
faq_questions = [faq["question"] for faq in FAQS]
faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

# ------------------------------
# 5. Define Schema
# ------------------------------
class UserQuery(BaseModel):
    question: str

# ------------------------------
# 6. Core Logic — Semantic Matching
# ------------------------------
@app.post("/ask")
def ask_question(query: UserQuery):
    try:
        query_embedding = model.encode(query.question, convert_to_tensor=True)
        similarities = util.cos_sim(query_embedding, faq_embeddings)
        best_match_idx = torch.argmax(similarities).item()
        best_score = float(similarities[0][best_match_idx])
        best_faq = FAQS[best_match_idx]

        if best_score < 0.5:
            return {
                "question": query.question,
                "answer": "I'm not sure about that. Please contact support for more information.",
                "similarity_score": best_score
            }

        return {
            "question": query.question,
            "matched_faq": best_faq["question"],
            "answer": best_faq["answer"],
            "similarity_score": best_score
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------------
# 7. Optional — Reload Endpoint (Admin Feature)
# ------------------------------
@app.post("/reload")
def reload_faqs():
    """
    Reload FAQ data and embeddings without restarting the server.
    """
    global FAQS, faq_embeddings
    FAQS = load_faq_data("faqs.csv")
    faq_questions = [faq["question"] for faq in FAQS]
    faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)
    return {"status": "✅ FAQ data reloaded", "count": len(FAQS)}

# ------------------------------
# 8. Run Command (CLI)
# ------------------------------
# uvicorn faq_bot_api:app --reload
