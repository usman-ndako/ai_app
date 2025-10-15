# """
# AI Customer Support Chatbot API — Day 25
# ----------------------------------------
# This script upgrades our previous FAQ Bot with GPT-powered dynamic responses,
# using the OpenRouter API for affordable access to advanced language models.
# """

# # ============================================================
# # 1. IMPORTS & ENVIRONMENT SETUP
# # ============================================================
# import os
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import requests
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

# # Initialize FastAPI app
# app = FastAPI(title="AI Support Chatbot API")

# # Allow CORS (important for frontend integration)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],     # update with frontend URL in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ============================================================
# # 2. REQUEST MODEL
# # ============================================================
# class ChatRequest(BaseModel):
#     message: str
#     history: list = []  # [{"user": "Hello", "bot": "Hi there!"}]

# # ============================================================
# # 3. GPT CHAT FUNCTION
# # ============================================================
# def ask_gpt(message: str, history: list):
#     """
#     Sends user message + history to the GPT model via OpenRouter API.
#     Returns the chatbot's response.
#     """
#     url = "https://openrouter.ai/api/v1/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_KEY}",
#         "Content-Type": "application/json",
#     }

#     # Construct full conversation context
#     messages = [{"role": "system", "content": "You are a helpful AI customer support assistant."}]
#     for msg in history:
#         messages.append({"role": "user", "content": msg.get("user", "")})
#         messages.append({"role": "assistant", "content": msg.get("bot", "")})
#     messages.append({"role": "user", "content": message})

#     data = {
#         "model": "gpt-4o-mini",   # low-cost, high-quality model
#         "messages": messages,
#     }

#     response = requests.post(url, headers=headers, json=data)
#     if response.status_code != 200:
#         return f"Error: {response.text}"

#     result = response.json()
#     return result["choices"][0]["message"]["content"]

# # ============================================================
# # 4. FASTAPI ENDPOINT
# # ============================================================
# @app.post("/chat")
# async def chat_endpoint(request: ChatRequest):
#     """
#     Receives chat messages from frontend and returns GPT-generated replies.
#     """
#     user_message = request.message
#     history = request.history or []

#     bot_reply = ask_gpt(user_message, history)
#     return {"reply": bot_reply}

# # ============================================================
# # 5. RUN SERVER LOCALLY
# # ============================================================
# if __name__ == "__main__":
#     import uvicorn
#     print("🚀 Starting AI Chatbot API on http://127.0.0.1:8000")
#     uvicorn.run(app, host="0.0.0.0", port=8000)


# gpt_chatbot_api.py
# ------------------------------------------------------------
# 🚀 AI Chatbot API with Context Memory + Custom Personality
# Compatible with Swagger UI | FastAPI + OpenRouter + LangChain
# ------------------------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

# ------------------------------------------------------------
# Load environment variables
# ------------------------------------------------------------
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_KEY")
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

# ------------------------------------------------------------
# Initialize OpenRouter client
# ------------------------------------------------------------
client = OpenAI(api_key=os.getenv("OPENROUTER_KEY"), base_url="https://openrouter.ai/api/v1")

# ------------------------------------------------------------
# FastAPI setup
# ------------------------------------------------------------
app = FastAPI(
    title="Boss AI Chatbot API",
    description="Conversational chatbot API with memory and custom personality.",
    version="2.0"
)

# ------------------------------------------------------------
# Data models
# ------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str
    history: list = []  # [{user: "...", bot: "..."}]

class ChatResponse(BaseModel):
    reply: str

# ------------------------------------------------------------
# Helper: Generate response with memory and personality
# ------------------------------------------------------------
def generate_response(message: str, history: list):
    # Build conversation context
    conversation = "The following is a friendly and intelligent AI chatbot named BossBot, built by an entrepreneur known as 'Boss'.\n"
    conversation += "BossBot can answer FAQs, recall previous parts of the conversation, and maintain a helpful, professional tone.\n\n"

    for turn in history:
        conversation += f"User: {turn['user']}\nBossBot: {turn['bot']}\n"
    conversation += f"User: {message}\nBossBot:"

    # Make API request to OpenRouter model
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are BossBot — a knowledgeable AI chatbot assistant designed for business and FAQ conversations. Always respond naturally, as if chatting live."},
            {"role": "user", "content": conversation}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

# ------------------------------------------------------------
# API Endpoint
# ------------------------------------------------------------
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    reply = generate_response(req.message, req.history)
    return {"reply": reply}

# ------------------------------------------------------------
# Run server
# ------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting BossBot API on http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
