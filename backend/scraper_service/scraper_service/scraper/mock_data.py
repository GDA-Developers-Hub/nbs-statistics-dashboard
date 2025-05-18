"""
Mock data generators for testing the Somalia scraper.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class MockDataGenerator:
    """
    Generate realistic mock data for various categories of Somalia statistics.
    """
    
    def __init__(self):
        # Set random seed for reproducibility
        np.random.seed(42)
        random.seed(42)
        
        self.regions = [
            'Awdal', 'Bakool', 'Banaadir', 'Bari', 'Bay', 'Galguduud', 
            'Gedo', 'Hiiraan', 'Jubbada Dhexe', 'Jubbada Hoose', 'Mudug', 
            'Nugaal', 'Sanaag', 'Shabeellaha Dhexe', 'Shabeellaha Hoose', 
            'Sool', 'Togdheer', 'Woqooyi Galbeed'
        ]
        
        self.districts = {
            'Awdal': ['Baki', 'Borama', 'Lughaye', 'Zeila'],
            'Bakool': ['El Barde', 'Huddur', 'Tayeglow', 'Wajid'],
            'Banaadir': ['Abdiaziz', 'Bondhere', 'Daynile', 'Dharkenley', 'Hamar-Jajab', 'Hamar-Weyne', 'Hawl-Wadag', 'Hodan', 'Karaan', 'Shangani', 'Shibis', 'Waberi', 'Wadajir', 'Wardhigley', 'Yaqshid'],
            'Bari': ['Bandar Beyla', 'Bosaso', 'Iskushuban', 'Qandala', 'Qardho'],
            'Bay': ['Baidoa', 'Burhakaba', 'Dinsor', 'Qansax Dheere'],
            'Galguduud': ['Abudwak', 'Adado', 'Dhusamareb', 'El Bur', 'Galhareeri'],
            'Gedo': ['Baardheere', 'Belet Haawo', 'Doolow', 'Garbahaarrey', 'Luuq'],
            'Hiiraan': ['Beledweyne', 'Buloburte', 'Jalalaqsi', 'Mahas'],
            'Jubbada Dhexe': ['Bu\'aale', 'Jilib', 'Saakow'],
            'Jubbada Hoose': ['Afmadow', 'Badhaadhe', 'Jamaame', 'Kismayo'],
            'Mudug': ['Galkayo', 'Hobyo', 'Jariban'],
            'Nugaal': ['Burtinle', 'Eyl', 'Garoowe'],
            'Sanaag': ['Ceel Afweyn', 'Ceerigaabo', 'Las Qorey'],
            'Shabeellaha Dhexe': ['Aden Yabal', 'Balcad', 'Cadale', 'Jowhar'],
            'Shabeellaha Hoose': ['Afgooye', 'Baraawe', 'Kurtunwaarey', 'Marka', 'Qoryooley', 'Sablaale', 'Wanla Weyn'],
            'Sool': ['Ainabo', 'Las Anod', 'Taleh'],
            'Togdheer': ['Burao', 'Odweyne', 'Sheikh'],
            'Woqooyi Galbeed': ['Berbera', 'Gebiley', 'Hargeisa']
        }
        
        self.years = list(range(2018, 2025))
        self.current_year = datetime.now().year
    
    def generate_population_data(self):
        """Generate mock population data by region."""
        df = pd.DataFrame()
        df['Region'] = self.regions
        
        # Base populations with some variation
        base_populations = {
            'Banaadir': 2500000,  # Mogadishu region
            'Woqooyi Galbeed': 1800000,  # Hargeisa region
            'Togdheer': 800000,
            'Shabeellaha Hoose': 950000,
            'Jubbada Hoose': 700000,
        }
        
        # Default population for regions not specified
        default_population = 400000
        
        # Generate population values for 2022
        pop_2022 = []
        for region in self.regions:
            base = base_populations.get(region, default_population)
            variation = np.random.normal(0, 0.05)  # 5% standard deviation
            pop_2022.append(int(base * (1 + variation)))
        
        df['Population_2022'] = pop_2022
        
        # Generate population for other years based on growth rates
        yearly_growth = {
            2018: 0.97,  # 3% less than 2022
            2019: 0.98,  # 2% less than 2022
            2020: 0.99,  # 1% less than 2022
            2021: 0.995,  # 0.5% less than 2022
            2022: 1.0,    # reference year
            2023: 1.027,  # 2.7% more than 2022
            2024: 1.054   # 5.4% more than 2022 (compounded 2.7%)
        }
        
        for year in self.years:
            if year != 2022:  # 2022 already added
                growth_factor = yearly_growth[year]
                df[f'Population_{year}'] = (df['Population_2022'] * growth_factor).astype(int)
        
        # Add male/female split (roughly 50/50 with small variations)
        for year in self.years:
            male_ratio = np.random.normal(0.495, 0.01, len(self.regions))  # slightly more female
            male_ratio = np.clip(male_ratio, 0.47, 0.52)  # Ensure reasonable bounds
            
            df[f'Male_{year}'] = (df[f'Population_{year}'] * male_ratio).astype(int)
            df[f'Female_{year}'] = (df[f'Population_{year}'] - df[f'Male_{year}']).astype(int)
        
        return df
    
    def generate_economic_data(self):
        """Generate mock economic indicators."""
        years = self.years
        
        # GDP data (in millions USD)
        gdp_base = 7500  # Base GDP for 2018 in millions USD
        gdp_growth_rates = [2.8, 2.9, -1.5, 2.2, 3.1, 3.6, 3.9]  # Annual growth rates
        
        gdp_values = [gdp_base]
        for rate in gdp_growth_rates[:-1]:  # Use one less rate to match the number of years
            gdp_values.append(gdp_values[-1] * (1 + rate/100))
        
        # Make sure we have the correct number of values
        gdp_values = gdp_values[:len(years)]
        
        # Ensure all arrays have the same length
        num_years = len(years)
        
        # Inflation data
        inflation_rates = [5.2, 4.7, 4.3, 4.6, 7.2, 6.1, 5.5][:num_years]
        
        # Unemployment data
        unemployment_rates = [14.7, 14.3, 14.6, 14.9, 14.8, 14.5, 14.2][:num_years]
        
        # Export and Import data (in millions USD)
        exports = [900, 950, 880, 920, 980, 1050, 1120][:num_years]
        imports = [2700, 2850, 2600, 2750, 2900, 3100, 3250][:num_years]
        
        # Exchange rate (Somali Shilling to USD)
        exchange_rates = [24500, 25200, 26100, 25900, 26800, 27500, 28100][:num_years]
        
        # Create dataframe
        data = {
            'Year': years,
            'GDP_Millions_USD': [round(val, 1) for val in gdp_values],
            'GDP_Growth_Rate': gdp_growth_rates[:num_years],
            'Inflation_Rate': inflation_rates,
            'Unemployment_Rate': unemployment_rates,
            'Exports_Millions_USD': exports,
            'Imports_Millions_USD': imports,
            'Trade_Balance_Millions_USD': [e-i for e, i in zip(exports, imports)],
            'Exchange_Rate_SOS_to_USD': exchange_rates
        }
        
        return pd.DataFrame(data)
    
    def generate_education_data(self):
        """Generate mock education statistics."""
        # Literacy rate by region and gender
        literacy_data = []
        
        for region in self.regions:
            # Base literacy varies by region
            if region in ['Banaadir', 'Woqooyi Galbeed']:
                base_literacy = 65  # Higher in urban areas
            elif region in ['Shabeellaha Hoose', 'Jubbada Hoose', 'Hiiraan']:
                base_literacy = 55  # Medium
            else:
                base_literacy = 45  # Lower in rural areas
            
            # Add variation
            variation = np.random.normal(0, 3)
            total_literacy = max(min(base_literacy + variation, 85), 35)
            
            # Gender gap - male literacy typically higher
            gender_gap = np.random.uniform(10, 18)
            male_literacy = min(total_literacy + gender_gap/2, 90)
            female_literacy = max(total_literacy - gender_gap/2, 25)
            
            literacy_data.append({
                'Region': region,
                'Total_Literacy_Rate': round(total_literacy, 1),
                'Male_Literacy_Rate': round(male_literacy, 1),
                'Female_Literacy_Rate': round(female_literacy, 1),
                'Year': 2023
            })
        
        # School enrollment data
        enrollment_data = []
        years = range(2018, 2025)
        
        enrollment_levels = {
            'Primary': {
                'base': 42,
                'growth': 1.8,
                'gender_gap': 10
            },
            'Secondary': {
                'base': 15,
                'growth': 2.2,
                'gender_gap': 12
            },
            'Tertiary': {
                'base': 5,
                'growth': 1.5,
                'gender_gap': 8
            }
        }
        
        for year in years:
            for level, params in enrollment_levels.items():
                # Calculate total enrollment with annual growth
                years_since_2018 = year - 2018
                total_rate = params['base'] + (years_since_2018 * params['growth'])
                
                # Gender breakdown
                gender_gap = params['gender_gap'] * (1 - years_since_2018 * 0.05)  # Gap reduces slightly over time
                male_rate = total_rate + gender_gap/2
                female_rate = total_rate - gender_gap/2
                
                enrollment_data.append({
                    'Year': year,
                    'Education_Level': level,
                    'Total_Enrollment_Rate': round(total_rate, 1),
                    'Male_Enrollment_Rate': round(male_rate, 1),
                    'Female_Enrollment_Rate': round(female_rate, 1)
                })
        
        return pd.DataFrame(literacy_data), pd.DataFrame(enrollment_data)
    
    def generate_health_data(self):
        """Generate mock health statistics."""
        # Infant mortality rate over years
        infant_mortality_data = []
        
        base_rate = 94.0  # Infant mortality per 1000 births (2018)
        annual_reduction = 1.8  # Estimated reduction per year
        
        for year in self.years:
            rate = base_rate - ((year - 2018) * annual_reduction)
            infant_mortality_data.append({
                'Year': year,
                'Infant_Mortality_Rate': round(rate, 1)
            })
            
        # Vaccination coverage by region
        vaccination_data = []
        vaccines = ['BCG', 'DPT3', 'Polio3', 'Measles']
        
        for region in self.regions:
            # Base coverage varies by region
            if region in ['Banaadir', 'Woqooyi Galbeed']:
                base_coverage = 70  # Higher in urban areas
            elif region in ['Shabeellaha Hoose', 'Jubbada Hoose']:
                base_coverage = 60  # Medium
            else:
                base_coverage = 45  # Lower in rural areas
            
            for vaccine in vaccines:
                # Add variation by vaccine
                if vaccine == 'BCG':
                    modifier = 5  # BCG has higher coverage
                elif vaccine == 'Measles':
                    modifier = -5  # Measles has lower coverage
                else:
                    modifier = 0
                
                # Add random variation
                variation = np.random.normal(0, 3)
                coverage = max(min(base_coverage + modifier + variation, 95), 30)
                
                vaccination_data.append({
                    'Region': region,
                    'Vaccine': vaccine,
                    'Coverage_Percent': round(coverage, 1),
                    'Year': 2023
                })
        
        # Life expectancy data
        life_expectancy_data = []
        
        for year in self.years:
            # Base life expectancy with slow improvement
            male_exp = 53.0 + (year - 2018) * 0.4
            female_exp = 56.5 + (year - 2018) * 0.4
            
            # Add small random variation
            male_exp += np.random.normal(0, 0.2)
            female_exp += np.random.normal(0, 0.2)
            
            life_expectancy_data.append({
                'Year': year,
                'Male_Life_Expectancy': round(male_exp, 1),
                'Female_Life_Expectancy': round(female_exp, 1),
                'Total_Life_Expectancy': round((male_exp + female_exp) / 2, 1)
            })
            
        return pd.DataFrame(infant_mortality_data), pd.DataFrame(vaccination_data), pd.DataFrame(life_expectancy_data)
    
    def generate_inflation_data(self):
        """Generate mock CPI and inflation data."""
        # Monthly CPI data for the past 3 years
        start_date = datetime(self.current_year - 3, 1, 1)
        end_date = datetime.now()
        
        # Generate dates
        dates = []
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date)
            current_date = current_date + timedelta(days=30)  # Approximate month
        
        # Generate CPI data with seasonal patterns and trend
        cpi_base = 100.0
        monthly_inflation = 0.4  # Base monthly inflation
        seasonal_amplitude = 1.2  # Seasonal variation
        
        cpi_values = []
        for i, date in enumerate(dates):
            # Add trend
            trend = cpi_base + (i * monthly_inflation)
            
            # Add seasonality (higher in mid-year)
            month = date.month
            seasonal = seasonal_amplitude * np.sin(np.pi * month / 6)
            
            # Add noise
            noise = np.random.normal(0, 0.5)
            
            # Calculate CPI
            cpi = trend + seasonal + noise
            cpi_values.append(round(cpi, 1))
            
        # Calculate year-over-year inflation
        yoy_inflation = []
        for i, cpi in enumerate(cpi_values):
            if i >= 12:  # Need at least 12 months of data
                inflation = ((cpi / cpi_values[i-12]) - 1) * 100
                yoy_inflation.append(round(inflation, 1))
            else:
                yoy_inflation.append(None)
        
        # Create dataframe
        data = {
            'Date': dates,
            'CPI': cpi_values,
            'YoY_Inflation': yoy_inflation
        }
        
        # Add category-specific inflation
        categories = ['Food', 'Housing', 'Transport', 'Healthcare', 'Education']
        for category in categories:
            # Different categories have different inflation profiles
            if category == 'Food':
                multiplier = 1.2  # Food inflation higher
                var = 0.8
            elif category == 'Transport':
                multiplier = 1.1
                var = 1.0
            elif category == 'Healthcare':
                multiplier = 0.9
                var = 0.5
            else:
                multiplier = 1.0
                var = 0.7
                
            category_inflation = []
            for inf in yoy_inflation:
                if inf is not None:
                    # Add variation to category inflation
                    cat_inf = inf * multiplier + np.random.normal(0, var)
                    category_inflation.append(round(cat_inf, 1))
                else:
                    category_inflation.append(None)
                    
            data[f'{category}_Inflation'] = category_inflation
        
        return pd.DataFrame(data)
    
    def generate_mock_data_for_category(self, category):
        """Generate mock data for a specific category."""
        if category == 'demographics':
            return {'Population Data': self.generate_population_data()}
        elif category == 'economy':
            return {'Economic Indicators': self.generate_economic_data()}
        elif category == 'education':
            literacy, enrollment = self.generate_education_data()
            return {'Literacy Rates': literacy, 'School Enrollment': enrollment}
        elif category == 'health':
            infant_mortality, vaccination, life_expectancy = self.generate_health_data()
            return {
                'Infant Mortality': infant_mortality, 
                'Vaccination Coverage': vaccination,
                'Life Expectancy': life_expectancy
            }
        elif category == 'inflation':
            return {'Consumer Price Index': self.generate_inflation_data()}
        else:
            return {} 