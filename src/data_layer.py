"""
📊 Data Processing Layer for Car Market Analysis Executive Dashboard

Advanced data loading, validation, feature engineering, and export functionality.
Handles data quality assessment and preprocessing for executive-grade analytics.
"""

import pandas as pd
import numpy as np
import os
import json
from typing import Dict, List, Optional, Any, Tuple, Union
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import configuration
try:
    from .components.config.data_config import (
        DATA_FILES, COLUMN_MAPPING, VALIDATION_RULES, 
        SALES_YEARS, DATA_QUALITY_THRESHOLDS, MEMORY_CONFIG, EXPORT_CONFIG
    )
    from .components.config.app_config import DATA_CONFIG
except ImportError:
    # Fallback configuration
    DATA_FILES = {}
    COLUMN_MAPPING = {}
    VALIDATION_RULES = {}
    SALES_YEARS = []
    DATA_QUALITY_THRESHOLDS = {'missing_data_warning': 0.05, 'missing_data_error': 0.20}
    MEMORY_CONFIG = {'chunk_size': 10000, 'optimize_dtypes': True}
    EXPORT_CONFIG = {'default_format': 'csv', 'supported_formats': ['csv', 'xlsx']}
    DATA_CONFIG = {}


class DataProcessor:
    """
    🏭 Advanced Data Processing Engine
    
    Handles data loading, validation, feature engineering, and export functionality
    with executive-grade quality standards and performance optimization.
    """

    def __init__(self, data_path: str = 'data/'):
        """
        Initialize the DataProcessor with configuration and validation rules.
        
        Args:
            data_path (str): Path to the directory containing CSV files
        """
        self.data_path = data_path
        self.datasets: Dict[str, pd.DataFrame] = {}
        self.validation_results: Dict[str, Dict[str, Any]] = {}
        self.quality_report: Dict[str, Dict[str, float]] = {}
        self.feature_engineering_config: Dict[str, Any] = {}
        
        # Initialize processing pipeline
        self._setup_feature_engineering()
        self._load_and_validate_data()

    def _setup_feature_engineering(self) -> None:
        """Setup feature engineering configuration and rules."""
        self.feature_engineering_config = {
            'price_features': {
                'price_tiers': {
                    'budget': (0, 20000),
                    'mid_range': (20000, 50000),
                    'premium': (50000, 100000),
                    'luxury': (100000, float('inf'))
                },
                'price_volatility_threshold': 0.3
            },
            'sales_features': {
                'performance_tiers': {
                    'low': (0, 10000),
                    'medium': (10000, 50000),
                    'high': (50000, 100000),
                    'excellent': (100000, float('inf'))
                },
                'trend_calculation': True
            },
            'market_features': {
                'market_segments': ['budget', 'mid_range', 'premium', 'luxury'],
                'competitor_analysis': True
            }
        }

    def _load_and_validate_data(self) -> None:
        """Load all datasets and perform initial validation."""
        print("[INFO] Loading and validating data...")
        
        for name, config in DATA_FILES.items():
            filename = config['filename']
            file_path = os.path.join(self.data_path, filename)
            
            try:
                # Load data with optimization
                df = self._load_single_file(file_path, name)
                if not df.empty:
                    self.datasets[name] = df
                    
                    # Perform validation
                    validation_result = self._validate_dataset(df, name, config)
                    self.validation_results[name] = validation_result
                    
                    # Generate quality report
                    quality_metrics = self._assess_data_quality(df, name)
                    self.quality_report[name] = quality_metrics
                    
                    print(f"[OK] {name.upper()}: Loaded and validated - {df.shape}")
                else:
                    print(f"[ERROR] {name.upper()}: Failed to load - Empty DataFrame")
                    
            except Exception as e:
                print(f"[ERROR] {name.upper()}: Error loading {filename} - {str(e)}")
                self.datasets[name] = pd.DataFrame()
                self.validation_results[name] = {'status': 'error', 'message': str(e)}

    def _load_single_file(self, file_path: str, dataset_name: str) -> pd.DataFrame:
        """Load a single CSV file with optimization and error handling."""
        try:
            # Load with chunking for large files
            chunk_size = MEMORY_CONFIG.get('chunk_size', 10000)
            
            if os.path.getsize(file_path) > 50 * 1024 * 1024:  # 50MB
                print(f"[INFO] Loading large file {dataset_name} in chunks...")
                chunks = []
                for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                    chunks.append(chunk)
                df = pd.concat(chunks, ignore_index=True)
            else:
                df = pd.read_csv(file_path)
            
            # Optimize data types if enabled
            if MEMORY_CONFIG.get('optimize_dtypes', True):
                df = self._optimize_dataframe_dtypes(df, dataset_name)
            
            # Apply column mapping
            df = self._apply_column_mapping(df, dataset_name)
            
            return df
            
        except Exception as e:
            print(f"[ERROR] Error loading {file_path}: {str(e)}")
            return pd.DataFrame()

    def _optimize_dataframe_dtypes(self, df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
        """Optimize DataFrame memory usage by converting dtypes."""
        optimized_df = df.copy()
        
        for col in optimized_df.columns:
            col_type = optimized_df[col].dtype
            
            if col_type != 'object':
                # Optimize numeric types
                if col_type in ['int64', 'int32']:
                    if optimized_df[col].min() >= 0:
                        if optimized_df[col].max() < 255:
                            optimized_df[col] = optimized_df[col].astype('uint8')
                        elif optimized_df[col].max() < 65535:
                            optimized_df[col] = optimized_df[col].astype('uint16')
                        elif optimized_df[col].max() < 4294967295:
                            optimized_df[col] = optimized_df[col].astype('uint32')
                    else:
                        if optimized_df[col].min() > -128 and optimized_df[col].max() < 127:
                            optimized_df[col] = optimized_df[col].astype('int8')
                        elif optimized_df[col].min() > -32768 and optimized_df[col].max() < 32767:
                            optimized_df[col] = optimized_df[col].astype('int16')
                        elif optimized_df[col].min() > -2147483648 and optimized_df[col].max() < 2147483647:
                            optimized_df[col] = optimized_df[col].astype('int32')
                
                elif col_type in ['float64']:
                    optimized_df[col] = optimized_df[col].astype('float32')
            
            else:
                # Convert object columns to category if beneficial
                if optimized_df[col].nunique() / len(optimized_df) < 0.5:
                    optimized_df[col] = optimized_df[col].astype('category')
        
        return optimized_df

    def _apply_column_mapping(self, df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
        """Apply column name standardization based on configuration."""
        if dataset_name in COLUMN_MAPPING:
            mapping = COLUMN_MAPPING[dataset_name]
            df = df.rename(columns=mapping)
        
        return df

    def _validate_dataset(self, df: pd.DataFrame, dataset_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate dataset against predefined rules."""
        validation_result = {
            'status': 'success',
            'warnings': [],
            'errors': [],
            'metrics': {}
        }
        
        # Check required columns
        required_columns = config.get('required_columns', [])
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            validation_result['errors'].append(f"Missing required columns: {missing_columns}")
            validation_result['status'] = 'error'
        
        # Apply validation rules
        if dataset_name in VALIDATION_RULES:
            rules = VALIDATION_RULES[dataset_name]
            
            for column, rule in rules.items():
                if column in df.columns:
                    column_validation = self._validate_column(df[column], column, rule)
                    validation_result['metrics'][column] = column_validation
                    
                    if column_validation['status'] == 'error':
                        validation_result['errors'].extend(column_validation['errors'])
                        validation_result['status'] = 'error'
                    elif column_validation['status'] == 'warning':
                        validation_result['warnings'].extend(column_validation['warnings'])
        
        return validation_result

    def _validate_column(self, series: pd.Series, column_name: str, rules: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a single column against rules."""
        result = {
            'status': 'success',
            'warnings': [],
            'errors': [],
            'statistics': {}
        }
        
        # Type validation
        if 'type' in rules:
            expected_type = rules['type']
            if expected_type == 'string':
                if not pd.api.types.is_string_dtype(series):
                    result['warnings'].append(f"Column {column_name} is not string type")
            elif expected_type == 'int':
                if not pd.api.types.is_integer_dtype(series):
                    result['warnings'].append(f"Column {column_name} is not integer type")
        
        # Required validation
        if rules.get('required', False):
            null_count = series.isnull().sum()
            if null_count > 0:
                result['errors'].append(f"Column {column_name} has {null_count} null values but is required")
                result['status'] = 'error'
        
        # Unique validation
        if rules.get('unique', False):
            duplicate_count = series.duplicated().sum()
            if duplicate_count > 0:
                result['warnings'].append(f"Column {column_name} has {duplicate_count} duplicate values")
                if result['status'] != 'error':
                    result['status'] = 'warning'
        
        # Range validation
        if 'min' in rules or 'max' in rules:
            if pd.api.types.is_numeric_dtype(series):
                min_val = rules.get('min')
                max_val = rules.get('max')
                
                if min_val is not None and series.min() < min_val:
                    result['warnings'].append(f"Column {column_name} has values below minimum {min_val}")
                
                if max_val is not None and series.max() > max_val:
                    result['warnings'].append(f"Column {column_name} has values above maximum {max_val}")
        
        # Calculate statistics
        result['statistics'] = {
            'count': len(series),
            'null_count': series.isnull().sum(),
            'unique_count': series.nunique(),
            'duplicate_count': series.duplicated().sum()
        }
        
        if pd.api.types.is_numeric_dtype(series):
            result['statistics'].update({
                'min': series.min(),
                'max': series.max(),
                'mean': series.mean(),
                'std': series.std()
            })
        
        return result

    def _assess_data_quality(self, df: pd.DataFrame, dataset_name: str) -> Dict[str, float]:
        """Assess overall data quality metrics for a dataset."""
        quality_metrics = {}
        
        # Completeness score (0-100)
        total_cells = len(df) * len(df.columns)
        null_cells = df.isnull().sum().sum()
        completeness = (1 - null_cells / total_cells) * 100
        quality_metrics['completeness_score'] = completeness
        
        # Uniqueness score (0-100)
        duplicate_rows = df.duplicated().sum()
        uniqueness = (1 - duplicate_rows / len(df)) * 100
        quality_metrics['uniqueness_score'] = uniqueness
        
        # Consistency score (0-100)
        consistency_score = 100.0
        for col in df.select_dtypes(include=['object']).columns:
            # Check for inconsistent values
            inconsistent_values = df[col].str.contains('N/A|NULL|null|undefined', case=False, na=False).sum()
            if inconsistent_values > 0:
                consistency_score -= (inconsistent_values / len(df)) * 20
        
        quality_metrics['consistency_score'] = max(0, consistency_score)
        
        # Overall quality score
        overall_score = (completeness * 0.4 + uniqueness * 0.3 + consistency_score * 0.3)
        quality_metrics['overall_quality_score'] = overall_score
        
        # Memory efficiency
        memory_mb = df.memory_usage(deep=True).sum() / 1024**2
        quality_metrics['memory_mb'] = memory_mb
        
        return quality_metrics

    # ==================== FEATURE ENGINEERING METHODS ====================

    def engineer_price_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer price-related features."""
        engineered_df = df.copy()
        
        if 'Entry_price' in engineered_df.columns:
            # Price tiers
            price_tiers = self.feature_engineering_config['price_features']['price_tiers']
            
            def categorize_price(price):
                if pd.isna(price):
                    return 'unknown'
                for tier, (min_price, max_price) in price_tiers.items():
                    if min_price <= price < max_price:
                        return tier
                return 'unknown'
            
            engineered_df['price_tier'] = engineered_df['Entry_price'].apply(categorize_price)
            
            # Price volatility (if multiple prices per model)
            if 'Genmodel_ID' in engineered_df.columns:
                price_volatility = engineered_df.groupby('Genmodel_ID')['Entry_price'].std() / \
                                 engineered_df.groupby('Genmodel_ID')['Entry_price'].mean()
                engineered_df['price_volatility'] = engineered_df['Genmodel_ID'].map(price_volatility)
                
                # High volatility flag
                volatility_threshold = self.feature_engineering_config['price_features']['price_volatility_threshold']
                engineered_df['high_price_volatility'] = engineered_df['price_volatility'] > volatility_threshold
        
        return engineered_df

    def engineer_sales_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer sales-related features."""
        engineered_df = df.copy()
        
        # Reshape sales data if needed
        year_columns = [col for col in df.columns if col.isdigit()]
        if year_columns:
            # Calculate total sales
            engineered_df['total_sales'] = engineered_df[year_columns].sum(axis=1)
            
            # Calculate average sales
            engineered_df['avg_sales'] = engineered_df[year_columns].mean(axis=1)
            
            # Calculate sales trend
            if len(year_columns) >= 2:
                def calculate_trend(row):
                    years = [int(col) for col in year_columns]
                    sales = [row[col] for col in year_columns]
                    if len(sales) > 1:
                        return np.polyfit(years, sales, 1)[0]
                    return 0
                
                engineered_df['sales_trend'] = engineered_df.apply(calculate_trend, axis=1)
            
            # Performance tiers
            performance_tiers = self.feature_engineering_config['sales_features']['performance_tiers']
            
            def categorize_performance(total_sales):
                if pd.isna(total_sales):
                    return 'unknown'
                for tier, (min_sales, max_sales) in performance_tiers.items():
                    if min_sales <= total_sales < max_sales:
                        return tier
                return 'unknown'
            
            engineered_df['performance_tier'] = engineered_df['total_sales'].apply(categorize_performance)
        
        return engineered_df

    def engineer_market_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer market-related features."""
        engineered_df = df.copy()
        
        if 'Automaker' in engineered_df.columns:
            # Market concentration
            automaker_counts = engineered_df['Automaker'].value_counts()
            total_models = len(engineered_df)
            
            engineered_df['automaker_market_share'] = engineered_df['Automaker'].map(
                automaker_counts / total_models
            )
            
            # Market segment analysis
            if 'price_tier' in engineered_df.columns:
                market_segments = self.feature_engineering_config['market_features']['market_segments']
                engineered_df['market_segment'] = engineered_df['price_tier']
        
        return engineered_df

    def engineer_all_features(self, df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
        """Apply all feature engineering methods to a dataset."""
        engineered_df = df.copy()
        
        # Apply dataset-specific feature engineering
        if dataset_name == 'price':
            engineered_df = self.engineer_price_features(engineered_df)
        elif dataset_name == 'sales':
            engineered_df = self.engineer_sales_features(engineered_df)
        
        # Apply general market features
        if any(col in engineered_df.columns for col in ['Automaker', 'price_tier']):
            engineered_df = self.engineer_market_features(engineered_df)
        
        return engineered_df

    # ==================== DATA EXPORT METHODS ====================

    def export_dataset(self, dataset_name: str, format: str = 'csv', 
                      include_metadata: bool = True) -> str:
        """Export a dataset to specified format with optional metadata."""
        if dataset_name not in self.datasets:
            raise ValueError(f"Dataset '{dataset_name}' not found")
        
        df = self.datasets[dataset_name]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == 'csv':
            filename = f"{dataset_name}_{timestamp}.csv"
            filepath = os.path.join(self.data_path, filename)
            df.to_csv(filepath, index=False)
            
        elif format == 'xlsx':
            filename = f"{dataset_name}_{timestamp}.xlsx"
            filepath = os.path.join(self.data_path, filename)
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Data', index=False)
                
                if include_metadata:
                    # Add metadata sheet
                    metadata_df = self._create_metadata_sheet(dataset_name)
                    metadata_df.to_excel(writer, sheet_name='Metadata', index=False)
                    
                    # Add quality report sheet
                    quality_df = self._create_quality_report_sheet(dataset_name)
                    quality_df.to_excel(writer, sheet_name='Quality_Report', index=False)
        
        elif format == 'json':
            filename = f"{dataset_name}_{timestamp}.json"
            filepath = os.path.join(self.data_path, filename)
            df.to_json(filepath, orient='records', indent=2)
        
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        print(f"[OK] Exported {dataset_name} to {filename}")
        return filepath

    def _create_metadata_sheet(self, dataset_name: str) -> pd.DataFrame:
        """Create metadata information for export."""
        metadata = []
        
        # Basic information
        df = self.datasets[dataset_name]
        metadata.append(['Dataset Name', dataset_name])
        metadata.append(['Shape', f"{df.shape[0]} rows x {df.shape[1]} columns"])
        metadata.append(['Memory Usage', f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"])
        metadata.append(['Export Timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        
        # Column information
        metadata.append(['', ''])  # Empty row
        metadata.append(['Column Information', ''])
        for col in df.columns:
            metadata.append([col, str(df[col].dtype)])
        
        return pd.DataFrame(metadata, columns=['Property', 'Value'])

    def _create_quality_report_sheet(self, dataset_name: str) -> pd.DataFrame:
        """Create quality report for export."""
        if dataset_name in self.quality_report:
            quality_data = self.quality_report[dataset_name]
            return pd.DataFrame(list(quality_data.items()), columns=['Metric', 'Value'])
        return pd.DataFrame()

    def export_all_datasets(self, format: str = 'xlsx') -> List[str]:
        """Export all datasets to specified format."""
        exported_files = []
        
        for dataset_name in self.datasets.keys():
            try:
                filepath = self.export_dataset(dataset_name, format, include_metadata=True)
                exported_files.append(filepath)
            except Exception as e:
                print(f"[ERROR] Error exporting {dataset_name}: {str(e)}")
        
        return exported_files

    # ==================== DATA SUMMARY METHODS ====================

    def get_data_summary(self) -> Dict[str, Any]:
        """Get comprehensive data summary including quality metrics."""
        summary = {
            'datasets': {},
            'overall_quality': {},
            'validation_summary': {},
            'export_info': EXPORT_CONFIG
        }
        
        # Dataset summaries
        for name, df in self.datasets.items():
            summary['datasets'][name] = {
                'shape': df.shape,
                'memory_mb': df.memory_usage(deep=True).sum() / 1024**2,
                'columns': list(df.columns),
                'dtypes': df.dtypes.to_dict(),
                'quality_score': self.quality_report.get(name, {}).get('overall_quality_score', 0)
            }
        
        # Overall quality metrics
        if self.quality_report:
            overall_scores = [metrics.get('overall_quality_score', 0) for metrics in self.quality_report.values()]
            summary['overall_quality'] = {
                'average_quality_score': np.mean(overall_scores),
                'total_datasets': len(self.datasets),
                'total_memory_mb': sum(df.memory_usage(deep=True).sum() / 1024**2 for df in self.datasets.values()),
                'total_rows': sum(len(df) for df in self.datasets.values())
            }
        
        # Validation summary
        for name, validation in self.validation_results.items():
            summary['validation_summary'][name] = {
                'status': validation.get('status', 'unknown'),
                'error_count': len(validation.get('errors', [])),
                'warning_count': len(validation.get('warnings', []))
            }
        
        return summary

    def get_quality_report(self) -> Dict[str, Dict[str, float]]:
        """Get detailed quality report for all datasets."""
        return self.quality_report

    def get_validation_results(self) -> Dict[str, Dict[str, Any]]:
        """Get validation results for all datasets."""
        return self.validation_results

    # ==================== UTILITY METHODS ====================

    def get_dataset(self, name: str) -> pd.DataFrame:
        """Get a specific dataset by name."""
        return self.datasets.get(name, pd.DataFrame())

    def list_datasets(self) -> List[str]:
        """List all available dataset names."""
        return list(self.datasets.keys())

    def get_dataset_info(self, name: str) -> Dict[str, Any]:
        """Get detailed information about a specific dataset."""
        if name not in self.datasets:
            return {}
        
        df = self.datasets[name]
        return {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'memory_mb': df.memory_usage(deep=True).sum() / 1024**2,
            'quality_metrics': self.quality_report.get(name, {}),
            'validation_result': self.validation_results.get(name, {})
        }

    def reload_dataset(self, name: str) -> bool:
        """Reload a specific dataset from file."""
        if name not in DATA_FILES:
            print(f"[ERROR] Unknown dataset: {name}")
            return False
        
        config = DATA_FILES[name]
        filename = config['filename']
        file_path = os.path.join(self.data_path, filename)
        
        try:
            df = self._load_single_file(file_path, name)
            if not df.empty:
                self.datasets[name] = df
                
                # Re-validate and assess quality
                validation_result = self._validate_dataset(df, name, config)
                self.validation_results[name] = validation_result
                
                quality_metrics = self._assess_data_quality(df, name)
                self.quality_report[name] = quality_metrics
                
                print(f"[OK] Reloaded {name} successfully")
                return True
            else:
                print(f"[ERROR] Failed to reload {name} - Empty DataFrame")
                return False
                
        except Exception as e:
            print(f"[ERROR] Error reloading {name}: {str(e)}")
            return False


# Global instance for use throughout the application
data_processor = DataProcessor()
