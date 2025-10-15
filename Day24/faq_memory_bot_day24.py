"""
Day 24 — LangChain Basics + Memory
Goal: Add conversational memory to your FAQ chatbot using LangChain
"""

# =========================================================
# 1️⃣ Imports & Setup
# =========================================================
import os
import pandas as pd
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.document import Document
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain.embeddings.base import Embeddings  # ✅ required base class

# =========================================================
# 2️⃣ Load Environment & API Keys
# =========================================================
load_dotenv()

OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
if not OPENROUTER_KEY:
    raise ValueError("❌ Missing OPENROUTER_KEY environment variable. Add it to your .env file.")

# =========================================================
# 3️⃣ Load FAQ Dataset
# =========================================================
FAQ_CSV_PATH = "faq.csv"

if not os.path.exists(FAQ_CSV_PATH):
    raise FileNotFoundError("❌ faq.csv file not found. Please place it in the same directory.")

faq_df = pd.read_csv(FAQ_CSV_PATH)
print(f"✅ Loaded {len(faq_df)} FAQs from {FAQ_CSV_PATH}")

faq_docs = [
    Document(page_content=row["question"], metadata={"answer": row["answer"]})
    for _, row in faq_df.iterrows()
]

# =========================================================
# 4️⃣ Local Embedding Model (Proper LangChain Class)
# =========================================================
class LocalEmbeddingModel(Embeddings):
    """Local embedding model compatible with LangChain's FAISS store."""
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_documents(self, texts):
        return self.model.encode(texts, show_progress_bar=False).tolist()

    def embed_query(self, text):
        return self.model.encode([text])[0].tolist()

embeddings = LocalEmbeddingModel()

# Build FAISS index
faq_index = FAISS.from_documents(faq_docs, embeddings)
print("✅ FAISS vector index created successfully.")

# =========================================================
# 5️⃣ Initialize LLM (Chat via OpenRouter)
# =========================================================
chat_llm = ChatOpenAI(
    model="gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_KEY,
    temperature=0.7
)

# =========================================================
# 6️⃣ Add Memory
# =========================================================
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)

# =========================================================
# 7️⃣ Conversational Retrieval Chain
# =========================================================
chatbot = ConversationalRetrievalChain.from_llm(
    llm=chat_llm,
    retriever=faq_index.as_retriever(search_type="similarity", search_kwargs={"k": 3}),
    memory=memory,
    return_source_documents=False,
)
print("✅ Chatbot initialized with memory and FAQ retrieval.")

# =========================================================
# 8️⃣ Chat Loop
# =========================================================
print("\n💬 Chatbot is ready! Type 'exit' to quit.\n")

while True:
    query = input("You: ")
    if query.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    response = chatbot.invoke({"question": query})
    print("Bot:", response["answer"])