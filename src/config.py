"""
Configuration settings for the RAG system
"""

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Retrieval settings
RETRIEVAL_K = 5
MIN_CONFIDENCE_SCORE = 30

# Vector store settings
VECTOR_STORE_DIR = "vector_store"
COLLECTION_NAME = "complaint_embeddings"

# Business intelligence settings
BUSINESS_CONTEXTS = {
    "urgent": ["urgent", "critical", "emergency", "immediate"],
    "trending": ["trend", "pattern", "increase", "decrease", "over time"],
    "comparative": ["compare", "vs", "versus", "difference", "better", "worse"],
    "root_cause": ["why", "reason", "cause", "root", "source"],
    "volume": ["many", "often", "frequent", "common", "typical"]
}

# Product categories mapping
PRODUCT_CATEGORIES = {
    "credit card": ["Credit card", "credit card", "Credit Card", "Credit-card"],
    "personal loan": ["Personal loan", "personal loan", "Personal Loan", "Personal-loan"],
    "savings account": ["Savings account", "savings account", "Savings Account", "Savings-account"],
    "money transfers": ["Money transfers", "money transfers", "Money Transfers", "Money-transfers"],
    "mortgage": ["Mortgage", "mortgage", "Home loan"],
    "checking account": ["Checking account", "checking account", "Checking Account", "Checking-account"]
}