"""
Unit Tests for Analytics Module
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from analytics.theft_detector import TheftDetector
from analytics.anomaly_detector import AnomalyDetector
from analytics.queue_optimizer import QueueOptimizer
from analytics.inventory_tracker import InventoryTracker
from utils.config import Config


class TestTheftDetector(unittest.TestCase):
    """Test TheftDetector functionality"""
    
    def setUp(self):
        self.config = Config()
        self.detector = TheftDetector(self.config)
    
    def test_detector_initialization(self):
        """Test detector can be initialized"""
        self.assertIsNotNone(self.detector)
    
    def test_detect_empty_data(self):
        """Test detection with empty data"""
        result = self.detector.detect([])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)


class TestAnomalyDetector(unittest.TestCase):
    """Test AnomalyDetector functionality"""
    
    def setUp(self):
        self.config = Config()
        self.detector = AnomalyDetector(self.config)
    
    def test_detector_initialization(self):
        """Test detector can be initialized"""
        self.assertIsNotNone(self.detector)


class TestQueueOptimizer(unittest.TestCase):
    """Test QueueOptimizer functionality"""
    
    def setUp(self):
        self.config = Config()
        self.optimizer = QueueOptimizer(self.config)
    
    def test_optimizer_initialization(self):
        """Test optimizer can be initialized"""
        self.assertIsNotNone(self.optimizer)


class TestInventoryTracker(unittest.TestCase):
    """Test InventoryTracker functionality"""
    
    def setUp(self):
        self.config = Config()
        self.tracker = InventoryTracker(self.config)
    
    def test_tracker_initialization(self):
        """Test tracker can be initialized"""
        self.assertIsNotNone(self.tracker)


if __name__ == '__main__':
    unittest.main()
