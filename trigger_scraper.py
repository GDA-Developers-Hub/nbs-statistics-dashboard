#!/usr/bin/env python
"""
Trigger Scraper - A script to trigger web scraping for Somalia Statistics Dashboard
"""
import requests
import time
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API endpoints
SCRAPER_SERVICE_URL = "http://localhost:8002/api/v1"
API_SERVICE_URL = "http://localhost:8000/api/v1"
AUTH_SERVICE_URL = "http://localhost:8001/api/auth"

def trigger_statistics_scraper():
    """Trigger the statistics scraper and monitor its progress"""
    try:
        # Trigger the scraper
        logger.info("Triggering statistics scraper...")
        response = requests.post(
            f"{SCRAPER_SERVICE_URL}/scraper/jobs/statistics/",
            json={"publish": True}
        )
        
        if response.status_code != 201 and response.status_code != 200:
            logger.error(f"Failed to trigger scraper: {response.status_code} - {response.text}")
            return False
        
        # Get the job ID from the response
        job_data = response.json()
        job_id = job_data.get('id')
        
        if not job_id:
            logger.error("No job ID returned from the API")
            return False
        
        logger.info(f"Scraper job started with ID: {job_id}")
        
        # Monitor the job status
        max_attempts = 60  # Wait for up to 5 minutes (60 * 5 seconds)
        for attempt in range(max_attempts):
            # Check job status
            status_response = requests.get(f"{SCRAPER_SERVICE_URL}/scraper/jobs/{job_id}/")
            
            if status_response.status_code != 200:
                logger.error(f"Failed to get job status: {status_response.status_code}")
                time.sleep(5)
                continue
            
            status_data = status_response.json()
            job_status = status_data.get('status')
            
            logger.info(f"Job status: {job_status} - Found: {status_data.get('items_found', 0)}, "
                       f"Processed: {status_data.get('items_processed', 0)}, "
                       f"Failed: {status_data.get('items_failed', 0)}")
            
            if job_status == 'completed':
                logger.info("Scraper job completed successfully!")
                return True
            elif job_status == 'failed':
                logger.error(f"Scraper job failed: {status_data.get('error_message')}")
                return False
            
            # Wait before checking again
            time.sleep(5)
        
        logger.warning("Maximum monitoring time reached, job may still be running")
        return False
        
    except Exception as e:
        logger.exception(f"Error triggering statistics scraper: {str(e)}")
        return False

def trigger_publications_scraper():
    """Trigger the publications scraper and monitor its progress"""
    try:
        # Trigger the scraper
        logger.info("Triggering publications scraper...")
        response = requests.post(
            f"{SCRAPER_SERVICE_URL}/scraper/jobs/publications/",
            json={"publish": True}
        )
        
        if response.status_code != 201 and response.status_code != 200:
            logger.error(f"Failed to trigger scraper: {response.status_code} - {response.text}")
            return False
        
        # Get the job ID from the response
        job_data = response.json()
        job_id = job_data.get('id')
        
        if not job_id:
            logger.error("No job ID returned from the API")
            return False
        
        logger.info(f"Scraper job started with ID: {job_id}")
        
        # Monitor the job status
        max_attempts = 120  # Wait for up to 10 minutes (120 * 5 seconds)
        for attempt in range(max_attempts):
            # Check job status
            status_response = requests.get(f"{SCRAPER_SERVICE_URL}/scraper/jobs/{job_id}/")
            
            if status_response.status_code != 200:
                logger.error(f"Failed to get job status: {status_response.status_code}")
                time.sleep(5)
                continue
            
            status_data = status_response.json()
            job_status = status_data.get('status')
            
            logger.info(f"Job status: {job_status} - Found: {status_data.get('items_found', 0)}, "
                       f"Processed: {status_data.get('items_processed', 0)}, "
                       f"Failed: {status_data.get('items_failed', 0)}")
            
            if job_status == 'completed':
                logger.info("Scraper job completed successfully!")
                return True
            elif job_status == 'failed':
                logger.error(f"Scraper job failed: {status_data.get('error_message')}")
                return False
            
            # Wait before checking again
            time.sleep(5)
        
        logger.warning("Maximum monitoring time reached, job may still be running")
        return False
        
    except Exception as e:
        logger.exception(f"Error triggering publications scraper: {str(e)}")
        return False

def check_etl_status():
    """Check the status of the ETL consumer"""
    try:
        response = requests.get(f"{SCRAPER_SERVICE_URL}/etl/status/")
        
        if response.status_code != 200:
            logger.error(f"Failed to get ETL status: {response.status_code}")
            return False
        
        status_data = response.json()
        logger.info(f"ETL consumer status: {status_data.get('status')}")
        
        return status_data.get('status') == 'running'
        
    except Exception as e:
        logger.exception(f"Error checking ETL status: {str(e)}")
        return False

def main():
    """Main function to trigger scrapers"""
    logger.info("Starting Somalia Statistics Dashboard scraper")
    
    # First check if the ETL consumer is running
    logger.info("Checking ETL consumer status...")
    if not check_etl_status():
        logger.warning("ETL consumer does not appear to be running, data may not be processed")
    
    # Trigger statistics scraper
    logger.info("Starting statistics scraper...")
    if trigger_statistics_scraper():
        logger.info("Statistics scraper completed successfully")
    else:
        logger.error("Statistics scraper failed or timed out")
    
    # Trigger publications scraper
    logger.info("Starting publications scraper...")
    if trigger_publications_scraper():
        logger.info("Publications scraper completed successfully")
    else:
        logger.error("Publications scraper failed or timed out")
    
    logger.info("All scraping jobs completed")

if __name__ == "__main__":
    main()
