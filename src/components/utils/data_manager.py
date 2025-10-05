"""
🗄️ Data Manager Utility Component for Car Market Analysis Executive Dashboard

Advanced data management utility providing caching, session state management,
data loading optimization, and memory management for the dashboard.
"""

import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Optional, Any, Union
import time
import json
import hashlib
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import components
try:
    from ...business_logic import analyzer
    from ...data_layer import data_processor
except ImportError:
    # Fallback imports
    analyzer = None
    data_processor = None


class DataManager:
    """
    🗂️ Executive-Grade Data Manager
    
    Provides advanced data management capabilities including caching,
    session state management, data loading optimization, and memory management.
    """

    def __init__(self):
        """Initialize the DataManager with configuration."""
        self.analyzer = analyzer
        self.data_processor = data_processor
        self.cache = {}
        self.cache_metadata = {}
        self.loading_states = {}
        
        # Cache configuration
        self.cache_config = {
            'max_size_mb': 100,  # Maximum cache size in MB
            'ttl_hours': 24,     # Time to live in hours
            'auto_cleanup': True  # Auto cleanup expired entries
        }

    # ==================== DATA LOADING METHODS ====================

    def load_data_with_cache(self, data_key: str, loader_function: callable, 
                           force_reload: bool = False, ttl_hours: int = None) -> Any:
        """Load data with intelligent caching."""
        if ttl_hours is None:
            ttl_hours = self.cache_config['ttl_hours']
        
        # Check if data is already in cache and not expired
        if not force_reload and self._is_cache_valid(data_key, ttl_hours):
            return self.cache[data_key]['data']
        
        # Load data with loading state
        self._set_loading_state(data_key, True)
        
        try:
            # Load data using provided function
            data = loader_function()
            
            # Store in cache with metadata
            self._cache_data(data_key, data)
            
            return data
            
        except Exception as e:
            st.error(f"Error loading data for {data_key}: {str(e)}")
            return None
            
        finally:
            self._set_loading_state(data_key, False)

    def load_sales_data(self, force_reload: bool = False) -> pd.DataFrame:
        """Load sales data with caching."""
        def loader():
            if self.analyzer:
                return self.analyzer.get_sales_summary()
            return pd.DataFrame()
        
        return self.load_data_with_cache('sales_data', loader, force_reload)

    def load_price_data(self, force_reload: bool = False) -> pd.DataFrame:
        """Load price data with caching."""
        def loader():
            if self.analyzer:
                return self.analyzer.get_price_range_by_model()
            return pd.DataFrame()
        
        return self.load_data_with_cache('price_data', loader, force_reload)

    def load_market_share_data(self, force_reload: bool = False) -> pd.DataFrame:
        """Load market share data with caching."""
        def loader():
            if self.analyzer:
                return self.analyzer.calculate_market_share()
            return pd.DataFrame()
        
        return self.load_data_with_cache('market_share_data', loader, force_reload)

    def load_basic_data(self, force_reload: bool = False) -> pd.DataFrame:
        """Load basic data with caching."""
        def loader():
            if self.analyzer:
                return self.analyzer.basic
            return pd.DataFrame()
        
        return self.load_data_with_cache('basic_data', loader, force_reload)

    def load_all_data(self, force_reload: bool = False) -> Dict[str, pd.DataFrame]:
        """Load all available data with caching."""
        data_keys = ['sales_data', 'price_data', 'market_share_data', 'basic_data']
        all_data = {}
        
        for key in data_keys:
            loader_method = getattr(self, f'load_{key}')
            all_data[key] = loader_method(force_reload)
        
        return all_data

    # ==================== CACHE MANAGEMENT ====================

    def _cache_data(self, key: str, data: Any) -> None:
        """Cache data with metadata."""
        cache_entry = {
            'data': data,
            'timestamp': datetime.now(),
            'size_mb': self._calculate_data_size(data),
            'hash': self._calculate_data_hash(data)
        }
        
        self.cache[key] = cache_entry
        self.cache_metadata[key] = cache_entry
        
        # Auto cleanup if enabled
        if self.cache_config['auto_cleanup']:
            self._cleanup_cache()

    def _is_cache_valid(self, key: str, ttl_hours: int) -> bool:
        """Check if cached data is still valid."""
        if key not in self.cache:
            return False
        
        cache_entry = self.cache[key]
        age = datetime.now() - cache_entry['timestamp']
        
        return age < timedelta(hours=ttl_hours)

    def _calculate_data_size(self, data: Any) -> float:
        """Calculate data size in MB."""
        try:
            if isinstance(data, pd.DataFrame):
                return data.memory_usage(deep=True).sum() / (1024 * 1024)
            elif isinstance(data, dict):
                return sum(self._calculate_data_size(v) for v in data.values())
            else:
                return len(str(data)) / (1024 * 1024)
        except:
            return 0.0

    def _calculate_data_hash(self, data: Any) -> str:
        """Calculate hash for data integrity checking."""
        try:
            if isinstance(data, pd.DataFrame):
                # Use pandas hash for DataFrames
                return str(hash(data.to_string()))
            else:
                # Use string hash for other data types
                return hashlib.md5(str(data).encode()).hexdigest()
        except:
            return str(time.time())

    def _cleanup_cache(self) -> None:
        """Clean up expired and oversized cache entries."""
        current_time = datetime.now()
        total_size = sum(entry['size_mb'] for entry in self.cache.values())
        
        # Remove expired entries
        expired_keys = []
        for key, entry in self.cache.items():
            age = current_time - entry['timestamp']
            if age > timedelta(hours=self.cache_config['ttl_hours']):
                expired_keys.append(key)
        
        for key in expired_keys:
            self._remove_from_cache(key)
        
        # Remove oldest entries if cache is too large
        if total_size > self.cache_config['max_size_mb']:
            sorted_entries = sorted(
                self.cache.items(),
                key=lambda x: x[1]['timestamp']
            )
            
            while total_size > self.cache_config['max_size_mb'] and sorted_entries:
                key, entry = sorted_entries.pop(0)
                self._remove_from_cache(key)
                total_size -= entry['size_mb']

    def _remove_from_cache(self, key: str) -> None:
        """Remove entry from cache."""
        if key in self.cache:
            del self.cache[key]
        if key in self.cache_metadata:
            del self.cache_metadata[key]

    def clear_cache(self, key: str = None) -> None:
        """Clear cache entries."""
        if key:
            self._remove_from_cache(key)
        else:
            self.cache.clear()
            self.cache_metadata.clear()

    def get_cache_info(self) -> Dict[str, Any]:
        """Get cache information and statistics."""
        total_entries = len(self.cache)
        total_size = sum(entry['size_mb'] for entry in self.cache.values())
        
        cache_ages = []
        for entry in self.cache.values():
            age = datetime.now() - entry['timestamp']
            cache_ages.append(age.total_seconds() / 3600)  # Age in hours
        
        return {
            'total_entries': total_entries,
            'total_size_mb': round(total_size, 2),
            'max_size_mb': self.cache_config['max_size_mb'],
            'utilization_percent': round((total_size / self.cache_config['max_size_mb']) * 100, 1),
            'average_age_hours': round(np.mean(cache_ages), 2) if cache_ages else 0,
            'oldest_entry_hours': round(max(cache_ages), 2) if cache_ages else 0,
            'newest_entry_hours': round(min(cache_ages), 2) if cache_ages else 0
        }

    # ==================== LOADING STATE MANAGEMENT ====================

    def _set_loading_state(self, key: str, loading: bool) -> None:
        """Set loading state for a data key."""
        self.loading_states[key] = loading

    def is_loading(self, key: str) -> bool:
        """Check if data is currently loading."""
        return self.loading_states.get(key, False)

    def get_loading_states(self) -> Dict[str, bool]:
        """Get all loading states."""
        return self.loading_states.copy()

    def show_loading_indicator(self, key: str, message: str = "Loading...") -> None:
        """Show loading indicator for a data key."""
        if self.is_loading(key):
            st.spinner(message)

    # ==================== SESSION STATE MANAGEMENT ====================

    def init_session_state(self) -> None:
        """Initialize Streamlit session state."""
        if 'data_manager_cache' not in st.session_state:
            st.session_state['data_manager_cache'] = {}
        if 'data_manager_metadata' not in st.session_state:
            st.session_state['data_manager_metadata'] = {}
        if 'data_manager_loading' not in st.session_state:
            st.session_state['data_manager_loading'] = {}

    def save_to_session_state(self, key: str, data: Any) -> None:
        """Save data to Streamlit session state."""
        self.init_session_state()
        
        # Convert pandas DataFrames to JSON for session state
        if isinstance(data, pd.DataFrame):
            st.session_state['data_manager_cache'][key] = data.to_json(orient='records')
        else:
            st.session_state['data_manager_cache'][key] = data
        
        # Save metadata
        st.session_state['data_manager_metadata'][key] = {
            'timestamp': datetime.now().isoformat(),
            'type': type(data).__name__,
            'size_mb': self._calculate_data_size(data)
        }

    def load_from_session_state(self, key: str) -> Any:
        """Load data from Streamlit session state."""
        self.init_session_state()
        
        if key in st.session_state.get('data_manager_cache', {}):
            data = st.session_state['data_manager_cache'][key]
            metadata = st.session_state.get('data_manager_metadata', {}).get(key, {})
            
            # Convert JSON back to DataFrame if needed
            if metadata.get('type') == 'DataFrame':
                try:
                    return pd.read_json(data, orient='records')
                except:
                    return pd.DataFrame()
            
            return data
        
        return None

    def clear_session_state(self, key: str = None) -> None:
        """Clear data from Streamlit session state."""
        self.init_session_state()
        
        if key:
            if key in st.session_state.get('data_manager_cache', {}):
                del st.session_state['data_manager_cache'][key]
            if key in st.session_state.get('data_manager_metadata', {}):
                del st.session_state['data_manager_metadata'][key]
        else:
            st.session_state['data_manager_cache'] = {}
            st.session_state['data_manager_metadata'] = {}

    # ==================== DATA FILTERING METHODS ====================

    def filter_data_by_automakers(self, data: pd.DataFrame, automakers: List[str]) -> pd.DataFrame:
        """Filter data by selected automakers."""
        if data.empty or not automakers:
            return data
        
        if 'Automaker' in data.columns:
            return data[data['Automaker'].isin(automakers)]
        
        return data

    def filter_data_by_price_range(self, data: pd.DataFrame, min_price: float, max_price: float) -> pd.DataFrame:
        """Filter data by price range."""
        if data.empty:
            return data
        
        if 'price_mean' in data.columns:
            return data[(data['price_mean'] >= min_price) & (data['price_mean'] <= max_price)]
        
        return data

    def filter_data_by_sales_range(self, data: pd.DataFrame, min_sales: float, max_sales: float) -> pd.DataFrame:
        """Filter data by sales range."""
        if data.empty:
            return data
        
        if 'total_sales' in data.columns:
            return data[(data['total_sales'] >= min_sales) & (data['total_sales'] <= max_sales)]
        
        return data

    def filter_data_by_year_range(self, data: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame:
        """Filter data by year range."""
        if data.empty:
            return data
        
        # Filter by year columns
        year_columns = [col for col in data.columns if col.isdigit() and start_year <= int(col) <= end_year]
        
        if year_columns:
            # Keep only the specified year columns plus metadata columns
            metadata_columns = ['Automaker', 'Genmodel', 'Genmodel_ID']
            columns_to_keep = [col for col in metadata_columns if col in data.columns] + year_columns
            return data[columns_to_keep]
        
        return data

    def apply_filters(self, data: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Apply multiple filters to data."""
        filtered_data = data.copy()
        
        # Apply automaker filter
        if 'automakers' in filters and filters['automakers']:
            filtered_data = self.filter_data_by_automakers(filtered_data, filters['automakers'])
        
        # Apply price range filter
        if 'price_range' in filters:
            min_price, max_price = filters['price_range']
            filtered_data = self.filter_data_by_price_range(filtered_data, min_price, max_price)
        
        # Apply sales range filter
        if 'sales_range' in filters:
            min_sales, max_sales = filters['sales_range']
            filtered_data = self.filter_data_by_sales_range(filtered_data, min_sales, max_sales)
        
        # Apply year range filter
        if 'year_range' in filters:
            start_year, end_year = filters['year_range']
            filtered_data = self.filter_data_by_year_range(filtered_data, start_year, end_year)
        
        return filtered_data

    # ==================== DATA AGGREGATION METHODS ====================

    def aggregate_data_by_automaker(self, data: pd.DataFrame, agg_functions: Dict[str, str] = None) -> pd.DataFrame:
        """Aggregate data by automaker."""
        if data.empty or 'Automaker' not in data.columns:
            return data
        
        if agg_functions is None:
            agg_functions = {
                'total_sales': 'sum',
                'price_mean': 'mean',
                'avg_sales': 'mean'
            }
        
        # Only aggregate numeric columns
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        agg_columns = {col: agg_functions.get(col, 'mean') for col in numeric_columns if col in agg_functions}
        
        if agg_columns:
            return data.groupby('Automaker').agg(agg_columns).reset_index()
        
        return data

    def aggregate_data_by_year(self, data: pd.DataFrame) -> pd.DataFrame:
        """Aggregate data by year."""
        if data.empty:
            return data
        
        # Find year columns
        year_columns = [col for col in data.columns if col.isdigit()]
        
        if not year_columns:
            return data
        
        # Sum sales across all models for each year
        yearly_totals = data[year_columns].sum()
        
        # Create DataFrame with year and total sales
        result = pd.DataFrame({
            'Year': [int(year) for year in year_columns],
            'Total_Sales': yearly_totals.values
        })
        
        return result.sort_values('Year')

    def top_n_models(self, data: pd.DataFrame, n: int = 10, column: str = 'total_sales') -> pd.DataFrame:
        """Get top N models by specified column."""
        if data.empty or column not in data.columns:
            return data
        
        return data.nlargest(n, column)

    def top_n_automakers(self, data: pd.DataFrame, n: int = 10, column: str = 'total_sales') -> pd.DataFrame:
        """Get top N automakers by specified column."""
        if data.empty or 'Automaker' not in data.columns or column not in data.columns:
            return data
        
        automaker_data = data.groupby('Automaker')[column].sum().nlargest(n).reset_index()
        return automaker_data

    # ==================== DATA VALIDATION METHODS ====================

    def validate_data_quality(self, data: pd.DataFrame, data_type: str = 'general') -> Dict[str, Any]:
        """Validate data quality and return quality metrics."""
        if data.empty:
            return {'status': 'empty', 'message': 'Data is empty'}
        
        quality_metrics = {
            'total_rows': len(data),
            'total_columns': len(data.columns),
            'missing_data_percent': (data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100,
            'duplicate_rows': data.duplicated().sum(),
            'memory_usage_mb': data.memory_usage(deep=True).sum() / (1024 * 1024)
        }
        
        # Type-specific validation
        if data_type == 'sales':
            year_columns = [col for col in data.columns if col.isdigit()]
            quality_metrics['year_columns_count'] = len(year_columns)
            quality_metrics['sales_data_coverage'] = (data['total_sales'] > 0).sum() / len(data) * 100 if 'total_sales' in data.columns else 0
        
        elif data_type == 'price':
            if 'price_mean' in data.columns:
                quality_metrics['price_range'] = {
                    'min': data['price_mean'].min(),
                    'max': data['price_mean'].max(),
                    'mean': data['price_mean'].mean()
                }
        
        # Overall quality score
        quality_score = 100
        if quality_metrics['missing_data_percent'] > 10:
            quality_score -= 20
        if quality_metrics['duplicate_rows'] > 0:
            quality_score -= 10
        if quality_metrics['memory_usage_mb'] > 50:
            quality_score -= 5
        
        quality_metrics['quality_score'] = max(0, quality_score)
        quality_metrics['status'] = 'good' if quality_score >= 80 else 'warning' if quality_score >= 60 else 'poor'
        
        return quality_metrics

    # ==================== UTILITY METHODS ====================

    def get_data_summary(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Get comprehensive data summary."""
        if data.empty:
            return {'status': 'empty', 'message': 'Data is empty'}
        
        summary = {
            'shape': data.shape,
            'columns': list(data.columns),
            'dtypes': data.dtypes.to_dict(),
            'memory_usage_mb': data.memory_usage(deep=True).sum() / (1024 * 1024),
            'missing_values': data.isnull().sum().to_dict(),
            'numeric_columns': list(data.select_dtypes(include=[np.number]).columns),
            'categorical_columns': list(data.select_dtypes(include=['object', 'category']).columns),
            'datetime_columns': list(data.select_dtypes(include=['datetime']).columns)
        }
        
        # Add basic statistics for numeric columns
        if summary['numeric_columns']:
            summary['numeric_stats'] = data[summary['numeric_columns']].describe().to_dict()
        
        return summary

    def export_data(self, data: pd.DataFrame, format: str = 'csv', filename: str = None) -> str:
        """Export data to specified format."""
        if data.empty:
            return "No data to export"
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"exported_data_{timestamp}"
        
        if format.lower() == 'csv':
            return data.to_csv(index=False)
        elif format.lower() == 'json':
            return data.to_json(orient='records', indent=2)
        elif format.lower() == 'excel':
            # This would require openpyxl
            return "Excel export requires additional dependencies"
        else:
            return f"Unsupported format: {format}"

    def get_manager_status(self) -> Dict[str, Any]:
        """Get data manager status and statistics."""
        return {
            'cache_info': self.get_cache_info(),
            'loading_states': self.get_loading_states(),
            'analyzer_available': self.analyzer is not None,
            'data_processor_available': self.data_processor is not None,
            'cache_config': self.cache_config,
            'session_state_initialized': 'data_manager_cache' in st.session_state if 'st' in globals() else False
        }


# Global instance for use throughout the application
data_manager = DataManager()

