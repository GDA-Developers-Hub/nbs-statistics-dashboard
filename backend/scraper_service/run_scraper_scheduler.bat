@echo off
cd %~dp0
echo Running Somalia Statistics Scraper at %date% %time%
python manage.py run_somalia_scraper_test
echo Scraping completed at %date% %time% 