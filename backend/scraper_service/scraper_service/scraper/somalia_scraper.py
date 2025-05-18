import logging
import re
import json
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from .scrapers import BaseScraper
from .models import ScraperJob, ScrapedItem
import requests
import time

logger = logging.getLogger(__name__)

class SomaliaStatsScraper(BaseScraper):
    """
    Specialized scraper for Somalia National Bureau of Statistics website.
    Focuses on extracting key economic and demographic indicators.
    Connects to the actual nbs.gov.so website to extract real data.
    """
    def __init__(self):
        super().__init__()
        # Define paths based on actual website structure
        self.paths = {
            'demographics': '/statistics',
            'economy': '/statistics',
            'inflation': '/statistics',
            'health': '/statistics',
            'education': '/statistics',
            'publications': '/publications/statistical-publications'
        }
        
        # For command output
        self.stdout = None
        
    def run(self):
        """
        Run the Somalia statistics scraper job.
        """
        # Create job record
        job = self.log_job_start(ScraperJob.TYPE_STATISTICS, self.base_url)
        
        try:
            # First, scrape the homepage for key statistics
            self.scrape_homepage_stats(job)
            
            # Track overall statistics
            total_found = 0
            total_processed = 0
            total_failed = 0
            
            # Process each statistics category
            for category, path in self.paths.items():
                url = self.get_absolute_url(path)
                if self.stdout:
                    self.stdout.write(f"Scraping {category} data from {url}")
                else:
                    logger.info(f"Scraping {category} data from {url}")
                
                try:
                    items_found, items_processed, items_failed = self.process_category(job, category, url)
                    total_found += items_found
                    total_processed += items_processed
                    total_failed += items_failed
                except Exception as e:
                    logger.error(f"Error processing category {category}: {str(e)}")
                    total_failed += 1
            
            # Log job completion
            self.log_job_complete(job, total_found, total_processed, total_failed)
            return job
            
        except Exception as e:
            # Log job failure
            self.log_job_failed(job, str(e))
            logger.exception(f"Error running Somalia statistics scraper: {str(e)}")
            return job
    
    def scrape_homepage_stats(self, job):
        """
        Scrape key statistics from the homepage.
        """
        try:
            # Fetch the homepage
            homepage_url = self.base_url
            response = self.fetch_page(homepage_url)
            soup = self.parse_html(response.text)
            
            # Look for key statistics on the homepage (often in h6 tags with statistics)
            key_stats = []
            stat_elements = soup.find_all('h6')
            
            for stat_elem in stat_elements:
                # Skip elements without text
                if not stat_elem.text.strip():
                    continue
                    
                # Extract the statistic and its value
                stat_text = stat_elem.text.strip()
                
                # Skip non-stat elements
                if not any(keyword in stat_text.lower() for keyword in ['rate', 'index', 'gdp', 'mortality']):
                    continue
                
                # Try to split into title and value
                parts = stat_text.split('\n')
                if len(parts) >= 2:
                    title = parts[0].strip()
                    value = parts[-1].strip()
                    
                    key_stats.append({
                        'title': title,
                        'value': value
                    })
            
            # If we found key statistics, create a dataframe and save to database
            if key_stats:
                df = pd.DataFrame(key_stats)
                
                # Save to database
                ScrapedItem.objects.create(
                    job=job,
                    item_type=ScrapedItem.TYPE_HTML_TABLE,
                    source_url=homepage_url,
                    title="Key Somalia Statistics",
                    content=df.to_json(orient='table'),
                    metadata={
                        'category': 'key_indicators',
                        'columns': list(df.columns),
                        'shape': df.shape,
                        'time_period': datetime.now().strftime("%Y")
                    }
                )
                
                logger.info(f"Extracted {len(key_stats)} key statistics from homepage")
                
        except Exception as e:
            logger.error(f"Error scraping homepage statistics: {str(e)}")
    
    def process_category(self, job, category, url):
        """
        Process a specific category of statistics by scraping the actual website.
        """
        try:
            response = self.fetch_page(url)
            soup = self.parse_html(response.text)
            
            # Extract tables or structured data
            tables = soup.find_all('table')
            items_found = len(tables)
            items_processed = 0
            items_failed = 0
            
            # If no tables found, look for other structured data
            if not tables:
                # Try to find data in other formats (lists, paragraphs with numbers, etc.)
                data_dict = self.extract_structured_data(soup, category, url)
                if data_dict:
                    items_found = len(data_dict)
                    for title, data in data_dict.items():
                        try:
                            # Convert to DataFrame if not already
                            if not isinstance(data, pd.DataFrame):
                                df = pd.DataFrame(data)
                            else:
                                df = data
                                
                            # Extract time period
                            time_period = self.extract_time_period(soup) or datetime.now().strftime("%Y")
                            
                            # Create ScrapedItem record
                            ScrapedItem.objects.create(
                                job=job,
                                item_type=ScrapedItem.TYPE_HTML_TABLE,
                                source_url=url,
                                title=f"{category.title()} - {title}",
                                content=df.to_json(orient='table'),
                                metadata={
                                    'category': category,
                                    'columns': list(df.columns),
                                    'shape': df.shape,
                                    'time_period': time_period
                                }
                            )
                            
                            items_processed += 1
                            
                        except Exception as e:
                            logger.error(f"Error processing {category} data {title} from {url}: {str(e)}")
                            items_failed += 1
                else:
                    # If still no data, create a message item
                    logger.warning(f"No data found for {category} at {url}")
                    items_found = 1
                    items_failed = 1
            else:
                # Process tables found in the HTML
                for i, table in enumerate(tables):
                    try:
                        # Convert HTML table to pandas DataFrame
                        try:
                            df = pd.read_html(str(table))[0]
                        except:
                            # Sometimes simple read_html fails, try a more robust method
                            df = self.html_table_to_df(table)
                            
                        # If table is empty or invalid, skip it
                        if df.empty or len(df.columns) <= 1:
                            continue
                            
                        # Extract title for the table
                        title = self.extract_table_title(table, i, category)
                        
                        # Extract time period
                        time_period = self.extract_time_period(soup) or self.extract_time_period_from_df(df)
                        
                        # Create ScrapedItem record
                        ScrapedItem.objects.create(
                            job=job,
                            item_type=ScrapedItem.TYPE_HTML_TABLE,
                            source_url=url,
                            title=title,
                            content=df.to_json(orient='table'),
                            metadata={
                                'category': category,
                                'columns': list(df.columns),
                                'shape': df.shape,
                                'time_period': time_period
                            }
                        )
                        
                        items_processed += 1
                        
                    except Exception as e:
                        logger.error(f"Error processing {category} table {i} from {url}: {str(e)}")
                        items_failed += 1
            
            # If this is a publication category, try to extract PDF links
            if category == 'publications':
                # Look for publications or documents
                pdf_links = self.extract_pdf_links(soup, url)
                if pdf_links:
                    items_found += len(pdf_links)
                    for link_title, link_url in pdf_links.items():
                        try:
                            # Save publication link as a scraped item
                            ScrapedItem.objects.create(
                                job=job,
                                item_type=ScrapedItem.TYPE_PDF_TEXT,
                                source_url=link_url,
                                title=f"Publication - {link_title}",
                                content=json.dumps({"url": link_url, "title": link_title}),
                                metadata={
                                    'category': 'publications',
                                    'type': 'pdf_link',
                                    'time_period': datetime.now().strftime("%Y")
                                }
                            )
                            items_processed += 1
                        except Exception as e:
                            logger.error(f"Error processing publication link {link_url}: {str(e)}")
                            items_failed += 1
                
            return items_found, items_processed, items_failed
            
        except Exception as e:
            logger.error(f"Error in process_category for {category} at {url}: {str(e)}")
            return 1, 0, 1
    
    def extract_table_title(self, table, index, category):
        """Extract title for a table."""
        # Try to find a caption
        caption = table.find('caption')
        if caption and caption.text.strip():
            return caption.text.strip()
            
        # Try to find preceding header
        previous_tag = table.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if previous_tag and previous_tag.text.strip():
            return previous_tag.text.strip()
            
        # Default title
        return f"{category.title()} Table {index+1}"
    
    def extract_time_period(self, soup):
        """Extract time period information from the page."""
        # Look for dates in the text
        text = soup.get_text(" ")
        
        # Look for year patterns
        year_pattern = r'(20\d{2})'
        year_matches = re.findall(year_pattern, text)
        
        if year_matches:
            years = [int(y) for y in year_matches]
            min_year = min(years)
            max_year = max(years)
            
            if min_year == max_year:
                return str(min_year)
            else:
                return f"{min_year}-{max_year}"
                
        # Look for month-year patterns
        month_year_pattern = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (20\d{2})'
        month_year_matches = re.findall(month_year_pattern, text, re.IGNORECASE)
        
        if month_year_matches:
            return f"{month_year_matches[0][0]} {month_year_matches[0][1]}"
            
        # Default to current year
        return datetime.now().strftime("%Y")
    
    def extract_time_period_from_df(self, df):
        """
        Extract time period information from the dataframe.
        """
        # Check column names for year information
        year_columns = []
        for col in df.columns:
            if isinstance(col, str):
                # Look for years like 2020, 2021, etc.
                year_match = re.search(r'(20\d{2})', col)
                if year_match:
                    year_columns.append(int(year_match.group(1)))
        
        # If we found year columns, determine the time period
        if year_columns:
            min_year = min(year_columns)
            max_year = max(year_columns)
            
            if min_year == max_year:
                return str(min_year)
            else:
                return f"{min_year}-{max_year}"
                
        # Check for a Year column
        if 'Year' in df.columns:
            years = df['Year'].unique()
            if len(years) > 0:
                min_year = min(years)
                max_year = max(years)
                
                if min_year == max_year:
                    return str(min_year)
                else:
                    return f"{min_year}-{max_year}"
        
        # Check for Date column
        if 'Date' in df.columns:
            try:
                dates = pd.to_datetime(df['Date'])
                min_date = min(dates)
                max_date = max(dates)
                
                if min_date.year == max_date.year:
                    if min_date.month == max_date.month:
                        return f"{min_date.strftime('%B %Y')}"
                    else:
                        return f"{min_date.strftime('%B')}-{max_date.strftime('%B %Y')}"
                else:
                    return f"{min_date.year}-{max_date.year}"
            except:
                pass
        
        # Default to current year if no time period found
        return str(datetime.now().year)
    
    def html_table_to_df(self, table):
        """Convert an HTML table to DataFrame manually."""
        # Get headers
        headers = []
        header_row = table.find('thead')
        if header_row:
            header_cells = header_row.find_all(['th', 'td'])
            headers = [cell.text.strip() for cell in header_cells]
        
        # If no headers found in thead, check first row
        if not headers:
            first_row = table.find('tr')
            if first_row:
                header_cells = first_row.find_all(['th', 'td'])
                headers = [cell.text.strip() for cell in header_cells]
        
        # If still no headers, use generic column names
        if not headers:
            # Find the max number of columns in any row
            max_cols = 0
            for row in table.find_all('tr'):
                cols = len(row.find_all(['td', 'th']))
                max_cols = max(max_cols, cols)
            
            headers = [f'Column {i+1}' for i in range(max_cols)]
        
        # Get rows data
        rows = []
        for row in table.find_all('tr'):
            cells = row.find_all(['td', 'th'])
            # Skip header row
            if cells and cells[0].name == 'td':  # Only process data rows
                row_data = [cell.text.strip() for cell in cells]
                # Ensure row has same number of columns as headers
                while len(row_data) < len(headers):
                    row_data.append('')
                rows.append(row_data[:len(headers)])
        
        # Create DataFrame
        df = pd.DataFrame(rows, columns=headers)
        return df
    
    def extract_structured_data(self, soup, category, url):
        """
        Extract structured data from non-table elements.
        Returns a dictionary of titles to DataFrame objects.
        """
        data_dict = {}
        
        # Look for structured content based on category
        if category == 'demographics':
            # Look for population statistics
            population_data = self.extract_population_data(soup)
            if population_data is not None:
                data_dict['Population Statistics'] = population_data
                
        elif category == 'economy':
            # Look for GDP and other economic indicators
            gdp_data = self.extract_economic_data(soup)
            if gdp_data is not None:
                data_dict['Economic Indicators'] = gdp_data
                
        elif category == 'inflation':
            # Look for CPI data
            cpi_data = self.extract_inflation_data(soup)
            if cpi_data is not None:
                data_dict['Consumer Price Index'] = cpi_data
        
        # Try generic extraction for lists with numbers
        list_data = self.extract_list_data(soup)
        if list_data is not None:
            list_title = f"{category.title()} Indicators"
            data_dict[list_title] = list_data
            
        return data_dict
    
    def extract_population_data(self, soup):
        """Extract population data from various elements."""
        # Look for population figures in text
        text = soup.get_text(" ")
        population_matches = re.findall(r'population of (\d[\d,]*)', text, re.IGNORECASE)
        population_matches += re.findall(r'(\d[\d,]*) people', text, re.IGNORECASE)
        
        if population_matches:
            data = []
            for match in population_matches[:5]:  # Limit to 5 entries
                # Clean the number
                value = match.replace(',', '')
                if value.isdigit():
                    # Try to find a label near this number
                    data.append({'Metric': 'Population', 'Value': int(value)})
            
            if data:
                return pd.DataFrame(data)
        
        return None
    
    def extract_economic_data(self, soup):
        """Extract economic indicators."""
        # Look for GDP, growth rates, etc.
        text = soup.get_text(" ")
        
        # GDP
        gdp_matches = re.findall(r'GDP.{1,30}([\d\.]+)%', text)
        gdp_value_matches = re.findall(r'GDP.{1,30}(\$[\d\.]+)\s*(billion|million)', text)
        
        # Unemployment
        unemployment_matches = re.findall(r'unemployment.{1,30}([\d\.]+)%', text, re.IGNORECASE)
        
        # Create data records
        data = []
        
        if gdp_matches:
            data.append({'Indicator': 'GDP Growth Rate', 'Value': f"{gdp_matches[0]}%"})
            
        if gdp_value_matches:
            amount, unit = gdp_value_matches[0]
            data.append({'Indicator': 'GDP', 'Value': f"{amount} {unit}"})
            
        if unemployment_matches:
            data.append({'Indicator': 'Unemployment Rate', 'Value': f"{unemployment_matches[0]}%"})
            
        # Add any other indicators found in headers or strong tags
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong']):
            text = tag.text.strip()
            
            # Look for percentage patterns
            percentage_match = re.search(r'([A-Za-z\s]+):\s*([\d\.]+)%', text)
            if percentage_match:
                indicator, value = percentage_match.groups()
                data.append({'Indicator': indicator.strip(), 'Value': f"{value}%"})
                continue
                
            # Look for currency patterns
            currency_match = re.search(r'([A-Za-z\s]+):\s*\$([\d\.]+)', text)
            if currency_match:
                indicator, value = currency_match.groups()
                data.append({'Indicator': indicator.strip(), 'Value': f"${value}"})
        
        if data:
            return pd.DataFrame(data)
            
        return None
    
    def extract_inflation_data(self, soup):
        """Extract inflation/CPI data."""
        # Look for CPI numbers
        text = soup.get_text(" ")
        
        # CPI value
        cpi_matches = re.findall(r'CPI.{1,30}([\d\.]+)', text)
        inflation_matches = re.findall(r'inflation.{1,30}([\d\.]+)%', text, re.IGNORECASE)
        
        data = []
        
        if cpi_matches:
            data.append({'Metric': 'Consumer Price Index', 'Value': cpi_matches[0]})
            
        if inflation_matches:
            data.append({'Metric': 'Inflation Rate', 'Value': f"{inflation_matches[0]}%"})
            
        # Look for time series data in headers
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = tag.text.strip()
            
            # Look for month/year with CPI value
            month_cpi_match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (20\d{2}).{1,20}([\d\.]+)', text, re.IGNORECASE)
            if month_cpi_match:
                month, year, value = month_cpi_match.groups()
                data.append({'Metric': f'CPI {month} {year}', 'Value': value})
        
        if data:
            return pd.DataFrame(data)
            
        return None
    
    def extract_list_data(self, soup):
        """Extract structured data from lists."""
        # Find lists with numbers
        lists = soup.find_all(['ul', 'ol'])
        
        data = []
        for list_elem in lists:
            items = list_elem.find_all('li')
            for item in items:
                text = item.text.strip()
                
                # Look for key-value patterns
                kv_match = re.search(r'([^:]+):\s*(.+)', text)
                if kv_match:
                    key, value = kv_match.groups()
                    data.append({'Indicator': key.strip(), 'Value': value.strip()})
                    continue
                    
                # Look for percentage patterns
                percentage_match = re.search(r'(.+?)\s+([\d\.]+)%', text)
                if percentage_match:
                    label, value = percentage_match.groups()
                    data.append({'Indicator': label.strip(), 'Value': f"{value}%"})
        
        if data:
            return pd.DataFrame(data)
            
        return None
    
    def extract_pdf_links(self, soup, base_url):
        """
        Extract links to PDF documents.
        Returns a dictionary of {title: url}.
        """
        pdf_links = {}
        
        # Find all links
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            title = link.text.strip()
            
            # Skip empty titles or navigation links
            if not title or len(title) < 5 or title.lower() in ['home', 'next', 'previous']:
                continue
                
            # Check if link points to PDF
            if href.lower().endswith('.pdf') or 'download' in href.lower() or 'publication' in href.lower():
                # Get absolute URL
                full_url = self.get_absolute_url(href)
                
                # Add to dictionary with a sensible title
                pdf_links[title] = full_url
        
        return pdf_links 