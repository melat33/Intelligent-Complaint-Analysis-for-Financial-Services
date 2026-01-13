import time
from datetime import datetime
from typing import Dict, List
import streamlit as st

class SearchManager:
    def __init__(self):
        self.query_history = []
        
    def add_to_history(self, query: str) -> None:
        """Add query to search history"""
        self.query_history.append({
            "query": query,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        # Keep only last 50 entries
        if len(self.query_history) > 50:
            self.query_history = self.query_history[-50:]
    
    def calculate_relevance(self, distance: float) -> float:
        """Calculate relevance percentage from distance"""
        if distance is None:
            return 100.0
        return max(0, min(100, 100 - (distance * 100)))
    
    def get_recent_searches(self, limit: int = 5) -> List[Dict]:
        """Get recent search queries"""
        return list(reversed(self.query_history[-limit:]))