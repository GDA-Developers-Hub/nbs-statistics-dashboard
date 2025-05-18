import logging
from django.core.management.base import BaseCommand
from scraper_service.scraper.somalia_scraper import SomaliaStatsScraper
from scraper_service.scraper.models import ScraperJob
import traceback

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run the specialized Somalia statistics scraper to test without RabbitMQ'

    def add_arguments(self, parser):
        parser.add_argument(
            '--categories',
            nargs='+',
            help='Specific categories to scrape (demographics, economy, health, education, agriculture, inflation, poverty)',
        )
        
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Run in debug mode with detailed output',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Somalia statistics scraper test...'))
        
        # Set debug mode
        debug_mode = options.get('debug', False)
        
        # Run the scraper
        scraper = SomaliaStatsScraper()
        
        # Filter categories if specified
        if options.get('categories'):
            valid_categories = set(scraper.paths.keys())
            requested_categories = set(options['categories'])
            invalid_categories = requested_categories - valid_categories
            
            if invalid_categories:
                self.stdout.write(self.style.WARNING(
                    f'Invalid categories: {", ".join(invalid_categories)}. ' 
                    f'Valid options are: {", ".join(valid_categories)}'
                ))
            
            # Filter to only valid requested categories
            categories_to_scrape = requested_categories.intersection(valid_categories)
            scraper.paths = {k: v for k, v in scraper.paths.items() if k in categories_to_scrape}
            
            self.stdout.write(self.style.SUCCESS(
                f'Scraping specific categories: {", ".join(categories_to_scrape)}'
            ))
        
        job = None
        
        try:
            # Add stdout method to scraper for command output
            scraper.stdout = self.stdout
            
            # For debug mode
            if debug_mode:
                self.stdout.write("Running in DEBUG mode with detailed output")
                
            # Run the scraper (with just one category for testing if in debug mode)
            if debug_mode and not options.get('categories'):
                self.stdout.write("Debug mode: limiting to homepage only")
                # Just scrape the homepage in debug mode
                scraper.paths = {'demographics': '/statistics'}
                
            job = scraper.run()
            
            if job.status == ScraperJob.STATUS_COMPLETED:
                self.stdout.write(self.style.SUCCESS(
                    f'Scraper job completed successfully. '
                    f'Found: {job.items_found}, '
                    f'Processed: {job.items_processed}, '
                    f'Failed: {job.items_failed}'
                ))
                
                # Show summary of scraped items
                items = job.items.all()
                self.stdout.write(self.style.SUCCESS(f'Scraped {items.count()} items:'))
                
                for i, item in enumerate(items[:10]):  # Show up to 10 items
                    self.stdout.write(f"{i+1}. {item.title} from {item.source_url}")
                
                if items.count() > 10:
                    self.stdout.write(f"... and {items.count() - 10} more items")
                
            else:
                self.stdout.write(self.style.ERROR(
                    f'Scraper job failed: {job.error_message}'
                ))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error running Somalia scraper: {str(e)}'))
            if debug_mode:
                # Print full traceback in debug mode
                self.stdout.write(traceback.format_exc())
            logger.exception('Error in run_somalia_scraper_test command')
            
        self.stdout.write(self.style.SUCCESS('Somalia statistics scraper test finished')) 