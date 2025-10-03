# Project Sentinel - System Architecture

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         INPUT DATA                              │
├─────────────────────────────────────────────────────────────────┤
│  • rfid_readings.jsonl        (RFID sensor data)               │
│  • queue_monitoring.jsonl     (Queue camera data)              │
│  • pos_transactions.jsonl     (POS transaction data)           │
│  • product_recognition.jsonl  (AI product recognition)         │
│  • inventory_snapshots.jsonl  (Inventory updates)              │
│  • products_list.csv          (Product catalog)                │
│  • customer_data.csv          (Customer database)              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DATA PROCESSING LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │  DataLoader      │→ │  DataValidator   │                   │
│  │                  │  │                  │                   │
│  │ • Load JSONL     │  │ • Validate       │                   │
│  │ • Load CSV       │  │ • Handle errors  │                   │
│  │ • Parse data     │  │ • Clean data     │                   │
│  └──────────────────┘  └──────────────────┘                   │
│           ↓                                                     │
│  ┌─────────────────────────────────────────┐                  │
│  │     DataSynchronizer                     │                  │
│  │ @algorithm Time-Window Correlation       │                  │
│  │                                          │                  │
│  │ • Sync timestamps (5-second windows)     │                  │
│  │ • Correlate RFID + POS + Queue + AI     │                  │
│  │ • Match inventory snapshots              │                  │
│  │ • Group by station                       │                  │
│  └─────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     ANALYTICS ENGINE                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ TheftDetector                                             │ │
│  ├───────────────────────────────────────────────────────────┤ │
│  │ @algorithm Scan Avoidance Detection                       │ │
│  │   → Compares RFID (items in area) vs POS (items scanned) │ │
│  │                                                            │ │
│  │ @algorithm Barcode Switching Detection                    │ │
│  │   → Compares AI recognition vs POS scanned product        │ │
│  │                                                            │ │
│  │ @algorithm Weight Discrepancy Detection                   │ │
│  │   → Validates expected weight vs actual weight            │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ AnomalyDetector                                           │ │
│  ├───────────────────────────────────────────────────────────┤ │
│  │ @algorithm System Crash Detection                         │ │
│  │   → Identifies "System Crash" status in streams           │ │
│  │                                                            │ │
│  │ @algorithm Error Pattern Detection                        │ │
│  │   → Tracks "Read Error" patterns across systems           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ QueueOptimizer                                            │ │
│  ├───────────────────────────────────────────────────────────┤ │
│  │ @algorithm Queue Length Analysis                          │ │
│  │   → Monitors average_dwell_time > threshold (180s)        │ │
│  │                                                            │ │
│  │ @algorithm Dynamic Station Allocation                     │ │
│  │   → Calculates customers/station ratio                    │ │
│  │   → Recommends OPEN_STATION or CLOSE_STATION              │ │
│  │                                                            │ │
│  │ @algorithm Staffing Forecast                              │ │
│  │   → Analyzes historical patterns for predictions          │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ InventoryTracker                                          │ │
│  ├───────────────────────────────────────────────────────────┤ │
│  │ @algorithm Inventory Reconciliation                       │ │
│  │   → Builds expected vs actual inventory state             │ │
│  │                                                            │ │
│  │ @algorithm Discrepancy Detection                          │ │
│  │   → Flags items with > 2% variance                        │ │
│  │                                                            │ │
│  │ @algorithm Shrinkage Pattern Analysis                     │ │
│  │   → Identifies widespread loss patterns (5+ items)        │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      EVENT GENERATION                           │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────┐                   │
│  │     EventGenerator                       │                   │
│  │                                          │                   │
│  │ • Collects all detected events           │                   │
│  │ • Formats as JSONL                       │                   │
│  │ • Sorts by timestamp                     │                   │
│  │ • Writes to events.jsonl                 │                   │
│  └─────────────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                         OUTPUT                                  │
├─────────────────────────────────────────────────────────────────┤
│  📄 evidence/output/test/events.jsonl                          │
│  📄 evidence/output/final/events.jsonl                         │
│                                                                  │
│  Event Format:                                                   │
│  {                                                               │
│    "event_type": "SCAN_AVOIDANCE",                             │
│    "timestamp": "2025-10-03T10:30:15",                         │
│    "station_id": "SCC1",                                        │
│    "severity": "HIGH",                                          │
│    "details": { ... }                                           │
│  }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    VISUALIZATION LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Flask Dashboard                        │   │
│  │                                                          │   │
│  │  Routes:                                                 │   │
│  │  • GET /                → Dashboard HTML                │   │
│  │  • GET /api/events      → List all events               │   │
│  │  • GET /api/summary     → Statistics summary            │   │
│  │  • GET /api/stations    → Station status                │   │
│  │                                                          │   │
│  │  Features:                                               │   │
│  │  • Real-time event feed                                  │   │
│  │  • Statistics cards (Critical/High/Medium/Low)           │   │
│  │  • Station status grid                                   │   │
│  │  • Event filtering by severity                           │   │
│  │  • Auto-refresh every 5 seconds                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Access: http://localhost:5000                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Station Layout

```
┌─────────────────────────────────────────────────────────────┐
│                    SUPERMARKET LAYOUT                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐          │
│   │  SCC1  │  │  SCC2  │  │  SCC3  │  │  SCC4  │          │
│   │ Self   │  │ Self   │  │ Self   │  │ Self   │          │
│   │Checkout│  │Checkout│  │Checkout│  │Checkout│          │
│   └────────┘  └────────┘  └────────┘  └────────┘          │
│                                                              │
│                      ┌────────┐                             │
│                      │  RC1   │                             │
│                      │Regular │                             │
│                      │Counter │                             │
│                      └────────┘                             │
│                                                              │
│  Strategy:                                                   │
│  • Start with 1 SCC + 1 RC1 open                            │
│  • Open more SCCs as customer traffic increases             │
│  • Target: ~6 customers per active station                  │
└─────────────────────────────────────────────────────────────┘
```

## Event Types & Severity

```
┌──────────────────────────┬───────────┬─────────────────────────┐
│ Event Type               │ Severity  │ Description             │
├──────────────────────────┼───────────┼─────────────────────────┤
│ SCAN_AVOIDANCE          │ HIGH      │ Items not scanned       │
│ BARCODE_SWITCHING       │ HIGH      │ Wrong barcode used      │
│ WEIGHT_DISCREPANCY      │ MEDIUM    │ Weight mismatch         │
│ SYSTEM_CRASH            │ CRITICAL  │ System failure          │
│ SCANNING_ERROR          │ MEDIUM    │ Read errors             │
│ LONG_WAIT_TIME          │ HIGH      │ Excessive wait          │
│ STATION_ALLOCATION      │ MEDIUM/LOW│ Staffing recommendation │
│ INVENTORY_DISCREPANCY   │ MEDIUM    │ Inventory mismatch      │
│ INVENTORY_SHRINKAGE     │ HIGH      │ Loss pattern detected   │
└──────────────────────────┴───────────┴─────────────────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY STACK                         │
├─────────────────────────────────────────────────────────────┤
│  Language:     Python 3.8+                                  │
│  Data:         Pandas, NumPy                                │
│  Web:          Flask, Flask-CORS                            │
│  Frontend:     HTML5, CSS3, JavaScript (Vanilla)            │
│  Format:       JSON Lines (JSONL)                           │
│  Testing:      pytest                                       │
│  Logging:      Python logging module                        │
└─────────────────────────────────────────────────────────────┘
```

## Configuration Parameters

```
┌─────────────────────────────────────────────────────────────┐
│                    KEY PARAMETERS                           │
├─────────────────────────────────────────────────────────────┤
│  TIME_WINDOW_SECONDS              = 5                       │
│  MAX_DWELL_TIME_SECONDS           = 180  (3 minutes)        │
│  TARGET_CUSTOMERS_PER_STATION     = 6                       │
│  SHRINKAGE_THRESHOLD              = 0.02  (2%)              │
│  WEIGHT_TOLERANCE                 = 0.05  (5%)              │
│  RECOGNITION_CONFIDENCE_THRESHOLD = 0.8   (80%)             │
└─────────────────────────────────────────────────────────────┘

Location: src/utils/config.py
Modify these to tune detection sensitivity
```

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   MAIN EXECUTION FLOW                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Parse command-line arguments                            │
│     ↓                                                        │
│  2. Setup logging                                           │
│     ↓                                                        │
│  3. Load data from all sources (DataLoader)                 │
│     ↓                                                        │
│  4. Synchronize data into time windows (DataSynchronizer)   │
│     ↓                                                        │
│  5. Run analytics engines in parallel:                      │
│     • TheftDetector                                         │
│     • AnomalyDetector                                       │
│     • QueueOptimizer                                        │
│     • InventoryTracker                                      │
│     ↓                                                        │
│  6. Collect all detected events                             │
│     ↓                                                        │
│  7. Generate events.jsonl (EventGenerator)                  │
│     ↓                                                        │
│  8. Optional: Launch dashboard                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Algorithm Summary

```
Total Algorithms: 12

Data Processing:
  1. Time-Window Correlation

Theft Detection:
  2. Scan Avoidance Detection
  3. Barcode Switching Detection
  4. Weight Discrepancy Detection

Anomaly Detection:
  5. System Crash Detection
  6. Error Pattern Detection

Queue Optimization:
  7. Queue Length Analysis
  8. Dynamic Station Allocation
  9. Staffing Forecast

Inventory Tracking:
  10. Inventory Reconciliation
  11. Discrepancy Detection
  12. Shrinkage Pattern Analysis
```

## File Structure Map

```
src/
├── main.py ─────────────────────► Entry point
│
├── data_processing/
│   ├── data_loader.py ──────────► Loads JSONL/CSV
│   ├── data_synchronizer.py ────► Time correlation
│   └── data_validator.py ───────► Validation
│
├── analytics/
│   ├── theft_detector.py ───────► 3 algorithms
│   ├── anomaly_detector.py ─────► 2 algorithms
│   ├── queue_optimizer.py ──────► 3 algorithms
│   └── inventory_tracker.py ────► 3 algorithms
│
├── events/
│   └── event_generator.py ──────► JSONL output
│
├── dashboard/
│   ├── app.py ──────────────────► Flask backend
│   └── templates/
│       └── dashboard.html ──────► Frontend UI
│
└── utils/
    ├── config.py ───────────────► Configuration
    └── logger.py ───────────────► Logging
```

---

**Total Lines of Code:** ~1,500+ lines
**Total Files Created:** 20+ files
**Algorithms Implemented:** 12
**Time to Complete Setup:** ~10 minutes

**Ready to go!** 🚀
