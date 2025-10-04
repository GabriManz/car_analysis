"""
Business Logic Module for Car Market Analysis Dashboard
Contains the CarDataAnalyzer class for data processing and analysis.
"""

import pandas as pd
import numpy as np
import os
from typing import Dict, List, Optional, Any


class CarDataAnalyzer:
    """
    A class to perform SQL-like queries on car datasets without merging them.
    Keeps all data separate and provides flexible analysis methods.
    """

    def __init__(self, data_path: str = '../data/'):
        """
        Initialize the CarDataAnalyzer with datasets from the specified path.
        
        Args:
            data_path (str): Path to the directory containing CSV files
        """
        self.data_path = data_path
        self.datasets = {}
        self._load_datasets()
        self._standardize_columns()

    def _load_datasets(self) -> None:
        """Load all CSV datasets from the data directory."""
        files_to_load = {
            'basic': 'Basic_table.csv',
            'trim': 'Trim_table.csv',
            'price': 'Price_table.csv',
            'sales': 'Sales_table.csv'
        }

        for name, filename in files_to_load.items():
            file_path = os.path.join(self.data_path, filename)
            try:
                self.datasets[name] = pd.read_csv(file_path)
                print(f"[OK] {name.upper()}: {filename} - Shape: {self.datasets[name].shape}")
            except FileNotFoundError:
                print(f"[ERROR] {filename} not found at {file_path}")

        # Assign datasets to instance variables for easier access
        self.basic = self.datasets.get('basic', pd.DataFrame())
        self.trim = self.datasets.get('trim', pd.DataFrame())
        self.price = self.datasets.get('price', pd.DataFrame())
        self.sales = self.datasets.get('sales', pd.DataFrame())

    def _standardize_columns(self) -> None:
        """Standardize column names across all datasets."""
        # Standardize 'Maker' to 'Automaker' in all datasets that have it
        for name, df in self.datasets.items():
            if 'Maker' in df.columns:
                df.rename(columns={'Maker': 'Automaker'}, inplace=True)
                print(f"[OK] {name.upper()}: Renamed 'Maker' to 'Automaker'")

    def get_basic_info(self) -> Dict[str, Any]:
        """Get basic information about all datasets."""
        info = {}
        for name, df in self.datasets.items():
            info[name] = {
                'shape': df.shape,
                'memory_mb': df.memory_usage(deep=True).sum() / 1024**2,
                'columns': list(df.columns),
                'unique_genmodel_ids': df['Genmodel_ID'].nunique() if 'Genmodel_ID' in df.columns else 0
            }
        return info

    def get_automaker_list(self) -> List[str]:
        """Get a sorted list of all automakers."""
        if not self.basic.empty and 'Automaker' in self.basic.columns:
            return sorted(self.basic['Automaker'].unique().tolist())
        return []

    def get_model_count_by_automaker(self) -> pd.Series:
        """Get the count of models for each automaker."""
        if not self.basic.empty and 'Automaker' in self.basic.columns:
            return self.basic['Automaker'].value_counts()
        return pd.Series()

    def query_models_by_automaker(self, automaker: str) -> pd.DataFrame:
        """Get all models for a specific automaker."""
        if not self.basic.empty and 'Automaker' in self.basic.columns:
            return self.basic[self.basic['Automaker'] == automaker]
        return pd.DataFrame()

    def query_trim_details(self, genmodel_id: str) -> pd.DataFrame:
        """Get all trim details for a specific model."""
        if not self.trim.empty and 'Genmodel_ID' in self.trim.columns:
            return self.trim[self.trim['Genmodel_ID'] == genmodel_id]
        return pd.DataFrame()

    def query_price_history(self, genmodel_id: str) -> pd.DataFrame:
        """Get price history for a specific model."""
        if not self.price.empty and 'Genmodel_ID' in self.price.columns:
            return self.price[self.price['Genmodel_ID'] == genmodel_id]
        return pd.DataFrame()

    def query_sales_data(self, genmodel_id: str) -> pd.DataFrame:
        """Get sales data for a specific model."""
        if not self.sales.empty and 'Genmodel_ID' in self.sales.columns:
            return self.sales[self.sales['Genmodel_ID'] == genmodel_id]
        return pd.DataFrame()

    def get_price_range_by_model(self) -> pd.DataFrame:
        """Get price range (min, max, avg) for each model."""
        if self.price.empty or 'Entry_price' not in self.price.columns:
            return pd.DataFrame()

        price_stats = self.price.groupby('Genmodel_ID')['Entry_price'].agg(['min', 'max', 'mean', 'count']).reset_index()
        price_stats.columns = ['Genmodel_ID', 'price_min', 'price_max', 'price_mean', 'price_entries']

        # Join with basic info
        if not self.basic.empty:
            result = self.basic.merge(price_stats, on='Genmodel_ID', how='left')
            return result
        return price_stats

    def get_trim_summary_by_model(self) -> pd.DataFrame:
        """Get trim summary statistics for each model."""
        if self.trim.empty or 'Price' not in self.trim.columns:
            return pd.DataFrame()

        trim_stats = self.trim.groupby('Genmodel_ID').agg({
            'Price': ['min', 'max', 'mean', 'count'],
            'Year': ['min', 'max'],
            'Fuel_type': lambda x: x.mode().iloc[0] if not x.mode().empty else None,
            'Trim': 'count'
        }).reset_index()

        # Flatten column names
        trim_stats.columns = ['Genmodel_ID', 'trim_price_min', 'trim_price_max', 'trim_price_mean',
                             'trim_price_count', 'year_min', 'year_max', 'most_common_fuel', 'trim_count']

        # Join with basic info
        if not self.basic.empty:
            result = self.basic.merge(trim_stats, on='Genmodel_ID', how='left')
            return result
        return trim_stats

    def get_sales_summary(self) -> pd.DataFrame:
        """Get sales summary by model."""
        if self.sales.empty:
            return pd.DataFrame()

        # Reshape sales data from wide to long
        year_columns = [col for col in self.sales.columns if col.isdigit()]
        sales_long = pd.melt(
            self.sales,
            id_vars=['Automaker', 'Genmodel', 'Genmodel_ID'],
            value_vars=year_columns,
            var_name='Year',
            value_name='Sales_Volume'
        )

        # Calculate summary statistics
        sales_stats = sales_long.groupby('Genmodel_ID')['Sales_Volume'].agg(['sum', 'mean', 'max', 'count']).reset_index()
        sales_stats.columns = ['Genmodel_ID', 'total_sales', 'avg_sales', 'max_sales', 'years_with_data']

        # Join with basic info
        if not self.basic.empty:
            result = self.basic.merge(sales_stats, on='Genmodel_ID', how='left')
            return result
        return sales_stats

    def get_comprehensive_model_info(self, genmodel_id: str) -> Dict[str, pd.DataFrame]:
        """Get comprehensive information for a specific model."""
        return {
            'basic_info': self.query_models_by_automaker(genmodel_id),
            'trim_details': self.query_trim_details(genmodel_id),
            'price_history': self.query_price_history(genmodel_id),
            'sales_data': self.query_sales_data(genmodel_id)
        }

    def get_filtered_data(self, automakers: List[str] = None, models: List[str] = None) -> Dict[str, pd.DataFrame]:
        """
        Get filtered datasets based on automaker and model filters.
        
        Args:
            automakers: List of automaker names to filter by
            models: List of model names to filter by
            
        Returns:
            Dictionary containing filtered datasets
        """
        filtered_datasets = {}
        
        for name, df in self.datasets.items():
            filtered_df = df.copy()
            
            # Apply automaker filter
            if automakers and 'Automaker' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['Automaker'].isin(automakers)]
            
            # Apply model filter
            if models and 'Genmodel' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['Genmodel'].isin(models)]
            
            filtered_datasets[name] = filtered_df
        
        return filtered_datasets


# Global instance for use throughout the application
analyzer = CarDataAnalyzer()
