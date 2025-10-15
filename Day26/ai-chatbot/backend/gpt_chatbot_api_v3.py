# import os
# import numpy as np
# import pandas as pd
# import requests
# from fastapi import FastAPI, HTTPException, Request, UploadFile, File
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
# from sentence_transformers import SentenceTransformer
# from typing import Dict, List
# from datetime import datetime, timedelta
# import io

# # ---------- LOAD ENV ----------
# load_dotenv()
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# if not OPENROUTER_API_KEY:
#     raise ValueError("❌ Missing OPENROUTER_API_KEY in environment variables")

# # ---------- INIT FASTAPI ----------
# app = FastAPI(title="AI Chatbot API with Memory", version="4.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ---------- LOAD LOCAL EMBEDDING MODEL ----------
# print("🔄 Loading local embedding model...")
# embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
# print("✅ Local embedding model loaded successfully!")

# # ---------- LOAD FAQ ----------
# faq_path = os.path.join(os.path.dirname(__file__), "faq.csv")
# if not os.path.exists(faq_path):
#     raise FileNotFoundError(f"❌ faq.csv not found at {faq_path}")

# faq_df = pd.read_csv(faq_path)
# faq_df["embedding"] = faq_df["question"].apply(lambda x: embedding_model.encode(str(x), convert_to_numpy=True))
# print(f"✅ Loaded {len(faq_df)} FAQ entries with embeddings.")

# # ---------- RELOAD FAQ HELPER ----------
# def reload_faq():
#     """Reload FAQ from CSV and recompute embeddings."""
#     global faq_df
#     faq_df = pd.read_csv(faq_path)
#     faq_df["embedding"] = faq_df["question"].apply(lambda x: embedding_model.encode(str(x), convert_to_numpy=True))
#     print(f"✅ Reloaded {len(faq_df)} FAQ entries with embeddings.")

# # ---------- SESSION MEMORY ----------
# conversation_memory: Dict[str, List[Dict]] = {}
# MEMORY_EXPIRY_MINUTES = 30
# MAX_MEMORY_MESSAGES = 10

# def clean_expired_sessions():
#     now = datetime.utcnow()
#     expired_sessions = [
#         sid for sid, msgs in conversation_memory.items()
#         if (now - msgs[-1]["timestamp"]) > timedelta(minutes=MEMORY_EXPIRY_MINUTES)
#     ]
#     for sid in expired_sessions:
#         del conversation_memory[sid]
#         print(f"[Memory Cleanup] Expired session removed: {sid}")

# # ---------- EMBEDDING HELPER ----------
# def embed_text(text: str):
#     try:
#         return embedding_model.encode(text, convert_to_numpy=True)
#     except Exception as e:
#         print(f"[Embedding Error] {e}")
#         return np.zeros(384)

# # ---------- FIND FAQ MATCH ----------
# def find_best_match(user_query: str):
#     query_emb = embed_text(user_query)
#     similarities = faq_df["embedding"].apply(
#         lambda emb: np.dot(emb, query_emb)
#         / (np.linalg.norm(emb) * np.linalg.norm(query_emb) + 1e-10)
#     )
#     best_idx = similarities.idxmax()
#     best_score = similarities.max()

#     if best_score > 0.55:
#         return faq_df.iloc[best_idx]["answer"]
#     return None

# # ---------- AI COMPLETION ----------
# def generate_ai_response(prompt: str, memory: List[Dict], faq_context: str = None):
#     """Generate conversational AI response with optional memory and FAQ context."""
#     system_message = {
#         "role": "system",
#         "content": (
#             "You are a Chatbot designed to assist users with their inquiries. "
#             "You are a warm, empathetic, and conversational support assistant. "
#             "You remember previous parts of the conversation and maintain context naturally. "
#             "Be concise but engaging, and stay consistent with prior responses."
#         ),
#     }

#     messages = [system_message]

#     # Add short-term memory (last 10 messages)
#     for item in memory[-MAX_MEMORY_MESSAGES:]:
#         messages.append({"role": "user" if item["sender"] == "user" else "assistant", "content": item["message"]})

#     # Add new prompt
#     if faq_context:
#         messages.append({
#             "role": "user",
#             "content": f"User question: {prompt}\n\nRelevant FAQ info: {faq_context}",
#         })
#     else:
#         messages.append({"role": "user", "content": prompt})

#     try:
#         response = requests.post(
#             "https://openrouter.ai/api/v1/chat/completions",
#             headers={
#                 "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#                 "HTTP-Referer": "http://localhost:3000",
#                 "X-Title": "AI Chatbot with Memory",
#                 "Content-Type": "application/json",
#             },
#             json={
#                 "model": "openai/gpt-4o-mini",
#                 "messages": messages,
#             },
#             timeout=40,
#         )

#         if response.status_code != 200:
#             print(f"[AI Error] {response.status_code}: {response.text[:200]}")
#             return "I'm sorry, there was an issue connecting to my AI engine."

#         data = response.json()
#         return data["choices"][0]["message"]["content"]

#     except Exception as e:
#         print(f"[AI Exception] {type(e).__name__}: {e}")
#         return "I'm sorry, something went wrong. Please try again later."

# # ---------- REQUEST SCHEMA ----------
# class ChatRequest(BaseModel):
#     session_id: str
#     message: str

# class AddFAQRequest(BaseModel):
#     question: str
#     answer: str

# # ---------- HELPER TO CHECK FOR DUPLICATES ----------
# def get_unique_faqs(existing_df: pd.DataFrame, new_entries: pd.DataFrame) -> pd.DataFrame:
#     """Filter new entries to exclude duplicates based on exact question + answer match."""
#     if new_entries.empty:
#         return new_entries
    
#     # Create a combined key for exact matching (question + answer)
#     existing_df['key'] = existing_df['question'].astype(str) + '|||' + existing_df['answer'].astype(str)
#     new_entries['key'] = new_entries['question'].astype(str) + '|||' + new_entries['answer'].astype(str)
    
#     # Find duplicates
#     duplicates_mask = new_entries['key'].isin(existing_df['key'])
    
#     # Return only non-duplicates
#     unique_new = new_entries[~duplicates_mask].drop(columns=['key'])
#     return unique_new

# # ---------- ADD FAQ ROUTE ----------
# @app.post("/add_faq")
# def add_faq(req: AddFAQRequest):
#     if not req.question.strip() or not req.answer.strip():
#         raise HTTPException(status_code=400, detail="Question and answer cannot be empty.")

#     # Check for duplicate
#     new_entry_df = pd.DataFrame([{"question": req.question, "answer": req.answer}])
#     unique_entry = get_unique_faqs(faq_df, new_entry_df)
    
#     if unique_entry.empty:
#         return {
#             "success": False,
#             "message": f"FAQ already exists: '{req.question}'",
#             "total_faqs": len(faq_df)
#         }

#     # Append to CSV
#     unique_entry.to_csv(faq_path, mode='a', header=False, index=False)

#     # Reload FAQ with new embedding
#     reload_faq()

#     return {
#         "success": True,
#         "message": f"FAQ added successfully! New entry: '{req.question}'",
#         "total_faqs": len(faq_df)
#     }

# # ---------- UPLOAD CSV FAQ ROUTE ----------
# @app.post("/upload_faq_csv")
# def upload_faq_csv(file: UploadFile = File(...)):
#     if not file.filename.endswith('.csv'):
#         raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

#     try:
#         # Read uploaded CSV into DataFrame
#         content = file.file.read()
#         df_new = pd.read_csv(io.BytesIO(content))

#         if 'question' not in df_new.columns or 'answer' not in df_new.columns:
#             raise HTTPException(status_code=400, detail="CSV must have 'question' and 'answer' columns.")

#         if df_new.empty:
#             raise HTTPException(status_code=400, detail="CSV is empty.")

#         # Filter for unique entries only
#         df_unique = get_unique_faqs(faq_df, df_new[['question', 'answer']])

#         if df_unique.empty:
#             raise HTTPException(status_code=400, detail="All FAQs in CSV already exist. No new entries added.")

#         # Append unique new rows to existing CSV
#         df_unique.to_csv(faq_path, mode='a', header=False, index=False)

#         # Reload FAQ with new embeddings
#         reload_faq()

#         return {
#             "success": True,
#             "message": f"Successfully added {len(df_unique)} unique FAQs from CSV (skipped {len(df_new) - len(df_unique)} duplicates)!",
#             "total_faqs": len(faq_df)
#         }

#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

# # ---------- GET FAQ ROUTE ----------
# @app.get("/get_faqs")
# @app.get("/faq")
# def get_faqs():
#     # Select only serializable columns and convert to list of dicts
#     faqs_list = faq_df[["question", "answer"]].to_dict(orient="records")
#     return {
#         "faqs": faqs_list,
#         "total": len(faqs_list)
#     }

# # ---------- MAIN CHAT ROUTE (REVERTED: Synchronous non-streaming) ----------
# @app.post("/chat")
# def chat(req: ChatRequest):
#     user_message = req.message.strip()
#     if not user_message:
#         raise HTTPException(status_code=400, detail="Empty message.")

#     clean_expired_sessions()

#     # Initialize session memory if new
#     if req.session_id not in conversation_memory:
#         conversation_memory[req.session_id] = []
#         print(f"[New Session] {req.session_id}")

#     # Retrieve conversation memory
#     memory = conversation_memory[req.session_id]

#     # Try FAQ match
#     faq_answer = find_best_match(user_message)
#     ai_reply = generate_ai_response(user_message, memory, faq_context=faq_answer)

#     # Store new messages in memory
#     memory.append({"sender": "user", "message": user_message, "timestamp": datetime.utcnow()})
#     memory.append({"sender": "assistant", "message": ai_reply, "timestamp": datetime.utcnow()})

#     # Trim memory
#     if len(memory) > 2 * MAX_MEMORY_MESSAGES:
#         conversation_memory[req.session_id] = memory[-2 * MAX_MEMORY_MESSAGES :]

#     return {
#         "reply": ai_reply,
#         "source": "faq_enhanced" if faq_answer else "ai_original",
#         "memory_length": len(conversation_memory[req.session_id]),
#     }

# # ---------- ROUTES ----------
# @app.get("/")
# def root():
#     return {
#         "message": "✅ AI Chatbot API with Memory is running",
#         "sessions": len(conversation_memory),
#         "faq_count": len(faq_df),
#     }

# @app.get("/health")
# def health():
#     return {"status": "healthy", "active_sessions": len(conversation_memory)}

import os
import numpy as np
import requests
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import Dict, List
from datetime import datetime, timedelta
import io
import csv

#---------- LOAD ENV ----------
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
JINA_API_KEY = os.getenv("JINA_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("❌ Missing OPENROUTER_API_KEY in environment variables")
if not JINA_API_KEY:
    raise ValueError("❌ Missing JINA_API_KEY in environment variables")

#---------- INIT FASTAPI ----------
app = FastAPI(title="AI Chatbot API with Memory", version="4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#---------- API EMBEDDING MODEL ----------
class HybridEmbeddings:
    def __init__(self):
        self.dimension = 1024  # Jina embeddings are 1024-dimensional
        self.fallback_used = False

    def encode(self, text: str) -> np.ndarray:
        """Try Jina first, then fallback to simple embedding"""
        # Try Jina
        emb = self._jina_embedding(text)
        if emb is not None:
            return emb
        
        # Fallback to simple character-based embedding
        return self._simple_embedding(text)

    def _jina_embedding(self, text: str):
        """Jina embedding API call"""
        try:
            response = requests.post(
                "https://api.jina.ai/v1/embeddings",
                headers={
                    "Authorization": f"Bearer {JINA_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "jina-embeddings-v3",
                    "input": text
                },
                timeout=20
            )
            
            print(f"🔍 Jina API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Jina embedding successful!")
                return np.array(data['data'][0]['embedding'])
            else:
                print(f"⚠️ Jina embedding failed: {response.status_code} - {response.text[:200]}")
                return None
            
        except Exception as e:
            print(f"⚠️ Jina embedding exception: {e}")
            return None

    def _simple_embedding(self, text: str):
        """Simple fallback embedding using character frequency"""
        if not self.fallback_used:
            print("🔄 Using simple fallback embeddings...")
            self.fallback_used = True
            
        # Create a simple embedding based on character frequencies
        text = text.lower()
        # Use first 1024 characters or pad with zeros
        chars = list(text[:self.dimension])
        embedding = np.zeros(self.dimension)
        
        for i, char in enumerate(chars):
            if i < self.dimension:
                # Simple character encoding
                embedding[i] = ord(char) / 1000.0
                
        return embedding

    def encode_batch(self, texts: List[str]) -> List[np.ndarray]:
        """Process texts one by one"""
        print(f"🔍 Getting embeddings for {len(texts)} texts...")
        embeddings = []
        for i, text in enumerate(texts):
            if i % 10 == 0:  # Progress indicator
                print(f"🔍 Processed {i}/{len(texts)} embeddings...")
            emb = self.encode(text)
            embeddings.append(emb)
        print("✅ All embeddings processed!")
        return embeddings

print("🔄 Initializing hybrid embedding model...")
embedding_model = HybridEmbeddings()
print("✅ Hybrid embedding model initialized successfully!")

#---------- LOAD FAQ ----------
faq_path = os.path.join(os.path.dirname(__file__), "faq.csv")
if not os.path.exists(faq_path):
    raise FileNotFoundError(f"❌ faq.csv not found at {faq_path}")

# FAQ data structure: list of dicts with question, answer, embedding
faq_data: List[Dict] = []

def load_faq_with_api():
    """Load FAQ and generate embeddings via Jina API"""
    global faq_data
    faq_data = []

    # Read CSV without pandas
    with open(faq_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        questions = []
        answers = []
        
        for row in reader:
            questions.append(row["question"])
            answers.append(row["answer"])

    if not questions:
        print("⚠️ No FAQ entries found in CSV")
        return []

    # Get embeddings in batch (more efficient)
    print(f"🔄 Generating embeddings for {len(questions)} FAQ entries...")
    embeddings = embedding_model.encode_batch(questions)

    # Combine questions, answers, and embeddings
    faq_data = []
    for i, (q, a) in enumerate(zip(questions, answers)):
        faq_data.append({
            "question": q,
            "answer": a,
            "embedding": embeddings[i] if i < len(embeddings) else np.zeros(embedding_model.dimension)
        })

    print(f"✅ Loaded {len(faq_data)} FAQ entries with embeddings.")
    return faq_data

# Initial FAQ load
faq_data = load_faq_with_api()

#---------- RELOAD FAQ HELPER ----------
def reload_faq():
    """Reload FAQ from CSV and recompute embeddings via API."""
    global faq_data
    faq_data = load_faq_with_api()
    print(f"✅ Reloaded {len(faq_data)} FAQ entries with embeddings.")

#---------- SESSION MEMORY ----------
conversation_memory: Dict[str, List[Dict]] = {}
MEMORY_EXPIRY_MINUTES = 30
MAX_MEMORY_MESSAGES = 10

def clean_expired_sessions():
    now = datetime.utcnow()
    expired_sessions = [
        sid for sid, msgs in conversation_memory.items()
        if msgs and (now - msgs[-1]["timestamp"]) > timedelta(minutes=MEMORY_EXPIRY_MINUTES)
    ]
    for sid in expired_sessions:
        del conversation_memory[sid]
        print(f"[Memory Cleanup] Expired session removed: {sid}")

#---------- EMBEDDING HELPER ----------
def embed_text(text: str):
    """Get embedding for text using Jina API"""
    return embedding_model.encode(text)

#---------- FIND FAQ MATCH ----------
def find_best_match(user_query: str):
    if not faq_data:
        return None

    query_emb = embed_text(user_query)
    best_score = 0
    best_answer = None

    for item in faq_data:
        emb = item["embedding"]
        similarity = np.dot(emb, query_emb) / (
            np.linalg.norm(emb) * np.linalg.norm(query_emb) + 1e-10
        )
        if similarity > best_score:
            best_score = similarity
            best_answer = item["answer"]

    print(f"🔍 Best FAQ match score: {best_score:.3f}")
    if best_score > 0.55:
        return best_answer
    return None

#---------- AI COMPLETION ----------
def generate_ai_response(prompt: str, memory: List[Dict], faq_context: str = None):
    """Generate conversational AI response with optional memory and FAQ context."""
    system_message = {
        "role": "system",
        "content": (
            "You are a Chatbot designed to assist users with their inquiries. "
            "You are a warm, empathetic, and conversational support assistant. "
            "You remember previous parts of the conversation and maintain context naturally. "
            "Be concise but engaging, and stay consistent with prior responses."
        ),
    }

    messages = [system_message]

    # Add short-term memory (last 10 messages)
    for item in memory[-MAX_MEMORY_MESSAGES:]:
        messages.append({"role": "user" if item["sender"] == "user" else "assistant", "content": item["message"]})

    # Add new prompt
    if faq_context:
        messages.append({
            "role": "user",
            "content": f"User question: {prompt}\n\nRelevant FAQ info: {faq_context}",
        })
    else:
        messages.append({"role": "user", "content": prompt})

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "AI Chatbot with Memory",
                "Content-Type": "application/json",
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": messages,
            },
            timeout=40,
        )

        if response.status_code != 200:
            print(f"[AI Error] {response.status_code}: {response.text[:200]}")
            return "I'm sorry, there was an issue connecting to my AI engine."

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"[AI Exception] {type(e).__name__}: {e}")
        return "I'm sorry, something went wrong. Please try again later."

#---------- REQUEST SCHEMA ----------
class ChatRequest(BaseModel):
    session_id: str
    message: str

class AddFAQRequest(BaseModel):
    question: str
    answer: str

#---------- HELPER TO CHECK FOR DUPLICATES ----------
def get_unique_faqs(new_entries: List[Dict]) -> List[Dict]:
    """Filter new entries to exclude duplicates based on exact question + answer match."""
    if not new_entries:
        return []

    unique_new = []
    existing_keys = set(f"{item['question']}|||{item['answer']}" for item in faq_data)

    for entry in new_entries:
        key = f"{entry['question']}|||{entry['answer']}"
        if key not in existing_keys:
            unique_new.append(entry)

    return unique_new

#---------- ADD FAQ ROUTE ----------
@app.post("/add_faq")
def add_faq(req: AddFAQRequest):
    if not req.question.strip() or not req.answer.strip():
        raise HTTPException(status_code=400, detail="Question and answer cannot be empty.")

    # Check for duplicate
    new_entry = {"question": req.question, "answer": req.answer}
    unique_entries = get_unique_faqs([new_entry])

    if not unique_entries:
        return {
            "success": False,
            "message": f"FAQ already exists: '{req.question}'",
            "total_faqs": len(faq_data)
        }

    # Append to CSV
    with open(faq_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['question', 'answer'])
        writer.writerow(new_entry)

    # Reload FAQ with new embedding
    reload_faq()

    return {
        "success": True,
        "message": f"FAQ added successfully! New entry: '{req.question}'",
        "total_faqs": len(faq_data)
    }

#---------- UPLOAD CSV FAQ ROUTE ----------
@app.post("/upload_faq_csv")
def upload_faq_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    try:
        # Read uploaded CSV
        content = file.file.read()
        decoded_content = content.decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_content)

        new_entries = []
        for row in reader:
            if 'question' in row and 'answer' in row:
                new_entries.append({
                    "question": row["question"],
                    "answer": row["answer"]
                })

        if not new_entries:
            raise HTTPException(status_code=400, detail="CSV is empty or missing required columns.")

        # Filter for unique entries only
        unique_entries = get_unique_faqs(new_entries)

        if not unique_entries:
            raise HTTPException(status_code=400, detail="All FAQs in CSV already exist. No new entries added.")

        # Append unique new rows to existing CSV
        with open(faq_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['question', 'answer'])
            for entry in unique_entries:
                writer.writerow(entry)

        # Reload FAQ with new embeddings
        reload_faq()

        return {
            "success": True,
            "message": f"Successfully added {len(unique_entries)} unique FAQs from CSV (skipped {len(new_entries) - len(unique_entries)} duplicates)!",
            "total_faqs": len(faq_data)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

#---------- GET FAQ ROUTE ----------
@app.get("/get_faqs")
@app.get("/faq")
def get_faqs():
    # Return questions and answers only (no embeddings)
    faqs_list = [{"question": item["question"], "answer": item["answer"]} for item in faq_data]
    return {
        "faqs": faqs_list,
        "total": len(faqs_list)
    }

#---------- MAIN CHAT ROUTE ----------
@app.post("/chat")
def chat(req: ChatRequest):
    user_message = req.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Empty message.")

    clean_expired_sessions()

    # Initialize session memory if new
    if req.session_id not in conversation_memory:
        conversation_memory[req.session_id] = []
        print(f"[New Session] {req.session_id}")

    # Retrieve conversation memory
    memory = conversation_memory[req.session_id]

    # Try FAQ match
    faq_answer = find_best_match(user_message)
    ai_reply = generate_ai_response(user_message, memory, faq_context=faq_answer)

    # Store new messages in memory
    memory.append({"sender": "user", "message": user_message, "timestamp": datetime.utcnow()})
    memory.append({"sender": "assistant", "message": ai_reply, "timestamp": datetime.utcnow()})

    # Trim memory
    if len(memory) > 2 * MAX_MEMORY_MESSAGES:
        conversation_memory[req.session_id] = memory[-2 * MAX_MEMORY_MESSAGES :]

    return {
        "reply": ai_reply,
        "source": "faq_enhanced" if faq_answer else "ai_original",
        "memory_length": len(conversation_memory[req.session_id]),
    }

#---------- ROUTES ----------
@app.get("/")
def root():
    return {
        "message": "✅ AI Chatbot API with Memory is running",
        "sessions": len(conversation_memory),
        "faq_count": len(faq_data),
    }

@app.get("/health")
def health():
    return {"status": "healthy", "active_sessions": len(conversation_memory)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)