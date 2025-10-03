"""
Event Generation Module
Generates and exports events in JSONL format
"""

import json
import logging
from pathlib import Path
from typing import List, Dict
from datetime import datetime


class EventGenerator:
    """Generates events.jsonl output file"""
    
    def __init__(self, output_path: str):
        self.output_path = Path(output_path)
        self.logger = logging.getLogger('sentinel.event_generator')
    
    def generate(self, events: List[Dict]) -> str:
        """
        Generate events.jsonl file from detected events
        """
        # Create output directory if it doesn't exist
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Output file path
        output_file = self.output_path / 'events.jsonl'
        
        # Sort events by timestamp
        sorted_events = sorted(
            [e for e in events if e.get('timestamp')],
            key=lambda x: x.get('timestamp', '')
        )
        
        # Add events without timestamps at the end
        no_timestamp = [e for e in events if not e.get('timestamp')]
        sorted_events.extend(no_timestamp)
        
        # Write events to file
        with open(output_file, 'w', encoding='utf-8') as f:
            for event in sorted_events:
                # Format event
                formatted_event = self._format_event(event)
                f.write(json.dumps(formatted_event) + '\n')
        
        self.logger.info(f"Generated {len(events)} events to {output_file}")
        return str(output_file)
    
    def _format_event(self, event: Dict) -> Dict:
        """
        Format event for output
        Ensures consistent structure
        """
        formatted = {
            'event_type': event.get('event_type', 'UNKNOWN'),
            'timestamp': event.get('timestamp'),
            'station_id': event.get('station_id'),
            'severity': event.get('severity', 'LOW'),
            'details': event.get('details', {})
        }
        
        return formatted
    
    def generate_summary(self, events: List[Dict]) -> Dict:
        """
        Generate summary statistics for events
        """
        summary = {
            'total_events': len(events),
            'by_type': {},
            'by_severity': {},
            'by_station': {}
        }
        
        for event in events:
            # Count by type
            event_type = event.get('event_type', 'UNKNOWN')
            summary['by_type'][event_type] = summary['by_type'].get(event_type, 0) + 1
            
            # Count by severity
            severity = event.get('severity', 'LOW')
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1
            
            # Count by station
            station = event.get('station_id', 'UNKNOWN')
            summary['by_station'][station] = summary['by_station'].get(station, 0) + 1
        
        return summary
