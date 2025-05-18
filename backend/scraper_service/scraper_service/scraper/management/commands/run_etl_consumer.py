import logging
import time
from django.core.management.base import BaseCommand
from scraper_service.scraper.etl.consumer import start_consumer

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run the ETL consumer process to process scraped data from the message queue'

    def add_arguments(self, parser):
        parser.add_argument(
            '--timeout',
            type=int,
            default=0,
            help='Run for specified number of seconds then exit (0 for no timeout)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting ETL consumer process...'))
        
        timeout = options.get('timeout', 0)
        consumer = None
        
        try:
            # Start the consumer
            consumer = start_consumer()
            
            if timeout > 0:
                self.stdout.write(self.style.SUCCESS(f'ETL consumer will run for {timeout} seconds'))
                time.sleep(timeout)
                if consumer:
                    consumer.stop()
                self.stdout.write(self.style.SUCCESS('ETL consumer stopped after timeout'))
            else:
                self.stdout.write(self.style.SUCCESS('ETL consumer running indefinitely. Press Ctrl+C to stop.'))
                # Keep the process running
                while True:
                    time.sleep(10)
                    
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Received keyboard interrupt, stopping ETL consumer'))
            if consumer:
                consumer.stop()
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error running ETL consumer: {str(e)}'))
            logger.exception('Error in run_etl_consumer command')
            if consumer:
                consumer.stop()
            
        self.stdout.write(self.style.SUCCESS('ETL consumer process finished'))
