"""
Data Synchronizer Module
Synchronizes and correlates data from different sources based on timestamps
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging


class DataSynchronizer:
    """Synchronizes timestamped data across different sources"""
    
    def __init__(self, time_window_seconds: int = 5):
        self.time_window = timedelta(seconds=time_window_seconds)
        self.logger = logging.getLogger('sentinel.synchronizer')
    
    # @algorithm Time-Window Correlation | Correlates events within time windows
    def process(self, raw_data: Dict[str, Any]) -> List[Dict]:
        """
        Synchronize and correlate data from all sources
        Groups events by time windows and station
        """
        synchronized_events = []
        
        # Convert JSONL data to DataFrames for easier processing
        rfid_df = self._to_dataframe(raw_data.get('rfid', []))
        queue_df = self._to_dataframe(raw_data.get('queue', []))
        pos_df = self._to_dataframe(raw_data.get('pos', []))
        recognition_df = self._to_dataframe(raw_data.get('product_recognition', []))
        inventory_df = self._to_dataframe(raw_data.get('inventory', []))
        
        # Get unique timestamps across all sources
        all_timestamps = self._get_all_timestamps([
            rfid_df, queue_df, pos_df, recognition_df
        ])
        
        # Create time windows
        for timestamp in sorted(all_timestamps):
            window_start = timestamp
            window_end = timestamp + self.time_window
            
            # Get all stations
            stations = self._get_active_stations([rfid_df, queue_df, pos_df, recognition_df])
            
            for station in stations:
                window_data = {
                    'timestamp': timestamp.isoformat(),
                    'window_start': window_start.isoformat(),
                    'window_end': window_end.isoformat(),
                    'station_id': station,
                    'rfid_events': self._filter_by_window(rfid_df, station, window_start, window_end),
                    'queue_events': self._filter_by_window(queue_df, station, window_start, window_end),
                    'pos_events': self._filter_by_window(pos_df, station, window_start, window_end),
                    'recognition_events': self._filter_by_window(recognition_df, station, window_start, window_end),
                    'inventory_snapshot': self._get_latest_inventory(inventory_df, timestamp)
                }
                
                synchronized_events.append(window_data)
        
        self.logger.info(f"Created {len(synchronized_events)} synchronized time windows")
        return synchronized_events
    
    def _to_dataframe(self, records: List[Dict]) -> pd.DataFrame:
        """Convert JSONL records to DataFrame with parsed timestamps"""
        if not records:
            return pd.DataFrame()
        
        df = pd.DataFrame(records)
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    
    def _get_all_timestamps(self, dataframes: List[pd.DataFrame]) -> List[datetime]:
        """Get all unique timestamps from multiple DataFrames"""
        all_times = []
        for df in dataframes:
            if not df.empty and 'timestamp' in df.columns:
                all_times.extend(df['timestamp'].tolist())
        return list(set(all_times))
    
    def _get_active_stations(self, dataframes: List[pd.DataFrame]) -> List[str]:
        """Get all unique station IDs"""
        stations = set()
        for df in dataframes:
            if not df.empty and 'station_id' in df.columns:
                stations.update(df['station_id'].unique())
        return sorted(list(stations))
    
    def _filter_by_window(self, df: pd.DataFrame, station: str, 
                          start: datetime, end: datetime) -> List[Dict]:
        """Filter DataFrame by station and time window"""
        if df.empty:
            return []
        
        mask = (
            (df['station_id'] == station) &
            (df['timestamp'] >= start) &
            (df['timestamp'] < end)
        )
        
        filtered = df[mask]
        return filtered.to_dict('records') if not filtered.empty else []
    
    def _get_latest_inventory(self, inventory_df: pd.DataFrame, 
                             timestamp: datetime) -> Dict:
        """Get the most recent inventory snapshot before the given timestamp"""
        if inventory_df.empty:
            return {}
        
        # Filter inventory snapshots before or at the timestamp
        mask = inventory_df['timestamp'] <= timestamp
        recent = inventory_df[mask]
        
        if recent.empty:
            return {}
        
        # Get the most recent one
        latest = recent.sort_values('timestamp', ascending=False).iloc[0]
        return latest.to_dict()
