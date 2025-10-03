"""
Dashboard Application
Flask-based real-time dashboard for retail analytics
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
import logging
from typing import Dict, List, Any


app = Flask(__name__)
CORS(app)

# Global state (in production, use proper state management)
current_events = []
current_data = {}


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/events')
def get_events():
    """API endpoint for events"""
    return jsonify({
        'events': current_events,
        'count': len(current_events)
    })


@app.route('/api/summary')
def get_summary():
    """API endpoint for summary statistics"""
    summary = generate_summary(current_events)
    return jsonify(summary)


@app.route('/api/stations')
def get_stations():
    """API endpoint for station status"""
    stations = analyze_stations(current_data)
    return jsonify(stations)


def generate_summary(events: List[Dict]) -> Dict:
    """Generate summary statistics"""
    summary = {
        'total_events': len(events),
        'critical': sum(1 for e in events if e.get('severity') == 'CRITICAL'),
        'high': sum(1 for e in events if e.get('severity') == 'HIGH'),
        'medium': sum(1 for e in events if e.get('severity') == 'MEDIUM'),
        'low': sum(1 for e in events if e.get('severity') == 'LOW'),
    }
    
    # Count by type
    event_types = {}
    for event in events:
        event_type = event.get('event_type', 'UNKNOWN')
        event_types[event_type] = event_types.get(event_type, 0) + 1
    
    summary['by_type'] = event_types
    
    return summary


def analyze_stations(data: Dict) -> List[Dict]:
    """Analyze station status"""
    stations = []
    
    for station_id in ['SCC1', 'SCC2', 'SCC3', 'SCC4', 'RC1']:
        stations.append({
            'id': station_id,
            'status': 'active',
            'type': 'self-checkout' if station_id.startswith('SCC') else 'regular'
        })
    
    return stations


def launch_dashboard(events: List[Dict], data: Dict):
    """Launch the dashboard"""
    global current_events, current_data
    current_events = events
    current_data = data
    
    logger = logging.getLogger('sentinel.dashboard')
    logger.info("Starting dashboard on http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=False)


if __name__ == '__main__':
    app.run(debug=True)
