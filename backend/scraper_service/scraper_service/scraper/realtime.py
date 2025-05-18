"""
Utilities for real-time data scraping and management.
"""
import logging
import threading
import time
from datetime import datetime, timedelta
from django.conf import settings
from django.core.management import call_command
from django.core.cache import cache
from .models import ScraperJob, ScrapedItem

logger = logging.getLogger(__name__)

class RealTimeDataManager:
    """
    Manages real-time data scraping and access.
    """
    def __init__(self):
        """Initialize the real-time data manager."""
        self.lock = threading.Lock()
        self.is_scraping = False
        self.last_scrape_time = {}
        self.scraper_config = getattr(settings, 'SCRAPER_CONFIG', {})
        self.real_time_categories = self.scraper_config.get('real_time_categories', 
                                                          ['demographics', 'economy', 'inflation'])
        
    def get_latest_data(self, category=None):
        """
        Get the latest scraped data for a category.
        
        Args:
            category (str, optional): Category to get data for. If None, returns all categories.
            
        Returns:
            dict: Dictionary with latest data for the requested category/categories.
        """
        # Get the latest completed job
        latest_job = ScraperJob.objects.filter(
            status=ScraperJob.STATUS_COMPLETED
        ).order_by('-end_time').first()
        
        if not latest_job:
            return {
                'status': 'error',
                'message': 'No completed scraper jobs found'
            }
        
        # Build query for items
        query = {'job': latest_job}
        if category:
            query['metadata__category'] = category
        
        # Get the items
        items = ScrapedItem.objects.filter(**query)
        
        # Format the response
        result = {
            'job_id': latest_job.id,
            'job_completed_at': latest_job.end_time,
            'total_items': items.count(),
            'last_updated': datetime.now().isoformat(),
            'categories': {}
        }
        
        # Group by category
        for item in items:
            item_category = item.metadata.get('category', 'other') if item.metadata else 'other'
            if item_category not in result['categories']:
                result['categories'][item_category] = []
                
            result['categories'][item_category].append({
                'id': item.id,
                'title': item.title,
                'time_period': item.metadata.get('time_period', '') if item.metadata else '',
                'url': f'/api/scraped-items/{item.id}/data/'
            })
        
        return result
    
    def trigger_scrape(self, categories=None, force=False):
        """
        Trigger a scraping operation for the specified categories.
        
        Args:
            categories (list, optional): List of categories to scrape. If None, uses real_time_categories.
            force (bool, optional): Force scraping even if it was recently done.
            
        Returns:
            dict: Status of the scraping operation.
        """
        with self.lock:
            if self.is_scraping and not force:
                return {
                    'status': 'in_progress',
                    'message': 'A scraping operation is already in progress'
                }
            
            # Use default categories if none provided
            if not categories:
                categories = self.real_time_categories
            
            # Check if we've scraped recently (within 5 minutes) to avoid too frequent requests
            now = datetime.now()
            can_scrape = force  # Always scrape if force=True
            
            if not can_scrape:
                # Check if any category is due for scraping
                for category in categories:
                    last_time = self.last_scrape_time.get(category)
                    if not last_time or (now - last_time) > timedelta(minutes=5):
                        can_scrape = True
                        break
            
            if not can_scrape:
                return {
                    'status': 'skipped',
                    'message': 'Data was scraped recently. Use force=True to override.',
                    'last_scrape_times': {k: v.isoformat() for k, v in self.last_scrape_time.items()}
                }
            
            # Set scraping flag
            self.is_scraping = True
        
        try:
            # Start scraper in background thread
            thread = threading.Thread(
                target=self._run_scraper,
                args=(categories,)
            )
            thread.daemon = True
            thread.start()
            
            return {
                'status': 'started',
                'message': f'Started scraping categories: {", ".join(categories)}',
                'categories': categories
            }
            
        except Exception as e:
            logger.exception(f"Error starting scraper: {str(e)}")
            with self.lock:
                self.is_scraping = False
            
            return {
                'status': 'error',
                'message': f'Error starting scraper: {str(e)}'
            }
    
    def _run_scraper(self, categories):
        """
        Run the scraper in a background thread.
        
        Args:
            categories (list): List of categories to scrape.
        """
        try:
            logger.info(f"Starting real-time scrape for categories: {', '.join(categories)}")
            
            # Run the scraper command with the specified categories
            call_command('run_somalia_scraper_test', '--categories', *categories)
            
            # Update last scrape time
            now = datetime.now()
            with self.lock:
                for category in categories:
                    self.last_scrape_time[category] = now
                    
                # Cache the latest data
                latest_data = self.get_latest_data()
                cache.set('latest_somalia_data', latest_data, 3600)  # Cache for 1 hour
                
                logger.info(f"Completed real-time scrape for categories: {', '.join(categories)}")
                
        except Exception as e:
            logger.exception(f"Error during real-time scraping: {str(e)}")
            
        finally:
            with self.lock:
                self.is_scraping = False

# Create a singleton instance
real_time_manager = RealTimeDataManager() 