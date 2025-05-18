"""
Direct Scraper for Somalia Statistics Dashboard

This script directly uses the scrapers.py module to scrape SNBS website
without requiring the full backend stack to be running.
"""
import sys
import os
import json
import datetime
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the backend directory to the path so we can import our modules
script_dir = Path(__file__).parent.absolute()
backend_dir = script_dir / 'backend'
sys.path.append(str(backend_dir))
sys.path.append(str(backend_dir / 'scraper_service'))

# Create output directory
output_dir = script_dir / 'scraped_data'
output_dir.mkdir(exist_ok=True)
stats_dir = output_dir / 'statistics'
stats_dir.mkdir(exist_ok=True)
pubs_dir = output_dir / 'publications'
pubs_dir.mkdir(exist_ok=True)

def main():
    """Run the scrapers directly"""
    try:
        # Import here to avoid errors until path is set up
        from scraper_service.scraper.scrapers import StatisticsScraper, PublicationsScraper

        logger.info("Starting direct scraper")
        
        # Create a basic settings module with minimal config
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraper_service.settings')
        
        # Basic environment variables
        os.environ['SNBS_BASE_URL'] = 'https://nbs.gov.so/'
        
        # Run statistics scraper
        try:
            logger.info("Running statistics scraper")
            stats_scraper = StatisticsScraper()
            stats_job = stats_scraper.run()
            
            # Save results
            stats_results = {
                'job_id': getattr(stats_job, 'id', None),
                'status': getattr(stats_job, 'status', 'unknown'),
                'items_found': getattr(stats_job, 'items_found', 0),
                'items_processed': getattr(stats_job, 'items_processed', 0),
                'items_failed': getattr(stats_job, 'items_failed', 0),
                'timestamp': datetime.datetime.now().isoformat(),
            }
            
            with open(stats_dir / 'stats_results.json', 'w') as f:
                json.dump(stats_results, f, indent=2)
                
            logger.info(f"Statistics scraper completed: found={stats_results['items_found']}, processed={stats_results['items_processed']}")
        except Exception as e:
            logger.error(f"Error running statistics scraper: {str(e)}")
        
        # Run publications scraper
        try:
            logger.info("Running publications scraper")
            pubs_scraper = PublicationsScraper()
            pubs_job = pubs_scraper.run()
            
            # Save results
            pubs_results = {
                'job_id': getattr(pubs_job, 'id', None),
                'status': getattr(pubs_job, 'status', 'unknown'),
                'items_found': getattr(pubs_job, 'items_found', 0),
                'items_processed': getattr(pubs_job, 'items_processed', 0),
                'items_failed': getattr(pubs_job, 'items_failed', 0),
                'timestamp': datetime.datetime.now().isoformat(),
            }
            
            with open(pubs_dir / 'pubs_results.json', 'w') as f:
                json.dump(pubs_results, f, indent=2)
                
            logger.info(f"Publications scraper completed: found={pubs_results['items_found']}, processed={pubs_results['items_processed']}")
        except Exception as e:
            logger.error(f"Error running publications scraper: {str(e)}")
            
        logger.info("Direct scraper completed")
            
    except ImportError as e:
        logger.error(f"Import error: {str(e)}")
        logger.error("Make sure you're running this script from the project root directory")
    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
