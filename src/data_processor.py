"""
Clean, focused data processor for Task 1 EDA
"""
import pandas as pd
import numpy as np
import re
from pathlib import Path

class ComplaintDataProcessor:
    """Simple but effective data processor"""
    
    @staticmethod
    def load_and_clean(filepath: str):
        """Load data and perform essential cleaning"""
        print(f"📦 Loading data from {filepath}")
        
        # Load with optimized types
        df = pd.read_csv(
            filepath, 
            dtype={'Product': 'category', 'State': 'category'},
            parse_dates=['Date received']
        )
        
        print(f"✅ Loaded {len(df):,} records")
        
        # Filter to our products
        target_products = [
            'Credit card', 
            'Payday loan, title loan, or personal loan',
            'Consumer Loan',
            'Money transfer, virtual currency, or money service',
            'Bank account or service'
        ]
        
        filtered = df[df['Product'].isin(target_products)].copy()
        print(f"📊 Filtered to {len(filtered):,} relevant complaints")
        
        # Clean text
        filtered['Cleaned_Narrative'] = filtered['Consumer complaint narrative'].apply(
            ComplaintDataProcessor.clean_text
        )
        
        # Remove empty narratives
        filtered = filtered[filtered['Cleaned_Narrative'].str.len() > 10]
        
        print(f"🎯 Final dataset: {len(filtered):,} clean complaints")
        return filtered
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean complaint text"""
        if pd.isna(text):
            return ""
        
        # Basic cleaning
        text = text.lower()
        text = re.sub(r'[^\w\s.,!?]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @staticmethod
    def generate_report(df: pd.DataFrame, output_dir: str = "reports"):
        """Generate executive report"""
        Path(output_dir).mkdir(exist_ok=True)
        
        # Basic statistics
        stats = {
            'total_complaints': len(df),
            'unique_products': df['Product'].nunique(),
            'avg_words': df['Cleaned_Narrative'].str.split().str.len().mean(),
            'date_range': f"{df['Date received'].min().date()} to {df['Date received'].max().date()}"
        }
        
        # Save summary
        with open(f"{output_dir}/summary.txt", 'w') as f:
            f.write("EXECUTIVE SUMMARY\n")
            f.write("="*50 + "\n")
            for key, value in stats.items():
                f.write(f"{key}: {value}\n")
        
        print(f"📄 Report saved to {output_dir}/")
        return stats