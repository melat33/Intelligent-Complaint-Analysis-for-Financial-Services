"""
Database connection and management for ChromaDB
"""
import chromadb
import os
from typing import Optional, List, Dict, Any
from config import VECTOR_STORE_PATH, RAG_CONFIG

class VectorDatabase:
    """Manages connections to ChromaDB vector store"""
    
    def __init__(self):
        self.client = None
        self.collection = None
        self.connected = False
        
    def connect(self) -> bool:
        """Connect to vector store with fallback options"""
        try:
            if not VECTOR_STORE_PATH.exists():
                print(f"❌ Vector store not found at: {VECTOR_STORE_PATH}")
                return False
            
            print(f"📁 Connecting to vector store at: {VECTOR_STORE_PATH}")
            self.client = chromadb.PersistentClient(path=str(VECTOR_STORE_PATH))
            print("✅ ChromaDB client connected")
            
            # Try different collection names
            self.collection = self._find_collection()
            
            if self.collection:
                self.connected = True
                count = self.collection.count()
                print(f"✅ Connected to '{self.collection.name}' with {count:,} documents")
                return True
            else:
                print("❌ No suitable collection found")
                return False
                
        except Exception as e:
            print(f"❌ Error connecting to vector store: {e}")
            return False
    
    def _find_collection(self):
        """Try different collection names until one works"""
        for collection_name in RAG_CONFIG["collection_names"]:
            try:
                print(f"  🔍 Trying collection: '{collection_name}'...")
                collection = self.client.get_collection(collection_name)
                print(f"  ✅ Found: '{collection_name}'")
                return collection
            except Exception:
                print(f"  ❌ Not found: '{collection_name}'")
                continue
        
        # List available collections if none found
        try:
            collections = self.client.list_collections()
            print(f"📋 Available collections: {[c.name for c in collections]}")
            if collections:
                collection = self.client.get_collection(collections[0].name)
                print(f"✅ Using first available: '{collection.name}'")
                return collection
        except Exception as e:
            print(f"⚠️ Cannot list collections: {e}")
        
        return None
    
    def query(self, query_text: str, product_filter: Optional[str] = None, n_results: int = 5) -> Optional[Dict]:
        """Query the vector database"""
        if not self.collection:
            raise ConnectionError("Database not connected")
        
        try:
            where_filter = None
            if product_filter:
                where_filter = {"product_category": product_filter}
            
            print(f"🔍 Querying: '{query_text[:50]}...'")
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where_filter,
                include=["documents", "metadatas", "distances"]
            )
            
            return results
        except Exception as e:
            print(f"⚠️ Query error: {e}")
            raise