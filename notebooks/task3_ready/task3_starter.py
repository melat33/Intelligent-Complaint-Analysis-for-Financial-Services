# TASK 3 STARTER SCRIPT

import faiss
import pickle
import numpy as np

print("TASK 3 STARTER - COMPLAINT RAG SYSTEM")

try:
    # Load FAISS
    index = faiss.read_index("vector_store/faiss_complaints.idx")
    print(f"FAISS index loaded: {index.ntotal:,} vectors")

    # Load metadata
    with open("vector_store/faiss_metadata.pkl", "rb") as f:
        metadata = pickle.load(f)
    print(f"Metadata loaded: {len(metadata):,} entries")

    # Simple query test
    print("\nTesting with sample query...")

    # Create a test query vector (500-dimensional like your embeddings)
    test_query = np.random.randn(1, 500).astype("float32")
    test_query = test_query / np.linalg.norm(test_query)

    # Search
    k = 3
    distances, indices = index.search(test_query, k)

    print(f"Found {len(indices[0])} similar chunks:")
    for i, (idx, dist) in enumerate(zip(indices[0], distances[0])):
        if idx < len(metadata):
            print(f"  {i+1}. Similarity: {dist:.3f}")
            print(f"     Complaint: {metadata[idx].get('complaint_id', 'N/A')}")
            print(f"     Product: {metadata[idx].get('product', 'Unknown')}")

except Exception as e:
    print(f"Error: {e}")
    print("Make sure you completed Section 6 successfully")
