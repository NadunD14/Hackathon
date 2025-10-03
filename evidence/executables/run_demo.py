"""
Automation Script - Run Demo
This script installs dependencies, runs the analysis, and generates outputs
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error during {description}")
        print(f"Exit code: {e.returncode}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Main execution function"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         PROJECT SENTINEL - AUTOMATED DEMO                 ║
    ║         Retail Analytics & Optimization Platform          ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Get project root
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    
    print(f"\n📁 Working directory: {project_root}")
    
    # Step 1: Install dependencies
    if not run_command(
        "pip install -r requirements.txt",
        "Installing Python dependencies"
    ):
        print("\n⚠️  Failed to install dependencies. Please install manually:")
        print("   pip install -r requirements.txt")
        return 1
    
    # Step 2: Run analysis on test data
    print("\n" + "="*60)
    print("📊 RUNNING ANALYSIS ON TEST DATA")
    print("="*60)
    
    if not run_command(
        "python src/main.py --input data --output evidence/output/test --mode test",
        "Processing test dataset"
    ):
        print("\n✗ Test analysis failed")
        return 1
    
    # Step 3: Run analysis on final data (if different)
    print("\n" + "="*60)
    print("📊 RUNNING ANALYSIS ON FINAL DATA")
    print("="*60)
    
    if not run_command(
        "python src/main.py --input data --output evidence/output/final --mode final",
        "Processing final dataset"
    ):
        print("\n✗ Final analysis failed")
        return 1
    
    # Step 4: Generate summary
    print("\n" + "="*60)
    print("📋 EXECUTION SUMMARY")
    print("="*60)
    
    # Check outputs
    test_output = project_root / "evidence" / "output" / "test" / "events.jsonl"
    final_output = project_root / "evidence" / "output" / "final" / "events.jsonl"
    
    print(f"\n✓ Test output: {test_output}")
    if test_output.exists():
        with open(test_output, 'r') as f:
            test_lines = len(f.readlines())
        print(f"  Events generated: {test_lines}")
    else:
        print(f"  ⚠️  File not found!")
    
    print(f"\n✓ Final output: {final_output}")
    if final_output.exists():
        with open(final_output, 'r') as f:
            final_lines = len(f.readlines())
        print(f"  Events generated: {final_lines}")
    else:
        print(f"  ⚠️  File not found!")
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETED SUCCESSFULLY")
    print("="*60)
    print("\n📁 Output files generated:")
    print(f"   - {test_output}")
    print(f"   - {final_output}")
    print("\n🌐 To view dashboard, run:")
    print("   python src/main.py --input data --output evidence/output/test --dashboard")
    print("\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
