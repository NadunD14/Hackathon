"""
Theft Detection Module
Detects scan avoidance, barcode switching, and weight discrepancies
"""

import logging
from typing import Dict, List, Any


class TheftDetector:
    """Detects potential theft incidents at self-checkout"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('sentinel.theft_detector')
        self.weight_tolerance = 0.05  # 5% tolerance
    
    def detect(self, synchronized_data: List[Dict]) -> List[Dict]:
        """Detect all types of theft incidents"""
        events = []
        
        for window in synchronized_data:
            # Detect scan avoidance
            scan_avoidance = self._detect_scan_avoidance(window)
            if scan_avoidance:
                events.append(scan_avoidance)
            
            # Detect barcode switching
            barcode_switch = self._detect_barcode_switching(window)
            if barcode_switch:
                events.append(barcode_switch)
            
            # Detect weight discrepancies
            weight_issues = self._detect_weight_discrepancy(window)
            if weight_issues:
                events.append(weight_issues)
        
        return events
    
    # @algorithm Scan Avoidance Detection | Detects items in scan area not scanned at POS
    def _detect_scan_avoidance(self, window: Dict) -> Dict:
        """
        Detect scan avoidance by comparing RFID readings with POS transactions
        If RFID detects items in scan area but no POS transaction occurs
        """
        rfid_events = window.get('rfid_events', [])
        pos_events = window.get('pos_events', [])
        
        # Get SKUs detected by RFID in scan area
        rfid_skus = set()
        for event in rfid_events:
            if event.get('status') == 'Active' and event.get('data'):
                if event['data'].get('location') == 'IN_SCAN_AREA':
                    rfid_skus.add(event['data'].get('sku'))
        
        # Get SKUs scanned at POS
        pos_skus = set()
        for event in pos_events:
            if event.get('status') == 'Active' and event.get('data'):
                pos_skus.add(event['data'].get('sku'))
        
        # Find items in scan area but not scanned
        unscanned = rfid_skus - pos_skus
        
        if unscanned:
            return {
                'event_type': 'SCAN_AVOIDANCE',
                'timestamp': window['timestamp'],
                'station_id': window['station_id'],
                'severity': 'HIGH',
                'details': {
                    'unscanned_skus': list(unscanned),
                    'rfid_count': len(rfid_skus),
                    'pos_count': len(pos_skus)
                }
            }
        
        return None
    
    # @algorithm Barcode Switching Detection | Detects mismatched SKUs between systems
    def _detect_barcode_switching(self, window: Dict) -> Dict:
        """
        Detect barcode switching by comparing product recognition with POS data
        If recognized product doesn't match scanned product
        """
        recognition_events = window.get('recognition_events', [])
        pos_events = window.get('pos_events', [])
        
        if not recognition_events or not pos_events:
            return None
        
        # Get recognized products
        recognized_skus = []
        for event in recognition_events:
            if event.get('status') == 'Active' and event.get('data'):
                if event['data'].get('accuracy', 0) > 0.8:  # High confidence only
                    recognized_skus.append(event['data'].get('predicted_product'))
        
        # Get scanned products
        scanned_skus = []
        for event in pos_events:
            if event.get('status') == 'Active' and event.get('data'):
                scanned_skus.append(event['data'].get('sku'))
        
        # Check for mismatches
        if recognized_skus and scanned_skus:
            mismatches = set(recognized_skus) - set(scanned_skus)
            if mismatches:
                return {
                    'event_type': 'BARCODE_SWITCHING',
                    'timestamp': window['timestamp'],
                    'station_id': window['station_id'],
                    'severity': 'HIGH',
                    'details': {
                        'recognized_skus': recognized_skus,
                        'scanned_skus': scanned_skus,
                        'potential_switches': list(mismatches)
                    }
                }
        
        return None
    
    # @algorithm Weight Discrepancy Detection | Compares expected vs actual weight
    def _detect_weight_discrepancy(self, window: Dict) -> Dict:
        """
        Detect weight discrepancies between scanned items and scale readings
        """
        pos_events = window.get('pos_events', [])
        
        if not pos_events:
            return None
        
        for event in pos_events:
            if event.get('status') == 'Active' and event.get('data'):
                data = event['data']
                expected_weight = data.get('weight_g', 0)
                
                # In real scenario, we'd compare with scale reading
                # For now, we'll flag if weight seems suspicious
                if expected_weight == 0:
                    return {
                        'event_type': 'WEIGHT_DISCREPANCY',
                        'timestamp': window['timestamp'],
                        'station_id': window['station_id'],
                        'severity': 'MEDIUM',
                        'details': {
                            'sku': data.get('sku'),
                            'expected_weight': expected_weight,
                            'issue': 'Zero weight detected'
                        }
                    }
        
        return None
