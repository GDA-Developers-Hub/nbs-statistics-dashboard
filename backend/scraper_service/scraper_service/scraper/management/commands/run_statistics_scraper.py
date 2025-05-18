import logging
from django.core.management.base import BaseCommand
from scraper_service.scraper.scrapers import StatisticsScraper
from scraper_service.scraper.models import ScraperJob
from scraper_service.scraper.message_queue import publish_scraped_items

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run the statistics scraper to extract data from HTML tables on the SNBS website'

    def add_arguments(self, parser):
        parser.add_argument(
            '--publish',
            action='store_true',
            help='Publish scraped data to message queue for ETL processing',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting statistics scraper...'))
        
        # Run the scraper
        scraper = StatisticsScraper()
        job = None
        
        try:
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
                    items = job.items.filter(status=ScraperJob.STATUS_PENDING)
                    count = publish_scraped_items(items)
                    self.stdout.write(self.style.SUCCESS(f'Published {count} items to message queue'))
            else:
                self.stdout.write(self.style.ERROR(
                    f'Scraper job failed: {job.error_message}'
                ))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error running scraper: {str(e)}'))
            logger.exception('Error in run_statistics_scraper command')
            
        self.stdout.write(self.style.SUCCESS('Statistics scraper finished'))
