"""
UI components and styling for the Gradio interface
"""
import gradio as gr
from typing import Dict, List
from config import COLORS

class UIComponents:
    """Reusable UI components for the application"""
    
    @staticmethod
    def get_css() -> str:
        """Return custom CSS for styling"""
        return f"""
        /* Modern CSS styling */
        .gradio-container {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        
        /* Header styling */
        .header {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }}
        
        /* Card styling */
        .card {{
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 1px solid #e5e7eb;
        }}
        
        /* Source cards */
        .source-card {{
            background: #f9fafb;
            border-left: 4px solid {COLORS['primary']};
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 4px;
        }}
        
        /* Stats badges */
        .stat-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 500;
            margin-right: 0.5rem;
        }}
        
        /* Button styling */
        button {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }}
        
        /* Status indicators */
        .status-good {{ color: {COLORS['high']}; }}
        .status-warning {{ color: {COLORS['medium']}; }}
        .status-error {{ color: {COLORS['low']}; }}
        """
    
    @staticmethod
    def create_header() -> gr.HTML:
        """Create the main header"""
        return gr.HTML("""
        <div class="header">
            <h1 style="margin: 0; font-size: 2.5rem;">🔍 Financial Complaints Analyst</h1>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
                AI-powered analysis of financial customer complaints
            </p>
            <div style="margin-top: 1rem; display: flex; justify-content: center; gap: 1rem;">
                <span style="background: rgba(255,255,255,0.2); padding: 0.25rem 0.75rem; border-radius: 9999px;">
                    📊 Business Intelligence
                </span>
                <span style="background: rgba(255,255,255,0.2); padding: 0.25rem 0.75rem; border-radius: 9999px;">
                    🎯 Confidence Scoring
                </span>
                <span style="background: rgba(255,255,255,0.2); padding: 0.25rem 0.75rem; border-radius: 9999px;">
                    📚 Source Attribution
                </span>
            </div>
        </div>
        """)
    
    @staticmethod
    def create_features_panel() -> gr.HTML:
        """Create features panel"""
        return gr.HTML("""
        <div class="card">
            <h3 style="margin-top: 0;">🎯 Features</h3>
            <ul style="margin: 0; padding-left: 1.25rem;">
                <li>Real-time complaint analysis</li>
                <li>Confidence scoring system</li>
                <li>Source attribution & evidence</li>
                <li>Product-specific filtering</li>
                <li>Business intelligence insights</li>
            </ul>
        </div>
        """)
    
    @staticmethod
    def create_sample_questions() -> gr.Accordion:
        """Create sample questions accordion"""
        with gr.Accordion("💡 Sample Questions", open=True) as accordion:
            gr.HTML("""
            <div style="padding: 1rem 0;">
                <p><strong>Product Analysis:</strong></p>
                <ul style="margin: 0.5rem 0; padding-left: 1.25rem;">
                    <li>What are common credit card fraud issues?</li>
                    <li>How do customers complain about loan fees?</li>
                    <li>What savings account problems exist?</li>
                </ul>
                
                <p><strong>Trend Analysis:</strong></p>
                <ul style="margin: 0.5rem 0; padding-left: 1.25rem;">
                    <li>What are trending complaint topics?</li>
                    <li>Compare complaints between products</li>
                    <li>What urgent issues need attention?</li>
                </ul>
            </div>
            """)
        return accordion
    
    @staticmethod
    def format_response(response: Dict) -> str:
        """Format RAG response for HTML display"""
        answer = response["answer"]
        confidence = response["confidence"]
        confidence_level = response["confidence_level"]
        sources = response["sources"]
        stats = response["stats"]
        
        # Get confidence color
        confidence_color = UIComponents.get_confidence_color(confidence)
        
        # Build HTML response
        html = f"""
        <div class="card">
            <h3 style="margin-top: 0;">📊 Analysis Results</h3>
            
            <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
                <div class="stat-badge" style="background: #dbeafe; color: #1d4ed8;">
                    🔍 {stats['total_complaints']} Complaints
                </div>
                <div class="stat-badge" style="background: #dcfce7; color: #166534;">
                    📈 {stats['products_covered']} Products
                </div>
                <div class="stat-badge" style="background: #fef3c7; color: #92400e;">
                    📝 {stats['issues_identified']} Issues
                </div>
                <div class="stat-badge" style="background: {confidence_color}20; color: {confidence_color};">
                    🎯 {confidence_level} ({confidence:.1f}%)
                </div>
            </div>
            
            {answer}
        </div>
        """
        
        # Add sources if available
        if sources:
            html += "<h3>📚 Source Evidence</h3>"
            for source in sources:
                html += f"""
                <div class="source-card">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <strong>#{source['id']} - {source['product']}</strong>
                        <small style="color: #6b7280;">{source['company']}</small>
                    </div>
                    <div style="color: #4b5563; font-size: 0.9rem;">{source['text']}</div>
                    <div style="margin-top: 0.5rem;">
                        <span style="background: #e5e7eb; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">
                            Issue: {source['issue']}
                        </span>
                    </div>
                </div>
                """
        
        return html
    
    @staticmethod
    def get_confidence_color(score: float) -> str:
        """Get color based on confidence score"""
        if score >= 70:
            return COLORS["high"]    # Green
        elif score >= 40:
            return COLORS["medium"]  # Yellow
        else:
            return COLORS["low"]     # Red
    
    @staticmethod
    def format_system_stats(rag_system, query_history: List) -> str:
        """Format system statistics for display"""
        count = rag_system.get_document_count()
        
        if rag_system.connected:
            status = "✅ Connected"
            status_class = "status-good"
        else:
            status = "⚠️ Not Connected"
            status_class = "status-warning"
        
        return f"""
        <div class="card">
            <h3>📊 System Statistics</h3>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
                <div style="text-align: center;">
                    <div style="font-size: 2rem; font-weight: bold; color: {COLORS['primary']};">{count:,}</div>
                    <div style="color: #6b7280;">Complaint Chunks</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem; font-weight: bold; color: {COLORS['high']};">5</div>
                    <div style="color: #6b7280;">Retrieval Limit</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem; font-weight: bold; color: {COLORS['medium']};">{len(query_history)}</div>
                    <div style="color: #6b7280;">Recent Queries</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem; font-weight: bold; color: #8b5cf6;">100%</div>
                    <div style="color: #6b7280;">Source Attribution</div>
                </div>
            </div>
            <div style="margin-top: 1rem; padding: 1rem; background: #f9fafb; border-radius: 6px;">
                <strong>System Status:</strong> <span class="{status_class}">{status}</span>
                <div style="margin-top: 0.5rem; font-size: 0.9rem; color: #6b7280;">
                    Vector Store: {'Available' if rag_system.connected else 'Not found'}
                </div>
            </div>
        </div>
        """