import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
import time

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

# Different specialized models for each summary type (all free)
MODEL_CONFIGS = {
    "standard": {
        "model": "facebook/bart-large-cnn",
        "description": "Balanced general-purpose summary for any document type",
        "prompt_template": "Provide a comprehensive and balanced summary of the following text:\n\n{text}"
    },
    "executive": {
        "model": "microsoft/DialoGPT-medium",  # Good for conversational, business-focused summaries
        "description": "Strategic C-suite brief focusing on decisions and business impact",
        "prompt_template": "Create a concise executive summary focusing on key business decisions, strategic implications, and actionable recommendations for senior leadership:\n\n{text}"
    },
    "legal": {
        "model": "nlpconnect/legal-pegasus-cnndm",  # Specialized legal summarization
        "description": "Precise legal summary with obligations, terms and deadlines",
        "prompt_template": "Summarize this legal document highlighting obligations, terms, conditions, deadlines, and key legal provisions:\n\n{text}"
    },
    "technical": {
        "model": "sshleifer/distilbart-cnn-12-6",  # Good for technical content
        "description": "Technical summary focusing on specs, metrics and implementations",
        "prompt_template": "Provide a technical summary focusing on specifications, requirements, methodologies, and implementation details:\n\n{text}"
    },
    "financial": {
        "model": "google/pegasus-xsum",  # Good for factual, data-heavy content
        "description": "Financial summary highlighting all numbers and metrics",
        "prompt_template": "Create a financial summary emphasizing quantitative data, metrics, numbers, percentages, and financial information:\n\n{text}"
    }
}

app = FastAPI(
    title="AI Document Summarizer API",
    description="Context-aware document summarization with specialized models for each summary type",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        "service": "AI Document Summarizer with Specialized Models",
        "available_types": list(MODEL_CONFIGS.keys())
    }


@app.get("/summary-types")
def get_summary_types():
    return {
        stype: {
            "description": config["description"],
            "model": config["model"]
        }
        for stype, config in MODEL_CONFIGS.items()
    }


def create_specialized_prompt(text: str, summary_type: str) -> str:
    """Create specialized prompts for each summary type"""
    config = MODEL_CONFIGS[summary_type]
    return config["prompt_template"].format(text=text)


def extract_summary_from_response(result, model_name: str) -> str:
    """Extract summary text from different model response formats"""
    if isinstance(result, list) and len(result) > 0:
        # Handle list response format
        if isinstance(result[0], dict):
            if "summary_text" in result[0]:
                return result[0]["summary_text"]
            elif "generated_text" in result[0]:
                return result[0]["generated_text"]
        return str(result[0])
    elif isinstance(result, dict):
        # Handle dict response format
        if "summary_text" in result:
            return result["summary_text"]
        elif "generated_text" in result:
            return result["generated_text"]
        elif "0" in result:  # Some models return with numeric keys
            return str(result["0"])
    return str(result)


@app.post("/summarize")
def create_summary(request: SummaryRequest):
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    if len(request.text) > 10000:
        raise HTTPException(
            status_code=400,
            detail="Text too long. Maximum 10,000 characters allowed."
        )

    # Get the appropriate model and create specialized prompt
    config = MODEL_CONFIGS[request.summary_type]
    model_url = f"https://api-inference.huggingface.co/models/{config['model']}"
    guided_text = create_specialized_prompt(request.text, request.summary_type)

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": guided_text}

    start_time = time.time()
    
    try:
        response = requests.post(model_url, json=payload, headers=headers, timeout=30)
        processing_time = time.time() - start_time

        if response.status_code == 200:
            result = response.json()
            summary = extract_summary_from_response(result, config['model'])
            
            return {
                "success": True,
                "summary": summary,
                "metadata": {
                    "summary_type": request.summary_type,
                    "specialized_model": config["model"],
                    "original_length": len(request.text),
                    "summary_length": len(summary),
                    "processing_time_seconds": round(processing_time, 2),
                    "technique": "specialized-model"
                }
            }
        elif response.status_code == 503:
            # Model is loading - provide helpful message
            raise HTTPException(
                status_code=503,
                detail=f"Model {config['model']} is currently loading. This is normal for less frequently used models. Please try again in 30-60 seconds."
            )
        else:
            # If specialized model fails, fall back to standard BART model
            print(f"Specialized model {config['model']} failed, falling back to standard model. Error: {response.text}")
            
            fallback_config = MODEL_CONFIGS["standard"]
            fallback_url = f"https://api-inference.huggingface.co/models/{fallback_config['model']}"
            fallback_prompt = create_specialized_prompt(request.text, request.summary_type)
            fallback_payload = {"inputs": fallback_prompt}
            
            fallback_response = requests.post(fallback_url, json=fallback_payload, headers=headers, timeout=30)
            
            if fallback_response.status_code == 200:
                fallback_result = fallback_response.json()
                summary = extract_summary_from_response(fallback_result, fallback_config['model'])
                
                return {
                    "success": True,
                    "summary": summary,
                    "metadata": {
                        "summary_type": request.summary_type,
                        "specialized_model": f"{config['model']} (failed, used {fallback_config['model']} fallback)",
                        "original_length": len(request.text),
                        "summary_length": len(summary),
                        "processing_time_seconds": round(processing_time, 2),
                        "note": "Specialized model unavailable, used standard model as fallback"
                    }
                }
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Both specialized and fallback models failed. Please try again later."
                )
    
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="Request timeout. Model may be loading.")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")


@app.get("/stats")
def get_stats():
    models_info = {
        stype: {
            "model": config["model"],
            "description": config["description"]
        }
        for stype, config in MODEL_CONFIGS.items()
    }
    
    return {
        "specialized_models": models_info,
        "available_summary_types": len(MODEL_CONFIGS),
        "max_text_length": 10000,
        "status": "operational",
        "pricing": "free (Hugging Face Inference API)"
    }


# Enhanced health check that tests all models
@app.get("/health")
def health_check():
    results = {}
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    
    for summary_type, config in MODEL_CONFIGS.items():
        model_url = f"https://api-inference.huggingface.co/models/{config['model']}"
        try:
            # Just check if model endpoint is accessible
            test_payload = {"inputs": "Test"}
            response = requests.post(model_url, json=test_payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                status = "accessible"
            elif response.status_code == 503:
                status = "loading (normal for less used models)"
            else:
                status = f"error: {response.status_code}"
                
            results[summary_type] = {
                "model": config["model"],
                "status": status
            }
            
        except requests.exceptions.Timeout:
            results[summary_type] = {
                "model": config["model"],
                "status": "timeout"
            }
        except Exception as e:
            results[summary_type] = {
                "model": config["model"],
                "status": f"error: {str(e)}"
            }
    
    return {"model_status": results}


# Test endpoint to compare different models
@app.post("/test-comparison")
def test_model_comparison(request: SummaryRequest):
    """Test endpoint to see summaries from all models for comparison"""
    results = {}
    
    for summary_type in MODEL_CONFIGS.keys():
        try:
            # Create test request for each type
            test_request = SummaryRequest(text=request.text, summary_type=summary_type)
            
            # Simulate the summarize logic
            config = MODEL_CONFIGS[summary_type]
            model_url = f"https://api-inference.huggingface.co/models/{config['model']}"
            guided_text = create_specialized_prompt(request.text, summary_type)
            
            headers = {"Authorization": f"Bearer {HF_API_KEY}"}
            payload = {"inputs": guided_text}
            
            response = requests.post(model_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                summary = extract_summary_from_response(result, config['model'])
                results[summary_type] = {
                    "summary": summary,
                    "model": config["model"],
                    "status": "success"
                }
            else:
                results[summary_type] = {
                    "summary": None,
                    "model": config["model"],
                    "status": f"failed: {response.status_code}",
                    "error": response.text
                }
                
        except Exception as e:
            results[summary_type] = {
                "summary": None,
                "model": config["model"],
                "status": f"exception: {str(e)}"
            }
    
    return {
        "original_text_sample": request.text[:200] + "..." if len(request.text) > 200 else request.text,
        "comparison_results": results
    }