"""
Vector store management utilities
"""
import chromadb
from typing import Optional
from .config import VECTOR_STORE_DIR, COLLECTION_NAME

def get_chroma_collection() -> chromadb.Collection:
    """
    Get or create ChromaDB collection with proper error handling
    """
    try:
        client = chromadb.PersistentClient(path=VECTOR_STORE_DIR)
        
        # Try to get existing collection
        try:
            collection = client.get_collection(COLLECTION_NAME)
            return collection
        except:
            # Try alternative collection names
            try:
                collection = client.get_collection("financial_complaints")
                return collection
            except:
                # Create new collection
                collection = client.create_collection(COLLECTION_NAME)
                return collection
                
    except Exception as e:
        print(f"⚠️ Vector store error: {e}")
        # Return dummy collection for testing
        class DummyCollection:
            def count(self):
                return 0
            def query(self, **kwargs):
                return {'documents': [[]], 'metadatas': [[]], 'distances': [[]]}
            def peek(self, limit=10):
                return {'metadatas': []}
        return DummyCollection()