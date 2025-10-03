# Output Files

This folder contains the generated `events.jsonl` files for test and final datasets.

## Structure

```
output/
├── test/
│   └── events.jsonl    # Events detected from test dataset
└── final/
    └── events.jsonl    # Events detected from final dataset
```

## Event Format

Each line in `events.jsonl` is a JSON object with the following structure:

```json
{
  "event_type": "SCAN_AVOIDANCE",
  "timestamp": "2025-10-03T10:30:15",
  "station_id": "SCC1",
  "severity": "HIGH",
  "details": {
    "unscanned_skus": ["SKU123"],
    "rfid_count": 3,
    "pos_count": 2
  }
}
```

## Event Types

- **SCAN_AVOIDANCE** - Items detected but not scanned
- **BARCODE_SWITCHING** - Mismatched product recognition vs POS
- **WEIGHT_DISCREPANCY** - Weight doesn't match expected
- **SYSTEM_CRASH** - System failure detected
- **SCANNING_ERROR** - Read errors in systems
- **LONG_WAIT_TIME** - Excessive customer wait times
- **STATION_ALLOCATION** - Staffing recommendations
- **INVENTORY_DISCREPANCY** - Inventory mismatches
- **INVENTORY_SHRINKAGE** - Pattern of inventory loss

## Severity Levels

- **CRITICAL** - Immediate attention required
- **HIGH** - High priority, address soon
- **MEDIUM** - Moderate priority
- **LOW** - Low priority, informational
