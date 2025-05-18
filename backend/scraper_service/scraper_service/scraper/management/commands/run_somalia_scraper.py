import logging
from django.core.management.base import BaseCommand
from scraper_service.scraper.somalia_scraper import SomaliaStatsScraper
from scraper_service.scraper.models import ScraperJob
from scraper_service.scraper.message_queue import publish_scraped_items

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run the specialized Somalia statistics scraper to extract structured data from the SNBS website'

    def add_arguments(self, parser):
        parser.add_argument(
            '--publish',
            action='store_true',
            help='Publish scraped data to message queue for ETL processing',
        )
        parser.add_argument(
            '--categories',
            nargs='+',
            help='Specific categories to scrape (demographics, economy, health, education, agriculture, inflation, poverty)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Somalia statistics scraper...'))
        
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
            
            job = scraper.run()
            
            if job.status == ScraperJob.STATUS_COMPLETED:
                self.stdout.write(self.style.SUCCESS(
                    f'Scraper job completed successfully. '
                    f'Found: {job.items_found}, '
                    f'Processed: {job.items_processed}, '
                    f'Failed: {job.items_failed}'
                ))
                
                # Publish to message queue if requested
                if options['publish']:
                    items = job.items.filter(status='pending')
                    count = publish_scraped_items(items)
                    self.stdout.write(self.style.SUCCESS(f'Published {count} items to message queue'))
            else:
                self.stdout.write(self.style.ERROR(
                    f'Scraper job failed: {job.error_message}'
                ))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error running Somalia scraper: {str(e)}'))
            logger.exception('Error in run_somalia_scraper command')
            
        self.stdout.write(self.style.SUCCESS('Somalia statistics scraper finished')) 