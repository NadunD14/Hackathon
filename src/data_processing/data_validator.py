"""
Data Validator Module
Validates data integrity and handles missing/corrupt data
"""

import logging
from typing import Dict, List, Any, Tuple


class DataValidator:
    """Validates data integrity and quality"""
    
    def __init__(self):
        self.logger = logging.getLogger('sentinel.validator')
    
    def validate_rfid_record(self, record: Dict) -> Tuple[bool, str]:
        """Validate RFID data record"""
        required_fields = ['timestamp', 'station_id', 'status']
        
        for field in required_fields:
            if field not in record:
                return False, f"Missing required field: {field}"
        
        if record['status'] == 'Active':
            if 'data' not in record:
                return False, "Active status requires data field"
            
            data_fields = ['epc', 'sku', 'location']
            for field in data_fields:
                if field not in record['data']:
                    return False, f"Missing data field: {field}"
        
        return True, "Valid"
    
    def validate_pos_record(self, record: Dict) -> Tuple[bool, str]:
        """Validate POS transaction record"""
        required_fields = ['timestamp', 'station_id', 'status']
        
        for field in required_fields:
            if field not in record:
                return False, f"Missing required field: {field}"
        
        if record['status'] == 'Active':
            if 'data' not in record:
                return False, "Active status requires data field"
            
            data_fields = ['customer_id', 'sku', 'price', 'weight_g']
            for field in data_fields:
                if field not in record['data']:
                    return False, f"Missing data field: {field}"
        
        return True, "Valid"
    
    def validate_queue_record(self, record: Dict) -> Tuple[bool, str]:
        """Validate queue monitoring record"""
        required_fields = ['timestamp', 'station_id', 'status']
        
        for field in required_fields:
            if field not in record:
                return False, f"Missing required field: {field}"
        
        if record['status'] == 'Active':
            if 'data' not in record:
                return False, "Active status requires data field"
            
            data_fields = ['customer_count', 'average_dwell_time']
            for field in data_fields:
                if field not in record['data']:
                    return False, f"Missing data field: {field}"
        
        return True, "Valid"
    
    def handle_missing_data(self, record: Dict, record_type: str) -> Dict:
        """Handle missing or corrupt data"""
        if record.get('status') == 'Read Error':
            self.logger.warning(f"Read error in {record_type} at {record.get('timestamp')}")
            return self._create_error_placeholder(record, record_type)
        
        return record
    
    def _create_error_placeholder(self, record: Dict, record_type: str) -> Dict:
        """Create placeholder for error records"""
        return {
            'timestamp': record.get('timestamp'),
            'station_id': record.get('station_id'),
            'status': 'Read Error',
            'record_type': record_type,
            'data': None
        }
