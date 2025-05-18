import logging
import time
import threading
import schedule
from django.core.management import call_command
from django.conf import settings

logger = logging.getLogger(__name__)

class ScraperScheduler:
    """
    Scheduler for running scraper jobs at regular intervals.
    """
    def __init__(self):
        self.scheduler_thread = None
        self.stop_event = threading.Event()
        self.scraper_config = getattr(settings, 'SCRAPER_CONFIG', {})
        self.schedule_interval = self.scraper_config.get('schedule_interval', {})
        
    def start(self):
        """
        Start the scheduler in a background thread.
        """
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            logger.warning("Scheduler is already running")
            return
            
        self.stop_event.clear()
        self.scheduler_thread = threading.Thread(target=self._run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        logger.info("Scraper scheduler started")
        
    def stop(self):
        """
        Stop the scheduler thread.
        """
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.stop_event.set()
            self.scheduler_thread.join(timeout=5)
            logger.info("Scraper scheduler stopped")
        else:
            logger.warning("Scheduler is not running")
            
    def _run_scheduler(self):
        """
        Run the scheduler loop.
        """
        # Schedule the scraper jobs
        self._schedule_jobs()
        
        # Run the scheduler loop
        while not self.stop_event.is_set():
            schedule.run_pending()
            time.sleep(1)
            
    def _schedule_jobs(self):
        """
        Set up the scheduled jobs.
        """
        # Schedule Somalia Statistics Scraper
        somalia_interval = self.schedule_interval.get('somalia_stats', '24h')
        self._schedule_somalia_scraper(somalia_interval)
        
        # Schedule Publications Scraper
        publications_interval = self.schedule_interval.get('publications', '24h')
        self._schedule_publications_scraper(publications_interval)
        
        # Log all scheduled jobs
        logger.info("Scheduled jobs:")
        for job in schedule.get_jobs():
            logger.info(f" - {job.job_func.__name__} (next run: {job.next_run})")
            
    def _schedule_somalia_scraper(self, interval):
        """
        Schedule the Somalia statistics scraper.
        """
        # Parse interval
        value, unit = self._parse_interval(interval)
        
        if unit == 'h':
            job = schedule.every(value).hours.do(self._run_somalia_scraper)
            logger.info(f"Scheduled Somalia statistics scraper to run every {value} hours")
        elif unit == 'm':
            job = schedule.every(value).minutes.do(self._run_somalia_scraper)
            logger.info(f"Scheduled Somalia statistics scraper to run every {value} minutes")
        elif unit == 'd':
            job = schedule.every(value).days.do(self._run_somalia_scraper)
            logger.info(f"Scheduled Somalia statistics scraper to run every {value} days")
        else:
            job = schedule.every().day.at("01:00").do(self._run_somalia_scraper)
            logger.info("Scheduled Somalia statistics scraper to run daily at 1:00 AM")
    
    def _schedule_publications_scraper(self, interval):
        """
        Schedule the publications scraper.
        """
        # Parse interval
        value, unit = self._parse_interval(interval)
        
        if unit == 'h':
            job = schedule.every(value).hours.do(self._run_publications_scraper)
            logger.info(f"Scheduled publications scraper to run every {value} hours")
        elif unit == 'm':
            job = schedule.every(value).minutes.do(self._run_publications_scraper)
            logger.info(f"Scheduled publications scraper to run every {value} minutes")
        elif unit == 'd':
            job = schedule.every(value).days.do(self._run_publications_scraper)
            logger.info(f"Scheduled publications scraper to run every {value} days")
        else:
            job = schedule.every().day.at("02:00").do(self._run_publications_scraper)
            logger.info("Scheduled publications scraper to run daily at 2:00 AM")
    
    def _parse_interval(self, interval):
        """
        Parse interval string into value and unit.
        """
        if isinstance(interval, (int, float)):
            return int(interval), 'm'  # Default to minutes
            
        try:
            value = int(interval[:-1])
            unit = interval[-1].lower()
            if unit not in ['m', 'h', 'd']:
                raise ValueError(f"Unknown time unit: {unit}")
            return value, unit
        except (ValueError, IndexError):
            logger.warning(f"Invalid interval format: {interval}. Using default (24h).")
            return 24, 'h'
    
    def _run_somalia_scraper(self):
        """
        Run the Somalia statistics scraper.
        """
        logger.info("Running Somalia statistics scraper")
        try:
            call_command('run_somalia_scraper', publish=True)
            logger.info("Somalia statistics scraper completed")
        except Exception as e:
            logger.exception(f"Error running Somalia statistics scraper: {str(e)}")
    
    def _run_publications_scraper(self):
        """
        Run the publications scraper.
        """
        logger.info("Running publications scraper")
        try:
            call_command('run_publications_scraper', publish=True)
            logger.info("Publications scraper completed")
        except Exception as e:
            logger.exception(f"Error running publications scraper: {str(e)}")


# Singleton instance
scheduler = ScraperScheduler() 