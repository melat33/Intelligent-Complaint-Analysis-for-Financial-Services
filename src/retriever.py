"""
Advanced retriever with hybrid search
"""
import chromadb
from sentence_transformers import SentenceTransformer
from typing import Dict, List, Optional
from src.config import *
from src.query_enhancer import QueryEnhancer
from src.vector_store import get_chroma_collection  # NEW IMPORT

class HybridRetriever:
    """Combines semantic and keyword retrieval"""
    
    def __init__(self):
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        self.query_enhancer = QueryEnhancer()
        
        # Get or create ChromaDB collection
        print("📚 Loading ChromaDB collection...")
        self.collection = get_chroma_collection()
        
        print(f"✅ HybridRetriever ready with {self.collection.count()} chunks")
    
    def semantic_retrieve(self, query: str, k: int = 3, 
                         filter_product: Optional[str] = None) -> Dict:
        """Semantic similarity search"""
        where_filter = None
        if filter_product:
            where_filter = {"product_category": {"$eq": filter_product}}
        
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
            where=where_filter,
            include=["documents", "metadatas", "distances"]
        )
        
        return {
            "method": "semantic",
            "chunks": results['documents'][0] if results['documents'] else [],
            "metadata": results['metadatas'][0] if results['metadatas'] else [],
            "distances": results['distances'][0] if results['distances'] else []
        }
    
    def hybrid_retrieve(self, question: str, k: int = RETRIEVAL_K,
                       filter_product: Optional[str] = None) -> Dict:
        """Combine semantic and keyword retrieval"""
        
        print(f"🔍 Retrieving for: '{question}'")
        
        # Analyze query
        query_analysis = self.query_enhancer.analyze_query(question)
        print(f"   Query Type: {query_analysis['type'].upper()}")
        if query_analysis['products']:
            print(f"   Products: {', '.join(query_analysis['products'])}")
        
        # Get enhanced queries
        enhanced_queries = self.query_enhancer.enhance_query(question, query_analysis)
        print(f"   Enhanced queries: {len(enhanced_queries)} variations")
        
        # Run semantic retrieval on top queries
        semantic_results = []
        for enhanced_query in enhanced_queries[:2]:  # Use top 2 enhanced queries
            result = self.semantic_retrieve(enhanced_query, k=k//2, 
                                          filter_product=filter_product)
            
            # Add method tag
            for chunk, meta, dist in zip(result['chunks'], result['metadata'], result['distances']):
                semantic_results.append((chunk, meta, dist, f"semantic_{enhanced_query[:20]}..."))
        
        # Sort by distance and deduplicate
        all_results = semantic_results
        all_results.sort(key=lambda x: x[2])  # Sort by distance
        
        # Deduplicate
        seen = set()
        final_results = []
        for chunk, meta, dist, method in all_results:
            chunk_hash = hash(chunk[:150])  # Check first 150 chars
            if chunk_hash not in seen:
                seen.add(chunk_hash)
                final_results.append((chunk, meta, dist, method))
        
        # Take top k
        final_results = final_results[:k]
        
        print(f"   Retrieved: {len(final_results)} unique chunks")
        
        return {
            "chunks": [r[0] for r in final_results],
            "metadata": [r[1] for r in final_results],
            "distances": [r[2] for r in final_results],
            "retrieval_methods": [r[3] for r in final_results],
            "query_analysis": query_analysis,
            "total_retrieved": len(final_results)
        }