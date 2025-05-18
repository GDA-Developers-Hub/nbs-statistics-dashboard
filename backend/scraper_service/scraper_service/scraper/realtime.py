"""
Utilities for real-time data scraping and management.
"""
import logging
import threading
import time
import json
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
            'job_completed_at': latest_job.end_time.isoformat() if latest_job.end_time else None,
            'job_duration': latest_job.duration,
            'total_items': items.count(),
            'last_updated': datetime.now().isoformat(),
            'categories': {}
        }
        
        # Group by category
        for item in items:
            item_category = item.metadata.get('category', 'other') if item.metadata else 'other'
            if item_category not in result['categories']:
                result['categories'][item_category] = {
                    'items': [],
                    'summary': {
                        'count': 0,
                        'latest_period': '',
                        'updated_at': item.updated_at.isoformat() if item.updated_at else None
                    }
                }
            
            # Extract data based on item type and format
            formatted_data = self._format_item_data(item)
            
            # Add the item to the category
            result['categories'][item_category]['items'].append({
                'id': item.id,
                'title': item.title,
                'time_period': item.metadata.get('time_period', '') if item.metadata else '',
                'url': f'/api/scraped-items/{item.id}/data/',
                'data_preview': formatted_data
            })
            
            # Update the summary
            result['categories'][item_category]['summary']['count'] += 1
            
            # Track the latest time period
            time_period = item.metadata.get('time_period', '') if item.metadata else ''
            current_latest = result['categories'][item_category]['summary']['latest_period']
            if time_period and (not current_latest or time_period > current_latest):
                result['categories'][item_category]['summary']['latest_period'] = time_period
        
        # Add category-specific statistics
        for category_name, category_data in result['categories'].items():
            if category_name == 'demographics':
                category_data['summary']['total_population'] = self._get_total_population(category_data['items'])
            elif category_name == 'economy':
                category_data['summary']['gdp_growth'] = self._get_latest_gdp_growth(category_data['items'])
            elif category_name == 'inflation':
                category_data['summary']['current_inflation'] = self._get_current_inflation(category_data['items'])
            elif category_name == 'health':
                category_data['summary']['vaccination_coverage'] = self._get_vaccination_coverage(category_data['items'])
            elif category_name == 'education':
                category_data['summary']['literacy_rate'] = self._get_literacy_rate(category_data['items'])
        
        return result
    
    def _format_item_data(self, item):
        """Format item data for preview based on its type and category."""
        try:
            if not item.content:
                return None
                
            # Parse content
            content = item.content
            if isinstance(content, str):
                try:
                    content = json.loads(content)
                except json.JSONDecodeError:
                    return {'error': 'Invalid JSON content'}
            
            # Format based on category
            category = item.metadata.get('category', '') if item.metadata else ''
            
            if category == 'demographics':
                # Return first few rows of population data
                if isinstance(content, list) and len(content) > 0:
                    return content[:3]  # First 3 items
                return content
                
            elif category == 'economy':
                # Return the most recent economic indicators
                if isinstance(content, list) and len(content) > 0:
                    # Sort by year if possible
                    if 'Year' in content[0]:
                        sorted_data = sorted(content, key=lambda x: x.get('Year', 0), reverse=True)
                        return sorted_data[0] if sorted_data else None
                return content[0] if isinstance(content, list) and len(content) > 0 else content
                
            elif category == 'inflation':
                # Return the latest inflation data
                if isinstance(content, list) and len(content) > 0:
                    # Sort by date if possible
                    if 'Date' in content[0]:
                        sorted_data = sorted(content, key=lambda x: x.get('Date', ''), reverse=True)
                        return sorted_data[0] if sorted_data else None
                    # Sort by year if date not available
                    elif 'Year' in content[0]:
                        sorted_data = sorted(content, key=lambda x: x.get('Year', 0), reverse=True)
                        return sorted_data[0] if sorted_data else None
                return content[0] if isinstance(content, list) and len(content) > 0 else content
                
            # Default formatting for other categories
            if isinstance(content, list):
                return content[:3] if len(content) > 3 else content  # First 3 items or all if less
            return content
            
        except Exception as e:
            logger.exception(f"Error formatting item data: {str(e)}")
            return {'error': str(e)}
    
    def _get_total_population(self, items):
        """Extract the total population from demographics items."""
        try:
            for item in items:
                if 'data_preview' in item and item['data_preview']:
                    # Look for the most recent year
                    latest_year = None
                    latest_population = 0
                    
                    data = item['data_preview']
                    if isinstance(data, list):
                        for row in data:
                            # Check for population keys
                            for key in row:
                                if 'Population' in key and isinstance(row[key], (int, float)):
                                    year = key.replace('Population_', '')
                                    if year.isdigit() and (latest_year is None or int(year) > latest_year):
                                        latest_year = int(year)
                                        latest_population = row[key]
                    
                    if latest_year and latest_population:
                        return {
                            'year': latest_year,
                            'value': latest_population
                        }
            return None
        except Exception as e:
            logger.exception(f"Error extracting total population: {str(e)}")
            return None
    
    def _get_latest_gdp_growth(self, items):
        """Extract the latest GDP growth rate from economy items."""
        try:
            for item in items:
                if 'data_preview' in item and item['data_preview']:
                    data = item['data_preview']
                    if isinstance(data, dict) and 'GDP_Growth_Rate' in data and 'Year' in data:
                        return {
                            'year': data['Year'],
                            'value': data['GDP_Growth_Rate']
                        }
            return None
        except Exception as e:
            logger.exception(f"Error extracting GDP growth: {str(e)}")
            return None
    
    def _get_current_inflation(self, items):
        """Extract the current inflation rate from inflation items."""
        try:
            for item in items:
                if 'data_preview' in item and item['data_preview']:
                    data = item['data_preview']
                    if isinstance(data, dict):
                        # Try different key patterns for inflation
                        for key in ['Inflation_Rate', 'CPI', 'Annual_Inflation']:
                            if key in data:
                                period = data.get('Date', data.get('Year', ''))
                                return {
                                    'period': period,
                                    'value': data[key]
                                }
            return None
        except Exception as e:
            logger.exception(f"Error extracting inflation rate: {str(e)}")
            return None
    
    def _get_vaccination_coverage(self, items):
        """Extract the vaccination coverage from health items."""
        try:
            # Implementation for vaccination data
            return None  # Placeholder
        except Exception as e:
            logger.exception(f"Error extracting vaccination coverage: {str(e)}")
            return None
    
    def _get_literacy_rate(self, items):
        """Extract the literacy rate from education items."""
        try:
            # Implementation for literacy rate data
            return None  # Placeholder
        except Exception as e:
            logger.exception(f"Error extracting literacy rate: {str(e)}")
            return None
    
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