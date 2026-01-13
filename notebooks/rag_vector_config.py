# VECTOR STORE CONFIGURATION
# Generated for Task 3 RAG Pipeline

import os

# Path Configuration
VECTOR_STORE_PATH = r"d:\10 acadamy\Intelligent Complaint Analysis for Financial Services\notebooks\vector_store_1768244751"
COLLECTION_NAME = "financial_complaints"
SOURCE_FILE = r"d:\10 acadamy\Intelligent Complaint Analysis for Financial Services\notebooks\data\processed\complaint_metadata_full.parquet"

# Statistics
TOTAL_DOCUMENTS = 5000
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CREATED_AT = "2026-01-12 22:19:18"

# Functions
def get_vector_store():
    """
    Get the ChromaDB collection for RAG pipeline

    Returns:
        chromadb.Collection: The vector store collection
    """
    import chromadb
    client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)
    return client.get_collection(COLLECTION_NAME)

def test_connection():
    """
    Test if vector store is accessible

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        collection = get_vector_store()
        count = collection.count()
        print("SUCCESS: Connected to vector store")
        print(f"Documents: {count:,}")
        print(f"Location: {VECTOR_STORE_PATH}")
        return True
    except Exception as e:
        print(f"ERROR: Connection failed: {e}")
        return False

# Quick test
if __name__ == "__main__":
    print("=" * 50)
    print("VECTOR STORE CONFIGURATION")
    print("=" * 50)
    print(f"Path: {VECTOR_STORE_PATH}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Documents: {TOTAL_DOCUMENTS:,}")

    if test_connection():
        print("\nREADY: RAG Pipeline is ready!")
    else:
        print("\nERROR: Configuration issue")
