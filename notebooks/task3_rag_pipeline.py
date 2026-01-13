
# task3_rag_pipeline.py
"""
TASK 3: RAG Pipeline for Financial Complaint Analysis
Complete implementation for retrieval and generation
"""

import chromadb
from sentence_transformers import SentenceTransformer
import os

class FinancialComplaintRAG:
    """RAG system for financial complaint analysis"""

    def __init__(self, vector_store_path="vector_store", collection_name="financial_complaints"):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self._init_vector_store(vector_store_path, collection_name)

    def _init_vector_store(self, path, collection_name):
        """Initialize connection to vector store"""
        try:
            self.client = chromadb.PersistentClient(path=path)
            self.collection = self.client.get_collection(collection_name)
            print(f"✅ Loaded vector store with {self.collection.count()} documents")
        except Exception as e:
            print(f"❌ Error loading vector store: {e}")
            raise

    def retrieve(self, query, k=5):
        """Retrieve relevant complaint chunks"""
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )

        return {
            "documents": results["documents"][0],
            "metadatas": results["metadatas"][0],
            "count": len(results["documents"][0])
        }

    def generate_response(self, query, retrieved_data):
        """Generate answer using prompt template"""
        # Create context from retrieved documents
        context = "\n".join([
            f"Complaint {i+1}: {doc[:150]}..."
            for i, doc in enumerate(retrieved_data["documents"])
        ])

        # Task 3 prompt template
        prompt = f"""You are a financial analyst assistant for CrediTrust. 
Your task is to answer questions about customer complaints. 
Use only the following retrieved complaint excerpts to formulate your answer. 
If the context doesn't contain the answer, state that you don't have enough information.

Context: {context}

Question: {query}

Answer:"""

        # In production, you would use an LLM here
        # For Task 3 demonstration, we return a simple analysis

        return self._simple_analysis(query, retrieved_data)

    def _simple_analysis(self, query, retrieved_data):
        """Simple analysis for Task 3 demonstration"""
        if retrieved_data["count"] == 0:
            return "No relevant complaints found."

        # Analyze metadata
        products = [meta.get("product", "Unknown") for meta in retrieved_data["metadatas"]]
        issues = [meta.get("issue", "General") for meta in retrieved_data["metadatas"]]

        # Find most common
        if products:
            top_product = max(set(products), key=products.count)
        else:
            top_product = "Unknown"

        if issues:
            top_issue = max(set(issues), key=issues.count)
        else:
            top_issue = "General"

        return f"Based on {retrieved_data['count']} relevant complaints: " +                f"Most complaints are about {top_product}, primarily regarding {top_issue}."

    def ask(self, query, k=5):
        """Main method: Ask a question about financial complaints"""
        # Step 1: Retrieve
        retrieved = self.retrieve(query, k)

        # Step 2: Generate
        answer = self.generate_response(query, retrieved)

        # Step 3: Return response
        return {
            "question": query,
            "answer": answer,
            "retrieved_count": retrieved["count"],
            "retrieved_documents": retrieved["documents"][:2]  # Top 2 sources
        }

# Example usage for Task 3
if __name__ == "__main__":
    print("Testing RAG pipeline for Task 3...")

    # Initialize
    rag = FinancialComplaintRAG()

    # Test query
    test_query = "What are common credit card complaints?"
    response = rag.ask(test_query)

    print(f"Question: {response['question']}")
    print(f"Answer: {response['answer']}")
    print(f"Retrieved: {response['retrieved_count']} complaints")
