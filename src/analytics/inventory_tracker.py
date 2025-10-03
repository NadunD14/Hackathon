"""
Inventory Tracking Module
Tracks inventory discrepancies and shrinkage
"""

import logging
from typing import Dict, List, Any
from collections import defaultdict


class InventoryTracker:
    """Tracks inventory and detects discrepancies"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('sentinel.inventory_tracker')
        self.shrinkage_threshold = 0.02  # 2% threshold
    
    def track(self, synchronized_data: List[Dict]) -> List[Dict]:
        """Track inventory and detect issues"""
        events = []
        
        # Build expected vs actual inventory
        inventory_state = self._build_inventory_state(synchronized_data)
        
        # Detect discrepancies
        discrepancies = self._detect_discrepancies(inventory_state)
        events.extend(discrepancies)
        
        # Detect shrinkage patterns
        shrinkage = self._detect_shrinkage(inventory_state)
        events.extend(shrinkage)
        
        return events
    
    # @algorithm Inventory Reconciliation | Compares expected vs actual inventory
    def _build_inventory_state(self, synchronized_data: List[Dict]) -> Dict:
        """
        Build inventory state by tracking all transactions and snapshots
        """
        inventory = defaultdict(lambda: {'expected': 0, 'actual': 0, 'transactions': []})
        
        for window in synchronized_data:
            # Process POS transactions (items sold)
            pos_events = window.get('pos_events', [])
            for event in pos_events:
                if event.get('status') == 'Active' and event.get('data'):
                    sku = event['data'].get('sku')
                    if sku:
                        inventory[sku]['transactions'].append({
                            'timestamp': window['timestamp'],
                            'type': 'sale',
                            'station': window['station_id']
                        })
            
            # Process inventory snapshots
            snapshot = window.get('inventory_snapshot', {})
            if snapshot and snapshot.get('data'):
                for sku, quantity in snapshot['data'].items():
                    if isinstance(quantity, (int, float)):
                        inventory[sku]['actual'] = quantity
        
        return dict(inventory)
    
    # @algorithm Discrepancy Detection | Identifies inventory mismatches
    def _detect_discrepancies(self, inventory_state: Dict) -> List[Dict]:
        """
        Detect discrepancies between expected and actual inventory
        """
        events = []
        
        for sku, data in inventory_state.items():
            expected = data.get('expected', 0)
            actual = data.get('actual', 0)
            
            # Check for significant discrepancies
            if expected > 0:
                discrepancy_rate = abs(expected - actual) / expected
                
                if discrepancy_rate > self.shrinkage_threshold:
                    events.append({
                        'event_type': 'INVENTORY_DISCREPANCY',
                        'timestamp': None,  # Summary event
                        'station_id': 'ALL',
                        'severity': 'MEDIUM',
                        'details': {
                            'sku': sku,
                            'expected': expected,
                            'actual': actual,
                            'difference': expected - actual,
                            'discrepancy_rate': discrepancy_rate
                        }
                    })
        
        return events
    
    # @algorithm Shrinkage Pattern Analysis | Identifies theft and loss patterns
    def _detect_shrinkage(self, inventory_state: Dict) -> List[Dict]:
        """
        Detect patterns indicating inventory shrinkage
        """
        events = []
        
        total_discrepancy = 0
        items_with_shrinkage = 0
        
        for sku, data in inventory_state.items():
            expected = data.get('expected', 0)
            actual = data.get('actual', 0)
            
            if actual < expected:
                total_discrepancy += (expected - actual)
                items_with_shrinkage += 1
        
        if items_with_shrinkage > 5:  # Threshold for pattern
            events.append({
                'event_type': 'INVENTORY_SHRINKAGE',
                'timestamp': None,
                'station_id': 'ALL',
                'severity': 'HIGH',
                'details': {
                    'affected_items': items_with_shrinkage,
                    'total_units_lost': total_discrepancy,
                    'pattern': 'Widespread shrinkage detected'
                }
            })
        
        return events
