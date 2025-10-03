"""
Project Sentinel - Main Entry Point
Retail Analytics & Optimization Platform
"""

import argparse
import sys
import logging
from pathlib import Path
from datetime import datetime

# Import core modules
from data_processing.data_loader import DataLoader
from data_processing.data_synchronizer import DataSynchronizer
from analytics.anomaly_detector import AnomalyDetector
from analytics.queue_optimizer import QueueOptimizer
from analytics.inventory_tracker import InventoryTracker
from analytics.theft_detector import TheftDetector
from events.event_generator import EventGenerator
from utils.logger import setup_logger
from utils.config import Config


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Project Sentinel - Retail Analytics Platform'
    )
    parser.add_argument(
        '--input',
        type=str,
        default='../data',
        help='Path to input data folder'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='evidence/output/test',
        help='Path to output folder'
    )
    parser.add_argument(
        '--mode',
        type=str,
        choices=['test', 'final', 'realtime'],
        default='test',
        help='Execution mode'
    )
    parser.add_argument(
        '--dashboard',
        action='store_true',
        help='Launch dashboard'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()


def main():
    """Main execution function"""
    # Parse arguments
    args = parse_arguments()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger('sentinel', log_level)
    
    logger.info("=" * 60)
    logger.info("Project Sentinel - Retail Analytics Platform")
    logger.info("=" * 60)
    logger.info(f"Mode: {args.mode}")
    logger.info(f"Input: {args.input}")
    logger.info(f"Output: {args.output}")
    logger.info(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        # Initialize configuration
        config = Config()
        
        # Step 1: Load Data
        logger.info("\n[STEP 1] Loading data from sources...")
        data_loader = DataLoader(args.input)
        raw_data = data_loader.load_all()
        logger.info(f"✓ Loaded {len(raw_data)} data sources")
        
        # Step 2: Synchronize and correlate data
        logger.info("\n[STEP 2] Synchronizing and correlating data...")
        synchronizer = DataSynchronizer()
        synchronized_data = synchronizer.process(raw_data)
        logger.info(f"✓ Synchronized {len(synchronized_data)} time windows")
        
        # Step 3: Run Analytics
        logger.info("\n[STEP 3] Running analytics engines...")
        
        # Initialize detectors
        theft_detector = TheftDetector(config)
        anomaly_detector = AnomalyDetector(config)
        queue_optimizer = QueueOptimizer(config)
        inventory_tracker = InventoryTracker(config)
        
        # Detect events
        events = []
        
        logger.info("  - Detecting theft incidents...")
        theft_events = theft_detector.detect(synchronized_data)
        events.extend(theft_events)
        logger.info(f"    Found {len(theft_events)} potential theft incidents")
        
        logger.info("  - Detecting anomalies...")
        anomaly_events = anomaly_detector.detect(synchronized_data)
        events.extend(anomaly_events)
        logger.info(f"    Found {len(anomaly_events)} anomalies")
        
        logger.info("  - Optimizing queue management...")
        queue_events = queue_optimizer.analyze(synchronized_data)
        events.extend(queue_events)
        logger.info(f"    Generated {len(queue_events)} queue insights")
        
        logger.info("  - Tracking inventory...")
        inventory_events = inventory_tracker.track(synchronized_data)
        events.extend(inventory_events)
        logger.info(f"    Found {len(inventory_events)} inventory issues")
        
        # Step 4: Generate output
        logger.info("\n[STEP 4] Generating event output...")
        event_generator = EventGenerator(args.output)
        output_file = event_generator.generate(events)
        logger.info(f"✓ Events written to: {output_file}")
        
        # Step 5: Launch dashboard (optional)
        if args.dashboard:
            logger.info("\n[STEP 5] Launching dashboard...")
            from dashboard.app import launch_dashboard
            launch_dashboard(events, synchronized_data)
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("EXECUTION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total Events Detected: {len(events)}")
        logger.info(f"Output File: {output_file}")
        logger.info(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        logger.info("✓ Processing completed successfully!")
        
        return 0
        
    except Exception as e:
        logger.error(f"\n✗ Error occurred: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
