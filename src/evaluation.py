"""
Evaluation framework
"""
import pandas as pd
from typing import List, Dict
from src.config import *

class RAGEvaluator:
    """Evaluate RAG system performance"""
    
    def __init__(self, rag_system):
        self.rag = rag_system
        self.test_questions = self._load_test_questions()
    
    def _load_test_questions(self) -> List[Dict]:
        """Load test questions"""
        return [
            {
                "id": 1,
                "question": "What are the main complaints about credit cards?",
                "expected_keywords": ["credit", "card", "fees", "billing", "interest", "charge"],
                "product_filter": "Credit card"
            },
            {
                "id": 2,
                "question": "Why are customers unhappy with money transfers?",
                "expected_keywords": ["transfer", "delay", "fee", "failed", "slow", "money"],
                "product_filter": "Money transfer"
            },
            {
                "id": 3,
                "question": "Compare issues between personal loans and savings accounts",
                "expected_keywords": ["compare", "loan", "savings", "difference", "personal", "account"],
                "product_filter": None
            },
            {
                "id": 4,
                "question": "How many complaints about mortgage processing delays?",
                "expected_keywords": ["mortgage", "delay", "processing", "complaint"],
                "product_filter": "Mortgage"
            }
        ]
    
    def run_evaluation(self) -> pd.DataFrame:
        """Run evaluation"""
        print("🧪 Running RAG Evaluation...")
        print("=" * 60)
        
        results = []
        for q in self.test_questions:
            try:
                response = self.rag.ask(
                    q["question"],
                    product_filter=q.get("product_filter")
                )
                
                # Extract answer text from business_insights
                answer_text = ""
                if "business_insights" in response:
                    insights = response["business_insights"]
                    # Combine executive_summary and key_findings
                    parts = []
                    if "executive_summary" in insights and insights["executive_summary"]:
                        parts.append(insights["executive_summary"])
                    if "key_findings" in insights and insights["key_findings"]:
                        parts.extend([str(f) for f in insights["key_findings"]])
                    answer_text = " ".join(parts)
                
                # Calculate keyword score
                answer_lower = answer_text.lower()
                keyword_hits = sum(1 for kw in q["expected_keywords"] if kw in answer_lower)
                keyword_score = (keyword_hits / len(q["expected_keywords"])) * 5
                
                # Get confidence score
                confidence_score = 50.0  # default
                if "confidence_metrics" in response:
                    if "total_score" in response["confidence_metrics"]:
                        confidence_score = response["confidence_metrics"]["total_score"]
                    elif "level" in response["confidence_metrics"]:
                        level = response["confidence_metrics"]["level"]
                        level_map = {
                            "VERY_HIGH": 90, "HIGH": 75, "MEDIUM": 50,
                            "LOW": 25, "VERY_LOW": 10, "NO_DATA": 0
                        }
                        confidence_score = level_map.get(level, 50)
                
                # Get retrieved count
                retrieved_count = 0
                if "retrieval_stats" in response and "total_complaints" in response["retrieval_stats"]:
                    retrieved_count = response["retrieval_stats"]["total_complaints"]
                elif "confidence_metrics" in response and "retrieved_count" in response["confidence_metrics"]:
                    retrieved_count = response["confidence_metrics"]["retrieved_count"]
                
                # Determine success
                success = retrieved_count > 0 and keyword_score > 2.0
                
                results.append({
                    "question_id": q["id"],
                    "question": q["question"],
                    "confidence": confidence_score,
                    "retrieved": retrieved_count,
                    "keyword_score": round(keyword_score, 2),
                    "success": success
                })
                
                print(f"\n📝 Q{q['id']}: {q['question'][:40]}...")
                print(f"   ✅ Retrieved: {retrieved_count} complaints")
                print(f"   🎯 Confidence: {confidence_score}/100")
                print(f"   📊 Keyword match: {keyword_score:.1f}/5")
                print(f"   📈 Success: {'Yes' if success else 'No'}")
                
            except Exception as e:
                print(f"\n❌ Error evaluating Q{q['id']}: {str(e)}")
                results.append({
                    "question_id": q["id"],
                    "question": q["question"],
                    "confidence": 0,
                    "retrieved": 0,
                    "keyword_score": 0,
                    "success": False
                })
        
        df_results = pd.DataFrame(results)
        
        # Print summary
        print("\n" + "=" * 60)
        print("📈 EVALUATION SUMMARY")
        print("=" * 60)
        print(f"Average Confidence: {df_results['confidence'].mean():.1f}/100")
        print(f"Average Retrieved: {df_results['retrieved'].mean():.1f}")
        print(f"Average Keyword Score: {df_results['keyword_score'].mean():.1f}/5")
        success_rate = (df_results['success'].sum() / len(df_results)) if len(df_results) > 0 else 0
        print(f"Success Rate: {success_rate:.1%}")
        
        return df_results