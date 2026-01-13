"""
Professional prompt templates for business intelligence
"""
from typing import Dict, List

class FinancialPrompts:
    """Business intelligence prompt templates"""
    
    @staticmethod
    def format_business_context(analysis: Dict) -> str:
        """Format business context for prompts"""
        context = f"BUSINESS CONTEXT:\n"
        context += f"- Query Type: {analysis['type'].upper()}\n"
        if analysis['products']:
            context += f"- Products: {', '.join(analysis['products'])}\n"
        context += f"- Intent: {analysis['business_intent']}\n"
        if analysis.get('time_period'):
            context += f"- Time Period: {analysis['time_period']['value']}\n"
        return context
    
    @staticmethod
    def get_executive_analyst_prompt(context: str, question: str, 
                                   retrieved_count: int) -> str:
        """Prompt for executive-level analysis"""
        return f"""You are the Chief Analytics Officer at CrediTrust Financial.

{context}

ANALYSIS REQUEST: {question}

DATA AVAILABLE: {retrieved_count} relevant customer complaints

REQUIRED FORMAT:
1. EXECUTIVE SUMMARY (1-2 sentences)
2. KEY BUSINESS FINDINGS (bullet points with evidence)
3. PATTERNS DETECTED (trends, clusters, anomalies)
4. RISK ASSESSMENT (high/medium/low priority issues)
5. ACTIONABLE RECOMMENDATIONS (specific, measurable)

RULES:
- Base analysis ONLY on available complaint data
- Cite specific complaint patterns when possible
- Focus on business impact and ROI
- Prioritize urgent/critical issues
- Provide measurable recommendations

ANALYSIS:"""