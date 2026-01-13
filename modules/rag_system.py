"""
RAG system for processing financial complaints queries
"""
from typing import Dict, List, Optional, Set, Tuple
from sentence_transformers import SentenceTransformer
from .database import VectorDatabase
from config import RAG_CONFIG

class FinancialComplaintsRAG:
    """Main RAG system for analyzing financial complaints"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.embedder = SentenceTransformer(RAG_CONFIG["embedding_model"])
        self.db = VectorDatabase()
        self.connected = self.db.connect()
        
    def ask(self, question: str, product_filter: Optional[str] = None) -> Dict:
        """Process a user query"""
        if not self.connected:
            return self._no_data_response(question)
        
        try:
            results = self.db.query(
                query_text=question,
                product_filter=product_filter,
                n_results=RAG_CONFIG["search_results"]
            )
            
            return self._process_results(question, results)
        except Exception as e:
            print(f"⚠️ RAG processing error: {e}")
            return self._error_response(question, str(e))
    
    def _process_results(self, question: str, results: Dict) -> Dict:
        """Process and format search results"""
        chunks = results['documents'][0] if results['documents'] else []
        metadatas = results['metadatas'][0] if results['metadatas'] else []
        distances = results['distances'][0] if results['distances'] else []
        
        count = len(chunks)
        
        # Extract metadata statistics
        products, issues, companies = self._extract_metadata(metadatas)
        
        # Calculate confidence
        confidence_score, confidence_level = self._calculate_confidence(distances)
        
        # Prepare sources
        sources = self._prepare_sources(chunks, metadatas)
        
        # Generate answer
        answer = self._generate_answer(count, confidence_level, confidence_score, products, issues)
        
        return {
            "question": question,
            "answer": answer,
            "confidence": confidence_score,
            "confidence_level": confidence_level,
            "sources": sources,
            "stats": {
                "total_complaints": count,
                "products_covered": len(products),
                "issues_identified": len(issues),
                "companies": len(companies)
            }
        }
    
    def _extract_metadata(self, metadatas: List[Dict]) -> Tuple[Set, Set, Set]:
        """Extract metadata from search results"""
        products = set()
        issues = set()
        companies = set()
        
        for meta in metadatas:
            if meta:
                if 'product_category' in meta and meta['product_category']:
                    products.add(str(meta['product_category']))
                if 'issue' in meta and meta['issue']:
                    issues.add(str(meta['issue']))
                if 'company' in meta and meta['company']:
                    companies.add(str(meta['company']))
        
        return products, issues, companies
    
    def _calculate_confidence(self, distances: List[float]) -> Tuple[float, str]:
        """Calculate confidence score and level"""
        if distances:
            avg_distance = sum(distances) / len(distances)
            confidence_score = (1 - avg_distance) * 100
        else:
            confidence_score = 50.0
        
        if confidence_score >= 70:
            confidence_level = "HIGH"
        elif confidence_score >= 40:
            confidence_level = "MEDIUM"
        else:
            confidence_level = "LOW"
        
        return round(confidence_score, 1), confidence_level
    
    def _prepare_sources(self, chunks: List[str], metadatas: List[Dict]) -> List[Dict]:
        """Prepare source information for display"""
        sources = []
        for i, (chunk, meta) in enumerate(zip(chunks, metadatas), 1):
            sources.append({
                "id": i,
                "text": chunk[:200] + "..." if len(chunk) > 200 else chunk,
                "product": meta.get('product_category', 'Unknown') if meta else 'Unknown',
                "issue": meta.get('issue', 'General') if meta else 'General',
                "company": meta.get('company', 'Unknown') if meta else 'Unknown'
            })
        return sources
    
    def _generate_answer(self, count: int, confidence_level: str, confidence_score: float,
                        products: Set, issues: Set) -> str:
        """Generate a formatted answer"""
        product_list = list(products)[:3]
        issue_list = list(issues)[:3]
        
        return f"""
**📊 Analysis Results:**
- **Complaints Analyzed:** {count}
- **Confidence Level:** {confidence_level} ({confidence_score:.1f}%)
- **Products Covered:** {len(products)}
- **Main Issues:** {', '.join(issue_list) if issue_list else 'Various'}

**💡 Key Insights:**
{', '.join(product_list) if product_list else 'Various financial products'} show patterns of {', '.join(issue_list) if issue_list else 'customer concerns'}.

**🎯 Recommendations:**
1. Review complaint patterns for identified products
2. Address the most frequent issues
3. Monitor customer feedback continuously
"""
    
    def _no_data_response(self, question: str) -> Dict:
        """Response when no data is available"""
        return {
            "question": question,
            "answer": self._get_no_data_message(),
            "confidence": 0,
            "confidence_level": "NO_DATA",
            "sources": [],
            "stats": {"total_complaints": 0, "products_covered": 0, "issues_identified": 0, "companies": 0}
        }
    
    def _error_response(self, question: str, error_msg: str) -> Dict:
        """Response when there's an error"""
        return {
            "question": question,
            "answer": self._get_error_message(error_msg),
            "confidence": 0,
            "confidence_level": "ERROR",
            "sources": [],
            "stats": {"total_complaints": 0, "products_covered": 0, "issues_identified": 0, "companies": 0}
        }
    
    def _get_no_data_message(self) -> str:
        """Message when vector store is not connected"""
        return """
**⚠️ System Configuration Required**

The vector store is not properly connected. Please check:

1. **Vector Store Location**: Ensure `vector_store_1768244751` is in the same directory
2. **Collection Name**: Check if collection name is different
3. **Permissions**: Verify read access to the vector store

**📋 For Demonstration:**
Try asking about common financial complaints like:
- Credit card fraud issues
- Personal loan application problems
- Savings account fee concerns
"""
    
    def _get_error_message(self, error_msg: str) -> str:
        """Error message template"""
        return f"""
**❌ System Error**

Error: {error_msg}

**🔧 Troubleshooting:**
1. Restart the application
2. Check vector store connection
3. Verify all dependencies are installed
"""
    
    def get_document_count(self) -> int:
        """Get total document count"""
        if self.connected and self.db.collection:
            try:
                return self.db.collection.count()
            except:
                return 0
        return 0