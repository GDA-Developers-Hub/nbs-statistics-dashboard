# Somalia Statistics Scraper Service

This service is responsible for scraping data from the Somalia National Bureau of Statistics (NBS) website at regular intervals to provide real-time statistics for the dashboard.

## Overview

The Scraper Service automatically extracts statistical data from the NBS website every 20 minutes, ensuring that the dashboard always displays the most current information available. The service is designed to be:

- **Reliable**: Built-in retry mechanisms and error handling
- **Efficient**: Smart caching to reduce load on the source website
- **Flexible**: Configurable scraping schedules for different data categories
- **Comprehensive**: Extracts data from multiple sections of the NBS website

## Key Components

### 1. `SomaliaStatsScraper`

The main scraper class in `somalia_scraper.py` that connects to the NBS website and extracts structured data. It includes:

- Specialized extraction methods for different data categories (demographics, economy, etc.)
- HTML table parsing to convert to structured data formats
- PDF link extraction for publications
- Text analysis for statistical indicators

### 2. `ScraperSchedulerService`

Manages the scheduling of scraping operations in `services.py`:

- Runs scrapers at configured intervals (20 minutes for statistics)
- Tracks last run times to prevent duplicate runs
- Implements threading for concurrent operation

### 3. `RealTimeDataManager`

Handles real-time access to the latest data in `realtime.py`:

- Provides cached access to the latest statistics
- Triggers on-demand scraping when data is stale
- Categorizes data for easy consumption by the frontend

## Data Flow

1. **Scheduled Trigger**: The scheduler runs every 20 minutes
2. **Data Extraction**: The scraper connects to NBS website and extracts data
3. **Data Processing**: Raw data is converted to structured formats (JSON)
4. **Storage**: Processed data is stored in the database
5. **API Access**: Frontend accesses the data through REST API endpoints
6. **Visualization**: Data is displayed on the dashboard

## Implementation Details

### Scraping Process

The scraper extracts data from the following sections of the NBS website:

- **Demographics**: Population statistics
- **Economy**: GDP, employment, trade data
- **Health**: Mortality rates, healthcare statistics
- **Education**: Literacy rates, enrollment figures
- **Inflation**: Consumer Price Index
- **Publications**: Statistical reports and publications

### Data Extraction Methods

The scraper uses multiple techniques to extract data:

1. **HTML Table Parsing**: Uses pandas to extract structured tables
2. **Text Pattern Matching**: Uses regex to extract numerical data from text
3. **Structured Content Extraction**: Extracts data from lists and structured elements
4. **PDF Link Collection**: Gathers links to statistical publications

### Scheduling Options

The service provides multiple scheduling options:

1. **Django Crontab**: For Linux/Unix systems
2. **Windows Task Scheduler**: For Windows environments
3. **Continuous Python Scheduler**: Platform-independent background process

## Setup and Configuration

### Installation

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure the database:
   ```bash
   python manage.py migrate
   ```

### Configuration Options

Edit `settings.py` to customize the scraper behavior:

```python
SCRAPER_CONFIG = {
    'base_url': 'https://nbs.gov.so/',
    'user_agent': 'SNBS Dashboard Scraper/1.0',
    'request_timeout': 30,
    'request_delay': 1.0,  # Seconds between requests
    'max_retries': 3,
    
    # Schedule intervals
    'schedule_interval': {
        'somalia_stats': '20m',  # Every 20 minutes
        'publications': '6h',    # Every 6 hours
    },
    
    # Categories to prioritize
    'real_time_categories': ['demographics', 'economy', 'inflation'],
}
```

## Running the Scraper

### Method 1: Manual Run

Run the scraper once manually:

```bash
python manage.py run_somalia_scraper_test
```

Run the scraper for a specific category:

```bash
python manage.py run_somalia_scraper_test --categories demographics economy
```

Run in debug mode for detailed output:

```bash
python manage.py run_somalia_scraper_test --debug
```

### Method 2: Scheduler Service

Run the scheduler once to check and run scheduled scrapers:

```bash
python manage.py run_scraper_scheduler
```

Force a run even if not scheduled:

```bash
python manage.py run_scraper_scheduler --force
```

Run continuously in the background (checking every minute if 20-minute interval is reached):

```bash
python manage.py run_scraper_scheduler --continuous
```

### Method 3: Windows Background Service

Start the scheduler as a background service on Windows:

```powershell
powershell -ExecutionPolicy Bypass -File start_scraper_service.ps1
```

### Method 4: Python Script

Run the continuous scraper script:

```bash
python run_continuous_scraper.py
```

## API Endpoints

The scraper service provides the following API endpoints:

### Scraper Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/jobs/` | GET | List all scraper jobs |
| `/api/jobs/run_scraper/` | POST | Manually trigger a scraper job |

### Data Access

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/scraped-items/` | GET | List all scraped items |
| `/api/scraped-items/<id>/data/` | GET | Get structured data for an item |
| `/api/scraped-items/categories/` | GET | List available data categories |

### Real-time Data

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/latest-statistics/` | GET | Get latest statistics for all categories |
| `/api/realtime/trigger/` | POST | Trigger a real-time scrape (body: `{"categories": ["demographics"], "force": true}`) |
| `/api/realtime/data/` | GET | Get real-time data with optional auto-update |
| `/api/realtime/data/<category>/` | GET | Get real-time data for a specific category |

## Monitoring

### Logs

The scraper logs to the following files:

- `scraper_scheduler.log`: Scheduler operation logs
- `scraper_output.log`: Standard output from scraper runs
- `scraper_error.log`: Error logs from scraper runs

### Admin Interface

Access the Django admin interface to view scraper operations:

1. Create an admin user: `python manage.py createsuperuser`
2. Run the development server: `python manage.py runserver`
3. Access the admin site at: `http://localhost:8000/admin/`
4. Navigate to "Scraper jobs" and "Scraped items"

## Troubleshooting

### Common Issues

1. **404 Errors**: The website structure may have changed. Check the paths in the scraper configuration.
2. **Timeout Errors**: The website may be slow or unreachable. Increase the `request_timeout` setting.
3. **Empty Data**: The scraper may not be finding the expected elements. Verify the HTML structure.

### Diagnostic Steps

1. Run the scraper in debug mode:
   ```bash
   python manage.py run_somalia_scraper_test --debug
   ```

2. Check the logs:
   ```bash
   tail -f scraper_output.log
   ```

3. Check the database:
   ```bash
   python manage.py shell
   # In the shell
   from scraper_service.scraper.models import ScraperJob, ScrapedItem
   ScraperJob.objects.order_by('-start_time').first().__dict__
   ```

## Development

### Extending the Scraper

#### Adding a New Category

1. Add a new path to the `SomaliaStatsScraper.paths` dictionary:
   ```python
   self.paths = {
       # ... existing paths
       'new_category': '/path/to/category',
   }
   ```

2. Create an extraction method in `SomaliaStatsScraper`:
   ```python
   def extract_new_category_data(self, soup):
       # Extract and process the data
       # Return a DataFrame or None
   ```

3. Add the new method to the `extract_structured_data` method:
   ```python
   if category == 'new_category':
       data = self.extract_new_category_data(soup)
       if data is not None:
           data_dict['New Category Data'] = data
   ```

#### Customizing the Scheduler

Modify the scheduling intervals in `settings.py`:

```python
'schedule_interval': {
    'somalia_stats': '20m',  # Change to desired interval
    'publications': '6h',
}
```

## License

This project is licensed under the MIT License. 