from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api_service.indicators.models import IndicatorValue

class StatisticsViewSet(viewsets.ViewSet):
    """
    API endpoints for aggregated statistics used in the dashboard.
    Provides summary data and recent updates.
    """
    
    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(settings.CACHE_TTL.get('summary', 900)))  # Cache for 15 minutes by default
    def summary(self, request):
        """
        Return aggregated summary statistics for the landing page.
        Includes key population, economic, social, and infrastructure metrics.
        """
        # This would normally involve complex database queries
        # For now, we'll return mock data that matches our frontend expectations
        summary_data = {
            "population": {
                "total": 17.3,  # in millions
                "growth_rate": 2.3,  # percent
                "last_updated": "May 2025"
            },
            "economic": {
                "gdp": 8.4,  # in billions USD
                "growth_rate": 5.2,  # percent
                "last_updated": "Feb 2025"
            },
            "education": {
                "literacy_rate": 45,  # percent
                "growth": 3,  # percent points increase
                "last_updated": "Jan 2025"
            },
            "health": {
                "life_expectancy": 58.2,  # years
                "change": 0.8,  # years increase
                "last_updated": "Mar 2025"
            }
        }
        
        return Response(summary_data)
        
    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(settings.CACHE_TTL.get('recent_updates', 300)))  # Cache for 5 minutes by default
    def recent_updates(self, request):
        """
        Return recently updated indicators for the landing page.
        """
        # In a real implementation, we'd query the database for recent updates
        # For now, we'll return mock data
        recent_updates = [
            {
                "indicator_name": "Census Population Data",
                "updated_at": "2025-05-15",
                "change_description": "Annual update with 2024 census data"
            },
            {
                "indicator_name": "Q1 2025 Economic Indicators",
                "updated_at": "2025-04-28",
                "change_description": "Quarterly economic indicators update"
            },
            {
                "indicator_name": "Annual Education Statistics",
                "updated_at": "2025-03-10",
                "change_description": "2024 educational outcomes report"
            },
            {
                "indicator_name": "Regional Development Indices",
                "updated_at": "2025-02-22",
                "change_description": "Updated development metrics by region"
            }
        ]
        
        return Response(recent_updates)
        
    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(settings.CACHE_TTL.get('dashboard', 600)))  # Cache for 10 minutes by default
    def dashboard_data(self, request, format=None):
        """
        Return pre-configured dashboard data based on type.
        
        Parameters:
        - type: The dashboard type (overview, population, economic, social, infrastructure)
        - region: Optional region code to filter data
        """
        dashboard_type = request.query_params.get('type', 'overview')
        region_code = request.query_params.get('region')
        
        # Mock data generation for each dashboard type
        # In a real implementation, we'd query the database based on the parameters
        
        if dashboard_type == 'population':
            # Population dashboard data
            data = {
                "population_growth": [
                    {"year": 2018, "population": 14.7, "growthRate": 2.9},
                    {"year": 2019, "population": 15.0, "growthRate": 3.0},
                    {"year": 2020, "population": 15.4, "growthRate": 2.8},
                    {"year": 2021, "population": 15.8, "growthRate": 2.7},
                    {"year": 2022, "population": 16.1, "growthRate": 2.6},
                    {"year": 2023, "population": 16.5, "growthRate": 2.5},
                    {"year": 2024, "population": 16.9, "growthRate": 2.4},
                    {"year": 2025, "population": 17.3, "growthRate": 2.3}
                ],
                "population_distribution": {
                    "urban": 45.8,
                    "rural": 54.2
                },
                "age_distribution": [
                    {"age_group": "0-14", "percentage": 46.2},
                    {"age_group": "15-24", "percentage": 19.5},
                    {"age_group": "25-54", "percentage": 28.9},
                    {"age_group": "55-64", "percentage": 3.4},
                    {"age_group": "65+", "percentage": 2.0}
                ]
            }
            
        elif dashboard_type == 'economic':
            # Economic dashboard data
            data = {
                "gdp_growth": [
                    {"year": 2018, "gdp": 7.1, "growth": 3.8},
                    {"year": 2019, "gdp": 7.3, "growth": 2.9},
                    {"year": 2020, "gdp": 7.5, "growth": 2.7},
                    {"year": 2021, "gdp": 7.7, "growth": 2.6},
                    {"year": 2022, "gdp": 7.9, "growth": 2.6},
                    {"year": 2023, "gdp": 8.1, "growth": 2.5},
                    {"year": 2024, "gdp": 8.2, "growth": 1.2},
                    {"year": 2025, "gdp": 8.4, "growth": 2.4}
                ],
                "cpi_trends": [
                    {"year": 2023, "quarter": "Q1", "cpi": 144},
                    {"year": 2023, "quarter": "Q2", "cpi": 146},
                    {"year": 2023, "quarter": "Q3", "cpi": 148},
                    {"year": 2023, "quarter": "Q4", "cpi": 150},
                    {"year": 2024, "quarter": "Q1", "cpi": 152},
                    {"year": 2024, "quarter": "Q2", "cpi": 154},
                    {"year": 2024, "quarter": "Q3", "cpi": 156},
                    {"year": 2024, "quarter": "Q4", "cpi": 158},
                    {"year": 2025, "quarter": "Q1", "cpi": 160}
                ],
                "sector_contribution": [
                    {"sector": "Agriculture", "percentage": 65.0},
                    {"sector": "Industry", "percentage": 10.0},
                    {"sector": "Services", "percentage": 25.0}
                ]
            }
            
        elif dashboard_type == 'social':
            # Social development dashboard data
            data = {
                "literacy_rate": [
                    {"year": 2018, "rate": 30},
                    {"year": 2019, "rate": 32},
                    {"year": 2020, "rate": 34},
                    {"year": 2021, "rate": 36},
                    {"year": 2022, "rate": 37},
                    {"year": 2023, "rate": 39},
                    {"year": 2024, "rate": 42},
                    {"year": 2025, "rate": 45}
                ],
                "vaccination_coverage": [
                    {"year": 2018, "coverage": 45},
                    {"year": 2019, "coverage": 52},
                    {"year": 2020, "coverage": 48},
                    {"year": 2021, "coverage": 56},
                    {"year": 2022, "coverage": 60},
                    {"year": 2023, "coverage": 65},
                    {"year": 2024, "coverage": 67},
                    {"year": 2025, "coverage": 70}
                ],
                "education_enrollment": {
                    "primary": 76.5,
                    "secondary": 42.3,
                    "tertiary": 8.7
                }
            }
            
        elif dashboard_type == 'infrastructure':
            # Infrastructure dashboard data
            data = {
                "electricity_access": [
                    {"year": 2018, "percentage": 32},
                    {"year": 2019, "percentage": 34},
                    {"year": 2020, "percentage": 36},
                    {"year": 2021, "percentage": 39},
                    {"year": 2022, "percentage": 42},
                    {"year": 2023, "percentage": 45},
                    {"year": 2024, "percentage": 49},
                    {"year": 2025, "percentage": 53}
                ],
                "road_network": {
                    "paved_km": 2875,
                    "unpaved_km": 18650,
                    "total_km": 21525
                },
                "water_access": {
                    "urban": 67.3,
                    "rural": 42.1,
                    "total": 52.8
                }
            }
            
        else:  # default to overview
            # Overview dashboard data with key metrics
            data = {
                "population_growth": [
                    {"year": 2020, "population": 15.4, "growthRate": 2.8},
                    {"year": 2021, "population": 15.8, "growthRate": 2.7},
                    {"year": 2022, "population": 16.1, "growthRate": 2.6},
                    {"year": 2023, "population": 16.5, "growthRate": 2.5},
                    {"year": 2024, "population": 16.9, "growthRate": 2.4},
                    {"year": 2025, "population": 17.3, "growthRate": 2.3}
                ],
                "literacy_rate": [
                    {"year": 2020, "rate": 34},
                    {"year": 2021, "rate": 36},
                    {"year": 2022, "rate": 37},
                    {"year": 2023, "rate": 39},
                    {"year": 2024, "rate": 42},
                    {"year": 2025, "rate": 45}
                ],
                "cpi_trends": [
                    {"year": 2024, "quarter": "Q1", "cpi": 152},
                    {"year": 2024, "quarter": "Q2", "cpi": 154},
                    {"year": 2024, "quarter": "Q3", "cpi": 156},
                    {"year": 2024, "quarter": "Q4", "cpi": 158},
                    {"year": 2025, "quarter": "Q1", "cpi": 160}
                ],
                "key_indicators": [
                    {"name": "GDP Growth", "value": "5.20%", "change": 0.8, "lastUpdated": "Feb 2025"},
                    {"name": "Inflation", "value": "7.10%", "change": -0.5, "lastUpdated": "Feb 2025"},
                    {"name": "Foreign Investment", "value": "$412M", "change": 2.3, "lastUpdated": "Jan 2025"},
                    {"name": "Urban Population", "value": "45.8%", "change": 1.2, "lastUpdated": "Mar 2025"},
                    {"name": "Unemployment", "value": "14.2%", "change": -0.3, "lastUpdated": "Dec 2024"},
                    {"name": "Primary School Enrollment", "value": "76.5%", "change": 3.1, "lastUpdated": "Feb 2025"}
                ]
            }
            
        return Response(data)
