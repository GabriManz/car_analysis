"""
🧠 Enhanced Business Logic Module for Car Market Analysis Executive Dashboard

Advanced analytics and business intelligence algorithms for automotive market analysis.
Contains the CarDataAnalyzer class with executive-grade analytical capabilities.
"""

import pandas as pd
import numpy as np
import os
from typing import Dict, List, Optional, Any, Tuple
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Import data cleaning functions (absolute imports)
from src.data_cleaner import (
    clean_automaker_data,
    validate_automaker_consistency,
    print_cleaning_report,
)

# Import configuration (absolute imports)
from src.components.config.app_config import (
    CORRELATION_CONFIG,
    OUTLIER_CONFIG,
    CLUSTERING_CONFIG,
    KPI_THRESHOLDS,
)
from src.components.config.data_config import DATA_QUALITY_THRESHOLDS


class CarDataAnalyzer:
    """
    🚗 Executive-Grade Car Market Analysis Engine
    
    Advanced analytics class for comprehensive automotive market intelligence.
    Provides SQL-like queries, statistical analysis, and business intelligence.
    """

    def __init__(self, data_path: str = None):
        """
        Initialize the CarDataAnalyzer with enhanced capabilities.
        
        Args:
            data_path (str): Path to the directory containing CSV files
        """
        if data_path is None:
            # Use the correct path for Streamlit Cloud (from repository root)
            self.data_path = 'data/'
            print(f"Using data path: {self.data_path}")
        else:
            self.data_path = data_path
        
        self.datasets: Dict[str, pd.DataFrame] = {}
        self._load_datasets()
        self._standardize_columns()
        self._validate_data_quality()

    def _load_datasets(self) -> None:
        """Load all CSV datasets with enhanced error handling and memory optimization."""
        files_to_load = {
            'basic': 'Basic_table.csv',
            'price': 'Price_table.csv',
            'sales': 'Sales_table.csv'
        }

        for name, filename in files_to_load.items():
            file_path = os.path.join(self.data_path, filename)
            
            # Path being loaded (debug line removed after verification)

            try:
                # Load with optimized dtypes and proper encoding
                try:
                    df = pd.read_csv(file_path, encoding='utf-8', nrows=100)
                except UnicodeDecodeError:
                    try:
                        df = pd.read_csv(file_path, encoding='latin-1', nrows=100)
                    except UnicodeDecodeError:
                        df = pd.read_csv(file_path, encoding='cp1252', nrows=100)
                
                self.datasets[name] = self._optimize_dtypes(df)
                
                # Apply data cleaning for Basic_table specifically
                if name == 'basic' and not self.datasets[name].empty:
                    print(f"\nAplicando limpieza de datos a {filename}...")
                    original_shape = self.datasets[name].shape
                    self.datasets[name] = clean_automaker_data(self.datasets[name])
                    final_shape = self.datasets[name].shape
                    
                    # Validate cleaning results
                    validation_report = validate_automaker_consistency(self.datasets[name])
                    if validation_report['status'] == 'success':
                        print(f"OK - Limpieza completada: {original_shape} -> {final_shape}")
                        if validation_report['quality_score'] < 80:
                            print(f"ADVERTENCIA - Score de calidad: {validation_report['quality_score']}/100")
                    else:
                        print(f"ADVERTENCIA - Error en validacion: {validation_report.get('message', 'Unknown error')}")
                
                print(f"[OK] {name.upper()}: {filename} - Shape: {self.datasets[name].shape}")
            except FileNotFoundError:
                print(f"[ERROR] {filename} not found at {file_path}")
                self.datasets[name] = pd.DataFrame()
            except Exception as e:
                print(f"[ERROR] Failed to load {filename}: {e}")
                self.datasets[name] = pd.DataFrame()

        # Assign datasets to instance variables for easier access
        self.basic = self.datasets.get('basic', pd.DataFrame())
        self.price = self.datasets.get('price', pd.DataFrame())
        self.sales = self.datasets.get('sales', pd.DataFrame())

    def _optimize_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optimize DataFrame memory usage by converting dtypes."""
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try to convert to category if it has few unique values
                if df[col].nunique() / len(df) < 0.5:
                    df[col] = df[col].astype('category')
            elif df[col].dtype == 'int64':
                # Downcast integers
                if df[col].min() >= 0:
                    if df[col].max() < 255:
                        df[col] = df[col].astype('uint8')
                    elif df[col].max() < 65535:
                        df[col] = df[col].astype('uint16')
                    elif df[col].max() < 4294967295:
                        df[col] = df[col].astype('uint32')
                else:
                    if df[col].min() > -128 and df[col].max() < 127:
                        df[col] = df[col].astype('int8')
                    elif df[col].min() > -32768 and df[col].max() < 32767:
                        df[col] = df[col].astype('int16')
                    elif df[col].min() > -2147483648 and df[col].max() < 2147483647:
                        df[col] = df[col].astype('int32')
        return df

    def _standardize_columns(self) -> None:
        """Standardize column names across all datasets."""
        for name, df in self.datasets.items():
            if not df.empty and 'Maker' in df.columns:
                df.rename(columns={'Maker': 'Automaker'}, inplace=True)
                print(f"[OK] {name.upper()}: Renamed 'Maker' to 'Automaker'")

    def _validate_data_quality(self) -> None:
        """Validate data quality and log issues."""
        quality_report = {}
        for name, df in self.datasets.items():
            if df.empty:
                continue
                
            missing_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns))
            duplicate_ratio = df.duplicated().sum() / len(df)
            
            quality_report[name] = {
                'missing_data_ratio': missing_ratio,
                'duplicate_ratio': duplicate_ratio,
                'memory_mb': df.memory_usage(deep=True).sum() / 1024**2
            }
            
            # Log warnings if thresholds exceeded
            if missing_ratio > DATA_QUALITY_THRESHOLDS.get('missing_data_warning', 0.05):
                print(f"[WARNING] {name.upper()}: High missing data ratio: {missing_ratio:.2%}")
            
            if duplicate_ratio > DATA_QUALITY_THRESHOLDS.get('duplicate_threshold', 0.02):
                print(f"[WARNING] {name.upper()}: High duplicate ratio: {duplicate_ratio:.2%}")
        
        self.quality_report = quality_report

    # ==================== BASIC QUERY METHODS ====================

    def get_basic_info(self) -> Dict[str, Any]:
        """Get comprehensive information about all datasets."""
        info = {}
        for name, df in self.datasets.items():
            info[name] = {
                'shape': df.shape,
                'memory_mb': df.memory_usage(deep=True).sum() / 1024**2,
                'columns': list(df.columns),
                'unique_genmodel_ids': df['Genmodel_ID'].nunique() if 'Genmodel_ID' in df.columns else 0,
                'quality_score': self._calculate_quality_score(df)
            }
        return info

    def _calculate_quality_score(self, df: pd.DataFrame) -> float:
        """Calculate a data quality score (0-100)."""
        if df.empty:
            return 0.0
        
        # Factors: completeness, uniqueness, consistency
        completeness = 1 - (df.isnull().sum().sum() / (len(df) * len(df.columns)))
        uniqueness = 1 - (df.duplicated().sum() / len(df))
        consistency = 1 - (df.select_dtypes(include=['object']).apply(lambda x: x.str.contains('N/A|NULL|null').sum().sum()) / (len(df) * len(df.select_dtypes(include=['object']).columns)))
        
        return (completeness * 0.5 + uniqueness * 0.3 + consistency * 0.2) * 100

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

    # ==================== ADVANCED ANALYTICS METHODS ====================

    def calculate_market_share(self) -> pd.DataFrame:
        """Calculate market share by automaker based on total sales."""
        sales_summary = self.get_sales_summary()
        if sales_summary.empty:
            return pd.DataFrame()
        
        # Calculate total market sales
        total_market_sales = sales_summary['total_sales'].sum()
        
        # Calculate market share by automaker
        market_share = sales_summary.groupby('Automaker')['total_sales'].sum().reset_index()
        market_share['market_share_percent'] = (market_share['total_sales'] / total_market_sales * 100).round(2)
        market_share = market_share.sort_values('market_share_percent', ascending=False)
        
        return market_share

    def calculate_price_elasticity(self) -> pd.DataFrame:
        """Calculate price elasticity analysis by model."""
        price_data = self.get_price_range_by_model()
        sales_data = self.get_sales_summary()
        
        if price_data.empty or sales_data.empty:
            return pd.DataFrame()
        
        # Merge price and sales data using composite key
        merged = price_data.merge(sales_data, on=['Automaker', 'Genmodel', 'Genmodel_ID'], how='inner')
        
        # Calculate price elasticity (simplified version)
        merged['price_elasticity'] = np.where(
            merged['price_mean'] > 0,
            -(merged['total_sales'].pct_change() / merged['price_mean'].pct_change()),
            np.nan
        )
        
        # Add elasticity categories
        merged['elasticity_category'] = pd.cut(
            merged['price_elasticity'],
            bins=[-np.inf, -1, -0.5, 0, 0.5, np.inf],
            labels=['Highly Elastic', 'Elastic', 'Inelastic', 'Slightly Inelastic', 'Highly Inelastic']
        )
        
        return merged[['Automaker', 'Genmodel', 'price_mean', 'total_sales', 'price_elasticity', 'elasticity_category']].dropna()

    def detect_outliers(self, method: str = 'iqr') -> Dict[str, pd.DataFrame]:
        """Detect outliers in key metrics using multiple methods."""
        outliers = {}
        
        # Get key datasets
        price_data = self.get_price_range_by_model()
        sales_data = self.get_sales_summary()
        
        if price_data.empty or sales_data.empty:
            return outliers
        
        # Merge data using composite key
        merged = price_data.merge(sales_data, on=['Automaker', 'Genmodel', 'Genmodel_ID'], how='inner')
        
        numeric_columns = OUTLIER_CONFIG.get('outlier_columns', ['price_mean', 'total_sales', 'avg_sales'])
        
        for col in numeric_columns:
            if col in merged.columns:
                if method == 'iqr':
                    Q1 = merged[col].quantile(0.25)
                    Q3 = merged[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outliers[col] = merged[(merged[col] < lower_bound) | (merged[col] > upper_bound)]
                
                elif method == 'zscore':
                    z_scores = np.abs(stats.zscore(merged[col].dropna()))
                    threshold = OUTLIER_CONFIG.get('zscore_threshold', 3)
                    outlier_indices = merged[col].dropna().index[z_scores > threshold]
                    outliers[col] = merged.loc[outlier_indices]
        
        return outliers

    def perform_clustering_analysis(self) -> pd.DataFrame:
        """Perform K-means clustering on vehicle models."""
        # Get comprehensive data
        price_data = self.get_price_range_by_model()
        sales_data = self.get_sales_summary()
        
        if price_data.empty or sales_data.empty:
            return pd.DataFrame()
        
        # Merge and prepare features using composite key
        merged = price_data.merge(sales_data, on=['Automaker', 'Genmodel', 'Genmodel_ID'], how='inner')
        
        # Select features for clustering
        features = CLUSTERING_CONFIG.get('clustering_features', ['price_mean', 'total_sales', 'avg_sales'])
        available_features = [f for f in features if f in merged.columns]
        
        if len(available_features) < 2:
            return pd.DataFrame()
        
        # Prepare data for clustering
        X = merged[available_features].fillna(0)
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Perform K-means clustering
        n_clusters = CLUSTERING_CONFIG.get('n_clusters', 5)
        random_state = CLUSTERING_CONFIG.get('random_state', 42)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
        merged['cluster'] = kmeans.fit_predict(X_scaled)
        
        # Add cluster interpretation
        cluster_summary = merged.groupby('cluster')[available_features].mean()
        merged['cluster_type'] = merged['cluster'].map({
            0: 'Budget Segment',
            1: 'Mid-Range Segment', 
            2: 'Premium Segment',
            3: 'Luxury Segment',
            4: 'Niche Segment'
        })
        
        return merged[['Automaker', 'Genmodel', 'cluster', 'cluster_type'] + available_features]

    def calculate_correlation_matrix(self) -> pd.DataFrame:
        """Calculate correlation matrix for numeric variables."""
        # Get comprehensive data
        price_data = self.get_price_range_by_model()
        sales_data = self.get_sales_summary()
        
        if price_data.empty or sales_data.empty:
            return pd.DataFrame()
        
        # Merge data using composite key
        merged = price_data.merge(sales_data, on=['Automaker', 'Genmodel', 'Genmodel_ID'], how='inner')
        
        # Select numeric columns
        numeric_columns = CORRELATION_CONFIG.get('numeric_columns', [])
        available_columns = [col for col in numeric_columns if col in merged.columns]
        
        if len(available_columns) < 2:
            return pd.DataFrame()
        
        # Calculate correlation matrix
        correlation_matrix = merged[available_columns].corr()
        
        return correlation_matrix

    def generate_market_insights(self) -> Dict[str, Any]:
        """Generate comprehensive market insights and recommendations."""
        insights = {}
        
        # Market share analysis
        market_share = self.calculate_market_share()
        if not market_share.empty:
            insights['market_leader'] = market_share.iloc[0]['Automaker']
            insights['market_concentration'] = market_share.head(3)['market_share_percent'].sum()
            insights['total_brands'] = len(market_share)
        
        # Price analysis
        price_data = self.get_price_range_by_model()
        if not price_data.empty:
            insights['avg_market_price'] = price_data['price_mean'].mean()
            insights['price_range'] = {
                'min': price_data['price_min'].min(),
                'max': price_data['price_max'].max()
            }
        
        # Sales performance
        sales_data = self.get_sales_summary()
        if not sales_data.empty:
            insights['total_market_sales'] = sales_data['total_sales'].sum()
            insights['avg_model_sales'] = sales_data['total_sales'].mean()
        
        # Outlier analysis
        outliers = self.detect_outliers()
        insights['outlier_count'] = sum(len(df) for df in outliers.values())
        
        # Generate recommendations
        insights['recommendations'] = self._generate_recommendations(insights)
        
        return insights

    def _generate_recommendations(self, insights: Dict[str, Any]) -> List[str]:
        """Generate business recommendations based on insights."""
        recommendations = []
        
        # Market concentration recommendations
        if insights.get('market_concentration', 0) > 60:
            recommendations.append("High market concentration detected. Consider diversification strategies.")
        
        # Price analysis recommendations
        if insights.get('avg_market_price', 0) > 50000:
            recommendations.append("Premium market positioning. Focus on luxury segment strategies.")
        
        # Outlier recommendations
        if insights.get('outlier_count', 0) > 10:
            recommendations.append("Multiple outliers detected. Investigate exceptional performers for best practices.")
        
        return recommendations

    # ==================== EXISTING METHODS (ENHANCED) ====================

    def get_price_range_by_model(self) -> pd.DataFrame:
        """Get enhanced price range analysis for each model using composite key."""
        if self.price.empty or 'Entry_price' not in self.price.columns:
            return pd.DataFrame()

        # Group by composite key to ensure unique combinations
        price_stats = self.price.groupby(['Automaker', 'Genmodel', 'Genmodel_ID'])['Entry_price'].agg([
            'min', 'max', 'mean', 'median', 'std', 'count'
        ]).reset_index()
        
        price_stats.columns = [
            'Automaker', 'Genmodel', 'Genmodel_ID', 'price_min', 'price_max', 'price_mean', 
            'price_median', 'price_std', 'price_entries'
        ]
        
        # Calculate price volatility
        price_stats['price_volatility'] = price_stats['price_std'] / price_stats['price_mean']

        # Join with basic info using composite key
        if not self.basic.empty:
            result = self.basic.merge(price_stats, on=['Automaker', 'Genmodel', 'Genmodel_ID'], how='left')
            return result
        return price_stats

    def get_sales_summary(self) -> pd.DataFrame:
        """Get enhanced sales summary with trend analysis using composite key."""
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

        # Calculate enhanced summary statistics using composite key
        sales_stats = sales_long.groupby(['Automaker', 'Genmodel', 'Genmodel_ID'])['Sales_Volume'].agg([
            'sum', 'mean', 'max', 'min', 'std', 'count'
        ]).reset_index()
        
        sales_stats.columns = [
            'Automaker', 'Genmodel', 'Genmodel_ID', 'total_sales', 'avg_sales', 'max_sales', 
            'min_sales', 'sales_std', 'years_with_data'
        ]
        
        # Calculate sales trend using composite key
        sales_trend = sales_long.groupby(['Automaker', 'Genmodel', 'Genmodel_ID']).apply(
            lambda x: np.polyfit(x['Year'].astype(int), x['Sales_Volume'], 1)[0] if len(x) > 1 else 0
        ).reset_index(name='sales_trend')

        sales_stats = sales_stats.merge(sales_trend, on=['Automaker', 'Genmodel', 'Genmodel_ID'], how='left')

        # Join with basic info using composite key
        if not self.basic.empty:
            result = self.basic.merge(sales_stats, on=['Automaker', 'Genmodel', 'Genmodel_ID'], how='left')
            sales_fill_columns = [
                'total_sales', 'avg_sales', 'max_sales', 'min_sales',
                'sales_std', 'years_with_data', 'sales_trend'
            ]
            for column_name in sales_fill_columns:
                if column_name in result.columns:
                    result[column_name] = result[column_name].fillna(0)
            return result
        return sales_stats

    def query_models_by_automaker(self, automaker: str) -> pd.DataFrame:
        """Get all models for a specific automaker with enhanced info."""
        if not self.basic.empty and 'Automaker' in self.basic.columns:
            models = self.basic[self.basic['Automaker'] == automaker].copy()
            
            # Add additional metrics
            price_data = self.get_price_range_by_model()
            sales_data = self.get_sales_summary()
            
            if not price_data.empty:
                models = models.merge(price_data, on=['Automaker', 'Genmodel', 'Genmodel_ID'], how='left')
            if not sales_data.empty:
                models = models.merge(sales_data, on=['Automaker', 'Genmodel', 'Genmodel_ID'], how='left')
            
            return models
        return pd.DataFrame()

    def get_filtered_data(self, automakers: List[str] = None, models: List[str] = None) -> Dict[str, pd.DataFrame]:
        """Enhanced filtered data with additional metrics."""
        filtered_datasets = {}
        
        for name, df in self.datasets.items():
            filtered_df = df.copy()
            
            # Apply filters
            if automakers and 'Automaker' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['Automaker'].isin(automakers)]
            
            if models and 'Genmodel' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['Genmodel'].isin(models)]
            
            filtered_datasets[name] = filtered_df
        
        return filtered_datasets

    # ==================== EXECUTIVE SUMMARY METHODS ====================

    def get_executive_summary(self) -> Dict[str, Any]:
        """Generate executive summary with key metrics and insights."""
        summary = {
            'data_overview': self.get_basic_info(),
            'market_insights': self.generate_market_insights(),
            'quality_report': getattr(self, 'quality_report', {}),
            'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return summary

    def get_kpi_dashboard(self) -> Dict[str, float]:
        """Generate KPI dashboard with key performance indicators."""
        kpis = {}
        
        # Basic metrics
        kpis['total_models'] = len(self.basic) if not self.basic.empty else 0
        kpis['total_automakers'] = len(self.get_automaker_list())
        
        # Sales metrics
        sales_data = self.get_sales_summary()
        if not sales_data.empty:
            kpis['total_market_sales'] = sales_data['total_sales'].sum()
            kpis['avg_sales_per_model'] = sales_data['total_sales'].mean()
            kpis['top_performing_model_sales'] = sales_data['total_sales'].max()
        
        # Price metrics
        price_data = self.get_price_range_by_model()
        if not price_data.empty:
            kpis['avg_market_price'] = price_data['price_mean'].mean()
            kpis['price_range_span'] = price_data['price_max'].max() - price_data['price_min'].min()
        
        # Market concentration
        market_share = self.calculate_market_share()
        if not market_share.empty:
            kpis['market_leader_share'] = market_share.iloc[0]['market_share_percent']
            kpis['top_3_concentration'] = market_share.head(3)['market_share_percent'].sum()
        
        return kpis

    def get_data_quality_report(self) -> Dict[str, Any]:
        """Generate comprehensive data quality report including cleaning status."""
        report = {
            'cleaning_status': 'enabled',
            'datasets_quality': {},
            'overall_quality_score': 0,
            'recommendations': []
        }
        
        # Analyze each dataset
        for name, df in self.datasets.items():
            if df.empty:
                report['datasets_quality'][name] = {
                    'status': 'empty',
                    'quality_score': 0,
                    'issues': ['Dataset is empty']
                }
                continue
            
            # Calculate quality metrics
            completeness = 1 - (df.isnull().sum().sum() / (len(df) * len(df.columns)))
            uniqueness = 1 - (df.duplicated().sum() / len(df))
            
            # Special validation for basic dataset (after cleaning)
            if name == 'basic' and 'Automaker' in df.columns:
                validation = validate_automaker_consistency(df)
                quality_score = validation.get('quality_score', 0)
                issues = validation.get('issues', [])
            else:
                quality_score = (completeness * 0.6 + uniqueness * 0.4) * 100
                issues = []
                
                if completeness < 0.95:
                    issues.append(f"Low completeness: {completeness:.1%}")
                if uniqueness < 0.98:
                    issues.append(f"High duplication: {1-uniqueness:.1%}")
            
            report['datasets_quality'][name] = {
                'status': 'good' if quality_score >= 80 else 'warning' if quality_score >= 60 else 'poor',
                'quality_score': round(quality_score, 1),
                'completeness': round(completeness, 3),
                'uniqueness': round(uniqueness, 3),
                'shape': df.shape,
                'issues': issues
            }
        
        # Calculate overall quality score
        if report['datasets_quality']:
            scores = [data['quality_score'] for data in report['datasets_quality'].values() if data['quality_score'] > 0]
            report['overall_quality_score'] = round(sum(scores) / len(scores), 1) if scores else 0
        
        # Generate recommendations
        if report['overall_quality_score'] < 80:
            report['recommendations'].append("Consider reviewing data cleaning processes")
        
        basic_quality = report['datasets_quality'].get('basic', {})
        if basic_quality.get('quality_score', 0) < 90:
            report['recommendations'].append("Basic table data quality needs attention")
        
        return report

    def get_price_segments(self) -> pd.DataFrame:
        """
        Segmenta los modelos de coches en categorías de precio.
        """
        price_data = self.get_price_range_by_model()
        if price_data.empty or 'price_mean' not in price_data.columns:
            return pd.DataFrame()

        # Definir los umbrales de los cuantiles para los segmentos
        quantiles = price_data['price_mean'].quantile([0.25, 0.75, 0.95]).to_dict()
        q25 = quantiles[0.25]
        q75 = quantiles[0.75]
        q95 = quantiles[0.95]

        # Crear la columna de segmento
        conditions = [
            price_data['price_mean'] <= q25,
            (price_data['price_mean'] > q25) & (price_data['price_mean'] <= q75),
            (price_data['price_mean'] > q75) & (price_data['price_mean'] <= q95),
            price_data['price_mean'] > q95
        ]
        choices = ['Budget', 'Mid-Range', 'Premium', 'Luxury']
        
        price_data['Price_Segment'] = np.select(conditions, choices, default='Unknown')
        
        return price_data

    def get_sales_by_segment(self) -> pd.DataFrame:
        """
        Calcula el volumen total de ventas para cada segmento de precio.
        """
        # Obtener los datos de ventas y de segmentos
        sales_data = self.get_sales_summary()
        segmented_data = self.get_price_segments()

        if sales_data.empty or segmented_data.empty:
            return pd.DataFrame()

        # Unir los dos dataframes usando la clave compuesta
        # Nos aseguramos de que solo nos quedamos con las columnas necesarias para evitar duplicados
        merged_data = pd.merge(
            sales_data[['Automaker', 'Genmodel', 'Genmodel_ID', 'total_sales']],
            segmented_data[['Automaker', 'Genmodel', 'Genmodel_ID', 'Price_Segment']],
            on=['Automaker', 'Genmodel', 'Genmodel_ID']
        )
        
        # Agrupar por segmento y sumar las ventas
        sales_by_segment = merged_data.groupby('Price_Segment')['total_sales'].sum().reset_index()
        
        # Eliminar el segmento 'Unknown' (modelos sin precio) ya que no aportan al análisis
        sales_by_segment = sales_by_segment[sales_by_segment['Price_Segment'] != 'Unknown']

        return sales_by_segment
