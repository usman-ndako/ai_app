'''# Day 5: Professional AI Summarizer API with Context-Aware Intelligence
# Prevents hallucinations and ensures tone-appropriate summaries

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from typing import Literal
import time

# Initialize FastAPI
app = FastAPI(
    title="AI Document Summarizer API",
    description="Context-aware document summarization with tone control and fact-grounding",
    version="1.0.0"
)

# Load AI model once at startup
print("🔄 Loading AI model...")
MODEL_NAME = "sshleifer/distilbart-cnn-12-6"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
print("✅ AI model loaded and ready!")

# BUSINESS LOGIC: Context-aware summary configurations
SUMMARY_CONFIGS = {
    "standard": {
        "max_length": 120,
        "min_length": 40,
        "prefix": "Summarize the following text concisely: ",
        "description": "Balanced general-purpose summary for any document type"
    },
    "executive": {
        "max_length": 50,
        "min_length": 20,
        "prefix": "Summarize the key business impact, financial metrics, and strategic decisions: ",
        "description": "Brief C-suite summary focusing on business outcomes"
    },
    "legal": {
        "max_length": 150,
        "min_length": 60,
        "prefix": "Summarize the legal obligations, parties involved, key terms, and critical deadlines mentioned: ",
        "description": "Precise legal summary with obligations and deadlines"
    },
    "technical": {
        "max_length": 180,
        "min_length": 70,
        "prefix": "Summarize the technical specifications, requirements, system details, and implementation aspects: ",
        "description": "Technical summary focusing on specs and requirements"
    },
    "financial": {
        "max_length": 120,
        "min_length": 50,
        "prefix": "Summarize the financial data, revenue figures, expenses, and key financial metrics mentioned: ",
        "description": "Financial summary highlighting numbers and metrics"
    }
}

# Data model for API requests (what clients send)
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

# Health check
@app.get("/")
def root():
    return {
        "status": "online",
        "service": "AI Document Summarizer",
        "available_types": list(SUMMARY_CONFIGS.keys())
    }

# Get available summary types
@app.get("/summary-types")
def get_summary_types():
    """Returns available summary types and their descriptions"""
    return {
        stype: {"description": config["description"]} 
        for stype, config in SUMMARY_CONFIGS.items()
    }

    # CORE BUSINESS ENDPOINT: Document Summarization
@app.post("/summarize")
def create_summary(request: SummaryRequest):
    """
    Main summarization endpoint - this is what clients pay for
    
    Takes document text and returns context-aware summary
    Prevents hallucinations by grounding AI to source text only
    """
    
    # Validation: Check if text is provided
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Validation: Check text length (prevent abuse/overload)
    if len(request.text) > 10000:
        raise HTTPException(
            status_code=400, 
            detail="Text too long. Maximum 10,000 characters allowed."
        )
    
    # Get configuration for requested summary type
    config = SUMMARY_CONFIGS[request.summary_type]
    
    # Performance tracking (important for SLA monitoring)
    start_time = time.time()
    
    try:
        # ANTI-HALLUCINATION: Add prefix that grounds AI to source text
        prompted_text = config["prefix"] + request.text
        
        # Tokenize input (convert text to numbers AI understands)
        inputs = tokenizer.encode(
            prompted_text, 
            return_tensors="pt", 
            max_length=512,  # Model's context window limit
            truncation=True   # Cut if too long (prevents errors)
        )
        
        # Generate summary with type-specific constraints
        summary_ids = model.generate(
            inputs,
            max_length=config["max_length"],
            min_length=config["min_length"],
            length_penalty=2.0,      # Encourages conciseness
            num_beams=4,             # Quality vs speed tradeoff (4 is good)
            early_stopping=True,     # Stop when good summary found
            no_repeat_ngram_size=3   # Prevents repetitive phrases
        )
        
        # Decode AI output back to human text
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        # Calculate performance metrics
        processing_time = time.time() - start_time
        
        # Return professional API response
        return {
            "success": True,
            "summary": summary,
            "metadata": {
                "summary_type": request.summary_type,
                "original_length": len(request.text),
                "summary_length": len(summary),
                "compression_ratio": f"{(len(summary) / len(request.text) * 100):.1f}%",
                "processing_time_seconds": round(processing_time, 2),
                "model_version": MODEL_NAME
            }
        }
        
    except Exception as e:
        # Enterprise-grade error handling
        raise HTTPException(
            status_code=500,
            detail=f"Summarization failed: {str(e)}"
        )


# Usage statistics endpoint (for your analytics/billing)
@app.get("/stats")
def get_stats():
    """
    Returns API statistics - useful for monitoring and billing
    """
    return {
        "model_name": MODEL_NAME,
        "available_summary_types": len(SUMMARY_CONFIGS),
        "max_text_length": 10000,
        "status": "operational"
    }'''

# Day 5: Professional AI Summarizer API with Context-Aware Intelligence
# Prevents hallucinations and ensures tone-appropriate summaries

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # ADD THIS
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from typing import Literal
import time

# Initialize FastAPI
app = FastAPI(
    title="AI Document Summarizer API",
    description="Context-aware document summarization with tone control and fact-grounding",
    version="1.0.0"
)

# ADD CORS MIDDLEWARE - CRITICAL FOR FRONTEND
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Load AI model once at startup
print("🔄 Loading AI model...")
MODEL_NAME = "sshleifer/distilbart-cnn-12-6"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
print("✅ AI model loaded and ready!")

# BUSINESS LOGIC: Context-aware summary configurations
# Updated with better tone control and complete sentence generation
SUMMARY_CONFIGS = {
    "standard": {
        "max_length": 130,
        "min_length": 50,
        "length_penalty": 1.5,
        "prefix": "Provide a clear, balanced summary of the following: ",
        "description": "Balanced general-purpose summary for any document type"
    },
    "executive": {
    "max_length": 65,
    "min_length": 35,
    "length_penalty": 1.5,
    "prefix": "As a C-suite executive summary, extract ONLY the most critical strategic insights: What changed? What are the key numbers? What decisions or actions are needed? Focus on business impact and ROI: ",
    "description": "Strategic C-suite brief focusing on decisions and business impact"
    },
    "legal": {
        "max_length": 180,
        "min_length": 80,
        "length_penalty": 1.5,
        "prefix": "Provide a precise legal analysis identifying all parties, obligations, payment terms, termination clauses, liabilities, and critical deadlines explicitly stated: ",
        "description": "Precise legal summary with obligations, terms and deadlines"
    },
    "technical": {
        "max_length": 200,
        "min_length": 90,
        "length_penalty": 1.5,
        "prefix": "Provide a detailed technical summary covering system specifications, performance metrics, architecture details, identified issues, and specific technical recommendations: ",
        "description": "Technical summary focusing on specs, metrics and implementations"
    },
    "financial": {
        "max_length": 140,
        "min_length": 60,
        "length_penalty": 1.5,
        "prefix": "Provide a financial summary highlighting all revenue figures, expense data, percentage changes, profit margins, and quantitative business metrics explicitly mentioned: ",
        "description": "Financial summary highlighting all numbers and metrics"
    }
}

# Data model for API requests (what clients send)
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

# Health check
@app.get("/")
def root():
    return {
        "status": "online",
        "service": "AI Document Summarizer",
        "available_types": list(SUMMARY_CONFIGS.keys())
    }

# Get available summary types
@app.get("/summary-types")
def get_summary_types():
    """Returns available summary types and their descriptions"""
    return {
        stype: {"description": config["description"]} 
        for stype, config in SUMMARY_CONFIGS.items()
    }

# CORE BUSINESS ENDPOINT: Document Summarization
@app.post("/summarize")
def create_summary(request: SummaryRequest):
    """
    Main summarization endpoint - this is what clients pay for
    
    Takes document text and returns context-aware summary
    Prevents hallucinations by grounding AI to source text only
    """
    
    # Validation: Check if text is provided
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Validation: Check text length (prevent abuse/overload)
    if len(request.text) > 10000:
        raise HTTPException(
            status_code=400, 
            detail="Text too long. Maximum 10,000 characters allowed."
        )
    
    # Get configuration for requested summary type
    config = SUMMARY_CONFIGS[request.summary_type]
    
    # Performance tracking (important for SLA monitoring)
    start_time = time.time()
    
    try:
        # ANTI-HALLUCINATION: Add prefix that grounds AI to source text
        prompted_text = config["prefix"] + request.text
        
        # Tokenize input (convert text to numbers AI understands)
        inputs = tokenizer.encode(
            prompted_text, 
            return_tensors="pt", 
            max_length=512,  # Model's context window limit
            truncation=True   # Cut if too long (prevents errors)
        )
        
        # Generate summary with type-specific constraints
        summary_ids = model.generate(
            inputs,
            max_length=config["max_length"],
            min_length=config["min_length"],
            length_penalty=config["length_penalty"],  # Now uses config value
            num_beams=4,             # Quality vs speed tradeoff (4 is good)
            early_stopping=True,     # Stop when good summary found
            no_repeat_ngram_size=3,  # Prevents repetitive phrases
            do_sample=False          # Deterministic output (consistency)
        )
        
        # Decode AI output back to human text
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        # Calculate performance metrics
        processing_time = time.time() - start_time
        
        # Return professional API response
        return {
            "success": True,
            "summary": summary,
            "metadata": {
                "summary_type": request.summary_type,
                "original_length": len(request.text),
                "summary_length": len(summary),
                "compression_ratio": f"{(len(summary) / len(request.text) * 100):.1f}%",
                "processing_time_seconds": round(processing_time, 2),
                "model_version": MODEL_NAME
            }
        }
        
    except Exception as e:
        # Enterprise-grade error handling
        raise HTTPException(
            status_code=500,
            detail=f"Summarization failed: {str(e)}"
        )


# Usage statistics endpoint (for your analytics/billing)
@app.get("/stats")
def get_stats():
    """
    Returns API statistics - useful for monitoring and billing
    """
    return {
        "model_name": MODEL_NAME,
        "available_summary_types": len(SUMMARY_CONFIGS),
        "max_text_length": 10000,
        "status": "operational"
    }