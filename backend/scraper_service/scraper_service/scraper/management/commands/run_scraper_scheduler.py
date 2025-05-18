import logging
import time
import traceback
from django.core.management.base import BaseCommand
from scraper_service.scraper.services import scraper_scheduler

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run the scraper scheduler service once or continuously'

    def add_arguments(self, parser):
        parser.add_argument(
            '--continuous',
            action='store_true',
            help='Run in continuous mode, checking every minute if scrapers should run',
        )
        
        parser.add_argument(
            '--job-type',
            choices=['somalia_stats', 'publications', 'all'],
            default='all',
            help='Specify which job type to run (default: all)',
        )
        
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force run even if not scheduled',
        )
        
        parser.add_argument(
            '--interval',
            type=int,
            default=60,
            help='Check interval in seconds when in continuous mode (default: 60)',
        )

    def handle(self, *args, **options):
        continuous_mode = options.get('continuous', False)
        job_type = options.get('job_type', 'all')
        force = options.get('force', False)
        check_interval = options.get('interval', 60)
        
        if continuous_mode:
            self.stdout.write(self.style.SUCCESS(
                f'Starting scraper scheduler in continuous mode. '
                f'Will check every {check_interval} seconds.'
            ))
            
            try:
                self.run_continuous(job_type, force, check_interval)
            except KeyboardInterrupt:
                self.stdout.write(self.style.SUCCESS('Scheduler stopped by user'))
        else:
            self.stdout.write(self.style.SUCCESS('Running scraper scheduler once'))
            self.run_once(job_type, force)
    
    def run_once(self, job_type, force):
        """Run the scheduler once for the specified job type."""
        try:
            if job_type == 'all':
                if force:
                    self.stdout.write('Force running all scrapers')
                    # Force run all scrapers
                    for scraper_type in scraper_scheduler.schedule_minutes.keys():
                        self.run_scraper(scraper_type, force=True)
                else:
                    # Check and run all scheduled scrapers
                    results = scraper_scheduler.check_and_run_all_scheduled_scrapers()
                    for job_type, ran in results.items():
                        status = 'Ran' if ran else 'Skipped'
                        self.stdout.write(f'{status} {job_type} scraper')
            else:
                # Run a specific scraper
                self.run_scraper(job_type, force)
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error in scheduler: {str(e)}'))
            self.stdout.write(traceback.format_exc())
    
    def run_continuous(self, job_type, force, check_interval):
        """Run the scheduler in continuous mode."""
        if force:
            self.stdout.write(self.style.WARNING(
                'Force flag is ignored in continuous mode after initial run'
            ))
            
        # Initial run with force if specified
        self.run_once(job_type, force)
        
        # Then run in a loop
        while True:
            try:
                # Sleep until next check
                time.sleep(check_interval)
                
                # Check and run
                self.stdout.write(f'Checking if scrapers should run at {time.strftime("%Y-%m-%d %H:%M:%S")}')
                
                if job_type == 'all':
                    results = scraper_scheduler.check_and_run_all_scheduled_scrapers()
                    for job_type, ran in results.items():
                        if ran:
                            self.stdout.write(self.style.SUCCESS(f'Ran {job_type} scraper'))
                else:
                    # Run a specific scraper if scheduled
                    if scraper_scheduler.run_scheduled_scraper(job_type):
                        self.stdout.write(self.style.SUCCESS(f'Ran {job_type} scraper'))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error in scheduler loop: {str(e)}'))
                # Continue the loop despite errors
    
    def run_scraper(self, job_type, force=False):
        """Run a specific scraper."""
        if force or scraper_scheduler.should_run_scraper(job_type):
            self.stdout.write(f'Running {job_type} scraper')
            
            # Force update the last run time if we're forcing a run
            if force:
                scraper_scheduler.update_last_run_time(job_type)
                
            # Run the scraper
            if job_type == 'somalia_stats':
                scraper_scheduler.run_scheduled_scraper('somalia_stats')
            elif job_type == 'publications':
                scraper_scheduler.run_scheduled_scraper('publications')
            
            self.stdout.write(self.style.SUCCESS(f'Completed {job_type} scraper'))
        else:
            self.stdout.write(f'Skipping {job_type} scraper: Not scheduled to run yet') 