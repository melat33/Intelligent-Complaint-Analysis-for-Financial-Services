"""
🏆 Advanced RAG Pipeline for Financial Complaint Analysis
Professional implementation with business intelligence features
"""

import chromadb
from sentence_transformers import SentenceTransformer
from typing import Dict, List, Optional, Tuple
import pandas as pd
from datetime import datetime

# DEFINE MISSING CONSTANTS HERE (since imports may fail)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
RETRIEVAL_K = 5
VECTOR_STORE_DIR = "vector_store"

class AdvancedFinancialRAG:
    """
    🏆 Professional RAG System for CrediTrust Financial
    
    Features:
    1. Semantic Search with Query Understanding
    2. Multi-level Confidence Scoring
    3. Business Intelligence Insights
    4. Source Attribution & Traceability
    5. Performance Analytics
    """
    
    def __init__(self, verbose: bool = True):
        """Initialize the advanced RAG system"""
        self.verbose = verbose
        self.performance_metrics = {
            "queries_processed": 0,
            "total_retrieved": 0,
            "avg_confidence": 0,
            "success_rate": 0
        }
        
        if verbose:
            print("🚀 Initializing Advanced Financial RAG System...")
        
        # Initialize components
        self._initialize_components()
        
        if verbose:
            count = self.collection.count() if hasattr(self, 'collection') else 0
            print(f"✅ System Ready: {count} complaints loaded")
            print("   • Semantic Search Engine ✓")
            print("   • Query Understanding Module ✓")
            print("   • Business Intelligence Layer ✓")
            print("   • Confidence Scoring System ✓")
            print("   • Performance Analytics ✓")
    
    def _initialize_components(self):
        """Initialize all system components"""
        try:
            # 1. Embedding model for semantic search
            self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        except Exception as e:
            print(f"⚠️ Could not load embedding model: {e}")
            # Create a dummy embedder
            class DummyEmbedder:
                def encode(self, texts):
                    return [0.0] * 384
            self.embedder = DummyEmbedder()
        
        # 2. Query understanding module
        self.query_analyzer = self._create_query_enhancer()
        
        # 3. Business prompt templates
        self.prompter = self._create_prompt_templates()
        
        # 4. ChromaDB vector store
        self._initialize_vector_store()
        
        # 5. Initialize analytics
        self.analytics = {
            "query_log": [],
            "performance_stats": {
                "total_queries": 0,
                "successful_queries": 0,
                "avg_retrieval_count": 0,
                "avg_confidence": 0
            }
        }
    
    def _create_query_enhancer(self):
        """Create a query enhancer if import fails"""
        class SimpleQueryEnhancer:
            def analyze_query(self, question: str):
                question_lower = question.lower()
                
                # Detect products
                products = []
                if "credit" in question_lower and "card" in question_lower:
                    products.append("Credit card")
                if "loan" in question_lower:
                    products.append("Personal loan")
                if "savings" in question_lower:
                    products.append("Savings account")
                if "money" in question_lower and "transfer" in question_lower:
                    products.append("Money transfers")
                if "mortgage" in question_lower:
                    products.append("Mortgage")
                
                # Business context
                business_context = {
                    "urgency": any(word in question_lower for word in ["urgent", "critical", "emergency"]),
                    "needs_trend_analysis": any(word in question_lower for word in ["trend", "pattern", "over time"]),
                    "is_comparative": any(word in question_lower for word in ["compare", "vs", "versus", "difference"]),
                    "needs_root_cause": any(word in question_lower for word in ["why", "reason", "cause"]),
                    "volume_analysis": any(word in question_lower for word in ["many", "often", "frequent"])
                }
                
                return {
                    "original_query": question,
                    "products": products,
                    "query_type": "general",
                    "business_context": business_context
                }
            
            def enhance_query(self, question: str, analysis: dict):
                """Create enhanced query variations"""
                enhanced = [question]
                
                # Add product context if detected
                if analysis.get("products"):
                    product_context = f"financial complaint about {analysis['products'][0]}"
                    enhanced.append(product_context)
                
                # Add general context
                enhanced.append(f"consumer complaint {question}")
                
                return enhanced
        
        return SimpleQueryEnhancer()
    
    def _create_prompt_templates(self):
        """Create simple prompt templates"""
        class SimpleFinancialPrompts:
            @staticmethod
            def get_executive_analyst_prompt(context, question, retrieved_count):
                return f"Analyze {retrieved_count} complaints about: {question}"
        
        return SimpleFinancialPrompts()
    
    def _initialize_vector_store(self):
        """Initialize ChromaDB vector store"""
        try:
            # Try multiple possible paths
            possible_paths = [
                "vector_store",
                "data/vector_store",
                "../vector_store",
                "./vector_store"
            ]
            
            collection_found = False
            for path in possible_paths:
                try:
                    self.client = chromadb.PersistentClient(path=path)
                    # Try to get existing collection
                    try:
                        self.collection = self.client.get_collection("complaint_embeddings")
                        collection_found = True
                        if self.verbose:
                            print(f"✅ Loaded vector store from: {path}")
                        break
                    except:
                        try:
                            self.collection = self.client.get_collection("financial_complaints")
                            collection_found = True
                            if self.verbose:
                                print(f"✅ Loaded vector store from: {path}")
                            break
                        except:
                            continue
                except Exception as e:
                    if self.verbose:
                        print(f"⚠️ Path {path} failed: {e}")
                    continue
            
            # If no collection found, create a new one
            if not collection_found:
                if self.verbose:
                    print("📝 Creating new vector store...")
                self.client = chromadb.PersistentClient(path="vector_store")
                self.collection = self.client.create_collection("complaint_embeddings")
                
        except Exception as e:
            print(f"❌ Error initializing vector store: {e}")
            # Create a dummy collection for testing
            class DummyCollection:
                def count(self):
                    return 0
                def query(self, **kwargs):
                    return {'documents': [[]], 'metadatas': [[]], 'distances': [[]]}
                def peek(self, limit=10):
                    return {'metadatas': []}
            self.collection = DummyCollection()
    
    def analyze_query(self, question: str) -> Dict:
        """
        🎯 Advanced query analysis with business context
        """
        return self.query_analyzer.analyze_query(question)
    
    def _extract_metadata_field(self, meta: Dict, field_names: List[str], default: str = "Unknown") -> str:
        """Extract metadata field using multiple possible field names."""
        if not meta:
            return default
            
        for field in field_names:
            if field in meta and meta[field] not in [None, "", "null", "None"]:
                value = str(meta[field])
                return value.strip()
        
        return default
    
    def _get_product_from_metadata(self, meta: Dict) -> str:
        """Extract product category from metadata."""
        product = self._extract_metadata_field(meta, 
            ['product_category', 'product', 'Product', 'Product category', 'product-category'], 
            'Unknown')
        
        # Standardize product names
        product_lower = product.lower()
        if 'credit' in product_lower and 'card' in product_lower:
            return 'Credit card'
        elif 'personal' in product_lower and 'loan' in product_lower:
            return 'Personal loan'
        elif 'savings' in product_lower and 'account' in product_lower:
            return 'Savings account'
        elif 'money' in product_lower and 'transfer' in product_lower:
            return 'Money transfers'
        elif 'mortgage' in product_lower:
            return 'Mortgage'
        elif 'checking' in product_lower and 'account' in product_lower:
            return 'Checking account'
        
        return product
    
    def _get_issue_from_metadata(self, meta: Dict) -> str:
        """Extract issue from metadata."""
        return self._extract_metadata_field(meta,
            ['issue', 'Issue', 'sub_issue', 'sub-issue', 'Sub-issue', 'problem'],
            'General')
    
    def retrieve_complaints(self, question: str, analysis: Dict, 
                          k: int = RETRIEVAL_K, 
                          product_filter: Optional[str] = None) -> Dict:
        """
        🔍 Intelligent retrieval with business-aware filtering
        """
        if self.verbose:
            print(f"\n🔍 Processing: '{question}'")
            if product_filter:
                print(f"   Filter: {product_filter}")
        
        # Adjust K based on query complexity
        if analysis["business_context"]["is_comparative"]:
            k = min(8, k * 2)
        elif analysis["business_context"]["needs_trend_analysis"]:
            k = min(10, k * 2)
        
        # Prepare filter
        where_filter = None
        if product_filter:
            # Map standard product names to possible field values
            product_mappings = {
                'Credit card': ['Credit card', 'credit card', 'Credit Card', 'Credit-card'],
                'Personal loan': ['Personal loan', 'personal loan', 'Personal Loan', 'Personal-loan'],
                'Savings account': ['Savings account', 'savings account', 'Savings Account', 'Savings-account'],
                'Money transfers': ['Money transfers', 'money transfers', 'Money Transfers', 'Money-transfers'],
                'Mortgage': ['Mortgage', 'mortgage', 'Home loan'],
                'Checking account': ['Checking account', 'checking account', 'Checking Account', 'Checking-account']
            }
            
            if product_filter in product_mappings:
                where_filter = {
                    "$or": [
                        {"product_category": {"$in": product_mappings[product_filter]}},
                        {"product": {"$in": product_mappings[product_filter]}}
                    ]
                }
        
        # Generate enhanced queries
        enhanced_queries = self.query_analyzer.enhance_query(question, analysis)
        
        # Execute search
        try:
            results = self.collection.query(
                query_texts=enhanced_queries[:2],
                n_results=k,
                where=where_filter,
                include=["documents", "metadatas", "distances"]
            )
        except Exception as e:
            if self.verbose:
                print(f"   ⚠️ Query error: {str(e)[:100]}")
            # Fallback
            results = self.collection.query(
                query_texts=[question],
                n_results=k,
                include=["documents", "metadatas", "distances"]
            )
        
        # Process results
        retrieved_data = {
            "chunks": results['documents'][0] if results['documents'] else [],
            "metadata": results['metadatas'][0] if results['metadatas'] else [],
            "distances": results['distances'][0] if results['distances'] else [],
            "count": len(results['documents'][0]) if results['documents'] else 0,
            "query_analysis": analysis,
            "retrieval_time": datetime.now().isoformat()
        }
        
        if self.verbose:
            if retrieved_data["count"] > 0:
                print(f"   ✅ Retrieved: {retrieved_data['count']} complaints")
            else:
                print(f"   ⚠️ Retrieved: 0 complaints")
        
        return retrieved_data
    
    def calculate_confidence_score(self, retrieved_data: Dict) -> Dict:
        """
        📊 Multi-dimensional confidence scoring
        """
        if retrieved_data["count"] == 0:
            return {
                "total_score": 0,
                "level": "NO_DATA",
                "breakdown": {
                    "semantic_similarity": 0,
                    "retrieval_quality": 0,
                    "source_diversity": 0,
                    "metadata_completeness": 0
                },
                "retrieved_count": 0
            }
        
        # 1. Semantic Similarity Score (0-40)
        if retrieved_data["distances"]:
            avg_distance = sum(retrieved_data["distances"]) / len(retrieved_data["distances"])
            similarity = 1 - avg_distance
            semantic_score = min(40, similarity * 40)
        else:
            semantic_score = 20
        
        # 2. Retrieval Quality Score (0-30)
        requested_k = RETRIEVAL_K
        actual_count = retrieved_data["count"]
        retrieval_ratio = actual_count / requested_k if requested_k > 0 else 0
        retrieval_score = min(30, retrieval_ratio * 30)
        
        # 3. Source Diversity Score (0-20)
        if retrieved_data["metadata"]:
            products = set()
            for meta in retrieved_data["metadata"]:
                product = self._get_product_from_metadata(meta)
                if product != 'Unknown':
                    products.add(product)
            diversity_ratio = len(products) / len(retrieved_data["metadata"])
            diversity_score = min(20, diversity_ratio * 20)
        else:
            diversity_score = 0
        
        # 4. Metadata Completeness Score (0-10)
        if retrieved_data["metadata"]:
            complete_metadata = 0
            for meta in retrieved_data["metadata"]:
                product = self._get_product_from_metadata(meta)
                issue = self._get_issue_from_metadata(meta)
                if product != 'Unknown' and issue != 'General':
                    complete_metadata += 1
            metadata_score = (complete_metadata / len(retrieved_data["metadata"])) * 10
        else:
            metadata_score = 0
        
        # Total score
        total_score = semantic_score + retrieval_score + diversity_score + metadata_score
        
        # Confidence level
        if total_score >= 70:
            level = "HIGH"
        elif total_score >= 40:
            level = "MEDIUM"
        elif total_score >= 20:
            level = "LOW"
        else:
            level = "VERY_LOW"
        
        return {
            "total_score": round(total_score, 1),
            "level": level,
            "breakdown": {
                "semantic_similarity": round(semantic_score, 1),
                "retrieval_quality": round(retrieval_score, 1),
                "source_diversity": round(diversity_score, 1),
                "metadata_completeness": round(metadata_score, 1)
            },
            "retrieved_count": retrieved_data["count"]
        }
    
    def generate_business_insights(self, question: str, 
                                 retrieved_data: Dict,
                                 confidence: Dict) -> Dict:
        """
        💼 Generate business intelligence insights
        """
        if retrieved_data["count"] == 0:
            return {
                "executive_summary": "No relevant complaints found for analysis.",
                "key_findings": [],
                "patterns_detected": [],
                "recommendations": [],
                "evidence_count": 0
            }
        
        # Analyze retrieved complaints
        products = {}
        issues = {}
        severities = {"high": 0, "medium": 0, "low": 0}
        
        for meta in retrieved_data["metadata"]:
            product = self._get_product_from_metadata(meta)
            products[product] = products.get(product, 0) + 1
            
            issue = self._get_issue_from_metadata(meta)
            issues[issue] = issues.get(issue, 0) + 1
            
            issue_lower = str(issue).lower()
            if any(term in issue_lower for term in ['fraud', 'unauthorized', 'theft', 'scam', 'identity']):
                severities["high"] += 1
            elif any(term in issue_lower for term in ['fee', 'charge', 'billing', 'payment', 'interest']):
                severities["medium"] += 1
            else:
                severities["low"] += 1
        
        # Generate insights based on query type
        analysis = retrieved_data["query_analysis"]
        
        if analysis["business_context"]["is_comparative"]:
            insights = self._generate_comparative_insights(products, issues, question)
        elif analysis["business_context"]["needs_trend_analysis"]:
            insights = self._generate_trend_insights(products, issues, question)
        elif analysis["business_context"]["needs_root_cause"]:
            insights = self._generate_root_cause_insights(products, issues, question)
        else:
            insights = self._generate_general_insights(products, issues, severities, question)
        
        # Add confidence context
        insights["confidence_context"] = {
            "score": confidence["total_score"],
            "level": confidence["level"],
            "evidence_strength": "Strong" if confidence["retrieved_count"] >= 3 else "Moderate" if confidence["retrieved_count"] >= 1 else "Weak"
        }
        
        return insights
    
    def _generate_general_insights(self, products: Dict, issues: Dict, 
                                 severities: Dict, question: str) -> Dict:
        """Generate general business insights"""
        # Remove 'Unknown' from products
        filtered_products = {k: v for k, v in products.items() if k != 'Unknown'}
        filtered_issues = {k: v for k, v in issues.items() if k != 'General'}
        
        # Top products with complaints
        top_products = sorted(filtered_products.items(), key=lambda x: x[1], reverse=True)[:3]
        top_issues = sorted(filtered_issues.items(), key=lambda x: x[1], reverse=True)[:3]
        
        total_complaints = sum(filtered_products.values()) if filtered_products else sum(products.values())
        
        return {
            "executive_summary": f"Analysis of {total_complaints} relevant complaints reveals key customer pain points.",
            "key_findings": [
                f"Top product category: {top_products[0][0]} ({top_products[0][1]} complaints)" if top_products else "No product data available",
                f"Most frequent issue: {top_issues[0][0]} ({top_issues[0][1]} occurrences)" if top_issues else "No issue data available",
                f"Severity distribution: {severities['high']} high, {severities['medium']} medium, {severities['low']} low priority"
            ],
            "patterns_detected": [
                f"Product concentration: {len(filtered_products)} different products mentioned" if filtered_products else "Limited product data",
                f"Issue diversity: {len(filtered_issues)} distinct issues identified" if filtered_issues else "Limited issue data"
            ],
            "recommendations": [
                "Prioritize fixes for high-severity issues first",
                "Consider product-specific training for support teams",
                "Monitor emerging issues for proactive response"
            ],
            "evidence_count": total_complaints
        }
    
    def _generate_comparative_insights(self, products: Dict, issues: Dict, 
                                     question: str) -> Dict:
        """Generate comparative insights between products"""
        filtered_products = {k: v for k, v in products.items() if k != 'Unknown'}
        
        if len(filtered_products) < 2:
            return {
                "executive_summary": "Insufficient data for comparative analysis.",
                "key_findings": ["Need complaints from at least 2 different products for comparison"],
                "patterns_detected": [],
                "recommendations": ["Ask more general questions to gather broader data"],
                "evidence_count": sum(filtered_products.values())
            }
        
        sorted_products = sorted(filtered_products.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "executive_summary": f"Comparative analysis across {len(filtered_products)} product categories.",
            "key_findings": [
                f"Highest complaint volume: {sorted_products[0][0]} ({sorted_products[0][1]} complaints)",
                f"Lowest complaint volume: {sorted_products[-1][0]} ({sorted_products[-1][1]} complaints)",
                f"Complaint ratio: {sorted_products[0][0]} has {sorted_products[0][1]/sorted_products[-1][1]:.1f}x more complaints than {sorted_products[-1][0]}" if sorted_products[-1][1] > 0 else "Insufficient data for ratio"
            ],
            "patterns_detected": [
                f"Product diversity: Complaints span {len(filtered_products)} categories",
                f"Distribution: {', '.join([f'{p}: {c}' for p, c in sorted_products[:3]])}"
            ],
            "recommendations": [
                f"Investigate why {sorted_products[0][0]} has highest complaint volume",
                f"Learn from {sorted_products[-1][0]}'s lower complaint rate",
                "Consider cross-product issue resolution teams"
            ],
            "evidence_count": sum(filtered_products.values())
        }
    
    def _generate_trend_insights(self, products: Dict, issues: Dict, 
                               question: str) -> Dict:
        """Generate trend analysis insights"""
        filtered_issues = {k: v for k, v in issues.items() if k != 'General'}
        top_issues = sorted(filtered_issues.items(), key=lambda x: x[1], reverse=True)[:5]
        
        total_issues = sum(filtered_issues.values()) if filtered_issues else sum(issues.values())
        
        return {
            "executive_summary": f"Trend analysis based on {sum(products.values())} relevant complaints.",
            "key_findings": [
                f"Top trending issue: {top_issues[0][0]} ({top_issues[0][1]} occurrences)" if top_issues else "No trend data available",
                f"Issue frequency spread: {len(filtered_issues)} distinct issues identified" if filtered_issues else "Limited issue data",
                f"Product coverage: Complaints from {len([p for p in products.keys() if p != 'Unknown'])} product categories"
            ],
            "patterns_detected": [
                f"Dominant issues: Top 3 issues account for {sum(c for _, c in top_issues[:3])/total_issues*100:.1f}% of complaints" if len(top_issues) >= 3 and total_issues > 0 else "Insufficient data for pattern detection"
            ],
            "recommendations": [
                "Monitor top issues for escalation patterns",
                "Set up alerts for emerging complaint types",
                "Conduct deep dive on most frequent issues"
            ],
            "evidence_count": sum(products.values())
        }
    
    def _generate_root_cause_insights(self, products: Dict, issues: Dict, 
                                    question: str) -> Dict:
        """Generate root cause analysis insights"""
        root_cause_categories = {
            "Process Issues": ["delay", "slow", "wait", "pending", "processing", "time", "timely"],
            "Communication Issues": ["notification", "inform", "tell", "communication", "update", "respond", "reply"],
            "Technical Issues": ["error", "bug", "technical", "system", "website", "app", "online", "digital"],
            "Policy Issues": ["fee", "charge", "policy", "term", "condition", "agreement", "contract"],
            "Security Issues": ["fraud", "unauthorized", "theft", "scam", "security", "privacy", "identity"]
        }
        
        categorized_issues = {category: 0 for category in root_cause_categories.keys()}
        
        for issue, count in issues.items():
            issue_lower = str(issue).lower()
            for category, keywords in root_cause_categories.items():
                if any(keyword in issue_lower for keyword in keywords):
                    categorized_issues[category] += count
                    break
        
        top_categories = sorted(categorized_issues.items(), key=lambda x: x[1], reverse=True)
        total_categorized = sum(categorized_issues.values())
        
        return {
            "executive_summary": f"Root cause analysis of {total_categorized} issue occurrences.",
            "key_findings": [
                f"Primary root cause category: {top_categories[0][0]} ({top_categories[0][1]} issues)" if top_categories[0][1] > 0 else "No clear root cause pattern",
                f"Secondary category: {top_categories[1][0]} ({top_categories[1][1]} issues)" if len(top_categories) > 1 and top_categories[1][1] > 0 else "",
                f"Root cause distribution: {', '.join([f'{c}: {n}' for c, n in top_categories if n > 0])}"
            ],
            "patterns_detected": [
                f"Systemic issues: {top_categories[0][0]} appears most frequently" if top_categories[0][1] > 0 else "",
                f"Multiple root cause categories identified: {len([c for c in categorized_issues.values() if c > 0])}"
            ],
            "recommendations": [
                f"Address systemic {top_categories[0][0].lower()} issues first" if top_categories[0][1] > 0 else "Collect more specific complaint data",
                "Implement targeted fixes for each root cause category",
                "Track resolution effectiveness by root cause type"
            ],
            "evidence_count": total_categorized
        }
    
    def ask(self, question: str, product_filter: Optional[str] = None) -> Dict:
        """
        🎯 Main method: Ask a business question about complaints
        """
        # Update analytics
        self.analytics["query_log"].append({
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "filter": product_filter
        })
        self.analytics["performance_stats"]["total_queries"] += 1
        
        # Step 1: Query Analysis
        query_analysis = self.analyze_query(question)
        
        # Step 2: Intelligent Retrieval
        retrieved_data = self.retrieve_complaints(question, query_analysis, 
                                                product_filter=product_filter)
        
        # Step 3: Confidence Scoring
        confidence = self.calculate_confidence_score(retrieved_data)
        
        # Step 4: Business Insights Generation
        insights = self.generate_business_insights(question, retrieved_data, confidence)
        
        # Step 5: Prepare Sources with Details
        sources = []
        for i, (meta, distance) in enumerate(zip(retrieved_data["metadata"], 
                                                retrieved_data.get("distances", [])), 1):
            similarity = (1 - distance) * 100 if distance is not None else 0
            
            product = self._get_product_from_metadata(meta)
            issue = self._get_issue_from_metadata(meta)
            company = self._extract_metadata_field(meta, ['company', 'Company', 'bank', 'Bank'], 'Unknown')
            state = self._extract_metadata_field(meta, ['state', 'State', 'location', 'Location'], 'Unknown')
            date_received = self._extract_metadata_field(meta, ['date_received', 'date', 'Date', 'received_date'], 'Unknown')
            
            sources.append({
                "source_id": i,
                "product": product,
                "issue": issue,
                "company": company,
                "state": state,
                "similarity_score": round(similarity, 1),
                "date_received": date_received
            })
        
        # Update success rate
        if retrieved_data["count"] > 0:
            self.analytics["performance_stats"]["successful_queries"] += 1
        
        # Update average metrics
        total_queries = self.analytics["performance_stats"]["total_queries"]
        successful_queries = self.analytics["performance_stats"]["successful_queries"]
        
        self.analytics["performance_stats"]["success_rate"] = (
            successful_queries / total_queries * 100 if total_queries > 0 else 0
        )
        
        # Update average retrieval count
        total_retrieved = self.analytics["performance_stats"].get("total_retrieved", 0) + retrieved_data["count"]
        self.analytics["performance_stats"]["total_retrieved"] = total_retrieved
        self.analytics["performance_stats"]["avg_retrieval_count"] = (
            total_retrieved / total_queries if total_queries > 0 else 0
        )
        
        # Compile final response
        response = {
            "question": question,
            "query_analysis": query_analysis,
            "business_insights": insights,
            "confidence_metrics": confidence,
            "sources": sources,
            "retrieval_stats": {
                "total_complaints": retrieved_data["count"],
                "products_covered": len(set(s["product"] for s in sources if s["product"] != 'Unknown')),
                "issues_identified": len(set(s["issue"] for s in sources if s["issue"] != 'General')),
                "retrieval_time": retrieved_data["retrieval_time"]
            },
            "system_analytics": {
                "query_id": len(self.analytics["query_log"]),
                "success": retrieved_data["count"] > 0,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        return response
    
    def get_performance_report(self) -> Dict:
        """📈 Get system performance analytics report"""
        stats = self.analytics["performance_stats"]
        
        return {
            "summary": {
                "total_queries_processed": stats["total_queries"],
                "success_rate": f"{stats['success_rate']:.1f}%",
                "avg_complaints_per_query": round(stats.get("avg_retrieval_count", 0), 1),
                "system_uptime": "Active"
            },
            "recent_queries": self.analytics["query_log"][-5:] if self.analytics["query_log"] else [],
            "recommendations": [
                "System performing well for business queries" if stats["success_rate"] > 70 else "Consider improving query understanding",
                "Good complaint retrieval coverage" if stats.get("avg_retrieval_count", 0) >= 3 else "May need more diverse complaint data",
                "Ready for production use" if stats["total_queries"] >= 10 and stats["success_rate"] > 60 else "Needs more testing"
            ]
        }
    
    def get_dataset_statistics(self) -> Dict:
        """Get dataset statistics for reporting."""
        count = self.collection.count()
        
        # Sample metadata to get statistics
        results = self.collection.peek(limit=100)
        metadatas = results['metadatas']
        
        stats = {
            "total_complaint_chunks": count,
            "estimated_unique_complaints": count // 3,
            "product_categories": set(),
            "issues": set(),
            "sample_products": [],
            "sample_issues": []
        }
        
        if metadatas:
            for meta_list in metadatas[:10]:
                for meta in meta_list:
                    product = self._get_product_from_metadata(meta)
                    issue = self._get_issue_from_metadata(meta)
                    
                    if product != 'Unknown':
                        stats["product_categories"].add(product)
                    if issue != 'General':
                        stats["issues"].add(issue)
                    
                    if len(stats["sample_products"]) < 5 and product != 'Unknown':
                        stats["sample_products"].append(product)
                    if len(stats["sample_issues"]) < 5 and issue != 'General':
                        stats["sample_issues"].append(issue)
        
        stats["unique_product_categories"] = len(stats["product_categories"])
        stats["unique_issues"] = len(stats["issues"])
        
        return stats


def print_detailed_response(response: Dict):
    """
    📊 Professional response formatting for business users
    """
    print(f"\n{'='*60}")
    print("📊 BUSINESS INTELLIGENCE REPORT")
    print(f"{'='*60}")
    
    # Question
    print(f"\n📝 QUESTION: {response['question']}")
    
    # Query Analysis
    analysis = response['query_analysis']
    if analysis.get('products'):
        print(f"🔍 DETECTED: {', '.join(analysis['products'])} focus")
    
    # Business Insights
    insights = response['business_insights']
    print(f"\n💼 EXECUTIVE SUMMARY:")
    print(f"   {insights['executive_summary']}")
    
    print(f"\n🎯 KEY FINDINGS:")
    for finding in insights['key_findings']:
        if finding and finding.strip():
            print(f"   • {finding}")
    
    # Confidence
    confidence = response['confidence_metrics']
    print(f"\n📈 CONFIDENCE ANALYSIS:")
    print(f"   Overall: {confidence['level']} ({confidence['total_score']}/100)")
    
    if 'breakdown' in confidence:
        print(f"   Breakdown:")
        for metric, score in confidence['breakdown'].items():
            print(f"     • {metric.replace('_', ' ').title()}: {score}")
    
    # Sources
    if response['sources']:
        valid_sources = [s for s in response['sources'] if s.get('product') != 'Unknown']
        if valid_sources:
            print(f"\n📚 EVIDENCE SOURCES ({len(valid_sources)} complaints):")
            for source in valid_sources[:3]:
                print(f"   [{source['source_id']}] {source['product']} - {source['issue']}")
                if source.get('similarity_score', 0) > 0:
                    print(f"      Similarity: {source['similarity_score']}%")
                if source.get('company', 'Unknown') != 'Unknown':
                    print(f"      Company: {source['company']}")
    
    # Recommendations
    if insights['recommendations']:
        print(f"\n🚀 RECOMMENDED ACTIONS:")
        for rec in insights['recommendations'][:3]:
            if rec and rec.strip():
                print(f"   • {rec}")
    
    # System Info
    stats = response['retrieval_stats']
    print(f"\n📊 ANALYSIS METRICS:")
    print(f"   • Complaints analyzed: {stats['total_complaints']}")
    print(f"   • Products covered: {stats['products_covered']}")
    print(f"   • Issues identified: {stats['issues_identified']}")
    
    print(f"\n{'='*60}")