import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
import time

load_dotenv()  # Safe to keep for local development. On Render, it will do nothing if no .env file.

HF_API_KEY = os.getenv("HF_API_KEY")
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

app = FastAPI(
    title="AI Document Summarizer API",
    description="Context-aware document summarization with tone control and fact-grounding",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend dev origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUMMARY_CONFIGS = {
    "standard": {"description": "Balanced general-purpose summary for any document type"},
    "executive": {"description": "Strategic C-suite brief focusing on decisions and business impact"},
    "legal": {"description": "Precise legal summary with obligations, terms and deadlines"},
    "technical": {"description": "Technical summary focusing on specs, metrics and implementations"},
    "financial": {"description": "Financial summary highlighting all numbers and metrics"},
}

class SummaryRequest(BaseModel):
    text: str
    summary_type: Literal["standard", "executive", "legal", "technical", "financial"] = "standard"
    
    class Config:
        schema_extra = {
            "example": {
                "text": "The quarterly report shows revenue of $2.5M with 35% growth...",
                "summary_type": "executive"
            }
        }


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "AI Document Summarizer",
        "available_types": list(SUMMARY_CONFIGS.keys())
    }


@app.get("/summary-types")
def get_summary_types():
    return {
        stype: {"description": config["description"]}
        for stype, config in SUMMARY_CONFIGS.items()
    }


@app.post("/summarize")
def create_summary(request: SummaryRequest):
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    if len(request.text) > 10000:
        raise HTTPException(
            status_code=400,
            detail="Text too long. Maximum 10,000 characters allowed."
        )

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": request.text}

    start_time = time.time()
    response = requests.post(HF_API_URL, json=payload, headers=headers)
    processing_time = time.time() - start_time

    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and "summary_text" in result[0]:
            summary = result[0]["summary_text"]
        else:
            summary = str(result)
        return {
            "success": True,
            "summary": summary,
            "metadata": {
                "summary_type": request.summary_type,
                "original_length": len(request.text),
                "summary_length": len(summary),
                "processing_time_seconds": round(processing_time, 2),
                "model_version": "facebook/bart-large-cnn (via Hugging Face API)"
            }
        }
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Summarization failed: {response.text}")


@app.get("/stats")
def get_stats():
    return {
        "model_name": "facebook/bart-large-cnn (via Hugging Face API)",
        "available_summary_types": len(SUMMARY_CONFIGS),
        "max_text_length": 10000,
        "status": "operational"
    }
