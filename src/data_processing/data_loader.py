"""
Data Loader Module
Loads data from various sources (JSONL, CSV)
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
import logging


class DataLoader:
    """Loads and parses data from multiple sources"""
    
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self.logger = logging.getLogger('sentinel.data_loader')
        
    def load_all(self) -> Dict[str, Any]:
        """Load all data sources"""
        data = {}
        
        try:
            # Load JSONL files
            data['rfid'] = self.load_jsonl('rfid_readings.jsonl')
            data['queue'] = self.load_jsonl('queue_monitoring.jsonl')
            data['pos'] = self.load_jsonl('pos_transactions.jsonl')
            data['product_recognition'] = self.load_jsonl('product_recognition.jsonl')
            data['inventory'] = self.load_jsonl('inventory_snapshots.jsonl')
            
            # Load CSV files
            data['products'] = self.load_csv('products_list.csv')
            data['customers'] = self.load_csv('customer_data.csv')
            
            self.logger.info(f"Successfully loaded all data sources")
            return data
            
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
            raise
    
    def load_jsonl(self, filename: str) -> List[Dict]:
        """Load JSONL file"""
        file_path = self.data_path / filename
        
        if not file_path.exists():
            self.logger.warning(f"File not found: {file_path}")
            return []
        
        records = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        self.logger.warning(f"Skipping invalid JSON line in {filename}: {e}")
        
        self.logger.info(f"Loaded {len(records)} records from {filename}")
        return records
    
    def load_csv(self, filename: str) -> pd.DataFrame:
        """Load CSV file"""
        file_path = self.data_path / filename
        
        if not file_path.exists():
            self.logger.warning(f"File not found: {file_path}")
            return pd.DataFrame()
        
        df = pd.read_csv(file_path)
        self.logger.info(f"Loaded {len(df)} rows from {filename}")
        return df
    
    def get_product_info(self, sku: str, products_df: pd.DataFrame) -> Dict:
        """Get product information by SKU"""
        product = products_df[products_df['SKU'] == sku]
        if not product.empty:
            return product.iloc[0].to_dict()
        return {}
    
    def get_customer_info(self, customer_id: str, customers_df: pd.DataFrame) -> Dict:
        """Get customer information by ID"""
        customer = customers_df[customers_df['Customer_ID'] == customer_id]
        if not customer.empty:
            return customer.iloc[0].to_dict()
        return {}
