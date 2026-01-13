# app_final_clean.py - Fixed all warnings
import streamlit as st
import chromadb
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Financial Complaints Analyzer",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Main container */
    .main-container {
        padding: 2rem;
    }
    
    /* Header styling */
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
    
    /* Search box */
    .stTextInput > div > div > input {
        border-radius: 25px;
        padding: 15px 20px;
        font-size: 16px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Cards for results */
    .result-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
        transition: all 0.3s;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .result-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    
    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #f0f0f0;
    }
    
    .result-number {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    /* Stats cards */
    .stat-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Tag styling */
    .tag {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 2px;
        font-weight: 500;
    }
    
    /* Sidebar styling */
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        color: #888;
        font-size: 0.9rem;
        border-top: 1px solid #e0e0e0;
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 4rem;
        background: #f8fafc;
        border-radius: 15px;
        border: 2px dashed #e2e8f0;
    }
    
    .empty-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "query_history" not in st.session_state:
    st.session_state.query_history = []
if "current_query" not in st.session_state:
    st.session_state.current_query = None
if "search_results" not in st.session_state:
    st.session_state.search_results = None

# Header section
st.markdown("""
<div class="main-header">
    <div class="main-title">💰 Financial Complaints Analyzer</div>
    <div class="subtitle">AI-powered insights from 5,000+ real consumer complaints</div>
</div>
""", unsafe_allow_html=True)

# Initialize ChromaDB
try:
    @st.cache_resource
    def get_collection():
        client = chromadb.PersistentClient(path="notebooks/vector_store_1768244751")
        return client.get_collection("financial_complaints")
    
    collection = get_collection()
    
    # Main layout
    col_left, col_right = st.columns([3, 1])
    
    with col_left:
        # Search section
        st.markdown("### 🔎 Search Complaints Database")
        
        # Search input with proper label handling
        query = st.text_input(
            "Search complaints",
            placeholder="Type your query here... (e.g., 'credit card payment issues', 'mortgage delays')",
            key="search_input",
            label_visibility="collapsed"
        )
        
        # Search button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            search_clicked = st.button("🚀 Search", use_container_width=True)
        
        # Process search
        if search_clicked or (query and query != st.session_state.get('last_processed_query')):
            if query:
                st.session_state.current_query = query
                st.session_state.last_processed_query = query
                st.session_state.query_history.append({
                    "query": query,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                
                # Show progress
                with st.spinner("🔍 Searching database..."):
                    progress_bar = st.progress(0)
                    
                    # Simulate progress
                    for i in range(100):
                        time.sleep(0.005)
                        progress_bar.progress(i + 1)
                    
                    # Actual search
                    start = time.time()
                    results = collection.query(
                        query_texts=[query],
                        n_results=5,
                        include=["documents", "metadatas", "distances"]
                    )
                    search_time = time.time() - start
                    
                    st.session_state.search_results = {
                        "documents": results['documents'][0],
                        "metadatas": results['metadatas'][0],
                        "distances": results['distances'][0] if results['distances'][0] else [],
                        "time": search_time,
                        "query": query
                    }
                    
                    progress_bar.empty()
        
        # Display results
        if st.session_state.search_results:
            results = st.session_state.search_results
            
            # Stats row
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{len(results['documents'])}</div>
                    <div class="stat-label">Complaints Found</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{results['time']:.2f}s</div>
                    <div class="stat-label">Search Time</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                # Calculate average relevance
                if results['distances']:
                    avg_distance = sum(results['distances']) / len(results['distances'])
                    relevance = 100 - (avg_distance * 100)
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-value">{relevance:.0f}%</div>
                        <div class="stat-label">Avg Relevance</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-value">—</div>
                        <div class="stat-label">Relevance</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("### 📋 Search Results")
            st.caption(f"Query: *'{results['query']}'*")
            
            # Display each result as a card
            for i, (doc, meta, distance) in enumerate(zip(
                results['documents'], 
                results['metadatas'], 
                results['distances'] if results['distances'] else [0] * len(results['documents'])
            )):
                # Calculate relevance percentage
                relevance = 100 - (distance * 100) if distance else 100
                
                # Create card
                with st.container():
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-header">
                            <div class="result-number">{i+1}</div>
                            <div style="font-size: 0.9rem; color: {'#10b981' if relevance > 70 else '#f59e0b' if relevance > 40 else '#ef4444'}; font-weight: 600;">
                                {relevance:.0f}% relevant
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Document content
                    st.write(doc)
                    
                    # Metadata tags
                    if meta:
                        tag_cols = st.columns(4)
                        meta_displayed = 0
                        
                        if meta.get('product'):
                            with tag_cols[meta_displayed % 4]:
                                st.markdown(f'<span class="tag">📊 {meta["product"]}</span>', unsafe_allow_html=True)
                            meta_displayed += 1
                        
                        if meta.get('issue'):
                            with tag_cols[meta_displayed % 4]:
                                st.markdown(f'<span class="tag">⚠️ {meta["issue"]}</span>', unsafe_allow_html=True)
                            meta_displayed += 1
                        
                        if meta.get('company'):
                            with tag_cols[meta_displayed % 4]:
                                st.markdown(f'<span class="tag">🏢 {meta["company"]}</span>', unsafe_allow_html=True)
                            meta_displayed += 1
                        
                        if meta.get('state'):
                            with tag_cols[meta_displayed % 4]:
                                st.markdown(f'<span class="tag">📍 {meta["state"]}</span>', unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # Quick actions
            st.markdown("---")
            st.markdown("### 💡 Quick Actions")
            action_cols = st.columns(4)
            
            with action_cols[0]:
                if st.button("📥 Export", use_container_width=True):
                    st.toast("Export feature coming soon! 🚀")
            
            with action_cols[1]:
                if st.button("🔄 New Search", use_container_width=True):
                    st.session_state.current_query = None
                    st.session_state.search_results = None
                    st.session_state.last_processed_query = None
                    st.rerun()
            
            with action_cols[2]:
                if st.button("📊 Analytics", use_container_width=True):
                    st.toast("Analytics dashboard coming soon! 📈")
            
            with action_cols[3]:
                if st.button("📈 Trends", use_container_width=True):
                    st.toast("Trend analysis coming soon! 🔍")
        
        else:
            # Show placeholder when no search
            st.markdown("---")
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">🔍</div>
                <h3 style="color: #475569;">Ready to Search</h3>
                <p style="color: #64748b;">Enter a query above to search through 5,000+ financial complaints</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col_right:
        # Sidebar content
        st.markdown('<div class="sidebar-header">📊 Dashboard</div>', unsafe_allow_html=True)
        
        # Database stats
        st.metric("Total Complaints", f"{collection.count():,}")
        st.metric("Search Speed", "< 0.5s", delta="Fast")
        
        st.markdown("---")
        
        # Recent searches
        st.markdown("**📝 Recent Searches**")
        if st.session_state.query_history:
            for i, search in enumerate(reversed(st.session_state.query_history[-5:])):
                with st.container():
                    st.caption(f"**{search['query'][:25]}...**")
                    st.caption(f"_{search['timestamp']}_")
                    st.markdown("---")
        else:
            st.caption("No searches yet")
        
        st.markdown("---")
        
        # Quick search suggestions
        st.markdown("**⚡ Quick Searches**")
        
        quick_searches = [
            ("💳 Credit Card Fees", "credit card hidden fees"),
            ("🏠 Mortgage Delays", "mortgage processing delays"),
            ("💰 Loan Issues", "personal loan problems"),
            ("👥 Customer Service", "poor bank customer service"),
            ("💸 Unauthorized Charges", "unauthorized transactions"),
            ("📄 Billing Errors", "billing statement errors")
        ]
        
        for label, search_term in quick_searches:
            if st.button(label, key=f"quick_{search_term}", use_container_width=True):
                st.session_state.current_query = search_term
                st.rerun()
        
        st.markdown("---")
        
        # Tips
        st.markdown("**💡 Search Tips**")
        st.info("""
        • Use specific financial terms
        • Include product names
        • Mention specific issues
        • Try different keywords
        """)
        
        # Info
        st.markdown("---")
        st.markdown("**ℹ️ About**")
        st.caption("""
        This system analyzes consumer financial complaints from regulatory databases.
        
        **Data Source:** CFPB Complaints
        **Total Records:** 5,000+
        **Last Updated:** Recent
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        Financial Complaints Analyzer • Powered by ChromaDB & Streamlit • Real-time search and analysis
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    # Error handling with modern UI
    st.error("### ⚠️ System Error")
    st.error(f"**Details:** {str(e)}")
    
    # Show troubleshooting tips
    with st.expander("🛠️ Troubleshooting Tips"):
        st.markdown("""
        1. **Check if vector store exists:**
           ```bash
           ls notebooks/vector_store_1768244751/
           ```
        
        2. **Verify collection name:**
           ```python
           import chromadb
           client = chromadb.PersistentClient(path="notebooks/vector_store_1768244751")
           print([c.name for c in client.list_collections()])
           ```
        
        3. **Reinstall dependencies:**
           ```bash
           pip install chromadb --upgrade
           ```
        """)
    
    # Fallback UI
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #fdfcfb 0%, #f8f9fa 100%); border-radius: 15px;">
        <div style="font-size: 5rem; margin-bottom: 1rem;">🔧</div>
        <h3 style="color: #475569;">System Maintenance</h3>
        <p style="color: #64748b;">We're experiencing technical difficulties. Please try again shortly.</p>
    </div>
    """, unsafe_allow_html=True)

# Add a simple JavaScript to hide Streamlit elements (optional)
st.markdown("""
<script>
// Hide Streamlit branding
const hideStreamlitStyle = `
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
`
const style = document.createElement('style');
style.textContent = hideStreamlitStyle;
document.head.appendChild(style);
</script>
""", unsafe_allow_html=True)