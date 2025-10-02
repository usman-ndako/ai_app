import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
import time
import re

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

# Using ONLY verified free Inference API models
MODEL_CONFIGS = {
    "standard": {
        "model": "facebook/bart-large-cnn",
        "description": "Balanced general-purpose summary",
        "use_prompt": False,
        "max_length": 350,
        "min_length": 150
    },
    "executive": {
        "model": "facebook/bart-large-cnn",
        "description": "Strategic business-focused brief",
        "use_prompt": False,
        "max_length": 250,
        "min_length": 80
    },
    "legal": {
        "model": "facebook/bart-large-cnn",
        "description": "Legal content analysis and obligations",
        "use_prompt": False,
        "max_length": 300,
        "min_length": 100
    },
    "technical": {
        "model": "sshleifer/distilbart-cnn-12-6",  # Lighter BART variant
        "description": "Technical specifications and capabilities",
        "use_prompt": False,
        "max_length": 300,
        "min_length": 100
    },
    "financial": {
        "model": "philschmid/bart-large-cnn-samsum",  # BART fine-tuned variant
        "description": "Financial metrics and quantitative data",
        "use_prompt": False,
        "max_length": 300,
        "min_length": 100
    }
}

app = FastAPI(
    title="AI Document Summarizer API",
    description="Multi-approach specialized summarization",
    version="8.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "https://ai-app-chi-two.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummaryRequest(BaseModel):
    text: str
    summary_type: Literal["standard", "executive", "legal", "technical", "financial"] = "standard"
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "The quarterly report shows revenue of $2.5M with 35% growth...",
                "summary_type": "executive"
            }
        }

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Multi-Approach Specialized Summarizer",
        "version": "8.0.0",
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

def extract_key_content(text: str, content_type: str) -> str:
    """Extract and emphasize specific content types from the original text"""
    
    # For standard, return full text for balanced summary
    if content_type == "standard":
        return text
    
    if content_type == "financial":
        # Extract sentences with financial data
        sentences = text.split('.')
        financial_sentences = []
        for sentence in sentences:
            if re.search(r'\$[\d,]+|\d+%|revenue|profit|earnings|fiscal|quarter|growth|margin', sentence, re.IGNORECASE):
                financial_sentences.append(sentence.strip())
        
        if financial_sentences:
            return '. '.join(financial_sentences[:10]) + '.'  # Top 10 financial sentences
        return text
    
    elif content_type == "legal":
        # Extract sentences with legal terms
        sentences = text.split('.')
        legal_sentences = []
        for sentence in sentences:
            if re.search(r'\b(contract|agreement|compliance|regulation|liable?ility|governance|patent|terms|conditions|obligation|lawsuit|policy|requirement|GDPR|intellectual property)\b', sentence, re.IGNORECASE):
                legal_sentences.append(sentence.strip())
        
        if legal_sentences:
            return '. '.join(legal_sentences[:10]) + '.'
        return text
    
    elif content_type == "technical":
        # Extract sentences with technical content
        sentences = text.split('.')
        technical_sentences = []
        for sentence in sentences:
            if re.search(r'\b(specification|architecture|system|processor|performance|implementation|algorithm|quantum|qubit|benchmark|GHz|MHz|throughput|API|protocol|latency|computing|hardware|software|technical|technology)\b', sentence, re.IGNORECASE):
                technical_sentences.append(sentence.strip())
        
        if technical_sentences:
            return '. '.join(technical_sentences[:10]) + '.'
        return text
    
    elif content_type == "executive":
        # Extract sentences with strategic/business content
        sentences = text.split('.')
        exec_sentences = []
        for sentence in sentences:
            if re.search(r'\b(strategic|strategy|business|market|competitive|growth|expansion|acquisition|partnership|investor|decision|opportunity|challenge|objective|goal|vision|mission|leadership|management)\b', sentence, re.IGNORECASE):
                exec_sentences.append(sentence.strip())
        
        if exec_sentences:
            return '. '.join(exec_sentences[:10]) + '.'
        return text
    
    return text

def extract_summary_from_response(result) -> str:
    """Extract summary from Hugging Face response"""
    if isinstance(result, list) and len(result) > 0:
        if isinstance(result[0], dict):
            if "summary_text" in result[0]:
                return result[0]["summary_text"]
            if "generated_text" in result[0]:
                return result[0]["generated_text"]
    return str(result)

def create_specialized_summary(summary: str, summary_type: str, original_text: str) -> str:
    """Create highly differentiated summaries based on type"""
    
    text_lower = original_text.lower()
    
    # For standard summary, return as-is without modification
    if summary_type == "standard":
        return summary
    
    # Extract specific data from original text
    financial_data = re.findall(r'\$[\d,]+(?:\.\d+)?[MBK]?|\d+\.?\d*%', original_text)
    legal_terms = re.findall(r'\b(contract|agreement|compliance|regulation|liable?ility|governance|patent|intellectual property|GDPR|terms|conditions|obligation|lawsuit|settlement|policy|requirement)\b', original_text, re.IGNORECASE)
    technical_terms = re.findall(r'\b(specification|architecture|processor|performance|algorithm|quantum|qubit|GHz|MHz|throughput|API|latency|computing|qubits?|system|technical)\b', original_text, re.IGNORECASE)
    business_terms = re.findall(r'\b(strategic|market|competitive|growth|expansion|acquisition|partnership|investor|revenue|profit)\b', original_text, re.IGNORECASE)
    
    if summary_type == "financial":
        if financial_data:
            # Create a financial-focused summary
            unique_numbers = list(dict.fromkeys(financial_data[:8]))  # Remove duplicates, keep order
            financial_highlights = ', '.join(unique_numbers)
            
            # Extract financial context from summary
            return f"**Financial Summary:** Key figures include {financial_highlights}. {summary}"
        else:
            return f"**Financial Analysis:** This document contains limited quantitative financial data. {summary}"
    
    elif summary_type == "legal":
        if legal_terms:
            unique_legal = list(dict.fromkeys([term.lower() for term in legal_terms[:6]]))
            legal_aspects = ', '.join(unique_legal)
            
            # Count specific legal content
            has_contracts = any(term in text_lower for term in ['contract', 'agreement'])
            has_compliance = any(term in text_lower for term in ['compliance', 'regulation', 'gdpr'])
            has_ip = any(term in text_lower for term in ['patent', 'intellectual property', 'trademark'])
            
            focus_areas = []
            if has_contracts:
                focus_areas.append("contractual agreements")
            if has_compliance:
                focus_areas.append("regulatory compliance")
            if has_ip:
                focus_areas.append("intellectual property")
            
            if focus_areas:
                areas_text = ' and '.join(focus_areas)
                return f"**Legal Overview:** Document addresses {areas_text}. Key legal aspects: {legal_aspects}. {summary}"
            else:
                return f"**Legal Analysis:** Legal elements identified: {legal_aspects}. {summary}"
        else:
            return f"**Legal Assessment:** No significant legal content (contracts, regulations, compliance requirements, or legal obligations) found in this document."
    
    elif summary_type == "technical":
        if technical_terms:
            unique_tech = list(dict.fromkeys([term.lower() for term in technical_terms[:6]]))
            tech_aspects = ', '.join(unique_tech)
            
            # Look for specific technical categories
            has_hardware = any(term in text_lower for term in ['processor', 'ghz', 'mhz', 'hardware', 'chip'])
            has_software = any(term in text_lower for term in ['algorithm', 'api', 'software', 'code', 'protocol'])
            has_performance = any(term in text_lower for term in ['performance', 'throughput', 'latency', 'benchmark', 'speed'])
            has_quantum = any(term in text_lower for term in ['quantum', 'qubit'])
            
            tech_categories = []
            if has_quantum:
                tech_categories.append("quantum computing")
            if has_hardware:
                tech_categories.append("hardware specifications")
            if has_software:
                tech_categories.append("software architecture")
            if has_performance:
                tech_categories.append("performance metrics")
            
            if tech_categories:
                cat_text = ', '.join(tech_categories)
                return f"**Technical Overview:** Covers {cat_text}. Technical elements: {tech_aspects}. {summary}"
            else:
                return f"**Technical Summary:** Technical aspects discussed: {tech_aspects}. {summary}"
        else:
            return f"**Technical Assessment:** Limited technical specifications or architecture details found in this document."
    
    elif summary_type == "executive":
        # Create executive brief with strategic focus
        if business_terms or financial_data:
            key_metrics = financial_data[:3] if financial_data else []
            metrics_text = f" Key metrics: {', '.join(key_metrics)}." if key_metrics else ""
            
            return f"**Executive Brief:** {summary}{metrics_text}"
        else:
            return f"**Executive Summary:** {summary}"
    
    # Standard summary
    return summary

@app.post("/summarize")
def create_summary(request: SummaryRequest):
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    if len(request.text) > 10000:
        raise HTTPException(status_code=400, detail="Text too long. Maximum 10,000 characters allowed.")

    config = MODEL_CONFIGS[request.summary_type]
    model_url = f"https://api-inference.huggingface.co/models/{config['model']}"
    
    # Pre-process text to focus on relevant content
    if request.summary_type != "standard":
        processed_text = extract_key_content(request.text, request.summary_type)
    else:
        processed_text = request.text

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    
    payload = {
        "inputs": processed_text[:4000],  # Limit for API
        "parameters": {
            "max_length": config["max_length"],
            "min_length": config["min_length"],
            "do_sample": False,
            "num_beams": 4,
            "early_stopping": True
        }
    }

    start_time = time.time()
    
    try:
        response = requests.post(model_url, json=payload, headers=headers, timeout=60)
        processing_time = time.time() - start_time

        if response.status_code == 200:
            result = response.json()
            summary = extract_summary_from_response(result)
            
            # Clean up
            summary = summary.strip()
            
            # Apply specialized formatting and enhancement
            summary = create_specialized_summary(summary, request.summary_type, request.text)
            
            return {
                "success": True,
                "summary": summary,
                "metadata": {
                    "summary_type": request.summary_type,
                    "model": config["model"],
                    "original_length": len(request.text),
                    "summary_length": len(summary),
                    "processing_time_seconds": round(processing_time, 2),
                    "technique": "content-extraction-and-enhancement"
                }
            }
        elif response.status_code == 503:
            raise HTTPException(
                status_code=503,
                detail=f"AI model is loading. Please try again in 30-60 seconds. Model: {config['model']}"
            )
        else:
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"API error: {response.text}"
            )
            
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="Request timeout. Please try again.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "models": list(set([config["model"] for config in MODEL_CONFIGS.values()])),
        "timestamp": time.time()
    }

@app.post("/analyze-content")
def analyze_content(request: SummaryRequest):
    """Analyze what type of content is in the document"""
    text_lower = request.text.lower()
    
    # Comprehensive analysis
    financial_patterns = re.findall(r'\$[\d,]+(?:\.\d+)?[MBK]?|\d+\.?\d*%|revenue|profit|earnings|fiscal|quarterly|margin|balance sheet', request.text, re.IGNORECASE)
    legal_patterns = re.findall(r'\b(contract|agreement|compliance|regulation|liable?ility|governance|patent|intellectual property|GDPR|terms|conditions|obligation|lawsuit|settlement|policy)\b', request.text, re.IGNORECASE)
    technical_patterns = re.findall(r'\b(specification|architecture|system|processor|performance|implementation|algorithm|quantum|qubit|benchmark|GHz|MHz|throughput|API|protocol|latency|computing|hardware|software)\b', request.text, re.IGNORECASE)
    business_patterns = re.findall(r'\b(strategic|strategy|business|market|competitive|growth|expansion|acquisition|partnership|investor|executive|management)\b', text_lower)
    
    analysis = {
        "financial_content": len(financial_patterns),
        "legal_terms": len(legal_patterns),
        "technical_terms": len(technical_patterns),
        "business_terms": len(business_patterns),
        "recommended_type": "standard",
        "confidence": "low",
        "content_distribution": {}
    }
    
    # Calculate percentages
    total = (analysis["financial_content"] + analysis["legal_terms"] + 
             analysis["technical_terms"] + analysis["business_terms"])
    
    if total > 0:
        analysis["content_distribution"] = {
            "financial": round((analysis["financial_content"] / total) * 100, 1),
            "legal": round((analysis["legal_terms"] / total) * 100, 1),
            "technical": round((analysis["technical_terms"] / total) * 100, 1),
            "business": round((analysis["business_terms"] / total) * 100, 1)
        }
    
    # Recommend best summary type
    max_score = max(analysis["legal_terms"], analysis["technical_terms"], 
                    analysis["financial_content"], analysis["business_terms"])
    
    if max_score > 5:
        analysis["confidence"] = "high"
    elif max_score > 2:
        analysis["confidence"] = "medium"
    
    if analysis["legal_terms"] >= max_score and analysis["legal_terms"] > 2:
        analysis["recommended_type"] = "legal"
    elif analysis["technical_terms"] >= max_score and analysis["technical_terms"] > 3:
        analysis["recommended_type"] = "technical" 
    elif analysis["financial_content"] >= max_score and analysis["financial_content"] > 3:
        analysis["recommended_type"] = "financial"
    elif analysis["business_terms"] >= max_score and analysis["business_terms"] > 3:
        analysis["recommended_type"] = "executive"
    
    return analysis