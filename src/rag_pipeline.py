from google import genai
import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from sentence_transformers import SentenceTransformer
from src.config import CHUNK_SIZE, CHUNK_OVERLAP
from src.config import CHROMA_DB_PATH
from src.config import TOP_K_RESULTS

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
# ChromaDB Setup

chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

collection = chroma_client.get_or_create_collection(
    name="support_kb"
)

# Load Documents
def load_documents(data_folder="data"):
    docs = []

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

# Gemini Embedding
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

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
            metadatas=[{
                "source": chunk["source"]
            }]
        )

    print("Documents stored in ChromaDB")


# Retrieve Context
def retrieve(query, top_k=TOP_K_RESULTS):

    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrieved_chunks = []

    for i in range(len(results["documents"][0])):

        retrieved_chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"]
        })

    return retrieved_chunks


# Test
if __name__ == "__main__":

    # Run only first time
    ingest_documents()

    query = "How do I reset my password?"

    results = retrieve(query)

    print("\nTop Results:\n")

    for item in results:
        print("=" * 50)
        print("Source:", item["source"])
        print(item["text"])
