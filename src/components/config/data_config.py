"""
📊 Data Configuration Module

Data-specific configuration for the Car Market Analysis Executive Dashboard.
Contains data loading settings, column mappings, and validation rules.
"""

# Data File Configuration
DATA_FILES = {
    'basic_table': {
        'filename': 'Basic_table.csv',
        'description': 'Core vehicle information and identifiers',
        'primary_key': 'Genmodel_ID',
        'required_columns': ['Automaker', 'Genmodel', 'Genmodel_ID']
    },
    'trim_table': {
        'filename': 'Trim_table.csv',
        'description': 'Vehicle trim levels and specifications',
        'primary_key': 'Genmodel_ID',
        'required_columns': ['Genmodel_ID', 'Trim', 'Year', 'Price']
    },
    'price_table': {
        'filename': 'Price_table.csv',
        'description': 'Pricing information by model and year',
        'primary_key': 'Genmodel_ID',
        'required_columns': ['Genmodel_ID', 'Year', 'Entry_price']
    },
    'sales_table': {
        'filename': 'Sales_table.csv',
        'description': 'Sales data by model and year',
        'primary_key': 'Genmodel_ID',
        'required_columns': ['Genmodel_ID', 'Genmodel']
    }
}

# Column Standardization Mapping
COLUMN_MAPPING = {
    'basic_table': {
        'Maker': 'Automaker',
        'Model': 'Genmodel',
        'Model_ID': 'Genmodel_ID'
    },
    'trim_table': {
        'Maker': 'Automaker',
        'Model': 'Genmodel',
        'Model_ID': 'Genmodel_ID'
    },
    'price_table': {
        'Maker': 'Automaker',
        'Model': 'Genmodel',
        'Model_ID': 'Genmodel_ID'
    },
    'sales_table': {
        'Maker': 'Automaker',
        'Model': 'Genmodel',
        'Model_ID': 'Genmodel_ID'
    }
}

# Data Validation Rules
VALIDATION_RULES = {
    'basic_table': {
        'Genmodel_ID': {'type': 'string', 'required': True, 'unique': True},
        'Automaker': {'type': 'string', 'required': True},
        'Genmodel': {'type': 'string', 'required': True}
    },
    'trim_table': {
        'Genmodel_ID': {'type': 'string', 'required': True},
        'Year': {'type': 'int', 'min': 2000, 'max': 2025},
        'Price': {'type': 'int', 'min': 1000, 'max': 1000000}
    },
    'price_table': {
        'Genmodel_ID': {'type': 'string', 'required': True},
        'Year': {'type': 'int', 'min': 2000, 'max': 2025},
        'Entry_price': {'type': 'int', 'min': 1000, 'max': 1000000}
    },
    'sales_table': {
        'Genmodel_ID': {'type': 'string', 'required': True},
        'Genmodel': {'type': 'string', 'required': True}
    }
}

# Sales Data Configuration
SALES_YEARS = [str(year) for year in range(2001, 2021)]  # 2001-2020

# Data Quality Thresholds
DATA_QUALITY_THRESHOLDS = {
    'missing_data_warning': 0.05,  # 5% missing data triggers warning
    'missing_data_error': 0.20,    # 20% missing data triggers error
    'duplicate_threshold': 0.02,   # 2% duplicates triggers warning
    'outlier_threshold': 0.05      # 5% outliers triggers review
}

# Memory Optimization Settings
MEMORY_CONFIG = {
    'chunk_size': 10000,
    'max_memory_usage': 0.8,  # 80% of available memory
    'optimize_dtypes': True,
    'use_categorical': True
}

# Export Configuration
EXPORT_CONFIG = {
    'default_format': 'csv',
    'supported_formats': ['csv', 'xlsx', 'json', 'parquet'],
    'max_rows_per_export': 1000000,
    'include_metadata': True
}

