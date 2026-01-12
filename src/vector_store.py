"""
Create and manage ChromaDB vector store
"""
import chromadb
import pandas as pd
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from src.config import *

def create_chroma_collection():
    """Create ChromaDB collection from parquet file"""
    
    print("📚 Creating ChromaDB collection from embeddings...")
    
    # Load embeddings
    print(f"Loading embeddings from: {EMBEDDINGS_PATH}")
    df = pd.read_parquet(EMBEDDINGS_PATH)
    
    # Take a sample for faster testing (remove for full dataset)
    df_sample = df.sample(min(10000, len(df)))  # Use 10K samples for testing
    print(f"Using {len(df_sample)} samples for collection creation")
    
    # Initialize ChromaDB
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
    
    # Create collection
    collection = client.create_collection(
        name="complaint_embeddings",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Add data in batches
    batch_size = 1000
    total_batches = (len(df_sample) + batch_size - 1) // batch_size
    
    for i in range(0, len(df_sample), batch_size):
        batch = df_sample.iloc[i:i+batch_size]
        
        # Prepare data
        ids = batch.index.astype(str).tolist()
        embeddings = batch['embedding'].tolist() if 'embedding' in batch.columns else None
        documents = batch['text_chunk'].tolist()
        
        # Prepare metadata
        metadatas = []
        for _, row in batch.iterrows():
            metadata = {
                'complaint_id': str(row.get('complaint_id', '')),
                'product_category': str(row.get('product_category', '')),
                'product': str(row.get('product', '')),
                'issue': str(row.get('issue', '')),
                'sub_issue': str(row.get('sub_issue', '')),
                'company': str(row.get('company', '')),
                'state': str(row.get('state', '')),
                'date_received': str(row.get('date_received', '')),
                'chunk_index': int(row.get('chunk_index', 0)),
                'total_chunks': int(row.get('total_chunks', 1))
            }
            metadatas.append(metadata)
        
        # Add to collection
        if embeddings:
            collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
        else:
            collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
        
        # Progress update
        batch_num = i // batch_size + 1
        print(f"  Added batch {batch_num}/{total_batches} ({len(batch)} items)")
    
    print(f"✅ Collection created: {collection.name}")
    print(f"   Total items: {collection.count()}")
    
    return collection

def get_chroma_collection():
    """Get existing ChromaDB collection or create if doesn't exist"""
    
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
    
    try:
        collection = client.get_collection("complaint_embeddings")
        print(f"✅ Loaded existing collection: {collection.name} ({collection.count()} items)")
        return collection
    except ValueError:
        print("⚠️ Collection not found. Creating new collection...")
        return create_chroma_collection()