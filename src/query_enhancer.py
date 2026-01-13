"""
Query enhancement and understanding module
"""
from typing import Dict, List
from .config import BUSINESS_CONTEXTS, PRODUCT_CATEGORIES

class QueryEnhancer:
    """Enhanced query understanding for business intelligence"""
    
    def analyze_query(self, question: str) -> Dict:
        """Deep analysis of business queries"""
        question_lower = question.lower()
        
        # Detect products
        detected_products = []
        for product_name, variations in PRODUCT_CATEGORIES.items():
            if any(variation.lower() in question_lower for variation in variations):
                detected_products.append(product_name.title())
        
        # Detect business context
        business_context = {}
        for context_type, keywords in BUSINESS_CONTEXTS.items():
            business_context[context_type] = any(
                keyword in question_lower for keyword in keywords
            )
        
        # Determine query type
        if business_context.get('comparative'):
            query_type = "comparative"
        elif business_context.get('trending'):
            query_type = "trend_analysis"
        elif business_context.get('root_cause'):
            query_type = "root_cause"
        elif detected_products:
            query_type = "product_analysis"
        else:
            query_type = "general_analysis"
        
        return {
            "original_query": question,
            "products": detected_products,
            "query_type": query_type,
            "business_context": business_context,
            "business_intent": self._determine_intent(question)
        }
    
    def enhance_query(self, question: str, analysis: Dict) -> List[str]:
        """Create enhanced query variations"""
        enhanced = [question]
        
        # Add product-specific variations
        if analysis["products"]:
            for product in analysis["products"][:2]:  # Top 2 products
                enhanced.append(f"{product} complaints {question}")
                enhanced.append(f"customer issues with {product} {question}")
        
        # Add context-based variations
        if analysis["business_context"].get("urgent"):
            enhanced.append(f"urgent critical {question}")
        if analysis["business_context"].get("trending"):
            enhanced.append(f"trend pattern {question}")
        
        # Add general business variations
        enhanced.append(f"financial customer complaint analysis {question}")
        enhanced.append(f"business intelligence {question}")
        
        return enhanced[:5]  # Return top 5 enhanced queries
    
    def _determine_intent(self, question: str) -> str:
        """Determine the business intent of the query"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["trend", "pattern", "increase", "decrease"]):
            return "monitor_performance"
        elif any(word in question_lower for word in ["compare", "vs", "versus", "difference"]):
            return "competitive_analysis"
        elif any(word in question_lower for word in ["why", "reason", "cause", "root"]):
            return "root_cause_analysis"
        elif any(word in question_lower for word in ["improve", "better", "fix", "solve"]):
            return "process_improvement"
        else:
            return "insight_generation"