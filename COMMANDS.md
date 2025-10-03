# 🚀 Project Sentinel - HACKATHON COMMANDS

## Quick Reference Card

### 🔧 Setup (Run Once)
```powershell
# Install dependencies
pip install -r requirements.txt
```

### 🏃 Running the System

#### Option 1: Quick Test
```powershell
python src/main.py --input data --output evidence/output/test
```

#### Option 2: With Dashboard
```powershell
python src/main.py --input data --output evidence/output/test --dashboard
```
Open: http://localhost:5000

#### Option 3: Verbose Mode (Debug)
```powershell
python src/main.py --input data --output evidence/output/test --verbose
```

#### Option 4: Full Automation
```powershell
python evidence/executables/run_demo.py
```

### 📊 Check Results
```powershell
# View test output
cat evidence/output/test/events.jsonl

# Count events
(Get-Content evidence/output/test/events.jsonl).Count

# View last 10 events
Get-Content evidence/output/test/events.jsonl -Tail 10

# Search for specific event type
Get-Content evidence/output/test/events.jsonl | Select-String "SCAN_AVOIDANCE"
```

### 🧪 Testing
```powershell
# Run all tests
python -m pytest src/tests/ -v

# Run specific test file
python -m pytest src/tests/test_analytics.py -v

# Run with coverage
python -m pytest src/tests/ --cov=src --cov-report=html
```

### 🔍 Find Algorithms
```powershell
# Find all algorithms (PowerShell)
Select-String -Path src\*.py,src\*\*.py -Pattern "@algorithm"

# Count algorithms
(Select-String -Path src\*.py,src\*\*.py -Pattern "@algorithm").Count
```

### 📁 File Operations
```powershell
# List data files
ls data

# Check if output exists
Test-Path evidence/output/test/events.jsonl

# View project structure
tree /F src
```

### 🌐 Dashboard Commands
```powershell
# Start dashboard only
cd src/dashboard
python app.py

# Check if Flask is running
curl http://localhost:5000/api/summary
```

### 📦 Before Submission
```powershell
# 1. Clean up
Remove-Item -Recurse -Force __pycache__,src\__pycache__,src\*\__pycache__

# 2. Run final automation
python evidence/executables/run_demo.py

# 3. Verify outputs exist
Test-Path evidence/output/test/events.jsonl
Test-Path evidence/output/final/events.jsonl

# 4. Count events
(Get-Content evidence/output/test/events.jsonl).Count
(Get-Content evidence/output/final/events.jsonl).Count

# 5. Verify algorithm tags
(Select-String -Path src\*\*.py -Pattern "@algorithm").Count

# 6. Create submission zip
Compress-Archive -Path * -DestinationPath ..\Team01_sentinel.zip
```

### 🐛 Troubleshooting
```powershell
# Check Python version
python --version

# Check installed packages
pip list

# Reinstall requirements
pip install -r requirements.txt --force-reinstall

# Check for Python errors
python -m py_compile src/main.py

# View logs (if created)
Get-Content logs/sentinel_*.log -Tail 50
```

### 📈 Performance Monitoring
```powershell
# Time the execution
Measure-Command { python src/main.py --input data --output evidence/output/test }

# Monitor memory (install psutil first)
python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"
```

### 🎯 Development Commands
```powershell
# Format code (if black is installed)
black src/

# Lint code (if pylint is installed)
pylint src/

# Type checking (if mypy is installed)
mypy src/
```

### 💡 Useful Python One-Liners
```powershell
# Count lines of code
(Get-ChildItem -Recurse -Include *.py src | Get-Content | Measure-Object -Line).Lines

# Find TODOs
Select-String -Path src\*\*.py -Pattern "TODO|FIXME"

# Check imports
Select-String -Path src\*\*.py -Pattern "^import |^from "
```

## 🎓 Common Workflow

### Initial Setup
```powershell
cd c:\Users\nadun\Desktop\hackthon\Project
pip install -r requirements.txt
```

### Development Cycle
```powershell
# 1. Make changes to code
# 2. Test changes
python src/main.py --input data --output evidence/output/test --verbose

# 3. Check output
cat evidence/output/test/events.jsonl

# 4. Run tests
python -m pytest src/tests/ -v

# 5. View in dashboard
python src/main.py --input data --output evidence/output/test --dashboard
```

### Final Submission
```powershell
# 1. Final run
python evidence/executables/run_demo.py

# 2. Take screenshots (manually)

# 3. Fill out SUBMISSION_GUIDE.md (manually)

# 4. Verify everything
Test-Path evidence/output/test/events.jsonl
Test-Path evidence/output/final/events.jsonl
Test-Path SUBMISSION_GUIDE.md

# 5. Create zip
Compress-Archive -Path * -DestinationPath ..\Team01_sentinel.zip
```

## 📞 Quick Help

**If main.py won't run:**
```powershell
python src/main.py --help
```

**If modules not found:**
```powershell
$env:PYTHONPATH="c:\Users\nadun\Desktop\hackthon\Project\src"
python src/main.py ...
```

**If dashboard won't start:**
```powershell
pip install flask flask-cors flask-socketio
```

**If data not found:**
```powershell
# Make sure you're in project root
cd c:\Users\nadun\Desktop\hackthon\Project
# Then run with full path
python src/main.py --input c:\Users\nadun\Desktop\hackthon\Project\data --output evidence/output/test
```

## ⚡ Emergency Commands

```powershell
# Complete reset
Remove-Item -Recurse -Force evidence/output/test/*,evidence/output/final/*,logs/*
python evidence/executables/run_demo.py

# Quick verification
python -c "from src.analytics.theft_detector import TheftDetector; print('✓ Imports work')"

# Generate minimal output
python -c "import json; open('evidence/output/test/events.jsonl', 'w').write(json.dumps({'event_type': 'TEST', 'timestamp': '2025-10-03T10:00:00', 'station_id': 'SCC1', 'severity': 'LOW', 'details': {}}) + '\n')"
```

---

**Remember:** You have 4 hours. Focus on:
1. ✅ Getting it working
2. 📊 Generating good events
3. 🎨 Making dashboard look nice
4. 🎤 Preparing presentation

**Good luck! 🍀**
