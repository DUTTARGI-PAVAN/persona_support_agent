import os
import chromadb
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from src.config import CHUNK_SIZE, CHUNK_OVERLAP
from src.config import CHROMA_DB_PATH
from src.config import TOP_K_RESULTS

# ChromaDB Setup
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(name="support_kb")

# Load Documents
def load_documents(data_folder="data"):
    docs = []
    if not os.path.exists(data_folder):
        print(f"Warning: Data folder '{data_folder}' not found.")
        return docs

    for file in os.listdir(data_folder):
        file_path = os.path.join(data_folder, file)

        # TXT and MD files
        if file.endswith(".txt") or file.endswith(".md"):
            with open(file_path, "r", encoding="utf-8") as f:
                docs.append({
                    "source": file,
                    "text": f.read()
                })

        # PDF files
        elif file.endswith(".pdf"):
            reader = PdfReader(file_path)
            pdf_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pdf_text += text + "\n"

            docs.append({
                "source": file,
                "text": pdf_text
            })

    return docs

# Chunk Documents
def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = []
    for doc in documents:
        split_text = splitter.split_text(doc["text"])
        for i, chunk in enumerate(split_text):
            chunks.append({
                "id": f"{doc['source']}_{i}",
                "source": doc["source"],
                "text": chunk
            })

    return chunks

# Local Embedding Setup (Offline-safe for deployment)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    return embedding_model.encode(text).tolist()

# Store Chunks
def ingest_documents():
    docs = load_documents()
    chunks = chunk_documents(docs)

    print(f"Loaded {len(docs)} documents")
    print(f"Created {len(chunks)} chunks")

    for chunk in chunks:
        embedding = get_embedding(chunk["text"])
        collection.add(
            ids=[chunk["id"]],
            embeddings=[embedding],
            documents=[chunk["text"]],
            metadatas=[{"source": chunk["source"]}]
        )

    print("Documents stored in ChromaDB")

# Retrieve Context (Updated with matching similarity score logic)
def retrieve(query, top_k=TOP_K_RESULTS):
    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrieved_chunks = []
    
    if results and results["documents"] and len(results["documents"][0]) > 0:
        for i in range(len(results["documents"][0])):
            # Safely grab distance and convert to standard similarity score framework
            distance = results["distances"][0][i] if "distances" in results and results["distances"] else 0.0
            similarity_score = 1.0 - distance

            retrieved_chunks.append({
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "score": similarity_score  # Passed back cleanly for downstream adaptive generators
            })

    return retrieved_chunks

# Test
if __name__ == "__main__":
    # Run ingestion check
    ingest_documents()

    query = "How do I reset my password?"
    results = retrieve(query)

    print("\nTop Results:\n")
    for item in results:
        print("=" * 50)
        print("Source:", item["source"])
        print("Score:", item["score"])
        print(item["text"])