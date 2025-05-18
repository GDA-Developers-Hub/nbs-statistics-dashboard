#!/usr/bin/env python
"""
Script to continuously run the Somalia scraper at regular intervals (every 20 minutes).
This can be kept running in the background to ensure regular data updates.
"""
import os
import sys
import time
import schedule
import datetime
import subprocess
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper_scheduler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("scraper_scheduler")

# Directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_scraper():
    """Run the Somalia scraper command."""
    try:
        logger.info("Starting scraper job at %s", datetime.datetime.now())
        
        # Run the scraper command
        result = subprocess.run(
            ["python", "manage.py", "run_somalia_scraper_test"],
            cwd=BASE_DIR,
            check=True,
            capture_output=True,
            text=True
        )
        
        # Log the output
        logger.info("Scraper output: %s", result.stdout)
        
        if result.stderr:
            logger.warning("Scraper warnings/errors: %s", result.stderr)
            
        logger.info("Completed scraper job at %s", datetime.datetime.now())
        return True
    except subprocess.CalledProcessError as e:
        logger.error("Error running scraper: %s", e)
        logger.error("Error output: %s", e.stderr)
        return False
    except Exception as e:
        logger.exception("Unexpected error running scraper: %s", e)
        return False

if __name__ == "__main__":
    logger.info("Starting Somalia Statistics Scraper Scheduler")
    logger.info("Will run scraper every 20 minutes")
    
    # Schedule the scraper to run every 20 minutes
    schedule.every(20).minutes.do(run_scraper)
    
    # Also run immediately on startup
    logger.info("Running initial scraper job")
    run_scraper()
    
    # Keep the script running and checking the schedule
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute for pending jobs 