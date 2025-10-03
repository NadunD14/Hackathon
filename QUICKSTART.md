# Project Sentinel - Quick Start Guide

## Quick Start

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Run Analysis
```powershell
python src/main.py --input data --output evidence/output/test
```

### 3. Launch Dashboard
```powershell
python src/main.py --input data --output evidence/output/test --dashboard
```
Then open: http://localhost:5000

### 4. Run Automated Demo
```powershell
python evidence/executables/run_demo.py
```

## Project Structure

```
Project/
├── src/                      # Source code
│   ├── main.py              # Main entry point
│   ├── data_processing/     # Data loading & synchronization
│   ├── analytics/           # Detection algorithms
│   ├── events/              # Event generation
│   ├── dashboard/           # Web dashboard
│   ├── utils/               # Utilities & config
│   └── tests/               # Unit tests
├── data/                     # Input data files
├── evidence/                 # Output & evidence
│   ├── output/              # Generated events.jsonl
│   ├── screenshots/         # Dashboard screenshots
│   └── executables/         # Automation scripts
├── requirements.txt         # Python dependencies
└── README.md                # Documentation
```

## Key Features

### 1. Theft Detection
- Scan avoidance detection
- Barcode switching detection
- Weight discrepancy analysis

### 2. Anomaly Detection
- System crash detection
- Scanning error patterns
- Unusual activity detection

### 3. Queue Optimization
- Wait time monitoring
- Dynamic station allocation
- Staffing recommendations

### 4. Inventory Tracking
- Inventory reconciliation
- Discrepancy detection
- Shrinkage pattern analysis

## Command Line Options

```powershell
python src/main.py [OPTIONS]

Options:
  --input PATH       Path to input data folder (default: ../data)
  --output PATH      Path to output folder (default: evidence/output/test)
  --mode MODE        Execution mode: test, final, realtime (default: test)
  --dashboard        Launch web dashboard
  --verbose          Enable verbose logging
```

## Running Tests

```powershell
python -m pytest src/tests/
```

## Algorithm Tagging

All algorithms are tagged with:
```python
# @algorithm AlgorithmName | Purpose description
```

Search for algorithms:
```powershell
grep -r "@algorithm" src
```

## Troubleshooting

### Issue: Module not found
**Solution:** Ensure you're in the project root directory and Python can find src/

### Issue: Data files not found
**Solution:** Check that data/ folder exists with required files:
- rfid_readings.jsonl
- queue_monitoring.jsonl
- pos_transactions.jsonl
- product_recognition.jsonl
- inventory_snapshots.jsonl
- products_list.csv
- customer_data.csv

### Issue: Dashboard won't start
**Solution:** Ensure Flask is installed: `pip install flask flask-cors`

## Development Tips

1. **Add new detection algorithms** in `src/analytics/`
2. **Modify event types** in `src/utils/config.py`
3. **Customize dashboard** in `src/dashboard/templates/`
4. **Add tests** in `src/tests/`

## Contact & Support

For questions or issues during the hackathon, refer to:
- README.md for detailed documentation
- SUBMISSION_GUIDE.md for submission requirements
- src/ code comments for implementation details

Good luck! 🚀
