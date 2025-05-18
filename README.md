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
````

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
