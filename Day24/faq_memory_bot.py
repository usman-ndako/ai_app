"""
FAQ + GPT Memory Chatbot
Author: Boss
Day 24 Project — Hybrid FAQ + Conversational Memory Bot
"""

import os
import pandas as pd
from dotenv import load_dotenv
from difflib import get_close_matches
from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# =========================
# 1️⃣ ENVIRONMENT SETUP
# =========================
load_dotenv()
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

if not OPENROUTER_KEY:
    raise ValueError("⚠️ Missing OPENROUTER_KEY in your .env file")

os.environ["OPENAI_API_KEY"] = OPENROUTER_KEY
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"


# =========================
# 2️⃣ LOAD FAQ DATA
# =========================
FAQ_PATH = "faq.csv"

if not os.path.exists(FAQ_PATH):
    raise FileNotFoundError(f"❌ FAQ file not found at {FAQ_PATH}")

faq_df = pd.read_csv(FAQ_PATH)

# Clean data
faq_df.columns = [c.strip().lower() for c in faq_df.columns]
if "question" not in faq_df.columns or "answer" not in faq_df.columns:
    raise ValueError("❌ CSV must have columns: 'question' and 'answer'")

faq_data = dict(zip(faq_df["question"], faq_df["answer"]))

print(f"✅ Loaded {len(faq_data)} FAQs from {FAQ_PATH}")


# =========================
# 3️⃣ FAQ CHECK FUNCTION
# =========================
def check_faq(user_input: str):
    """Find the closest FAQ match."""
    questions = list(faq_data.keys())
    match = get_close_matches(user_input, questions, n=1, cutoff=0.7)
    if match:
        return faq_data[match[0]]
    return None


# =========================
# 4️⃣ MODEL + MEMORY SETUP
# =========================
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful and polite customer-support assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# In-memory session store
session_store = {}


def get_session_history(session_id: str):
    """Return the chat history for a given session."""
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]


# Create a memory-enabled chatbot
chatbot = RunnableWithMessageHistory(
    runnable=prompt | llm,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

print("✅ Chatbot initialized with memory support.")


# =========================
# 5️⃣ UNIFIED RESPONSE LOGIC
# =========================
def chatbot_response(user_input: str, session_id="user_1") -> str:
    """Hybrid logic: use FAQ if possible, else GPT."""
    faq_answer = check_faq(user_input)
    if faq_answer:
        return f"(From FAQ) {faq_answer}"
    
    # Otherwise, fall back to GPT
    response = chatbot.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}}
    )
    return response.content


# =========================
# 6️⃣ MAIN LOOP (CLI)
# =========================
if __name__ == "__main__":
    print("\n🤖 Chatbot ready! Type 'exit' to end.\n")
    session_id = "boss_session"

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye, Boss!")
            break

        bot_reply = chatbot_response(user_input, session_id=session_id)
        print(f"Bot: {bot_reply}\n")