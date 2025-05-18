# 📊 NBS Statistics Dashboard

An open-data web application that visualizes key statistics published by the Somali National Bureau of Statistics (NBS). This dashboard allows users to explore, filter, and interact with national and regional data, including GIS-based visualizations for greater impact.

## 🌍 Project Overview

The NBS Statistics Dashboard aims to promote data-driven decision-making by providing an intuitive platform for accessing Somalia's official statistics. It combines interactive charts, downloadable reports, and a GIS map to allow exploration of data by region, sector, and time period.

## 🚀 Features

- 📈 Visual dashboards for economic, health, education, and population data
- 🗺️ Interactive GIS maps with regional insights
- 🔎 Filter and drill down by region, indicator, or year
- 📥 Export charts and reports
- 🔔 Update notifications for new datasets
- 🌐 Multilingual support (English, Somali)

## 🛠️ Tech Stack

- **Frontend:** React, TailwindCSS, Chart.js, Leaflet.js / Mapbox
- **Backend:** Django, Django REST Framework, GeoDjango
- **Database:** PostgreSQL with PostGIS extension
- **Scraping:** BeautifulSoup, Requests (for automated data updates)
- **Deployment:** Docker, NGINX, GitHub Actions, Vercel / DigitalOcean

## 🧭 Project Structure

```

nbs-statistics-dashboard/
├── backend/               # Django + GeoDjango API
│   ├── nbs/               # Core Django app
│   ├── scraper/           # Web scraping scripts
│   └── geo/               # GIS models & services
├── frontend/              # React dashboard interface
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── assets/
├── docs/                  # Documentation files
├── scripts/               # Data loaders and utils
├── .env.example
├── docker-compose.yml
└── README.md

````

## 🔧 Installation (Development)

```bash
# Clone the repo
git clone https://github.com/your-username/nbs-statistics-dashboard.git
cd nbs-statistics-dashboard

# Setup backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Setup frontend
cd ../frontend
npm install
npm run dev
```

## 🗺️ GIS Integration

The dashboard will use spatial data to visualize regional statistics using:

* Somali administrative boundary GeoJSON
* Leaflet.js + GeoDjango for interactive map rendering
* Region-wise drill-downs with statistical overlays

## 📊 Example Use Cases

* Compare regional literacy rates from 2016–2023
* View GDP contributions by region and year
* Analyze health infrastructure distribution across Somalia

## 📅 Project Timeline

| Phase                      | Timeline |
| -------------------------- | -------- |
| Planning                   | Month 1  |
| Dev Phase 1                | Month 2  |
| Dev Phase 2 (GIS + Charts) | Month 3  |
| Launch                     | Month 4  |

## 🤝 Contributing

We welcome contributions from developers, data analysts, and translators. Please read the [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for setup instructions.


## 📄 License

MIT License - See the [LICENSE](./LICENSE) file for details.

## 👩🏽‍💼 Maintained by GDA Developers.

# Somalia National Bureau of Statistics Dashboard

A comprehensive data dashboard system that displays statistics from Somalia's National Bureau of Statistics (NBS) with automated data scraping, ETL processing, and visualization.

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Scraper](#running-the-scraper)
- [API Endpoints](#api-endpoints)
- [Data Models](#data-models)
- [Dashboard Components](#dashboard-components)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [License](#license)

## Overview

This project creates a real-time statistics dashboard for Somalia, automatically extracting data from the [Somalia National Bureau of Statistics](https://nbs.gov.so/) website every 20 minutes. The system uses a microservices architecture with Django backend services and a React frontend to visualize key statistical indicators such as population demographics, economic indicators, inflation rates, and more.

## System Architecture

The system is built with a microservices architecture consisting of:

1. **Scraper Service**: Extracts data from the NBS website
2. **ETL Service**: Processes and transforms the raw data
3. **API Service**: Provides standardized access to the processed data
4. **Auth Service**: Handles user authentication and authorization
5. **Frontend**: React application to visualize and interact with the data

### Scraper Service

The Scraper Service is responsible for retrieving data from the Somalia National Bureau of Statistics website. Key components:

- **SomaliaStatsScraper**: Extracts structured data from the NBS website
- **ScraperSchedulerService**: Manages scheduled scraping (every 20 minutes)
- **Real-time Data Manager**: Enables on-demand scraping and caching

## Features

- **Automated Data Collection**: Scrapes the NBS website every 20 minutes
- **Real-time Updates**: Immediately reflects the latest statistics 
- **Category-based Scraping**: Organizes data into demographics, economy, inflation, health, education, and publications
- **Scheduled Jobs**: Configurable schedule for different data categories
- **Data Extraction**: Extracts from HTML tables, structured content, and PDF documents
- **API Access**: RESTful endpoints for accessing the latest data
- **Caching**: Efficient caching system to reduce load on the source website
- **Administrative Interface**: Monitor and manage scraper jobs and data items
- **Role-based Access**: Different permission levels for various user roles
- **Interactive Visualization**: Charts, maps and tables to explore the data

## Installation

### Prerequisites

- Python 3.8+
- Django 4.2+
- PostgreSQL
- Node.js and npm (for frontend)

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/nbs-statistics-dashboard.git
   cd nbs-statistics-dashboard
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. Configure the database:
   ```bash
   cd scraper_service
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Build the frontend:
   ```bash
   npm run build
   ```

## Configuration

### Scraper Configuration

The scraper settings are configured in `backend/scraper_service/scraper_service/settings.py`:

```python
SCRAPER_CONFIG = {
    'base_url': 'https://nbs.gov.so/',
    'user_agent': 'SNBS Dashboard Scraper/1.0',
    'request_timeout': 30,
    'request_delay': 1.0,
    'max_retries': 3,
    
    # Paths to scrape
    'statistics_path': '/statistics',
    'publications_path': '/publications',
    
    # Schedule intervals
    'schedule_interval': {
        'somalia_stats': '20m',  # Every 20 minutes for real-time updates
        'publications': '6h',    # Every 6 hours for publications
    },
    
    # Real-time scraping settings
    'real_time_categories': ['demographics', 'economy', 'inflation'],
}
```

### Scheduler Configuration

The scraper is scheduled to run every 20 minutes using one of several methods:

1. Django Crontab (Linux/Unix):
   ```python
   CRONJOBS = [
       ('*/20 * * * *', 'django.core.management.call_command', ['run_somalia_scraper_test']),
   ]
   ```

2. Windows Task Scheduler:
   - Use the `run_scraper_scheduler.bat` file
   - Schedule it to run every 20 minutes

3. Continuous Python Scheduler:
   - Use `run_continuous_scraper.py` or the management command
   - Runs in the background and automatically schedules jobs

## Running the Scraper

### Method 1: One-time Manual Run

```bash
cd backend/scraper_service
python manage.py run_somalia_scraper_test
```

### Method 2: Using the Scheduler Service (One-time)

```bash
python manage.py run_scraper_scheduler --force --job-type somalia_stats
```

### Method 3: Using the Scheduler Service (Continuous)

```bash
python manage.py run_scraper_scheduler --continuous --interval 60
```

### Method 4: Using the PowerShell Script (Windows)

```powershell
powershell -ExecutionPolicy Bypass -File start_scraper_service.ps1
```

### Method 5: Using the Python Script

```bash
python run_continuous_scraper.py
```

## API Endpoints

### Scraper API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/jobs/` | GET | List all scraper jobs |
| `/api/scraped-items/` | GET | List all scraped items |
| `/api/scraped-items/<id>/` | GET | Get details of a specific scraped item |
| `/api/scraped-items/<id>/data/` | GET | Get the structured data from a scraped item |
| `/api/scraped-items/categories/` | GET | Get all available data categories |
| `/api/latest-statistics/` | GET | Get the latest statistics for all categories |

### Real-time API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/realtime/trigger/` | POST | Trigger a real-time scrape |
| `/api/realtime/data/` | GET | Get real-time data for all categories |
| `/api/realtime/data/<category>/` | GET | Get real-time data for a specific category |

## Data Models

### ScraperJob

Represents a scraping operation:

| Field | Type | Description |
|-------|------|-------------|
| `job_type` | CharField | Type of scraper job (statistics/publications) |
| `url` | URLField | URL that was scraped |
| `status` | CharField | Status of the job (pending/running/completed/failed) |
| `start_time` | DateTimeField | When the job started |
| `end_time` | DateTimeField | When the job completed |
| `items_found` | IntegerField | Number of items found |
| `items_processed` | IntegerField | Number of items successfully processed |
| `items_failed` | IntegerField | Number of items that failed to process |
| `error_message` | TextField | Error message if the job failed |

### ScrapedItem

Represents a piece of data scraped from the website:

| Field | Type | Description |
|-------|------|-------------|
| `job` | ForeignKey | Reference to the ScraperJob |
| `item_type` | CharField | Type of item (html_table/pdf_table/pdf_text) |
| `source_url` | URLField | URL where the item was found |
| `title` | CharField | Title of the item |
| `content` | JSONField | The actual data content |
| `metadata` | JSONField | Additional metadata about the item |
| `status` | CharField | Status of the item (pending/processed/failed/invalid) |

## Dashboard Components

### RealTimeDataPanel

A React component that displays real-time statistics with auto-refresh capabilities:

- Automatically refreshes every 30 seconds
- Manual refresh button
- Category filtering
- Data tables with the latest statistics

### Statistical Charts

- Population Growth by Region
- Economic Indicators Over Time
- Inflation Rate Trends
- Health Statistics Comparison
- Education Metrics

## Monitoring and Maintenance

### Logs

All scraper operations are logged in the following files:

- `scraper_scheduler.log` - Scheduler operations
- `scraper_output.log` - Standard output from scraper runs
- `scraper_error.log` - Error logs from scraper runs

### Django Admin Interface

The Django admin interface provides a comprehensive view of the scraper operations:

1. Log in to the admin site at `/admin/`
2. Navigate to "Scraper jobs" to see all scraping operations
3. Navigate to "Scraped items" to see all data items

### Database Maintenance

Periodic maintenance tasks:

1. Remove old scraper jobs and data:
   ```bash
   python manage.py cleanup_old_scraper_data --days 30
   ```

2. Optimize database performance:
   ```bash
   python manage.py optimize_scraper_db
   ```

## Troubleshooting

### Common Issues

1. **Scraper fails to connect to the website**:
   - Check internet connectivity
   - Verify that the NBS website is accessible
   - Check if the website structure has changed

2. **Scheduler not running**:
   - Check if Python process is running
   - Review log files for errors
   - Restart the scheduler service

3. **No data being returned from API**:
   - Check if scraper jobs are completing successfully
   - Verify that scraped items exist in the database
   - Check API logs for errors

### Diagnostic Commands

```bash
# Check the status of the most recent scraper job
python manage.py check_scraper_status

# Perform a test scrape with verbose output
python manage.py run_somalia_scraper_test --debug

# Check database connectivity
python manage.py check_db
```

## Development

### Adding New Data Categories

1. Update the `SomaliaStatsScraper.paths` dictionary in `somalia_scraper.py`
2. Add a new extraction method in the same file
3. Update the `extract_structured_data` method to call your new extraction method

### Extending the API

1. Add new endpoints to `views.py`
2. Register the endpoints in `urls.py`
3. Update the serializers as needed

### Customizing the Scheduler

1. Modify schedule intervals in `settings.py`
2. Update the `ScraperSchedulerService` class in `services.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Somalia National Bureau of Statistics for providing the source data
- The Django and React communities for their excellent frameworks
