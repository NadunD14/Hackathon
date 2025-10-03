"""
Configuration Module
Application configuration and constants
"""

from pathlib import Path


class Config:
    """Application configuration"""
    
    # Data Processing
    TIME_WINDOW_SECONDS = 5
    
    # Theft Detection
    WEIGHT_TOLERANCE = 0.05  # 5%
    RECOGNITION_CONFIDENCE_THRESHOLD = 0.8
    
    # Queue Management
    MAX_DWELL_TIME_SECONDS = 180  # 3 minutes
    TARGET_CUSTOMERS_PER_STATION = 6
    MIN_CUSTOMERS_PER_STATION = 3
    MAX_CUSTOMERS_PER_STATION = 10
    
    # Inventory
    INVENTORY_UPDATE_INTERVAL = 600  # 10 minutes
    SHRINKAGE_THRESHOLD = 0.02  # 2%
    
    # Stations
    SELF_CHECKOUT_STATIONS = ['SCC1', 'SCC2', 'SCC3', 'SCC4']
    REGULAR_CHECKOUT_STATIONS = ['RC1']
    ALL_STATIONS = SELF_CHECKOUT_STATIONS + REGULAR_CHECKOUT_STATIONS
    
    # Severity Levels
    SEVERITY_CRITICAL = 'CRITICAL'
    SEVERITY_HIGH = 'HIGH'
    SEVERITY_MEDIUM = 'MEDIUM'
    SEVERITY_LOW = 'LOW'
    
    # Event Types
    EVENT_SCAN_AVOIDANCE = 'SCAN_AVOIDANCE'
    EVENT_BARCODE_SWITCHING = 'BARCODE_SWITCHING'
    EVENT_WEIGHT_DISCREPANCY = 'WEIGHT_DISCREPANCY'
    EVENT_SYSTEM_CRASH = 'SYSTEM_CRASH'
    EVENT_SCANNING_ERROR = 'SCANNING_ERROR'
    EVENT_LONG_WAIT_TIME = 'LONG_WAIT_TIME'
    EVENT_STATION_ALLOCATION = 'STATION_ALLOCATION'
    EVENT_INVENTORY_DISCREPANCY = 'INVENTORY_DISCREPANCY'
    EVENT_INVENTORY_SHRINKAGE = 'INVENTORY_SHRINKAGE'
    
    @classmethod
    def get_config_dict(cls) -> dict:
        """Get all configuration as dictionary"""
        return {
            key: value
            for key, value in cls.__dict__.items()
            if not key.startswith('_') and not callable(value)
        }
