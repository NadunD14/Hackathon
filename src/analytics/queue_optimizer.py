"""
Queue Optimization Module
Analyzes customer flow and optimizes checkout resource allocation
"""

import logging
from typing import Dict, List, Any
from collections import defaultdict


class QueueOptimizer:
    """Optimizes queue management and resource allocation"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('sentinel.queue_optimizer')
        self.max_dwell_time = 180  # 3 minutes
        self.target_customers_per_station = 6
    
    def analyze(self, synchronized_data: List[Dict]) -> List[Dict]:
        """Analyze queue data and generate optimization insights"""
        events = []
        
        # Aggregate queue data by timestamp
        queue_summary = self._aggregate_queue_data(synchronized_data)
        
        for window in synchronized_data:
            # Detect long wait times
            wait_time_event = self._detect_long_wait_times(window)
            if wait_time_event:
                events.append(wait_time_event)
            
            # Check station allocation
            allocation_event = self._check_station_allocation(window, queue_summary)
            if allocation_event:
                events.append(allocation_event)
        
        # Generate staffing recommendations
        staffing_events = self._generate_staffing_recommendations(queue_summary)
        events.extend(staffing_events)
        
        return events
    
    # @algorithm Queue Length Analysis | Monitors and flags excessive queue lengths
    def _detect_long_wait_times(self, window: Dict) -> Dict:
        """
        Detect situations with excessively long customer wait times
        """
        queue_events = window.get('queue_events', [])
        
        for event in queue_events:
            if event.get('status') == 'Active' and event.get('data'):
                data = event['data']
                dwell_time = data.get('average_dwell_time', 0)
                customer_count = data.get('customer_count', 0)
                
                if dwell_time > self.max_dwell_time:
                    return {
                        'event_type': 'LONG_WAIT_TIME',
                        'timestamp': window['timestamp'],
                        'station_id': window['station_id'],
                        'severity': 'HIGH',
                        'details': {
                            'average_dwell_time': dwell_time,
                            'customer_count': customer_count,
                            'threshold': self.max_dwell_time
                        }
                    }
        
        return None
    
    # @algorithm Dynamic Station Allocation | Optimizes active checkout stations
    def _check_station_allocation(self, window: Dict, queue_summary: Dict) -> Dict:
        """
        Check if current station allocation is optimal
        Recommends opening/closing stations based on customer flow
        """
        queue_events = window.get('queue_events', [])
        
        if not queue_events:
            return None
        
        total_customers = 0
        for event in queue_events:
            if event.get('status') == 'Active' and event.get('data'):
                total_customers += event['data'].get('customer_count', 0)
        
        # Count active stations
        active_stations = len([e for e in queue_events if e.get('status') == 'Active'])
        
        if active_stations == 0:
            return None
        
        customers_per_station = total_customers / active_stations if active_stations > 0 else 0
        
        # Recommend changes if ratio is off
        if customers_per_station > self.target_customers_per_station * 1.5:
            return {
                'event_type': 'STATION_ALLOCATION',
                'timestamp': window['timestamp'],
                'station_id': window['station_id'],
                'severity': 'MEDIUM',
                'details': {
                    'action': 'OPEN_STATION',
                    'current_stations': active_stations,
                    'total_customers': total_customers,
                    'customers_per_station': customers_per_station,
                    'target_ratio': self.target_customers_per_station
                }
            }
        elif customers_per_station < self.target_customers_per_station * 0.5 and active_stations > 1:
            return {
                'event_type': 'STATION_ALLOCATION',
                'timestamp': window['timestamp'],
                'station_id': window['station_id'],
                'severity': 'LOW',
                'details': {
                    'action': 'CLOSE_STATION',
                    'current_stations': active_stations,
                    'total_customers': total_customers,
                    'customers_per_station': customers_per_station,
                    'target_ratio': self.target_customers_per_station
                }
            }
        
        return None
    
    # @algorithm Staffing Forecast | Predicts optimal staff allocation
    def _generate_staffing_recommendations(self, queue_summary: Dict) -> List[Dict]:
        """
        Generate staffing recommendations based on historical patterns
        """
        events = []
        
        # Analyze patterns to recommend staffing
        # This is a simplified version - can be enhanced with ML
        
        return events
    
    def _aggregate_queue_data(self, synchronized_data: List[Dict]) -> Dict:
        """Aggregate queue data for analysis"""
        summary = defaultdict(list)
        
        for window in synchronized_data:
            queue_events = window.get('queue_events', [])
            for event in queue_events:
                if event.get('status') == 'Active' and event.get('data'):
                    summary[window['timestamp']].append(event['data'])
        
        return dict(summary)
