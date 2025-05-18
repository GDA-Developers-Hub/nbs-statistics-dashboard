# Real-Time Scraper Guide

This guide explains how to set up, configure, and run the real-time scraper for the Somalia Statistics Dashboard. The scraper is configured to automatically extract data from the Somalia National Bureau of Statistics website every 20 minutes, ensuring that your dashboard always displays the most current information available.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Methods](#running-methods)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Advanced Configuration](#advanced-configuration)

## Overview

The real-time scraper is a key component of the Somalia Statistics Dashboard, automatically collecting the latest statistical data every 20 minutes. This ensures that your dashboard displays up-to-date information without manual intervention.

### What Gets Scraped

The scraper extracts data from various sections of the NBS website:

- **Demographics Data**: Population statistics by region
- **Economic Indicators**: GDP, employment, trade data
- **Inflation Metrics**: Consumer Price Index and inflation rates
- **Health Statistics**: Mortality rates, vaccination coverage
- **Education Data**: Literacy rates, school enrollment
- **Publications**: Statistical reports and PDF documents

### Data Flow

1. The scheduler triggers the scraper every 20 minutes
2. The scraper connects to the NBS website and extracts data
3. The data is processed and stored in the database
4. The frontend retrieves the latest data through the API
5. Users see the most current statistics on the dashboard

## Installation

Before running the scraper, ensure you have properly installed the required components:

### Prerequisites

- Python 3.8+
- Django 4.2+
- PostgreSQL database
- Required Python packages

### Install Dependencies

```bash
cd nbs-statistics-dashboard/backend/scraper_service
pip install -r requirements.txt
```

Additional packages needed specifically for the scraper:

```bash
pip install pandas beautifulsoup4 lxml html5lib schedule django-crontab
```

### Database Setup

Ensure your database is properly configured in the settings:

```bash
python manage.py migrate
```

## Configuration

The scraper can be configured to match your specific requirements:

### Basic Configuration

Edit `settings.py` to customize scraper behavior:

```python
SCRAPER_CONFIG = {
    'base_url': 'https://nbs.gov.so/',
    'user_agent': 'SNBS Dashboard Scraper/1.0',
    'request_timeout': 30,  # Seconds before timeout
    'request_delay': 1.0,   # Seconds between requests
    'max_retries': 3,       # Number of retry attempts
    
    # Schedule intervals (in hours or minutes)
    'schedule_interval': {
        'somalia_stats': '20m',  # Every 20 minutes for real-time statistics
        'publications': '6h',    # Every 6 hours for publications
    },
    
    # Categories to prioritize for real-time updates
    'real_time_categories': ['demographics', 'economy', 'inflation'],
}
```

### Setting Up the 20-Minute Schedule

The default configuration runs the scraper every 20 minutes. This interval provides a good balance between having current data and not overloading the source website.

To modify the interval:

1. Change the `'somalia_stats'` value in the `'schedule_interval'` dictionary
2. Update any crontab or scheduler configurations to match

## Running Methods

There are multiple ways to run the scraper, depending on your environment and preferences:

### Method 1: Django Management Command (Manual)

Run the scraper manually for testing or one-time updates:

```bash
python manage.py run_somalia_scraper_test
```

To run just specific categories:

```bash
python manage.py run_somalia_scraper_test --categories demographics economy
```

For debugging:

```bash
python manage.py run_somalia_scraper_test --debug
```

### Method 2: Scheduler Service

The scheduler service automatically runs the scraper at the configured intervals:

#### One-time check and run:

```bash
python manage.py run_scraper_scheduler
```

#### Continuous mode (recommended for production):

```bash
python manage.py run_scraper_scheduler --continuous --interval 60
```

This will check every 60 seconds if the 20-minute interval has been reached and run the scraper if needed.

### Method 3: Windows Task Scheduler

For Windows servers, you can use the provided batch script with Task Scheduler:

1. Open Windows Task Scheduler
2. Create a new task
3. Set the trigger to run every 20 minutes
4. Add an action to run `run_scraper_scheduler.bat`
5. Set the start in directory to the scraper_service folder

Alternatively, use the PowerShell script for a background service:

```powershell
powershell -ExecutionPolicy Bypass -File start_scraper_service.ps1
```

### Method 4: Linux/Unix Cron

For Linux/Unix servers, add to crontab:

```bash
# Edit crontab
crontab -e

# Add the following line to run every 20 minutes
*/20 * * * * cd /path/to/nbs-statistics-dashboard/backend/scraper_service && python manage.py run_somalia_scraper_test
```

Alternatively, use django-crontab:

```bash
python manage.py crontab add
```

### Method 5: Docker Service

If running in Docker, add to your docker-compose.yml:

```yaml
services:
  scraper:
    build: ./backend/scraper_service
    command: python run_continuous_scraper.py
    volumes:
      - ./backend/scraper_service:/app
    depends_on:
      - db
```

## Monitoring

It's important to monitor the scraper's performance and ensure it's running correctly:

### Check Scraper Status

View recent scraper jobs:

```bash
python manage.py check_scraper_status
```

### Check Logs

Monitor the log files for errors or issues:

- `scraper_scheduler.log`: Log of scheduler operations
- `scraper_output.log`: Standard output from scraper runs
- `scraper_error.log`: Error logs from scraper runs

### Admin Interface

The Django admin interface provides a visual way to monitor scraping operations:

1. Run the server: `python manage.py runserver`
2. Access the admin site: `http://localhost:8000/admin/`
3. Navigate to "Scraper jobs" to see all scraping operations
4. Check "Scraped items" to see all the data items

### Automated Monitoring

Set up alerts for scraper failures:

```python
# In your settings.py
SCRAPER_MONITORING = {
    'email_alerts': True,
    'admin_email': 'admin@example.com',
    'alert_on_consecutive_failures': 3,  # Alert after 3 consecutive failures
}
```

## Troubleshooting

Common issues and their solutions:

### Scraper Failing to Connect

If the scraper can't connect to the NBS website:

1. Check your internet connection
2. Verify that https://nbs.gov.so/ is accessible in a browser
3. Increase the `request_timeout` and `max_retries` in settings
4. Check if IP blocking is occurring (consider adding rotation)

### No Data Being Scraped

If the scraper runs but doesn't extract data:

1. The website structure may have changed
2. Run with `--debug` to see detailed extraction attempts
3. Check the HTML structure of the website manually
4. Update the extraction patterns in `somalia_scraper.py`

### Scheduler Not Running

If the scheduler isn't triggering the scraper:

1. Check if the process is running: `ps aux | grep run_scraper`
2. Examine the scheduler logs for errors
3. Try running the scheduler manually to debug
4. Restart the scheduler service

## Advanced Configuration

### Fine-tuning the Scraper

For more advanced configuration:

#### Custom User Agent

Set a custom user agent to identify your scraper and be respectful:

```python
SCRAPER_CONFIG = {
    'user_agent': 'Somalia Dashboard Scraper (yourorganization.com)',
    # ... other settings
}
```

#### Proxy Configuration

If you need to use proxies:

```python
SCRAPER_CONFIG = {
    # ... existing settings
    'use_proxies': True,
    'proxies': [
        'http://proxy1.example.com:8080',
        'http://proxy2.example.com:8080',
    ],
}
```

#### Resource-aware Scheduling

To reduce server load during high-traffic periods:

```python
SCRAPER_CONFIG = {
    # ... existing settings
    'quiet_hours': {
        'enabled': True,
        'hours': [0, 1, 2, 3, 4, 5],  # Midnight to 5 AM
        'interval_multiplier': 2,     # Double the interval during quiet hours
    },
}
```

### Custom Data Processing

To add custom processing for extracted data:

1. Create a processor class in `processors.py`:
   ```python
   class CustomDataProcessor:
       def process(self, data, category):
           # Process the data
           return processed_data
   ```

2. Register the processor in settings:
   ```python
   SCRAPER_CONFIG = {
       # ... existing settings
       'processors': {
           'demographics': 'scraper.processors.CustomDataProcessor',
       },
   }
   ```

## Conclusion

With the real-time scraper properly configured and running, your Somalia Statistics Dashboard will always display the most current data available. The 20-minute update interval ensures that users have access to near-real-time statistics without placing undue load on the source website.

For further assistance or to report issues, please contact the development team or create an issue in the GitHub repository. 