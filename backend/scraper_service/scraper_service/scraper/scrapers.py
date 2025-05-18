import os
import time
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tabula
import pandas as pd
from django.conf import settings
from datetime import datetime
from .models import ScraperJob, ScrapedItem

logger = logging.getLogger(__name__)

class BaseScraper:
    """
    Base scraper class with common functionality for all scrapers.
    """
    def __init__(self):
        self.config = settings.SCRAPER_CONFIG
        self.base_url = self.config.get('base_url')
        self.user_agent = self.config.get('user_agent')
        self.request_timeout = self.config.get('request_timeout')
        self.request_delay = self.config.get('request_delay')
        self.max_retries = self.config.get('max_retries')
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.user_agent
        })
    
    def fetch_page(self, url):
        """
        Fetch a web page with retry mechanism.
        """
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.get(url, timeout=self.request_timeout)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"Attempt {attempt + 1} failed for {url}. Retrying in {wait_time}s. Error: {str(e)}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed to fetch {url} after {self.max_retries} attempts: {str(e)}")
                    raise
            
            # Respect rate limiting
            time.sleep(self.request_delay)
    
    def parse_html(self, content):
        """
        Parse HTML content with BeautifulSoup.
        """
        return BeautifulSoup(content, 'html.parser')
    
    def get_absolute_url(self, relative_url):
        """
        Convert relative URL to absolute URL.
        """
        return urljoin(self.base_url, relative_url)
    
    def log_job_start(self, job_type, url):
        """
        Create and log a new scraper job.
        """
        job = ScraperJob.objects.create(
            job_type=job_type,
            url=url,
            status=ScraperJob.STATUS_RUNNING
        )
        return job
    
    def log_job_complete(self, job, items_found, items_processed, items_failed=0):
        """
        Update job with completion details.
        """
        job.status = ScraperJob.STATUS_COMPLETED
        job.end_time = datetime.now()
        job.items_found = items_found
        job.items_processed = items_processed
        job.items_failed = items_failed
        job.save()
        
        logger.info(f"Job completed: {job}. Found: {items_found}, Processed: {items_processed}, Failed: {items_failed}")
        return job
    
    def log_job_failed(self, job, error_message):
        """
        Update job with failure details.
        """
        job.status = ScraperJob.STATUS_FAILED
        job.end_time = datetime.now()
        job.error_message = error_message
        job.save()
        
        logger.error(f"Job failed: {job}. Error: {error_message}")
        return job

class StatisticsScraper(BaseScraper):
    """
    Scraper for HTML tables on statistics pages.
    """
    def __init__(self):
        super().__init__()
        self.statistics_path = self.config.get('statistics_path')
    
    def run(self):
        """
        Run the statistics scraper job.
        """
        statistics_url = self.get_absolute_url(self.statistics_path)
        
        # Create job record
        job = self.log_job_start(ScraperJob.TYPE_STATISTICS, statistics_url)
        
        try:
            # Start by fetching the main statistics page
            response = self.fetch_page(statistics_url)
            soup = self.parse_html(response.text)
            
            # Find links to statistics pages (this will be specific to the SNBS website structure)
            # For this example, we'll look for links in the main content area
            stat_links = []
            content_area = soup.find('div', class_='main-content')  # Adjust selector based on actual site structure
            
            if content_area:
                links = content_area.find_all('a', href=True)
                for link in links:
                    href = link.get('href')
                    # Filter for statistics pages (adjust the condition based on actual link patterns)
                    if 'statistics' in href.lower() or 'stats' in href.lower():
                        stat_links.append(self.get_absolute_url(href))
            
            # Record how many statistics pages we found
            items_found = len(stat_links)
            items_processed = 0
            items_failed = 0
            
            # Process each statistics page
            for link in stat_links:
                try:
                    self.process_statistics_page(job, link)
                    items_processed += 1
                except Exception as e:
                    logger.error(f"Error processing statistics page {link}: {str(e)}")
                    items_failed += 1
                    continue
            
            # Log job completion
            self.log_job_complete(job, items_found, items_processed, items_failed)
            
            return job
            
        except Exception as e:
            # Log job failure
            self.log_job_failed(job, str(e))
            logger.exception(f"Error running statistics scraper: {str(e)}")
            return job
    
    def process_statistics_page(self, job, url):
        """
        Process a single statistics page and extract HTML tables.
        """
        response = self.fetch_page(url)
        soup = self.parse_html(response.text)
        
        # Find all tables on the page
        tables = soup.find_all('table')
        
        # Process each table
        for i, table in enumerate(tables):
            try:
                # Convert HTML table to pandas DataFrame
                df = pd.read_html(str(table))[0]
                
                # Extract table title
                title = None
                previous_tag = table.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'caption'])
                if previous_tag:
                    title = previous_tag.text.strip()
                
                # If no title found, use generic title
                if not title:
                    title = f"Table {i+1} from {os.path.basename(url)}"
                
                # Convert DataFrame to JSON
                table_json = df.to_json(orient='table')
                
                # Create ScrapedItem record
                ScrapedItem.objects.create(
                    job=job,
                    item_type=ScrapedItem.TYPE_HTML_TABLE,
                    source_url=url,
                    title=title[:255],  # Truncate to fit field length
                    content=table_json,
                    metadata={
                        'columns': list(df.columns),
                        'shape': df.shape,
                        'table_index': i
                    }
                )
                
            except Exception as e:
                logger.error(f"Error processing table {i} from {url}: {str(e)}")
                # Create failed item record
                ScrapedItem.objects.create(
                    job=job,
                    item_type=ScrapedItem.TYPE_HTML_TABLE,
                    source_url=url,
                    title=f"Failed Table {i+1} from {os.path.basename(url)}",
                    content={},
                    metadata={'table_index': i},
                    status=ScrapedItem.STATUS_FAILED,
                    error_message=str(e)
                )

class PublicationsScraper(BaseScraper):
    """
    Scraper for PDF documents on publications pages.
    """
    def __init__(self):
        super().__init__()
        self.publications_path = self.config.get('publications_path')
        self.pdf_max_pages = self.config.get('pdf_max_pages')
        self.pdf_tables_per_page = self.config.get('pdf_tables_per_page')
    
    def run(self):
        """
        Run the publications scraper job.
        """
        publications_url = self.get_absolute_url(self.publications_path)
        
        # Create job record
        job = self.log_job_start(ScraperJob.TYPE_PUBLICATIONS, publications_url)
        
        try:
            # Start by fetching the main publications page
            response = self.fetch_page(publications_url)
            soup = self.parse_html(response.text)
            
            # Find links to PDF files (this will be specific to the SNBS website structure)
            pdf_links = []
            content_area = soup.find('div', class_='publications')  # Adjust selector based on actual site structure
            
            if content_area:
                links = content_area.find_all('a', href=True)
                for link in links:
                    href = link.get('href')
                    # Filter for PDF links
                    if href.lower().endswith('.pdf'):
                        pdf_links.append(self.get_absolute_url(href))
            
            # Record how many PDFs we found
            items_found = len(pdf_links)
            items_processed = 0
            items_failed = 0
            
            # Process each PDF file
            for link in pdf_links:
                try:
                    self.process_pdf(job, link)
                    items_processed += 1
                except Exception as e:
                    logger.error(f"Error processing PDF {link}: {str(e)}")
                    items_failed += 1
                    continue
            
            # Log job completion
            self.log_job_complete(job, items_found, items_processed, items_failed)
            
            return job
            
        except Exception as e:
            # Log job failure
            self.log_job_failed(job, str(e))
            logger.exception(f"Error running publications scraper: {str(e)}")
            return job
    
    def process_pdf(self, job, url):
        """
        Download and process a PDF document to extract tables.
        """
        # Download the PDF file
        response = self.fetch_page(url)
        
        # Create a temporary file to save the PDF
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(response.content)
            pdf_path = temp_file.name
        
        try:
            # Determine PDF filename for title
            pdf_filename = os.path.basename(url)
            
            # Read tables from PDF using tabula-py
            # This will extract all tables from the PDF into a list of DataFrames
            tables = tabula.read_pdf(
                pdf_path, 
                pages='all', 
                multiple_tables=True,
                guess=True,
                max_pages=self.pdf_max_pages
            )
            
            # Process each table
            for i, df in enumerate(tables):
                if i >= self.pdf_max_pages * self.pdf_tables_per_page:
                    # Limit the number of tables we extract to avoid excessive resource usage
                    break
                
                if not df.empty:
                    try:
                        # Calculate page number (approximate)
                        page_number = (i // self.pdf_tables_per_page) + 1
                        table_number = (i % self.pdf_tables_per_page) + 1
                        
                        # Convert DataFrame to JSON
                        table_json = df.to_json(orient='table')
                        
                        # Create ScrapedItem record
                        ScrapedItem.objects.create(
                            job=job,
                            item_type=ScrapedItem.TYPE_PDF_TABLE,
                            source_url=url,
                            page_number=page_number,
                            table_number=table_number,
                            title=f"Table {table_number} from page {page_number} of {pdf_filename}",
                            content=table_json,
                            metadata={
                                'columns': list(df.columns),
                                'shape': df.shape,
                                'pdf_name': pdf_filename
                            }
                        )
                    except Exception as e:
                        logger.error(f"Error processing table {i} from PDF {url}: {str(e)}")
            
        finally:
            # Clean up the temporary file
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
