"""
Query handling and history management
"""
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from .rag_system import FinancialComplaintsRAG
from .ui_components import UIComponents

class QueryHandler:
    """Manages query processing and history"""
    
    def __init__(self, rag_system: FinancialComplaintsRAG):
        self.rag_system = rag_system
        self.query_history: List[Dict] = []
        
    def process_query(self, question: str, product_filter: str, show_sources: bool = True) -> Tuple[str, str]:
        """Process user query and return formatted response"""
        # Add to history
        self.add_to_history(question, product_filter)
        
        try:
            # Get response from RAG system
            product_filter_clean = product_filter if product_filter != "All" else None
            response = self.rag_system.ask(question, product_filter_clean)
            
            # Format response
            formatted_response = UIComponents.format_response(response)
            
            # Update history (keep only last 10)
            if len(self.query_history) > 10:
                self.query_history.pop(0)
            
            return formatted_response, json.dumps(response, indent=2)
        
        except Exception as e:
            error_msg = f"""
            <div class="card" style="border-left: 4px solid #ef4444;">
                <h3 style="color: #ef4444;">❌ Error Processing Query</h3>
                <p>{str(e)}</p>
                <p>Please try again or check the system connection.</p>
            </div>
            """
            return error_msg, json.dumps({"error": str(e)}, indent=2)
    
    def add_to_history(self, question: str, product_filter: str) -> None:
        """Add query to history"""
        self.query_history.append({
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "product_filter": product_filter
        })
    
    def clear_history(self) -> Tuple[str, str]:
        """Clear query history"""
        self.query_history.clear()
        return "✅ History cleared", ""
    
    def get_recent_activity_html(self) -> str:
        """Get HTML for recent activity display"""
        if not self.query_history:
            return "<p style='color: #6b7280;'>No recent queries</p>"
        
        html = "<div style='max-height: 300px; overflow-y: auto;'>"
        for query in reversed(self.query_history[-5:]):
            html += f"""
            <div style="background: #f9fafb; padding: 0.75rem; margin: 0.5rem 0; border-radius: 6px;">
                <div style="font-weight: 500;">{query['question'][:50]}...</div>
                <div style="font-size: 0.8rem; color: #6b7280;">
                    Filter: {query['product_filter']}
                </div>
            </div>
            """
        html += "</div>"
        return html
    
    def get_system_stats_html(self) -> str:
        """Get system statistics HTML"""
        return UIComponents.format_system_stats(self.rag_system, self.query_history)