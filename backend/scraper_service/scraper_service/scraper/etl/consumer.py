import json
import logging
import pika
import time
from threading import Thread
from django.conf import settings
from django.db import transaction

from ..models import ScrapedItem
from .processors import HTMLTableProcessor, PDFTableProcessor, DataCategorizer

logger = logging.getLogger(__name__)

class MessageQueueConsumer:
    """
    Consume messages from RabbitMQ for ETL processing.
    """
    def __init__(self):
        self.config = settings.RABBITMQ_CONFIG
        self.exchange = self.config.get('exchange', 'snbs')
        self.statistics_queue = self.config.get('statistics_queue', 'statistics_data')
        self.publications_queue = self.config.get('publications_queue', 'publications_data')
        self.connection = None
        self.channel = None
        self.running = False
        
    def connect(self):
        """
        Connect to RabbitMQ server.
        """
        parameters = pika.ConnectionParameters(
            host=self.config.get('host', 'localhost'),
            port=self.config.get('port', 5672),
            virtual_host=self.config.get('virtual_host', '/'),
            credentials=pika.PlainCredentials(
                username=self.config.get('username', 'guest'),
                password=self.config.get('password', 'guest')
            ),
            heartbeat=self.config.get('heartbeat', 600),
            connection_attempts=self.config.get('connection_attempts', 3),
            retry_delay=self.config.get('retry_delay', 5)
        )
        
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        
        # Declare exchange
        self.channel.exchange_declare(
            exchange=self.exchange,
            exchange_type='direct',
            durable=True
        )
        
        # Declare queues
        self.channel.queue_declare(
            queue=self.statistics_queue,
            durable=True
        )
        
        self.channel.queue_declare(
            queue=self.publications_queue,
            durable=True
        )
        
        # Bind queues to exchange
        self.channel.queue_bind(
            exchange=self.exchange,
            queue=self.statistics_queue,
            routing_key=self.statistics_queue
        )
        
        self.channel.queue_bind(
            exchange=self.exchange,
            queue=self.publications_queue,
            routing_key=self.publications_queue
        )
        
        # Set prefetch count to control message dispatching
        self.channel.basic_qos(prefetch_count=1)
        
        logger.info(f"Connected to RabbitMQ at {self.config.get('host')}:{self.config.get('port')}")
        
    def consume(self):
        """
        Start consuming messages from queues.
        """
        try:
            # Connect if not connected
            if not self.connection or self.connection.is_closed:
                self.connect()
            
            # Set up consumers
            self.channel.basic_consume(
                queue=self.statistics_queue,
                on_message_callback=self.process_message,
                auto_ack=False
            )
            
            self.channel.basic_consume(
                queue=self.publications_queue,
                on_message_callback=self.process_message,
                auto_ack=False
            )
            
            logger.info(f"Started consuming from queues: {self.statistics_queue}, {self.publications_queue}")
            
            # Start consuming
            self.running = True
            self.channel.start_consuming()
            
        except Exception as e:
            logger.exception(f"Error in message consumer: {str(e)}")
            self.cleanup()
    
    def process_message(self, channel, method, properties, body):
        """
        Process a message from the queue.
        """
        try:
            message = json.loads(body)
            
            logger.info(f"Processing message {properties.message_id} from {method.routing_key}")
            
            # Get the item ID from the message
            item_id = message.get('item_id')
            
            if not item_id:
                logger.error(f"Missing item_id in message: {message}")
                channel.basic_ack(delivery_tag=method.delivery_tag)
                return
            
            # Process the item
            with transaction.atomic():
                # Get the scraped item from the database
                try:
                    item = ScrapedItem.objects.get(id=item_id)
                except ScrapedItem.DoesNotExist:
                    logger.error(f"ScrapedItem {item_id} not found")
                    channel.basic_ack(delivery_tag=method.delivery_tag)
                    return
                
                # Process based on item type
                if item.item_type == ScrapedItem.TYPE_HTML_TABLE:
                    processor = HTMLTableProcessor()
                elif item.item_type == ScrapedItem.TYPE_PDF_TABLE:
                    processor = PDFTableProcessor()
                else:
                    logger.error(f"Unsupported item type: {item.item_type}")
                    item.status = ScrapedItem.STATUS_FAILED
                    item.error_message = f"Unsupported item type: {item.item_type}"
                    item.save()
                    channel.basic_ack(delivery_tag=method.delivery_tag)
                    return
                
                # Process the item content
                try:
                    # Process the content
                    processor.load(item.content).process()
                    result = processor.get_result()
                    
                    # Categorize the data
                    categorizer = DataCategorizer(result['data'], result['metadata'])
                    categories = categorizer.categorize()
                    
                    # Update the item with processed data
                    item.metadata.update({
                        'processed_metadata': result['metadata'],
                        'categories': categories
                    })
                    
                    # Update the item status
                    item.status = ScrapedItem.STATUS_PROCESSED
                    item.save()
                    
                    # Forward to the appropriate API service for database insertion
                    # This would normally call an API endpoint or message queue
                    # For now, we'll just log it
                    logger.info(f"Successfully processed item {item_id}")
                    logger.info(f"Data categories: {categories}")
                    
                except Exception as e:
                    logger.exception(f"Error processing item {item_id}: {str(e)}")
                    item.status = ScrapedItem.STATUS_FAILED
                    item.error_message = str(e)
                    item.save()
            
            # Acknowledge the message
            channel.basic_ack(delivery_tag=method.delivery_tag)
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in message: {str(e)}")
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.exception(f"Error processing message: {str(e)}")
            channel.basic_ack(delivery_tag=method.delivery_tag)
    
    def cleanup(self):
        """
        Clean up connections.
        """
        try:
            if self.channel and self.channel.is_open:
                self.channel.stop_consuming()
                
            if self.connection and self.connection.is_open:
                self.connection.close()
                
            self.running = False
            logger.info("Message consumer stopped and connections closed")
        except Exception as e:
            logger.exception(f"Error during cleanup: {str(e)}")
    
    def start(self):
        """
        Start the consumer in a separate thread.
        """
        thread = Thread(target=self.consume)
        thread.daemon = True
        thread.start()
        return thread
    
    def stop(self):
        """
        Stop the consumer.
        """
        self.running = False
        self.cleanup()


def start_consumer():
    """
    Start the message queue consumer.
    """
    consumer = MessageQueueConsumer()
    
    try:
        # Start consuming in a separate thread
        thread = consumer.start()
        logger.info("Message queue consumer started")
        
        # Keep the main thread alive
        while consumer.running:
            time.sleep(1)
            
        return consumer
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, stopping consumer")
        consumer.stop()
        
    except Exception as e:
        logger.exception(f"Error in message queue consumer: {str(e)}")
        consumer.stop()
        
    return None
