import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
import hashlib
from datetime import datetime

# Initialize paths
CHROMA_PATH = Path("data/chroma_db")
CHROMA_PATH.mkdir(parents=True, exist_ok=True)

# Initialize embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize ChromaDB client
client = chromadb.PersistentClient(path=str(CHROMA_PATH))
collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)


def generate_doc_id(text: str, doc_type: str) -> str:
    """
    Generate unique document ID using hash
    """
    content = f"{doc_type}_{text[:100]}_{datetime.now().isoformat()}"
    return hashlib.md5(content.encode()).hexdigest()


def store_embedding(text: str, metadata: dict, doc_type: str):
    """
    Store document with embedding in ChromaDB
    """
    try:
        # Generate embedding
        embedding = model.encode(text).tolist()
        
        # Create document ID
        doc_id = generate_doc_id(text, doc_type)
        
        # Prepare metadata
        meta = {
            "type": doc_type,
            "timestamp": datetime.now().isoformat(),
            **metadata
        }
        
        # Convert all metadata values to strings (ChromaDB requirement)
        meta = {k: str(v) if v is not None else "" for k, v in meta.items()}
        
        # Store in ChromaDB
        collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[meta],
            ids=[doc_id]
        )
        
        return doc_id
        
    except Exception as e:
        print(f"Error storing embedding: {e}")
        return None


def search_documents(query: str, n_results: int = 5, doc_type: str = None):
    """
    Search documents using semantic similarity
    """
    try:
        # Generate query embedding
        query_embedding = model.encode(query).tolist()
        
        # Build where filter if doc_type specified
        where_filter = {"type": doc_type} if doc_type else None
        
        # Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter
        )
        
        return results
        
    except Exception as e:
        print(f"Error searching documents: {e}")
        return None


def get_all_documents():
    """
    Retrieve all documents from ChromaDB
    """
    try:
        results = collection.get()
        return results
    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return None


def delete_document(doc_id: str):
    """
    Delete a document by ID
    """
    try:
        collection.delete(ids=[doc_id])
        return True
    except Exception as e:
        print(f"Error deleting document: {e}")
        return False


def get_collection_stats():
    """
    Get statistics about the collection
    """
    try:
        count = collection.count()
        return {
            "total_documents": count,
            "collection_name": collection.name
        }
    except Exception as e:
        print(f"Error getting stats: {e}")
        return {}