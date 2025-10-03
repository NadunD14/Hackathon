# Project Sentinel - Development Roadmap

## Phase 1: Foundation (Completed) ✅

### Data Processing
- [x] Data loader for JSONL and CSV files
- [x] Data synchronizer for time-window correlation
- [x] Data validator for integrity checks
- [x] Error handling for missing/corrupt data

### Core Analytics
- [x] Theft detector (scan avoidance, barcode switching, weight discrepancies)
- [x] Anomaly detector (system crashes, scanning errors)
- [x] Queue optimizer (wait times, station allocation)
- [x] Inventory tracker (discrepancies, shrinkage patterns)

### Infrastructure
- [x] Event generator for JSONL output
- [x] Configuration management
- [x] Logging system
- [x] Main entry point
- [x] Automation script

### Dashboard
- [x] Flask backend
- [x] HTML/CSS frontend
- [x] Real-time data endpoints
- [x] Event visualization

## Phase 2: Enhancement (To-Do)

### Advanced Analytics
- [ ] Machine learning for pattern prediction
- [ ] Customer behavior analysis
- [ ] Peak hour forecasting
- [ ] Seasonal trend analysis

### Detection Improvements
- [ ] Multi-station correlation
- [ ] Historical pattern matching
- [ ] Confidence scoring for events
- [ ] False positive reduction

### Dashboard Enhancements
- [ ] Interactive charts (Chart.js/Plotly)
- [ ] Real-time streaming updates
- [ ] Alert notifications
- [ ] Export functionality
- [ ] Historical data views

### Testing
- [ ] Integration tests
- [ ] Performance tests
- [ ] Data validation tests
- [ ] End-to-end tests

## Phase 3: Optimization (Future)

### Performance
- [ ] Batch processing optimization
- [ ] Memory usage optimization
- [ ] Parallel processing
- [ ] Caching strategies

### Features
- [ ] Configuration UI
- [ ] Alert rules engine
- [ ] Report generation
- [ ] Multi-store support
- [ ] API for external integrations

### Documentation
- [ ] API documentation
- [ ] Algorithm documentation
- [ ] Deployment guide
- [ ] User manual

## Quick Implementation Guide

### Adding a New Detection Algorithm

1. Create detector in `src/analytics/`:
```python
# @algorithm MyAlgorithm | Description
def detect_something(self, window: Dict) -> Dict:
    # Your logic here
    return event
```

2. Add to main analysis flow in `src/main.py`:
```python
my_detector = MyDetector(config)
my_events = my_detector.detect(synchronized_data)
events.extend(my_events)
```

3. Add event type to `src/utils/config.py`:
```python
EVENT_MY_NEW_TYPE = 'MY_NEW_TYPE'
```

### Adding a New Data Source

1. Add loader method in `src/data_processing/data_loader.py`:
```python
def load_new_source(self, filename: str):
    # Load logic
    return data
```

2. Update `load_all()` method:
```python
data['new_source'] = self.load_new_source('new_file.jsonl')
```

3. Update synchronizer to include new data

### Modifying Dashboard

1. Update Flask routes in `src/dashboard/app.py`
2. Modify HTML template in `src/dashboard/templates/dashboard.html`
3. Add CSS styling as needed

## Testing Strategy

### Unit Tests
```powershell
python -m pytest src/tests/ -v
```

### Integration Test
```powershell
python src/main.py --input data --output test_output
```

### Dashboard Test
```powershell
python src/main.py --input data --output evidence/output/test --dashboard
```

## Common Customizations

### Adjust Time Windows
In `src/utils/config.py`:
```python
TIME_WINDOW_SECONDS = 10  # Change from 5 to 10
```

### Change Thresholds
```python
MAX_DWELL_TIME_SECONDS = 240  # 4 minutes instead of 3
TARGET_CUSTOMERS_PER_STATION = 8  # Adjust ratio
```

### Add Custom Events
```python
# In your detector
return {
    'event_type': 'CUSTOM_EVENT',
    'timestamp': timestamp,
    'station_id': station_id,
    'severity': 'MEDIUM',
    'details': {
        'custom_field': value
    }
}
```

## Performance Tips

1. **Batch Processing**: Process data in chunks for large datasets
2. **Indexing**: Use pandas indexing for faster lookups
3. **Caching**: Cache frequently accessed product/customer data
4. **Parallel Processing**: Use multiprocessing for independent detectors
5. **Memory Management**: Clear processed data from memory

## Debugging Tips

1. **Enable Verbose Logging**:
```powershell
python src/main.py --verbose
```

2. **Check Logs**:
```powershell
cat logs/sentinel_*.log
```

3. **Validate Data**:
```python
from data_processing.data_validator import DataValidator
validator = DataValidator()
is_valid, msg = validator.validate_rfid_record(record)
```

4. **Test Individual Components**:
```python
# Test just the theft detector
detector = TheftDetector(config)
events = detector.detect(sample_data)
```

## Next Steps for Hackathon

1. **Test with real data** from data/ folder
2. **Refine detection algorithms** based on results
3. **Enhance dashboard** with better visualizations
4. **Add more event types** as needed
5. **Optimize performance** for 4-hour time limit
6. **Document your approach** in SUBMISSION_GUIDE.md
7. **Take screenshots** of dashboard
8. **Test automation script** multiple times
9. **Prepare presentation** (2 minutes)
10. **Practice demo** before judging

## Resources

- Python Documentation: https://docs.python.org/3/
- Pandas: https://pandas.pydata.org/docs/
- Flask: https://flask.palletsprojects.com/
- JSON Lines: http://jsonlines.org/

Good luck with your hackathon! 🚀
