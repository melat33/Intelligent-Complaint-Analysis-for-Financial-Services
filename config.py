"""
Configuration settings for the Financial Complaints Analyst
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
VECTOR_STORE_PATH = BASE_DIR / "vector_store_1768244751"

# RAG Configuration
RAG_CONFIG = {
    "embedding_model": "all-MiniLM-L6-v2",
    "collection_names": [
        "financial_complaints", 
        "complaint_embeddings", 
        "complaints", 
        "financial_data"
    ],
    "default_collection": "financial_complaints",
    "search_results": 5,
    "max_history_entries": 50
}

# UI Configuration
UI_CONFIG = {
    "theme": "Soft",
    "server_port": 7860,
    "server_name": "0.0.0.0",
    "title": "Financial Complaints Analyst"
}

# Colors for confidence scores
COLORS = {
    "high": "#10b981",    # Green
    "medium": "#f59e0b",  # Yellow
    "low": "#ef4444",     # Red
    "primary": "#667eea", # Blue
    "secondary": "#764ba2" # Purple
}