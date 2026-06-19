import os
from dotenv import load_dotenv

load_dotenv()

# API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ChromaDB
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "support_kb"

# RAG
CHUNK_SIZE = 400
CHUNK_OVERLAP = 40
TOP_K_RESULTS = 3

# Embedding Model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Persona Classes
PERSONAS = [
    "Technical Expert",
    "Frustrated User",
    "Business Executive"
]

# Escalation
ESCALATION_CONFIDENCE_THRESHOLD = 0.5