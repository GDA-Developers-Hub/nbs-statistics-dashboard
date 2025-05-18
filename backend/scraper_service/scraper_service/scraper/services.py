"""
Service layer for scraping operations.
Handles scheduled scraping and coordination.
"""
import logging
import threading
import time
from datetime import datetime, timedelta
from django.conf import settings
from django.core.management import call_command
from django.core.cache import cache
from django.utils import timezone

from .models import ScraperJob, ScrapedItem
from .realtime import real_time_manager

logger = logging.getLogger(__name__)

class ScraperSchedulerService:
    """
    Service to manage scheduled scraping operations.
    Ensures scraping operations run at the configured intervals.
    """
    def __init__(self):
        self.config = getattr(settings, 'SCRAPER_CONFIG', {})
        self.lock = threading.Lock()
        
        # Track last scrape times
        self.last_scrape_times = {
            'somalia_stats': None,
            'publications': None,
        }
        
        # Load schedule settings
        self.schedule_interval = self.config.get('schedule_interval', {
            'somalia_stats': '20m',  # Default to every 20 minutes
            'publications': '6h',    # Default to every 6 hours
        })
        
        # Parse schedule intervals to minutes
        self.schedule_minutes = {}
        for job_type, interval in self.schedule_interval.items():
            if interval.endswith('m'):
                minutes = int(interval[:-1])
            elif interval.endswith('h'):
                minutes = int(interval[:-1]) * 60
            else:
                minutes = int(interval)
            self.schedule_minutes[job_type] = minutes
            
        # Initialize last run times from the database
        self._load_last_run_times()
    
    def _load_last_run_times(self):
        """Load the last run times for each job type from the database."""
        try:
            # Get the most recent completed jobs for each type
            somalia_stats_job = ScraperJob.objects.filter(
                job_type=ScraperJob.TYPE_STATISTICS,
                status=ScraperJob.STATUS_COMPLETED
            ).order_by('-end_time').first()
            
            publications_job = ScraperJob.objects.filter(
                job_type=ScraperJob.TYPE_PUBLICATIONS,
                status=ScraperJob.STATUS_COMPLETED
            ).order_by('-end_time').first()
            
            # Update the last run times
            if somalia_stats_job and somalia_stats_job.end_time:
                self.last_scrape_times['somalia_stats'] = somalia_stats_job.end_time
                
            if publications_job and publications_job.end_time:
                self.last_scrape_times['publications'] = publications_job.end_time
                
            logger.info(f"Loaded last run times: {self.last_scrape_times}")
            
        except Exception as e:
            logger.error(f"Error loading last run times: {str(e)}")
    
    def should_run_scraper(self, job_type):
        """
        Check if a scraper should run based on its schedule.
        
        Args:
            job_type (str): The type of scraper job to check.
            
        Returns:
            bool: True if the scraper should run, False otherwise.
        """
        last_run = self.last_scrape_times.get(job_type)
        if not last_run:
            return True  # No previous runs, should run now
            
        # Calculate the scheduled interval in minutes
        interval_minutes = self.schedule_minutes.get(job_type, 20)  # Default to 20 minutes
        
        # Check if enough time has passed since the last run
        now = timezone.now()
        time_since_last_run = now - last_run
        
        return time_since_last_run >= timedelta(minutes=interval_minutes)
    
    def update_last_run_time(self, job_type):
        """Update the last run time for a job type to now."""
        with self.lock:
            self.last_scrape_times[job_type] = timezone.now()
    
    def run_scheduled_scraper(self, job_type):
        """
        Run a scraper job if it's scheduled to run.
        
        Args:
            job_type (str): The type of scraper job to run.
            
        Returns:
            bool: True if the scraper ran, False if it was not scheduled to run yet.
        """
        if not self.should_run_scraper(job_type):
            logger.info(f"Skipping {job_type} scraper: Not scheduled to run yet")
            return False
            
        with self.lock:
            # Double-check inside the lock to prevent race conditions
            if not self.should_run_scraper(job_type):
                return False
                
            logger.info(f"Running scheduled {job_type} scraper")
            
            try:
                # Update the last run time before running to prevent duplicate runs
                self.update_last_run_time(job_type)
                
                # Run the appropriate scraper
                if job_type == 'somalia_stats':
                    # Run the Somalia stats scraper
                    call_command('run_somalia_scraper_test')
                elif job_type == 'publications':
                    # Run just the publications category
                    call_command('run_somalia_scraper_test', '--categories', 'publications')
                else:
                    logger.warning(f"Unknown job type: {job_type}")
                    return False
                    
                logger.info(f"Completed scheduled {job_type} scraper")
                return True
                
            except Exception as e:
                logger.exception(f"Error running scheduled {job_type} scraper: {str(e)}")
                return False
    
    def check_and_run_all_scheduled_scrapers(self):
        """
        Check all scrapers and run those that are scheduled.
        
        Returns:
            dict: A dictionary with job types as keys and booleans as values,
                 indicating whether each scraper ran.
        """
        results = {}
        
        for job_type in self.schedule_minutes.keys():
            results[job_type] = self.run_scheduled_scraper(job_type)
            
        return results

# Create a singleton instance
scraper_scheduler = ScraperSchedulerService() 