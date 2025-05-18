import pandas as pd
import numpy as np
import re
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union

logger = logging.getLogger(__name__)

class BaseProcessor:
    """
    Base class for ETL processors with common functionality.
    """
    def __init__(self):
        self.raw_data = None
        self.processed_data = None
        self.metadata = {}
    
    def load(self, data: str):
        """
        Load data from JSON string or dict.
        """
        if isinstance(data, str):
            try:
                self.raw_data = json.loads(data)
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON data: {str(e)}")
                raise
        else:
            self.raw_data = data
        return self
    
    def process(self):
        """
        Process the data (to be implemented by subclasses).
        """
        raise NotImplementedError("Subclasses must implement process()")
    
    def get_result(self) -> Dict[str, Any]:
        """
        Get the processed result.
        """
        return {
            'data': self.processed_data,
            'metadata': self.metadata
        }
    
    @staticmethod
    def clean_string(value: str) -> str:
        """
        Clean a string value.
        """
        if not value or not isinstance(value, str):
            return ""
        
        # Remove extra whitespace
        value = re.sub(r'\s+', ' ', value).strip()
        
        # Remove special characters that might cause issues
        value = re.sub(r'[^\w\s\-\.,;:\'"%&\(\)]+', '', value)
        
        return value
    
    @staticmethod
    def normalize_column_name(column: str) -> str:
        """
        Normalize column names to snake_case.
        """
        if not column or not isinstance(column, str):
            return "unknown"
        
        # Remove special characters and replace spaces with underscores
        clean_name = re.sub(r'[^\w\s]', '', column)
        clean_name = re.sub(r'\s+', '_', clean_name).lower()
        
        return clean_name
    
    @staticmethod
    def extract_numeric(value: Any) -> Optional[float]:
        """
        Extract numeric value from string.
        """
        if pd.isna(value) or value is None:
            return None
        
        if isinstance(value, (int, float)):
            return float(value)
        
        if isinstance(value, str):
            # Remove non-numeric characters except decimal point and negative sign
            numeric_str = re.sub(r'[^\d\.-]', '', value)
            
            try:
                return float(numeric_str)
            except ValueError:
                return None
        
        return None
    
    @staticmethod
    def extract_date(value: Any) -> Optional[datetime]:
        """
        Extract date from string using various formats.
        """
        if pd.isna(value) or value is None:
            return None
        
        if isinstance(value, datetime):
            return value
        
        if isinstance(value, str):
            date_formats = [
                '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d',
                '%d-%m-%Y', '%m-%d-%Y', '%b %Y', '%B %Y', '%Y'
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(value.strip(), fmt)
                except ValueError:
                    continue
        
        return None
    
    def detect_data_types(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Detect data types for each column.
        """
        dtype_map = {}
        
        for col in df.columns:
            # Check if column is mostly numeric
            if pd.to_numeric(df[col], errors='coerce').notna().mean() > 0.7:
                dtype_map[col] = 'numeric'
            # Check if column is mostly dates
            elif pd.to_datetime(df[col], errors='coerce').notna().mean() > 0.7:
                dtype_map[col] = 'date'
            # Default to string
            else:
                dtype_map[col] = 'string'
        
        return dtype_map
    
    def detect_time_dimension(self, df: pd.DataFrame) -> Optional[str]:
        """
        Detect column that might represent time dimension.
        """
        # Look for columns with date in name
        date_columns = [col for col in df.columns if any(term in col.lower() for term in 
                                                       ['year', 'month', 'date', 'time', 'period'])]
        
        # Check if any column contains dates
        if not date_columns:
            dtype_map = self.detect_data_types(df)
            date_columns = [col for col, dtype in dtype_map.items() if dtype == 'date']
        
        # Return the first date column found, if any
        return date_columns[0] if date_columns else None


class HTMLTableProcessor(BaseProcessor):
    """
    Process HTML tables from the scraper.
    """
    def process(self) -> 'HTMLTableProcessor':
        """
        Process HTML table data from pandas DataFrame JSON.
        """
        if not self.raw_data or not isinstance(self.raw_data, dict):
            raise ValueError("Invalid data format")
        
        try:
            # Parse the table JSON created by pandas
            if 'data' in self.raw_data:
                df = pd.DataFrame(self.raw_data['data'])
                
                # If there are schema details, get column information
                if 'schema' in self.raw_data and 'fields' in self.raw_data['schema']:
                    column_info = {field.get('name'): field for field in self.raw_data['schema'].get('fields', [])}
                    self.metadata['column_info'] = column_info
            else:
                # If it's not in the expected format, try a direct conversion
                df = pd.DataFrame(self.raw_data)
            
            # Clean up the DataFrame
            self._clean_dataframe(df)
            
            # Detect data types and structure
            self._analyze_dataframe(df)
            
            # Convert to standardized format
            self.processed_data = self._to_records(df)
            
            return self
            
        except Exception as e:
            logger.error(f"Error processing HTML table: {str(e)}")
            raise
    
    def _clean_dataframe(self, df: pd.DataFrame):
        """
        Clean the DataFrame.
        """
        # Drop rows that are all NaN
        df.dropna(how='all', inplace=True)
        
        # Drop columns that are all NaN
        df.dropna(axis=1, how='all', inplace=True)
        
        # Clean column names
        df.columns = [self.normalize_column_name(col) for col in df.columns]
        
        # Clean string values
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(lambda x: self.clean_string(x) if isinstance(x, str) else x)
    
    def _analyze_dataframe(self, df: pd.DataFrame):
        """
        Analyze the DataFrame structure.
        """
        # Detect data types
        self.metadata['dtype_map'] = self.detect_data_types(df)
        
        # Detect time dimension
        time_col = self.detect_time_dimension(df)
        if time_col:
            self.metadata['time_dimension'] = time_col
        
        # Detect potential dimension columns (categorical variables)
        categorical_cols = []
        for col in df.columns:
            unique_vals = df[col].nunique()
            total_vals = len(df)
            
            # If column has relatively few unique values compared to total rows
            if unique_vals < total_vals * 0.5 and unique_vals > 1:
                categorical_cols.append(col)
        
        self.metadata['categorical_columns'] = categorical_cols
        
        # Store basic statistics
        self.metadata['row_count'] = len(df)
        self.metadata['column_count'] = len(df.columns)
    
    def _to_records(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Convert DataFrame to a list of records.
        """
        # Convert to dictionary records format
        records = df.to_dict(orient='records')
        
        # Clean up NaN values
        for record in records:
            for key, value in list(record.items()):
                if pd.isna(value):
                    record[key] = None
        
        return records


class PDFTableProcessor(HTMLTableProcessor):
    """
    Process PDF tables from the scraper.
    Extends HTMLTableProcessor since the data format is similar,
    but adds PDF-specific processing.
    """
    def process(self) -> 'PDFTableProcessor':
        """
        Process PDF table data.
        """
        # Use the parent process method
        super().process()
        
        # Add PDF-specific metadata
        self.metadata['source_type'] = 'pdf'
        
        # Additional PDF-specific cleaning if needed
        if self.processed_data:
            self._fix_pdf_extraction_issues()
            
        return self
    
    def _fix_pdf_extraction_issues(self):
        """
        Fix common issues with PDF table extraction.
        """
        # Detect and remove duplicate headers that may appear in PDF extractions
        if self.processed_data and len(self.processed_data) > 1:
            # Check if the first row matches any column names
            first_row = self.processed_data[0]
            column_names = set(first_row.keys())
            
            # Check if first row values are similar to column names
            matches = 0
            for col, val in first_row.items():
                if val and isinstance(val, str) and col.lower() in val.lower():
                    matches += 1
            
            # If many column values match column names, it's likely a header row
            if matches > len(column_names) * 0.5:
                self.processed_data = self.processed_data[1:]
                self.metadata['header_row_removed'] = True


class DataCategorizer:
    """
    Categorize the processed data into different indicators and datasets.
    """
    def __init__(self, processed_data, metadata):
        self.processed_data = processed_data
        self.metadata = metadata
        self.categorized_data = {}
    
    def categorize(self):
        """
        Categorize the data by detecting its type and structure.
        """
        # Initialize categories
        self.categorized_data = {
            'indicator_type': None,
            'time_series': False,
            'regional_data': False,
            'sector_data': False,
            'dimensions': [],
            'measures': [],
        }
        
        # Detect time series data
        if 'time_dimension' in self.metadata:
            self.categorized_data['time_series'] = True
            self.categorized_data['dimensions'].append(self.metadata['time_dimension'])
        
        # Detect regional data
        region_keywords = ['region', 'district', 'state', 'province', 'city', 'town', 'area']
        for col in self.metadata.get('categorical_columns', []):
            if any(keyword in col.lower() for keyword in region_keywords):
                self.categorized_data['regional_data'] = True
                self.categorized_data['dimensions'].append(col)
        
        # Detect sector data
        sector_keywords = ['sector', 'industry', 'category', 'type', 'group']
        for col in self.metadata.get('categorical_columns', []):
            if any(keyword in col.lower() for keyword in sector_keywords):
                self.categorized_data['sector_data'] = True
                self.categorized_data['dimensions'].append(col)
        
        # Identify measures (numeric columns)
        for col, dtype in self.metadata.get('dtype_map', {}).items():
            if dtype == 'numeric' and col not in self.categorized_data['dimensions']:
                self.categorized_data['measures'].append(col)
        
        # Determine indicator type based on detected patterns
        self._determine_indicator_type()
        
        return self.categorized_data
    
    def _determine_indicator_type(self):
        """
        Determine the most likely indicator type based on column names and data structure.
        """
        # Create a mapping of keywords to indicator types
        indicator_type_keywords = {
            'population': ['population', 'people', 'persons', 'inhabitants', 'demographics', 'citizen'],
            'economic': ['gdp', 'economy', 'inflation', 'cpi', 'price', 'income', 'economic', 'export', 'import', 'trade'],
            'education': ['education', 'school', 'literacy', 'student', 'teacher', 'enrollment'],
            'health': ['health', 'hospital', 'disease', 'mortality', 'vaccination', 'vaccine', 'immunization'],
            'infrastructure': ['infrastructure', 'road', 'water', 'electricity', 'energy', 'communication'],
            'agriculture': ['agriculture', 'crop', 'livestock', 'farming', 'land', 'food'],
        }
        
        # Count keyword matches for all columns
        type_scores = {indicator_type: 0 for indicator_type in indicator_type_keywords.keys()}
        
        # Check column names for keywords
        for col in self.metadata.get('dtype_map', {}):
            for indicator_type, keywords in indicator_type_keywords.items():
                if any(keyword in col.lower() for keyword in keywords):
                    type_scores[indicator_type] += 1
        
        # Get the indicator type with the highest score
        max_score = max(type_scores.values())
        if max_score > 0:
            # Find all types with the max score
            max_types = [t for t, s in type_scores.items() if s == max_score]
            self.categorized_data['indicator_type'] = max_types[0]  # Take the first one if there are ties
