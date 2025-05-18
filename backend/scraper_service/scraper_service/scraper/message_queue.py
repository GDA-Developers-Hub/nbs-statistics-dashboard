import json
import logging
import pika
from django.conf import settings
import uuid

logger = logging.getLogger(__name__)

def get_rabbitmq_connection():
    """
    Establish a connection to RabbitMQ server using settings.
    """
    config = settings.RABBITMQ_CONFIG
    
    parameters = pika.ConnectionParameters(
        host=config.get('host', 'localhost'),
        port=config.get('port', 5672),
        virtual_host=config.get('virtual_host', '/'),
        credentials=pika.PlainCredentials(
            username=config.get('username', 'guest'),
            password=config.get('password', 'guest')
        ),
        heartbeat=config.get('heartbeat', 600),
        connection_attempts=config.get('connection_attempts', 3),
        retry_delay=config.get('retry_delay', 5)
    )
    
    return pika.BlockingConnection(parameters)

def publish_scraped_items(items, batch_size=10):
    """
    Publish scraped items to RabbitMQ queue for ETL processing.
    
    Args:
        items: QuerySet of ScrapedItem objects to publish
        batch_size: Number of items to publish in a batch
    
    Returns:
        int: Number of items successfully published
    """
    if not items:
        logger.warning("No items to publish to message queue")
        return 0
    
    config = settings.RABBITMQ_CONFIG
    exchange = config.get('exchange', 'snbs')
    routing_key = config.get('scraper_queue', 'scraped_data')
    
    connection = None
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        # Declare exchange and queue
        channel.exchange_declare(
            exchange=exchange,
            exchange_type='direct',
            durable=True
        )
        
        channel.queue_declare(
            queue=routing_key,
            durable=True
        )
        
        channel.queue_bind(
            exchange=exchange,
            queue=routing_key,
            routing_key=routing_key
        )
        
        # Publish items in batches
        count = 0
        batch = []
        
        for item in items:
            # Create message
            message_id = str(uuid.uuid4())
            message = {
                'item_id': item.id,
                'item_type': item.item_type,
                'source_url': item.source_url,
                'content': item.content,
                'metadata': item.metadata,
                'message_id': message_id
            }
            
            # Add to batch
            batch.append((message_id, message))
            
            # If batch is full, publish
            if len(batch) >= batch_size:
                _publish_batch(channel, exchange, routing_key, batch, items)
                count += len(batch)
                batch = []
        
        # Publish any remaining items
        if batch:
            _publish_batch(channel, exchange, routing_key, batch, items)
            count += len(batch)
        
        return count
        
    except Exception as e:
        logger.error(f"Error publishing to message queue: {str(e)}")
        raise
    
    finally:
        if connection and connection.is_open:
            connection.close()

def _publish_batch(channel, exchange, routing_key, batch, items_queryset):
    """
    Publish a batch of messages to RabbitMQ and update the database.
    """
    for message_id, message in batch:
        try:
            # Publish message
            channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # persistent
                    message_id=message_id,
                    content_type='application/json'
                )
            )
            
            # Update ScrapedItem in database
            item_id = message['item_id']
            items_queryset.filter(id=item_id).update(
                message_id=message_id,
                queue_name=routing_key
            )
            
        except Exception as e:
            logger.error(f"Error publishing message {message_id}: {str(e)}")
            # Continue with other messages
