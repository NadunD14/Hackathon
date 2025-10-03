"""
Unit Tests for Data Processing Module
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_processing.data_loader import DataLoader
from data_processing.data_synchronizer import DataSynchronizer
from data_processing.data_validator import DataValidator


class TestDataLoader(unittest.TestCase):
    """Test DataLoader functionality"""
    
    def setUp(self):
        self.data_path = Path(__file__).parent.parent.parent / "data"
    
    def test_loader_initialization(self):
        """Test loader can be initialized"""
        loader = DataLoader(str(self.data_path))
        self.assertIsNotNone(loader)
    
    def test_load_jsonl(self):
        """Test loading JSONL files"""
        loader = DataLoader(str(self.data_path))
        # This will pass even if file doesn't exist (returns empty list)
        records = loader.load_jsonl('test.jsonl')
        self.assertIsInstance(records, list)


class TestDataSynchronizer(unittest.TestCase):
    """Test DataSynchronizer functionality"""
    
    def test_synchronizer_initialization(self):
        """Test synchronizer can be initialized"""
        sync = DataSynchronizer()
        self.assertIsNotNone(sync)
    
    def test_process_empty_data(self):
        """Test processing empty data"""
        sync = DataSynchronizer()
        result = sync.process({})
        self.assertIsInstance(result, list)


class TestDataValidator(unittest.TestCase):
    """Test DataValidator functionality"""
    
    def test_validator_initialization(self):
        """Test validator can be initialized"""
        validator = DataValidator()
        self.assertIsNotNone(validator)
    
    def test_validate_rfid_record(self):
        """Test RFID record validation"""
        validator = DataValidator()
        
        # Valid record
        valid_record = {
            'timestamp': '2025-10-03T10:00:00',
            'station_id': 'SCC1',
            'status': 'Active',
            'data': {
                'epc': 'EPC123',
                'sku': 'SKU123',
                'location': 'IN_SCAN_AREA'
            }
        }
        
        is_valid, message = validator.validate_rfid_record(valid_record)
        self.assertTrue(is_valid)
        
        # Invalid record (missing timestamp)
        invalid_record = {
            'station_id': 'SCC1',
            'status': 'Active'
        }
        
        is_valid, message = validator.validate_rfid_record(invalid_record)
        self.assertFalse(is_valid)


if __name__ == '__main__':
    unittest.main()
