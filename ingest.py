"""Load our documents into ChromaDB so they can be searched by meaning."""

import json
from pathlib import Path

import chromadb
import ollama

PROJECT_DIR = Path(__file__).parent
DOCUMENTS_FILE = PROJECT_DIR / "data" / "documents.json"
DB_DIR = PROJECT_DIR / "chroma_db"
COLLECTION_NAME = "ux_knowledge"
EMBED_MODEL = "nomic-embed-text"


def load_documents(path=DOCUMENTS_FILE):
    """Read our knowledge documents from JSON."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def embed_texts(texts):
    """Get embeddings for a list of texts in one call to Ollama."""
    response = ollama.embed(model=EMBED_MODEL, input=texts)
    return response["embeddings"]


def get_collection():
    """Open (or create) our ChromaDB collection on disk."""
    client = chromadb.PersistentClient(path=str(DB_DIR))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def ingest():
    documents = load_documents()
    collection = get_collection()

    collection.upsert(
        ids=[doc["id"] for doc in documents],
        documents=[doc["content"] for doc in documents],
        embeddings=embed_texts([doc["content"] for doc in documents]),
        metadatas=[
            {
                "title": doc["title"],
                "topics": ", ".join(doc["topics"]),
                "inspired_by": doc["inspired_by"],
                "fictional": doc["fictional"],
            }
            for doc in documents
        ],
    )
    print(f"Stored {collection.count()} documents in '{COLLECTION_NAME}'")


if __name__ == "__main__":
    ingest()