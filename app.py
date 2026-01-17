# app.py - COMPLETE WORKING VERSION
import streamlit as st
import chromadb
import time
import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import pandas as pd
from chromadb.utils import embedding_functions

# Page configuration
st.set_page_config(
    page_title="Financial Complaints Analyzer",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .main-title { 
        font-size: 2.5rem; 
        font-weight: 800; 
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    .subtitle { 
        font-size: 1.1rem; 
        opacity: 0.9; 
        font-weight: 300;
    }
    .card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .tag {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 2px 4px 2px 0;
        display: inline-block;
        font-weight: 500;
    }
    .result-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #667eea30;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        color: #667eea;
        margin: 0.5rem 0;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .confidence-high { color: #10b981; }
    .confidence-medium { color: #f59e0b; }
    .confidence-low { color: #ef4444; }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "query_history" not in st.session_state:
    st.session_state.query_history = []
if "search_results" not in st.session_state:
    st.session_state.search_results = None
if "db_initialized" not in st.session_state:
    st.session_state.db_initialized = False
if "collection" not in st.session_state:
    st.session_state.collection = None

class DatabaseManager:
    """Manages ChromaDB connection and operations"""
    
    def __init__(self):
        self.client = None
        self.collection = None
        self.embedding_function = None
        self.vector_store_path = "vector_store"
        
    def initialize(self) -> Tuple[bool, str]:
        """Initialize database connection with automatic setup"""
        try:
            # Create vector store directory if it doesn't exist
            os.makedirs(self.vector_store_path, exist_ok=True)
            
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(path=self.vector_store_path)
            
            # Setup embedding function
            self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
            
            # Try to get existing collection or create new one
            try:
                self.collection = self.client.get_collection(
                    name="financial_complaints",
                    embedding_function=self.embedding_function
                )
                count = self.collection.count()
                return True, f"✅ Connected to existing collection with {count:,} documents"
                
            except:
                # Create new collection
                self.collection = self.client.create_collection(
                    name="financial_complaints",
                    embedding_function=self.embedding_function,
                    metadata={"description": "Financial complaints database", "created": datetime.now().isoformat()}
                )
                
                # Load sample data
                self._load_sample_data()
                count = self.collection.count()
                return True, f"✅ Created new collection with {count:,} sample documents"
                
        except Exception as e:
            return False, f"❌ Database initialization failed: {str(e)}"
    
    def _load_sample_data(self):
        """Load sample financial complaint data"""
        sample_complaints = [
            {
                "text": "Customer reported unauthorized credit card charges totaling $500 from an online retailer. The charges appeared over the weekend without any notification.",
                "product": "Credit card",
                "issue": "Unauthorized transaction",
                "company": "Bank of America",
                "state": "CA",
                "date": "2024-01-15"
            },
            {
                "text": "Mortgage application delayed for 45 days due to missing documentation requests that were never clearly communicated by the loan officer.",
                "product": "Mortgage",
                "issue": "Application delay",
                "company": "Wells Fargo",
                "state": "NY",
                "date": "2024-01-10"
            },
            {
                "text": "Monthly checking account maintenance fee increased from $10 to $15 without proper notification 30 days in advance as required by regulation.",
                "product": "Checking account",
                "issue": "Hidden fees",
                "company": "Chase",
                "state": "TX",
                "date": "2024-01-05"
            },
            {
                "text": "Personal loan application rejected despite having excellent credit score of 780 and stable employment for 5+ years.",
                "product": "Personal loan",
                "issue": "Application rejection",
                "company": "Citibank",
                "state": "FL",
                "date": "2024-01-20"
            },
            {
                "text": "International money transfer delayed by 7 business days causing significant financial loss due to exchange rate fluctuations.",
                "product": "Money transfer",
                "issue": "Transfer delay",
                "company": "Western Union",
                "state": "IL",
                "date": "2024-01-12"
            },
            {
                "text": "Credit card interest rate increased from 15.99% to 22.99% without clear explanation or proper notice as required by law.",
                "product": "Credit card",
                "issue": "Interest rate increase",
                "company": "Capital One",
                "state": "OH",
                "date": "2024-01-18"
            },
            {
                "text": "Savings account withdrawal blocked for 3 days despite sufficient funds, causing bill payment failures and resulting in late fees.",
                "product": "Savings account",
                "issue": "Account access",
                "company": "Bank of America",
                "state": "CA",
                "date": "2024-01-08"
            },
            {
                "text": "Auto loan payment applied incorrectly to principal instead of interest, causing miscalculation of remaining balance.",
                "product": "Auto loan",
                "issue": "Payment processing",
                "company": "Ally Bank",
                "state": "MI",
                "date": "2024-01-22"
            },
            {
                "text": "Overdraft protection not activated despite customer request, resulting in $35 overdraft fees on 3 separate transactions.",
                "product": "Checking account",
                "issue": "Overdraft fees",
                "company": "Chase",
                "state": "TX",
                "date": "2024-01-14"
            },
            {
                "text": "Credit limit decreased from $10,000 to $2,000 without explanation, negatively impacting credit score and utilization ratio.",
                "product": "Credit card",
                "issue": "Credit limit decrease",
                "company": "Discover",
                "state": "GA",
                "date": "2024-01-25"
            }
        ]
        
        # Add documents to collection
        documents = []
        metadatas = []
        ids = []
        
        for i, complaint in enumerate(sample_complaints):
            documents.append(complaint["text"])
            metadatas.append({
                "product": complaint["product"],
                "issue": complaint["issue"],
                "company": complaint["company"],
                "state": complaint["state"],
                "date": complaint["date"],
                "source": "sample"
            })
            ids.append(f"complaint_{i}")
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, query: str, n_results: int = 5) -> Optional[Dict]:
        """Search the database"""
        if not self.collection:
            return None
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            return {
                "documents": results['documents'][0] if results['documents'] else [],
                "metadatas": results['metadatas'][0] if results['metadatas'] else [],
                "distances": results['distances'][0] if results['distances'] else [],
                "query": query,
                "count": len(results['documents'][0]) if results['documents'] else 0
            }
        except Exception as e:
            st.error(f"Search error: {str(e)}")
            return None
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        if not self.collection:
            return {"total_documents": 0, "status": "Not connected"}
        
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "status": "Connected",
                "collection_name": self.collection.name
            }
        except:
            return {"total_documents": 0, "status": "Error"}

def display_result_card(idx: int, document: str, metadata: Dict, distance: float):
    """Display a single search result card"""
    # Calculate relevance
    relevance = 100 - (distance * 100) if distance else 100
    confidence_class = "confidence-high" if relevance > 70 else "confidence-medium" if relevance > 40 else "confidence-low"
    
    with st.container():
        st.markdown(f"""
        <div class="result-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h4 style="margin: 0;">📄 Result #{idx+1}</h4>
                <span class="{confidence_class}" style="font-weight: bold;">
                    {relevance:.1f}% relevant
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        # Document text
        st.text_area("", document, height=120, key=f"doc_{idx}", disabled=True)
        
        # Metadata tags
        if metadata:
            cols = st.columns(4)
            metadata_items = [
                ("product", "📊"),
                ("issue", "⚠️"),
                ("company", "🏢"),
                ("state", "📍")
            ]
            
            for i, (key, icon) in enumerate(metadata_items):
                if key in metadata and metadata[key]:
                    with cols[i]:
                        st.markdown(f'<span class="tag">{icon} {metadata[key]}</span>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def main():
    """Main application"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="main-title">💰 Financial Complaints Analyzer</div>
        <div class="subtitle">AI-powered insights from consumer financial complaints database</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize database manager
    if "db_manager" not in st.session_state:
        st.session_state.db_manager = DatabaseManager()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔧 Database Connection")
        
        # Connection button
        if not st.session_state.db_initialized:
            if st.button("🚀 Connect to Database", type="primary", use_container_width=True):
                with st.spinner("Initializing database..."):
                    success, message = st.session_state.db_manager.initialize()
                    if success:
                        st.session_state.db_initialized = True
                        st.session_state.collection = st.session_state.db_manager.collection
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        else:
            st.success("✅ Database Connected")
        
        # Display stats if connected
        if st.session_state.db_initialized:
            stats = st.session_state.db_manager.get_stats()
            
            st.markdown("---")
            st.markdown("### 📊 Database Stats")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Documents", f"{stats['total_documents']:,}")
            with col2:
                st.metric("Status", stats['status'])
            
            st.markdown(f"**Collection:** `{stats.get('collection_name', 'N/A')}`")
        
        # Quick searches
        st.markdown("---")
        st.markdown("### ⚡ Quick Searches")
        
        quick_searches = [
            ("💳 Credit Card Fraud", "unauthorized credit card charges"),
            ("🏠 Mortgage Delays", "mortgage application delayed"),
            ("💰 Hidden Fees", "hidden fees checking account"),
            ("📄 Loan Rejection", "personal loan application rejected"),
            ("💸 Payment Issues", "payment processing problems")
        ]
        
        for emoji, query in quick_searches:
            if st.button(f"{emoji} {query}", key=f"quick_{query}", use_container_width=True):
                st.session_state.quick_query = query
                st.rerun()
        
        # History
        st.markdown("---")
        st.markdown("### 📝 Recent Searches")
        
        if st.session_state.query_history:
            for i, item in enumerate(reversed(st.session_state.query_history[-3:])):
                with st.container():
                    st.caption(f"**{item['query'][:30]}...**")
                    st.caption(f"⏱️ {item['time']:.2f}s | 📅 {item['timestamp']}")
                    if i < 2:
                        st.divider()
        else:
            st.info("No searches yet")
        
        # Clear button
        if st.session_state.query_history:
            if st.button("🗑️ Clear History", type="secondary", use_container_width=True):
                st.session_state.query_history = []
                st.session_state.search_results = None
                st.rerun()
    
    # Main content area
    col_main, col_info = st.columns([3, 1])
    
    with col_main:
        st.markdown("### 🔍 Search Financial Complaints")
        
        # Search input
        query_input = st.text_input(
            "Enter your question:",
            placeholder="E.g., 'What are common credit card complaints?' or 'mortgage application problems'",
            value=st.session_state.get('quick_query', ''),
            key="search_input",
            label_visibility="collapsed"
        )
        
        # Search button row
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            search_clicked = st.button("🚀 Search Database", type="primary", use_container_width=True)
        
        # Process search
        if search_clicked or 'quick_query' in st.session_state:
            if query_input:
                # Clear quick query flag
                if 'quick_query' in st.session_state:
                    query_input = st.session_state.quick_query
                    del st.session_state.quick_query
                
                if not st.session_state.db_initialized:
                    st.error("⚠️ Please connect to database first using the sidebar!")
                    st.info("Click the '🚀 Connect to Database' button in the sidebar")
                else:
                    with st.spinner("🔍 Searching database..."):
                        # Add progress bar
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                        
                        # Perform search
                        start_time = time.time()
                        results = st.session_state.db_manager.search(query_input)
                        search_time = time.time() - start_time
                        
                        progress_bar.empty()
                        
                        if results:
                            results['search_time'] = search_time
                            st.session_state.search_results = results
                            
                            # Add to history
                            st.session_state.query_history.append({
                                "query": query_input,
                                "time": search_time,
                                "timestamp": datetime.now().strftime("%H:%M:%S")
                            })
        
        # Display results
        if st.session_state.search_results:
            results = st.session_state.search_results
            
            # Statistics cards
            st.markdown("---")
            st.markdown("### 📊 Search Statistics")
            
            col_stats = st.columns(4)
            with col_stats[0]:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{results['count']}</div>
                    <div class="stat-label">Results Found</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_stats[1]:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{results['search_time']:.2f}s</div>
                    <div class="stat-label">Search Time</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_stats[2]:
                # Calculate average relevance
                if results['distances']:
                    avg_distance = sum(results['distances']) / len(results['distances'])
                    avg_relevance = 100 - (avg_distance * 100)
                else:
                    avg_relevance = 100
                
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{avg_relevance:.0f}%</div>
                    <div class="stat-label">Avg Relevance</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_stats[3]:
                # Count unique products
                products = set()
                for meta in results['metadatas']:
                    if meta and 'product' in meta:
                        products.add(meta['product'])
                
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{len(products)}</div>
                    <div class="stat-label">Products</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Display results
            st.markdown("---")
            st.markdown(f"### 📋 Results for: *'{results['query']}'*")
            
            for i, (doc, meta, dist) in enumerate(zip(
                results['documents'],
                results['metadatas'],
                results['distances']
            )):
                display_result_card(i, doc, meta, dist)
            
            # Export options
            st.markdown("---")
            st.markdown("### 💾 Export Results")
            col_exp1, col_exp2 = st.columns(2)
            
            with col_exp1:
                if st.button("📥 Download as JSON", use_container_width=True):
                    # Create JSON data
                    json_data = {
                        "query": results['query'],
                        "search_time": results['search_time'],
                        "total_results": results['count'],
                        "results": []
                    }
                    
                    for i, (doc, meta, dist) in enumerate(zip(
                        results['documents'],
                        results['metadatas'],
                        results['distances']
                    )):
                        json_data["results"].append({
                            "id": i + 1,
                            "relevance": 100 - (dist * 100) if dist else 100,
                            "document": doc,
                            "metadata": meta
                        })
                    
                    # Convert to JSON string
                    json_str = json.dumps(json_data, indent=2)
                    st.download_button(
                        label="Click to download",
                        data=json_str,
                        file_name=f"complaint_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            
            with col_exp2:
                if st.button("🔄 New Search", use_container_width=True):
                    st.session_state.search_results = None
                    st.rerun()
        
        else:
            # Empty state
            st.markdown("---")
            if not st.session_state.db_initialized:
                st.markdown("""
                <div style="text-align: center; padding: 4rem; background: #f8fafc; border-radius: 15px; border: 2px dashed #e2e8f0;">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">🔧</div>
                    <h3 style="color: #475569;">Database Connection Required</h3>
                    <p style="color: #64748b;">Please connect to the database using the sidebar to start searching</p>
                    <p style="color: #64748b; font-size: 0.9rem; margin-top: 2rem;">
                        Click the <strong>"🚀 Connect to Database"</strong> button in the sidebar
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 4rem; background: #f8fafc; border-radius: 15px; border: 2px dashed #e2e8f0;">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">🔍</div>
                    <h3 style="color: #475569;">Ready to Search</h3>
                    <p style="color: #64748b;">Enter a query above to search through financial complaints database</p>
                    <p style="color: #64748b; font-size: 0.9rem; margin-top: 2rem;">
                        Try: <strong>"credit card fraud"</strong> or <strong>"mortgage delays"</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    with col_info:
        st.markdown("### 💡 Tips")
        st.info("""
        **Search effectively:**
        
        1. Be specific about products
        2. Mention specific issues
        3. Use financial keywords
        4. Try different variations
        
        **Example queries:**
        - "credit card unauthorized charges"
        - "mortgage application problems"
        - "bank fee complaints"
        - "loan approval issues"
        """)
        
        st.markdown("---")
        st.markdown("### 📈 About")
        st.caption("""
        This system analyzes consumer financial complaints to provide actionable insights.
        
        **Features:**
        • Real-time semantic search
        • Relevance scoring
        • Metadata filtering
        • Export capabilities
        
        **Data:** Sample financial complaints
        **Version:** 1.0
        """)

# Run the app
if __name__ == "__main__":
    main()