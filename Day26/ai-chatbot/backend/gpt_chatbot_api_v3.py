# import os
# import numpy as np
# import requests
# from fastapi import FastAPI, HTTPException, Request, UploadFile, File
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
# from typing import Dict, List
# from datetime import datetime, timedelta
# import csv
# from pymongo import MongoClient
# from pymongo.errors import PyMongoError
# from collections import defaultdict
# import time

# #---------- LOAD ENV ----------
# load_dotenv()
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# JINA_API_KEY = os.getenv("JINA_API_KEY")
# MONGODB_URI = os.getenv("MONGODB_URI")

# if not OPENROUTER_API_KEY:
#     raise ValueError("❌ Missing OPENROUTER_API_KEY in environment variables")
# if not JINA_API_KEY:
#     raise ValueError("❌ Missing JINA_API_KEY in environment variables")
# if not MONGODB_URI:
#     raise ValueError("❌ Missing MONGODB_URI in environment variables")

# #---------- MONGODB CONNECTION ----------
# try:
#     mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
#     mongo_client.admin.command('ping')
#     print("✅ Connected to MongoDB Atlas!")
    
#     db = mongo_client["chatbot_db"]
#     faq_collection = db["faqs"]
    
#     # Create index on question for faster lookups
#     faq_collection.create_index("question")
#     print("✅ MongoDB indexes created")
    
# except PyMongoError as e:
#     print(f"❌ MongoDB connection error: {e}")
#     raise ValueError("❌ Failed to connect to MongoDB Atlas")

# #---------- RATE LIMITING ----------
# class RateLimiter:
#     """In-memory rate limiter for free tier without external dependencies"""
#     def __init__(self):
#         self.requests = defaultdict(list)  # session_id -> list of timestamps
        
#     def is_allowed(self, session_id: str, max_requests: int = 20, window_seconds: int = 3600) -> tuple[bool, int]:
#         """
#         Check if request is allowed.
#         Returns: (is_allowed: bool, remaining_requests: int)
#         """
#         now = time.time()
#         window_start = now - window_seconds
        
#         # Clean old requests outside window
#         self.requests[session_id] = [
#             req_time for req_time in self.requests[session_id] 
#             if req_time > window_start
#         ]
        
#         current_count = len(self.requests[session_id])
        
#         if current_count >= max_requests:
#             return False, 0
        
#         # Add current request
#         self.requests[session_id].append(now)
#         remaining = max_requests - current_count - 1
        
#         return True, remaining
    
#     def get_reset_time(self, session_id: str, window_seconds: int = 3600) -> int:
#         """Get Unix timestamp when rate limit resets"""
#         if not self.requests[session_id]:
#             return int(time.time() + window_seconds)
        
#         oldest_request = self.requests[session_id][0]
#         reset_time = int(oldest_request + window_seconds)
#         return reset_time
    
#     def cleanup_old_sessions(self, max_age_hours: int = 24):
#         """Remove sessions older than max_age to prevent memory bloat"""
#         now = time.time()
#         sessions_to_remove = []
        
#         for session_id, requests_list in self.requests.items():
#             if requests_list and (now - requests_list[-1]) > (max_age_hours * 3600):
#                 sessions_to_remove.append(session_id)
        
#         for session_id in sessions_to_remove:
#             del self.requests[session_id]
        
#         if sessions_to_remove:
#             print(f"[Rate Limit Cleanup] Removed {len(sessions_to_remove)} old sessions")

# rate_limiter = RateLimiter()

# # Periodic cleanup (runs every time a request comes in, but only cleans if needed)
# last_cleanup = time.time()

# def trigger_cleanup_if_needed():
#     global last_cleanup
#     now = time.time()
#     if (now - last_cleanup) > 3600:  # Cleanup every hour
#         rate_limiter.cleanup_old_sessions()
#         last_cleanup = now

# #---------- INIT FASTAPI ----------
# app = FastAPI(title="AI Chatbot API with Memory", version="4.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "https://ai-chatbot-ten-beta-64.vercel.app/",
#         "http://localhost:3000"  # for local development
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# #---------- API EMBEDDING MODEL ----------
# class HybridEmbeddings:
#     def __init__(self):
#         self.dimension = 1024  # Jina embeddings are 1024-dimensional
#         self.fallback_used = False

#     def encode(self, text: str) -> np.ndarray:
#         """Try Jina first, then fallback to simple embedding"""
#         # Try Jina
#         emb = self._jina_embedding(text)
#         if emb is not None:
#             return emb
        
#         # Fallback to simple character-based embedding
#         return self._simple_embedding(text)

#     def _jina_embedding(self, text: str):
#         """Jina embedding API call"""
#         try:
#             response = requests.post(
#                 "https://api.jina.ai/v1/embeddings",
#                 headers={
#                     "Authorization": f"Bearer {JINA_API_KEY}",
#                     "Content-Type": "application/json",
#                 },
#                 json={
#                     "model": "jina-embeddings-v3",
#                     "input": text
#                 },
#                 timeout=20
#             )
            
#             print(f"🔍 Jina API Response Status: {response.status_code}")
            
#             if response.status_code == 200:
#                 data = response.json()
#                 print("✅ Jina embedding successful!")
#                 return np.array(data['data'][0]['embedding'])
#             else:
#                 print(f"⚠️ Jina embedding failed: {response.status_code} - {response.text[:200]}")
#                 return None
            
#         except Exception as e:
#             print(f"⚠️ Jina embedding exception: {e}")
#             return None

#     def _simple_embedding(self, text: str):
#         """Simple fallback embedding using character frequency"""
#         if not self.fallback_used:
#             print("🔄 Using simple fallback embeddings...")
#             self.fallback_used = True
            
#         text = text.lower()
#         chars = list(text[:self.dimension])
#         embedding = np.zeros(self.dimension)
        
#         for i, char in enumerate(chars):
#             if i < self.dimension:
#                 embedding[i] = ord(char) / 1000.0
                
#         return embedding

#     def encode_batch(self, texts: List[str]) -> List[np.ndarray]:
#         """Process texts one by one"""
#         print(f"🔍 Getting embeddings for {len(texts)} texts...")
#         embeddings = []
#         for i, text in enumerate(texts):
#             if i % 10 == 0:
#                 print(f"🔍 Processed {i}/{len(texts)} embeddings...")
#             emb = self.encode(text)
#             embeddings.append(emb)
#         print("✅ All embeddings processed!")
#         return embeddings

# print("🔄 Initializing hybrid embedding model...")
# embedding_model = HybridEmbeddings()
# print("✅ Hybrid embedding model initialized successfully!")

# #---------- FAQ DATA ----------
# faq_path = os.path.join(os.path.dirname(__file__), "faq.csv")
# if not os.path.exists(faq_path):
#     raise FileNotFoundError(f"❌ faq.csv not found at {faq_path}")

# faq_data: List[Dict] = []

# def save_embeddings_to_db(data: List[Dict]):
#     """Save embeddings to MongoDB"""
#     try:
#         faq_collection.delete_many({})
#         db_data = [
#             {
#                 "question": item["question"],
#                 "answer": item["answer"],
#                 "embedding": item["embedding"].tolist() if isinstance(item["embedding"], np.ndarray) else item["embedding"]
#             }
#             for item in data
#         ]
#         faq_collection.insert_many(db_data)
#         print(f"💾 Saved {len(db_data)} embeddings to MongoDB!")
#     except PyMongoError as e:
#         print(f"⚠️ Failed to save embeddings to MongoDB: {e}")

# def load_embeddings_from_db():
#     """Load embeddings from MongoDB"""
#     try:
#         documents = list(faq_collection.find({}, {"_id": 0}))
#         if not documents:
#             print("ℹ️ No embeddings found in MongoDB")
#             return None
#         for doc in documents:
#             doc["embedding"] = np.array(doc["embedding"])
#         print(f"✅ Loaded {len(documents)} embeddings from MongoDB!")
#         return documents
#     except PyMongoError as e:
#         print(f"⚠️ Failed to load embeddings from MongoDB: {e}")
#         return None

# def load_faq_with_api():
#     """Load FAQ and generate embeddings via Jina API (only for new entries)"""
#     global faq_data

#     cached_faq = load_embeddings_from_db()
    
#     with open(faq_path, 'r', encoding='utf-8') as f:
#         reader = csv.DictReader(f)
#         current_questions = []
#         current_data = []
        
#         for row in reader:
#             current_questions.append(row["question"])
#             current_data.append({
#                 "question": row["question"],
#                 "answer": row["answer"]
#             })

#     if not current_questions:
#         print("⚠️ No FAQ entries found in CSV")
#         faq_data = []
#         return

#     if cached_faq:
#         cached_questions = {item["question"]: item for item in cached_faq}
        
#         new_entries = []
#         reused_entries = []
        
#         for item in current_data:
#             if item["question"] in cached_questions:
#                 reused_entries.append({
#                     **item,
#                     "embedding": cached_questions[item["question"]]["embedding"]
#                 })
#             else:
#                 new_entries.append(item)
        
#         if new_entries:
#             print(f"🔄 Generating embeddings for {len(new_entries)} NEW FAQ entries...")
#             new_questions = [item["question"] for item in new_entries]
#             embeddings = embedding_model.encode_batch(new_questions)
            
#             for item, emb in zip(new_entries, embeddings):
#                 item["embedding"] = emb
        
#         faq_data = reused_entries + new_entries
#         print(f"✅ Loaded {len(reused_entries)} FAQs from MongoDB + {len(new_entries)} new entries")
        
#     else:
#         print(f"🔄 No embeddings in MongoDB. Generating for {len(current_questions)} FAQ entries...")
#         questions = [item["question"] for item in current_data]
#         embeddings = embedding_model.encode_batch(questions)
        
#         faq_data = []
#         for item, emb in zip(current_data, embeddings):
#             faq_data.append({**item, "embedding": emb})
#         print(f"✅ Generated embeddings for {len(faq_data)} FAQ entries")
    
#     save_embeddings_to_db(faq_data)

# load_faq_with_api()

# #---------- RELOAD FAQ HELPER ----------
# def reload_faq():
#     """Reload FAQ from CSV and recompute embeddings via API."""
#     global faq_data
#     load_faq_with_api()
#     print(f"✅ Reloaded {len(faq_data)} FAQ entries.")

# #---------- SESSION MEMORY ----------
# conversation_memory: Dict[str, List[Dict]] = {}
# MEMORY_EXPIRY_MINUTES = 30
# MAX_MEMORY_MESSAGES = 10

# def clean_expired_sessions():
#     now = datetime.utcnow()
#     expired_sessions = [
#         sid for sid, msgs in conversation_memory.items()
#         if msgs and (now - msgs[-1]["timestamp"]) > timedelta(minutes=MEMORY_EXPIRY_MINUTES)
#     ]
#     for sid in expired_sessions:
#         del conversation_memory[sid]
#         print(f"[Memory Cleanup] Expired session removed: {sid}")

# #---------- EMBEDDING HELPER ----------
# query_embedding_cache = {}

# def embed_text(text: str, use_cache: bool = True):
#     """Get embedding for text using Jina API with optional caching"""
#     if use_cache and text in query_embedding_cache:
#         print(f"📦 Using cached embedding for query")
#         return query_embedding_cache[text]
    
#     embedding = embedding_model.encode(text)
    
#     if use_cache:
#         query_embedding_cache[text] = embedding
    
#     return embedding

# #---------- FIND FAQ MATCH ----------
# def find_best_match(user_query: str):
#     if not faq_data:
#         return None

#     query_emb = embed_text(user_query)
#     best_score = 0
#     best_answer = None

#     for item in faq_data:
#         emb = item["embedding"]
#         similarity = np.dot(emb, query_emb) / (
#             np.linalg.norm(emb) * np.linalg.norm(query_emb) + 1e-10
#         )
#         if similarity > best_score:
#             best_score = similarity
#             best_answer = item["answer"]

#     print(f"🔍 Best FAQ match score: {best_score:.3f}")
#     if best_score > 0.55:
#         return best_answer
#     return None

# #---------- AI COMPLETION ----------
# def generate_ai_response(prompt: str, memory: List[Dict], faq_context: str = None):
#     """Generate conversational AI response with optional memory and FAQ context."""
#     system_message = {
#         "role": "system",
#         "content": (
#             "You are a helpful support assistant for a company. Your role is to answer user questions professionally and courteously. "
#              "Be friendly, knowledgeable, and empathetic in your responses. "
#              "Maintain context from previous messages in the conversation. "
#              "Keep responses concise but helpful. "
#              "If a user asks something you cannot help with, politely suggest they contact the support team at usmanaliyu001@gmail.com. "
#              "Always respond in a normal, professional manner without using titles or formal address."
#         ),
#     }

#     messages = [system_message]

#     for item in memory[-MAX_MEMORY_MESSAGES:]:
#         messages.append({"role": "user" if item["sender"] == "user" else "assistant", "content": item["message"]})

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

# #---------- REQUEST SCHEMA ----------
# class ChatRequest(BaseModel):
#     session_id: str
#     message: str

# class AddFAQRequest(BaseModel):
#     question: str
#     answer: str

# #---------- DUPLICATE CHECK ----------
# def get_unique_faqs(new_entries: List[Dict]) -> List[Dict]:
#     """Filter new entries to exclude duplicates based on exact question + answer match."""
#     if not new_entries:
#         return []

#     unique_new = []
#     existing_keys = set(f"{item['question']}|||{item['answer']}" for item in faq_data)

#     for entry in new_entries:
#         key = f"{entry['question']}|||{entry['answer']}"
#         if key not in existing_keys:
#             unique_new.append(entry)

#     return unique_new

# #---------- ADD FAQ ROUTE ----------
# @app.post("/add_faq")
# def add_faq(req: AddFAQRequest):
#     if not req.question.strip() or not req.answer.strip():
#         raise HTTPException(status_code=400, detail="Question and answer cannot be empty.")

#     new_entry = {"question": req.question, "answer": req.answer}
#     unique_entries = get_unique_faqs([new_entry])

#     if not unique_entries:
#         return {
#             "success": False,
#             "message": f"FAQ already exists: '{req.question}'",
#             "total_faqs": len(faq_data)
#         }

#     with open(faq_path, 'a', newline='', encoding='utf-8') as f:
#         writer = csv.DictWriter(f, fieldnames=['question', 'answer'])
#         writer.writerow(new_entry)

#     reload_faq()

#     return {
#         "success": True,
#         "message": f"FAQ added successfully! New entry: '{req.question}'",
#         "total_faqs": len(faq_data)
#     }

# #---------- UPLOAD CSV FAQ ROUTE ----------
# @app.post("/upload_faq_csv")
# def upload_faq_csv(file: UploadFile = File(...)):
#     if not file.filename.endswith('.csv'):
#         raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

#     try:
#         content = file.file.read()
#         decoded_content = content.decode('utf-8').splitlines()
#         reader = csv.DictReader(decoded_content)

#         new_entries = []
#         for row in reader:
#             if 'question' in row and 'answer' in row:
#                 new_entries.append({
#                     "question": row["question"],
#                     "answer": row["answer"]
#                 })

#         if not new_entries:
#             raise HTTPException(status_code=400, detail="CSV is empty or missing required columns.")

#         unique_entries = get_unique_faqs(new_entries)

#         if not unique_entries:
#             raise HTTPException(status_code=400, detail="All FAQs in CSV already exist. No new entries added.")

#         with open(faq_path, 'a', newline='', encoding='utf-8') as f:
#             writer = csv.DictWriter(f, fieldnames=['question', 'answer'])
#             for entry in unique_entries:
#                 writer.writerow(entry)

#         reload_faq()

#         return {
#             "success": True,
#             "message": f"Successfully added {len(unique_entries)} unique FAQs from CSV (skipped {len(new_entries) - len(unique_entries)} duplicates)!",
#             "total_faqs": len(faq_data)
#         }

#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

# #---------- GET FAQ ROUTE ----------
# @app.get("/get_faqs")
# @app.get("/faq")
# def get_faqs():
#     faqs_list = [{"question": item["question"], "answer": item["answer"]} for item in faq_data]
#     return {
#         "faqs": faqs_list,
#         "total": len(faqs_list)
#     }

# #---------- MAIN CHAT ROUTE WITH RATE LIMITING ----------
# @app.post("/chat")
# def chat(req: ChatRequest):
#     trigger_cleanup_if_needed()
    
#     # Rate limiting check
#     is_allowed, remaining = rate_limiter.is_allowed(
#         req.session_id,
#         max_requests=20,
#         window_seconds=3600  # 20 requests per hour
#     )
    
#     if not is_allowed:
#         reset_time = rate_limiter.get_reset_time(req.session_id, window_seconds=3600)
#         reset_datetime = datetime.fromtimestamp(reset_time).strftime("%H:%M:%S UTC")
#         raise HTTPException(
#             status_code=429,
#             detail=f"Rate limit exceeded. Max 20 requests per hour. Resets at {reset_datetime}"
#         )
    
#     user_message = req.message.strip()
#     if not user_message:
#         raise HTTPException(status_code=400, detail="Empty message.")

#     clean_expired_sessions()

#     if req.session_id not in conversation_memory:
#         conversation_memory[req.session_id] = []
#         print(f"[New Session] {req.session_id}")

#     memory = conversation_memory[req.session_id]

#     greetings = ["hi", "hello", "hey", "greetings", "hiya", "howdy", "what's up", "sup"]
#     is_greeting = any(user_message.lower().strip() == g for g in greetings)
    
#     if is_greeting:
#         ai_reply = "Hello! How can I help you today?"
#         source = "greeting"
#     else:
#         faq_answer = find_best_match(user_message)
        
#         if not faq_answer:
#             ai_reply = (
#                 "That's a great question! To ensure you get the most accurate and personalized assistance, "
#                 "I'd recommend reaching out to our dedicated support team at usmanaliyu001@gmail.com. "
#                 "They'll be able to provide you with detailed guidance tailored to your specific needs. We appreciate your inquiry!"
#             )
#             source = "no_match"
#         else:
#             ai_reply = generate_ai_response(user_message, memory, faq_context=faq_answer)
#             source = "faq_enhanced"

#     memory.append({"sender": "user", "message": user_message, "timestamp": datetime.utcnow()})
#     memory.append({"sender": "assistant", "message": ai_reply, "timestamp": datetime.utcnow()})

#     if len(memory) > 2 * MAX_MEMORY_MESSAGES:
#         conversation_memory[req.session_id] = memory[-2 * MAX_MEMORY_MESSAGES :]

#     return {
#         "reply": ai_reply,
#         "source": source,
#         "memory_length": len(conversation_memory[req.session_id]),
#         "remaining_requests": remaining,
#     }

# #---------- ROUTES ----------
# @app.get("/")
# def root():
#     return {
#         "message": "✅ AI Chatbot API with Memory is running",
#         "sessions": len(conversation_memory),
#         "faq_count": len(faq_data),
#     }

# @app.get("/health")
# def health():
#     return {"status": "healthy", "active_sessions": len(conversation_memory)}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

import os
import numpy as np
import requests
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import Dict, List
from datetime import datetime, timedelta
import csv
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from collections import defaultdict
import time

#---------- LOAD ENV ----------
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
JINA_API_KEY = os.getenv("JINA_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")

if not OPENROUTER_API_KEY:
    raise ValueError("❌ Missing OPENROUTER_API_KEY in environment variables")
if not JINA_API_KEY:
    raise ValueError("❌ Missing JINA_API_KEY in environment variables")
if not MONGODB_URI:
    raise ValueError("❌ Missing MONGODB_URI in environment variables")

#---------- MONGODB CONNECTION ----------
try:
    mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    mongo_client.admin.command('ping')
    print("✅ Connected to MongoDB Atlas!")
    
    db = mongo_client["chatbot_db"]
    faq_collection = db["faqs"]
    
    # Create index on question for faster lookups
    faq_collection.create_index("question")
    print("✅ MongoDB indexes created")
    
except PyMongoError as e:
    print(f"❌ MongoDB connection error: {e}")
    raise ValueError("❌ Failed to connect to MongoDB Atlas")

#---------- RATE LIMITING ----------
class RateLimiter:
    """In-memory rate limiter for free tier without external dependencies"""
    def __init__(self):
        self.requests = defaultdict(list)  # session_id -> list of timestamps
        
    def is_allowed(self, session_id: str, max_requests: int = 20, window_seconds: int = 3600) -> tuple[bool, int]:
        """
        Check if request is allowed.
        Returns: (is_allowed: bool, remaining_requests: int)
        """
        now = time.time()
        window_start = now - window_seconds
        
        # Clean old requests outside window
        self.requests[session_id] = [
            req_time for req_time in self.requests[session_id] 
            if req_time > window_start
        ]
        
        current_count = len(self.requests[session_id])
        
        if current_count >= max_requests:
            return False, 0
        
        # Add current request
        self.requests[session_id].append(now)
        remaining = max_requests - current_count - 1
        
        return True, remaining
    
    def get_reset_time(self, session_id: str, window_seconds: int = 3600) -> int:
        """Get Unix timestamp when rate limit resets"""
        if not self.requests[session_id]:
            return int(time.time() + window_seconds)
        
        oldest_request = self.requests[session_id][0]
        reset_time = int(oldest_request + window_seconds)
        return reset_time
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Remove sessions older than max_age to prevent memory bloat"""
        now = time.time()
        sessions_to_remove = []
        
        for session_id, requests_list in self.requests.items():
            if requests_list and (now - requests_list[-1]) > (max_age_hours * 3600):
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            del self.requests[session_id]
        
        if sessions_to_remove:
            print(f"[Rate Limit Cleanup] Removed {len(sessions_to_remove)} old sessions")

rate_limiter = RateLimiter()

# Periodic cleanup (runs every time a request comes in, but only cleans if needed)
last_cleanup = time.time()

def trigger_cleanup_if_needed():
    global last_cleanup
    now = time.time()
    if (now - last_cleanup) > 3600:  # Cleanup every hour
        rate_limiter.cleanup_old_sessions()
        last_cleanup = now

#---------- INIT FASTAPI ----------
app = FastAPI(title="AI Chatbot API with Memory", version="4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-chatbot-ten-beta-64.vercel.app/",
        "http://localhost:3000"  # for local development
    ],
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
            
        text = text.lower()
        chars = list(text[:self.dimension])
        embedding = np.zeros(self.dimension)
        
        for i, char in enumerate(chars):
            if i < self.dimension:
                embedding[i] = ord(char) / 1000.0
                
        return embedding

    def encode_batch(self, texts: List[str]) -> List[np.ndarray]:
        """Process texts one by one"""
        print(f"🔍 Getting embeddings for {len(texts)} texts...")
        embeddings = []
        for i, text in enumerate(texts):
            if i % 10 == 0:
                print(f"🔍 Processed {i}/{len(texts)} embeddings...")
            emb = self.encode(text)
            embeddings.append(emb)
        print("✅ All embeddings processed!")
        return embeddings

print("🔄 Initializing hybrid embedding model...")
embedding_model = HybridEmbeddings()
print("✅ Hybrid embedding model initialized successfully!")

#---------- FAQ DATA ----------
faq_path = os.path.join(os.path.dirname(__file__), "faq.csv")

# Don't fail on startup if faq.csv missing - create empty file
if not os.path.exists(faq_path):
    print(f"⚠️ faq.csv not found at {faq_path}, creating empty file...")
    with open(faq_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['question', 'answer'])
        writer.writeheader()

faq_data: List[Dict] = []

def save_embeddings_to_db(data: List[Dict]):
    """Save embeddings to MongoDB"""
    try:
        faq_collection.delete_many({})
        db_data = [
            {
                "question": item["question"],
                "answer": item["answer"],
                "embedding": item["embedding"].tolist() if isinstance(item["embedding"], np.ndarray) else item["embedding"]
            }
            for item in data
        ]
        faq_collection.insert_many(db_data)
        print(f"💾 Saved {len(db_data)} embeddings to MongoDB!")
    except PyMongoError as e:
        print(f"⚠️ Failed to save embeddings to MongoDB: {e}")

def load_embeddings_from_db():
    """Load embeddings from MongoDB"""
    try:
        documents = list(faq_collection.find({}, {"_id": 0}))
        if not documents:
            print("ℹ️ No embeddings found in MongoDB")
            return None
        for doc in documents:
            doc["embedding"] = np.array(doc["embedding"])
        print(f"✅ Loaded {len(documents)} embeddings from MongoDB!")
        return documents
    except PyMongoError as e:
        print(f"⚠️ Failed to load embeddings from MongoDB: {e}")
        return None

def load_faq_with_api():
    """Load FAQ and generate embeddings via Jina API (only for new entries)"""
    global faq_data

    cached_faq = load_embeddings_from_db()
    
    with open(faq_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        current_questions = []
        current_data = []
        
        for row in reader:
            if row.get("question") and row.get("answer"):
                current_questions.append(row["question"])
                current_data.append({
                    "question": row["question"],
                    "answer": row["answer"]
                })

    if not current_questions:
        print("ℹ️ No FAQ entries found in CSV")
        faq_data = []
        return

    if cached_faq:
        cached_questions = {item["question"]: item for item in cached_faq}
        
        new_entries = []
        reused_entries = []
        
        for item in current_data:
            if item["question"] in cached_questions:
                reused_entries.append({
                    **item,
                    "embedding": cached_questions[item["question"]]["embedding"]
                })
            else:
                new_entries.append(item)
        
        if new_entries:
            print(f"🔄 Generating embeddings for {len(new_entries)} NEW FAQ entries...")
            new_questions = [item["question"] for item in new_entries]
            embeddings = embedding_model.encode_batch(new_questions)
            
            for item, emb in zip(new_entries, embeddings):
                item["embedding"] = emb
        
        faq_data = reused_entries + new_entries
        print(f"✅ Loaded {len(reused_entries)} FAQs from MongoDB + {len(new_entries)} new entries")
        
    else:
        print(f"🔄 No embeddings in MongoDB. Generating for {len(current_questions)} FAQ entries...")
        questions = [item["question"] for item in current_data]
        embeddings = embedding_model.encode_batch(questions)
        
        faq_data = []
        for item, emb in zip(current_data, embeddings):
            faq_data.append({**item, "embedding": emb})
        print(f"✅ Generated embeddings for {len(faq_data)} FAQ entries")
    
    save_embeddings_to_db(faq_data)

load_faq_with_api()

#---------- RELOAD FAQ HELPER ----------
def reload_faq():
    """Reload FAQ from CSV and recompute embeddings via API."""
    global faq_data
    load_faq_with_api()
    print(f"✅ Reloaded {len(faq_data)} FAQ entries.")

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
query_embedding_cache = {}

def embed_text(text: str, use_cache: bool = True):
    """Get embedding for text using Jina API with optional caching"""
    if use_cache and text in query_embedding_cache:
        print(f"📦 Using cached embedding for query")
        return query_embedding_cache[text]
    
    embedding = embedding_model.encode(text)
    
    if use_cache:
        query_embedding_cache[text] = embedding
    
    return embedding

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
            "You are a helpful support assistant for a company. Your role is to answer user questions professionally and courteously. "
             "Be friendly, knowledgeable, and empathetic in your responses. "
             "Maintain context from previous messages in the conversation. "
             "Keep responses concise but helpful. "
             "If a user asks something you cannot help with, politely suggest they contact the support team at usmanaliyu001@gmail.com. "
             "Always respond in a normal, professional manner without using titles or formal address."
        ),
    }

    messages = [system_message]

    for item in memory[-MAX_MEMORY_MESSAGES:]:
        messages.append({"role": "user" if item["sender"] == "user" else "assistant", "content": item["message"]})

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

#---------- DUPLICATE CHECK ----------
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

    new_entry = {"question": req.question, "answer": req.answer}
    unique_entries = get_unique_faqs([new_entry])

    if not unique_entries:
        return {
            "success": False,
            "message": f"FAQ already exists: '{req.question}'",
            "total_faqs": len(faq_data)
        }

    with open(faq_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['question', 'answer'])
        writer.writerow(new_entry)

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

        unique_entries = get_unique_faqs(new_entries)

        if not unique_entries:
            raise HTTPException(status_code=400, detail="All FAQs in CSV already exist. No new entries added.")

        with open(faq_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['question', 'answer'])
            for entry in unique_entries:
                writer.writerow(entry)

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
    faqs_list = [{"question": item["question"], "answer": item["answer"]} for item in faq_data]
    return {
        "faqs": faqs_list,
        "total": len(faqs_list)
    }

#---------- MAIN CHAT ROUTE WITH RATE LIMITING ----------
@app.post("/chat")
def chat(req: ChatRequest):
    trigger_cleanup_if_needed()
    
    # Rate limiting check
    is_allowed, remaining = rate_limiter.is_allowed(
        req.session_id,
        max_requests=20,
        window_seconds=3600  # 20 requests per hour
    )
    
    if not is_allowed:
        reset_time = rate_limiter.get_reset_time(req.session_id, window_seconds=3600)
        reset_datetime = datetime.fromtimestamp(reset_time).strftime("%H:%M:%S UTC")
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max 20 requests per hour. Resets at {reset_datetime}"
        )
    
    user_message = req.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Empty message.")

    clean_expired_sessions()

    if req.session_id not in conversation_memory:
        conversation_memory[req.session_id] = []
        print(f"[New Session] {req.session_id}")

    memory = conversation_memory[req.session_id]

    greetings = ["hi", "hello", "hey", "greetings", "hiya", "howdy", "what's up", "sup"]
    is_greeting = any(user_message.lower().strip() == g for g in greetings)
    
    if is_greeting:
        ai_reply = "Hello! How can I help you today?"
        source = "greeting"
    else:
        faq_answer = find_best_match(user_message)
        
        if not faq_answer:
            ai_reply = (
                "That's a great question! To ensure you get the most accurate and personalized assistance, "
                "I'd recommend reaching out to our dedicated support team at usmanaliyu001@gmail.com. "
                "They'll be able to provide you with detailed guidance tailored to your specific needs. We appreciate your inquiry!"
            )
            source = "no_match"
        else:
            ai_reply = generate_ai_response(user_message, memory, faq_context=faq_answer)
            source = "faq_enhanced"

    memory.append({"sender": "user", "message": user_message, "timestamp": datetime.utcnow()})
    memory.append({"sender": "assistant", "message": ai_reply, "timestamp": datetime.utcnow()})

    if len(memory) > 2 * MAX_MEMORY_MESSAGES:
        conversation_memory[req.session_id] = memory[-2 * MAX_MEMORY_MESSAGES :]

    return {
        "reply": ai_reply,
        "source": source,
        "memory_length": len(conversation_memory[req.session_id]),
        "remaining_requests": remaining,
    }

#---------- ROUTES ----------
@app.get("/")
@app.head("/")
def root():
    return {
        "message": "✅ AI Chatbot API with Memory is running",
        "sessions": len(conversation_memory),
        "faq_count": len(faq_data),
    }

@app.get("/health")
@app.head("/health")
def health():
    return {"status": "healthy", "active_sessions": len(conversation_memory)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)