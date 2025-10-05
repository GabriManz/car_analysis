"""
📊 KPI Calculator Component for Car Market Analysis Executive Dashboard

Executive-grade KPI calculation and performance metrics for automotive market analysis.
Provides business intelligence metrics and trend analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import configuration
try:
    from ..config.app_config import KPI_THRESHOLDS, COLOR_PALETTE
except ImportError:
    # Fallback configuration
    KPI_THRESHOLDS = {
        'sales_performance': {'low': 1000, 'medium': 10000, 'high': 100000},
        'price_range': {'budget': 15000, 'mid_range': 35000, 'premium': 70000},
        'market_share': {'low': 1, 'medium': 5, 'high': 10}
    }
    COLOR_PALETTE = {
        'primary': '#1f77b4',
        'secondary': '#0a9396',
        'success': '#2ca02c',
        'danger': '#d62728',
        'warning': '#ff7f0e'
    }


class KPICalculator:
    """
    📈 Executive-Grade KPI Calculator
    
    Calculates comprehensive business intelligence metrics for automotive market analysis.
    Provides executive dashboards with trend analysis and performance indicators.
    """

    def __init__(self):
        """Initialize the KPICalculator with configuration."""
        self.kpi_thresholds = KPI_THRESHOLDS
        self.color_palette = COLOR_PALETTE
        self.calculated_kpis = {}

    def calculate_executive_kpis(self, data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Calculate comprehensive executive KPIs."""
        kpis = {}
        
        # Basic metrics
        kpis.update(self._calculate_basic_metrics(data))
        
        # Sales performance KPIs
        if 'sales_data' in data:
            kpis.update(self._calculate_sales_kpis(data['sales_data']))
        
        # Market performance KPIs
        if 'market_share' in data:
            kpis.update(self._calculate_market_kpis(data['market_share']))
        
        # Price performance KPIs
        if 'price_data' in data:
            kpis.update(self._calculate_price_kpis(data['price_data']))
        
        # Growth and trend KPIs
        kpis.update(self._calculate_growth_kpis(data))
        
        # Performance ratings
        kpis['performance_ratings'] = self._calculate_performance_ratings(kpis)
        
        # Store calculated KPIs
        self.calculated_kpis = kpis
        
        return kpis

    def _calculate_basic_metrics(self, data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Calculate basic market metrics."""
        metrics = {}
        
        # Total models and automakers
        if 'basic_data' in data:
            basic_data = data['basic_data']
            metrics['total_models'] = len(basic_data)
            metrics['total_automakers'] = basic_data['Automaker'].nunique() if 'Automaker' in basic_data.columns else 0
        
        # Data coverage metrics
        total_records = sum(len(df) for df in data.values() if isinstance(df, pd.DataFrame))
        metrics['total_records'] = total_records
        
        return metrics

    def _calculate_sales_kpis(self, sales_data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate sales performance KPIs."""
        kpis = {}
        
        if sales_data.empty:
            return kpis
        
        # Total market sales
        year_columns = [col for col in sales_data.columns if col.isdigit()]
        if year_columns:
            total_sales = sales_data[year_columns].sum().sum()
            kpis['total_market_sales'] = total_sales
            
            # Average sales per model
            kpis['avg_sales_per_model'] = sales_data[year_columns].sum(axis=1).mean()
            
            # Top performing model
            model_sales = sales_data[year_columns].sum(axis=1)
            top_model_sales = model_sales.max()
            kpis['top_model_sales'] = top_model_sales
            
            # Sales distribution metrics
            kpis['sales_std'] = model_sales.std()
            kpis['sales_cv'] = kpis['sales_std'] / kpis['avg_sales_per_model'] if kpis['avg_sales_per_model'] > 0 else 0
            
            # Sales trend (last 5 years vs previous 5 years)
            if len(year_columns) >= 10:
                recent_years = sorted(year_columns)[-5:]
                previous_years = sorted(year_columns)[-10:-5]
                
                recent_sales = sales_data[recent_years].sum().sum()
                previous_sales = sales_data[previous_years].sum().sum()
                
                if previous_sales > 0:
                    kpis['sales_growth_rate'] = (recent_sales - previous_sales) / previous_sales
                else:
                    kpis['sales_growth_rate'] = 0
        
        return kpis

    def _calculate_market_kpis(self, market_share_data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate market share and concentration KPIs."""
        kpis = {}
        
        if market_share_data.empty:
            return kpis
        
        # Market concentration metrics
        if 'market_share_percent' in market_share_data.columns:
            market_shares = market_share_data['market_share_percent']
            
            # Market leader share
            kpis['market_leader_share'] = market_shares.max()
            
            # Top 3 concentration
            kpis['top_3_concentration'] = market_shares.nlargest(3).sum()
            
            # Top 5 concentration
            kpis['top_5_concentration'] = market_shares.nlargest(5).sum()
            
            # Herfindahl-Hirschman Index (market concentration)
            kpis['hhi_index'] = (market_shares ** 2).sum()
            
            # Market diversity (inverse of concentration)
            kpis['market_diversity'] = 1 / (kpis['hhi_index'] / 10000) if kpis['hhi_index'] > 0 else 0
            
            # Number of significant players (>1% market share)
            kpis['significant_players'] = (market_shares > 1).sum()
        
        return kpis

    def _calculate_price_kpis(self, price_data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate price performance KPIs."""
        kpis = {}
        
        if price_data.empty or 'price_mean' not in price_data.columns:
            return kpis
        
        price_values = price_data['price_mean'].dropna()
        
        if len(price_values) == 0:
            return kpis
        
        # Basic price metrics
        kpis['avg_market_price'] = price_values.mean()
        kpis['median_market_price'] = price_values.median()
        kpis['price_range'] = price_values.max() - price_values.min()
        kpis['price_std'] = price_values.std()
        kpis['price_cv'] = kpis['price_std'] / kpis['avg_market_price'] if kpis['avg_market_price'] > 0 else 0
        
        # Price distribution analysis
        thresholds = self.kpi_thresholds.get('price_range', {})
        
        budget_models = (price_values <= thresholds.get('budget', 15000)).sum()
        mid_range_models = ((price_values > thresholds.get('budget', 15000)) & 
                           (price_values <= thresholds.get('mid_range', 35000))).sum()
        premium_models = ((price_values > thresholds.get('mid_range', 35000)) & 
                         (price_values <= thresholds.get('premium', 70000))).sum()
        luxury_models = (price_values > thresholds.get('premium', 70000)).sum()
        
        total_models = len(price_values)
        
        kpis['budget_segment_pct'] = (budget_models / total_models) * 100
        kpis['mid_range_segment_pct'] = (mid_range_models / total_models) * 100
        kpis['premium_segment_pct'] = (premium_models / total_models) * 100
        kpis['luxury_segment_pct'] = (luxury_models / total_models) * 100
        
        return kpis

    def _calculate_growth_kpis(self, data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Calculate growth and trend KPIs."""
        kpis = {}
        
        # Market growth indicators
        if 'sales_data' in data:
            sales_data = data['sales_data']
            year_columns = [col for col in sales_data.columns if col.isdigit()]
            
            if len(year_columns) >= 2:
                # Calculate year-over-year growth
                yearly_totals = sales_data[year_columns].sum()
                
                if len(yearly_totals) >= 2:
                    # Latest year vs previous year
                    latest_year = yearly_totals.iloc[-1]
                    previous_year = yearly_totals.iloc[-2]
                    
                    if previous_year > 0:
                        kpis['yoy_growth_rate'] = (latest_year - previous_year) / previous_year
                    else:
                        kpis['yoy_growth_rate'] = 0
                    
                    # 5-year CAGR
                    if len(yearly_totals) >= 5:
                        first_year = yearly_totals.iloc[-5]
                        if first_year > 0:
                            kpis['cagr_5y'] = ((latest_year / first_year) ** (1/5)) - 1
                        else:
                            kpis['cagr_5y'] = 0
        
        return kpis

    def _calculate_performance_ratings(self, kpis: Dict[str, Any]) -> Dict[str, str]:
        """Calculate performance ratings based on thresholds."""
        ratings = {}
        
        # Sales performance rating
        if 'avg_sales_per_model' in kpis:
            avg_sales = kpis['avg_sales_per_model']
            sales_thresholds = self.kpi_thresholds.get('sales_performance', {})
            
            if avg_sales >= sales_thresholds.get('high', 100000):
                ratings['sales_performance'] = 'Excellent'
            elif avg_sales >= sales_thresholds.get('medium', 10000):
                ratings['sales_performance'] = 'Good'
            elif avg_sales >= sales_thresholds.get('low', 1000):
                ratings['sales_performance'] = 'Average'
            else:
                ratings['sales_performance'] = 'Poor'
        
        # Market concentration rating
        if 'top_3_concentration' in kpis:
            concentration = kpis['top_3_concentration']
            market_thresholds = self.kpi_thresholds.get('market_share', {})
            
            if concentration >= 70:
                ratings['market_concentration'] = 'Highly Concentrated'
            elif concentration >= 50:
                ratings['market_concentration'] = 'Concentrated'
            elif concentration >= 30:
                ratings['market_concentration'] = 'Moderate'
            else:
                ratings['market_concentration'] = 'Fragmented'
        
        # Price positioning rating
        if 'avg_market_price' in kpis:
            avg_price = kpis['avg_market_price']
            price_thresholds = self.kpi_thresholds.get('price_range', {})
            
            if avg_price >= price_thresholds.get('premium', 70000):
                ratings['price_positioning'] = 'Premium'
            elif avg_price >= price_thresholds.get('mid_range', 35000):
                ratings['price_positioning'] = 'Mid-Range'
            elif avg_price >= price_thresholds.get('budget', 15000):
                ratings['price_positioning'] = 'Budget'
            else:
                ratings['price_positioning'] = 'Entry-Level'
        
        # Growth rating
        if 'yoy_growth_rate' in kpis:
            growth_rate = kpis['yoy_growth_rate']
            
            if growth_rate >= 0.1:
                ratings['growth'] = 'Strong Growth'
            elif growth_rate >= 0.05:
                ratings['growth'] = 'Moderate Growth'
            elif growth_rate >= 0:
                ratings['growth'] = 'Stable'
            elif growth_rate >= -0.05:
                ratings['growth'] = 'Declining'
            else:
                ratings['growth'] = 'Sharp Decline'
        
        return ratings

    def calculate_trend_analysis(self, data: pd.DataFrame, metric_column: str, 
                                time_column: str = None) -> Dict[str, Any]:
        """Calculate trend analysis for a specific metric."""
        if data.empty or metric_column not in data.columns:
            return {}
        
        metric_data = data[metric_column].dropna()
        
        if len(metric_data) < 2:
            return {}
        
        # Calculate trend statistics
        x = np.arange(len(metric_data))
        slope, intercept = np.polyfit(x, metric_data, 1)
        
        # Calculate R-squared
        y_pred = slope * x + intercept
        ss_res = np.sum((metric_data - y_pred) ** 2)
        ss_tot = np.sum((metric_data - np.mean(metric_data)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # Determine trend direction and strength
        if slope > 0:
            trend_direction = 'Increasing'
        elif slope < 0:
            trend_direction = 'Decreasing'
        else:
            trend_direction = 'Stable'
        
        if abs(r_squared) >= 0.7:
            trend_strength = 'Strong'
        elif abs(r_squared) >= 0.4:
            trend_strength = 'Moderate'
        else:
            trend_strength = 'Weak'
        
        return {
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_squared,
            'trend_direction': trend_direction,
            'trend_strength': trend_strength,
            'trend_description': f"{trend_strength} {trend_direction.lower()} trend"
        }

    def generate_kpi_summary(self, kpis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of key KPIs for executive reporting."""
        summary = {
            'key_metrics': {},
            'performance_highlights': [],
            'areas_of_concern': [],
            'recommendations': []
        }
        
        # Extract key metrics
        key_metrics = [
            'total_models', 'total_automakers', 'total_market_sales',
            'avg_sales_per_model', 'market_leader_share', 'avg_market_price',
            'yoy_growth_rate', 'top_3_concentration'
        ]
        
        for metric in key_metrics:
            if metric in kpis:
                summary['key_metrics'][metric] = kpis[metric]
        
        # Generate performance highlights
        if 'avg_sales_per_model' in kpis and kpis['avg_sales_per_model'] > 50000:
            summary['performance_highlights'].append("Strong average sales performance per model")
        
        if 'market_leader_share' in kpis and kpis['market_leader_share'] > 15:
            summary['performance_highlights'].append("Dominant market leader position")
        
        if 'yoy_growth_rate' in kpis and kpis['yoy_growth_rate'] > 0.05:
            summary['performance_highlights'].append("Positive year-over-year growth")
        
        # Identify areas of concern
        if 'sales_cv' in kpis and kpis['sales_cv'] > 2:
            summary['areas_of_concern'].append("High sales volatility across models")
        
        if 'top_3_concentration' in kpis and kpis['top_3_concentration'] > 80:
            summary['areas_of_concern'].append("Very high market concentration")
        
        if 'yoy_growth_rate' in kpis and kpis['yoy_growth_rate'] < -0.05:
            summary['areas_of_concern'].append("Declining market performance")
        
        # Generate recommendations
        if 'market_diversity' in kpis and kpis['market_diversity'] < 0.5:
            summary['recommendations'].append("Consider market diversification strategies")
        
        if 'avg_market_price' in kpis and kpis['avg_market_price'] > 60000:
            summary['recommendations'].append("Premium market positioning - focus on luxury segment")
        
        if 'significant_players' in kpis and kpis['significant_players'] < 10:
            summary['recommendations'].append("Limited competition - opportunity for new entrants")
        
        return summary

    def get_kpi_dashboard_data(self) -> Dict[str, Any]:
        """Get formatted KPI data for dashboard display."""
        if not self.calculated_kpis:
            return {}
        
        # Format KPIs for dashboard display
        dashboard_kpis = []
        
        # Key performance indicators
        key_kpis = [
            ('Total Models', 'total_models', 'count'),
            ('Total Sales', 'total_market_sales', 'number'),
            ('Avg Sales/Model', 'avg_sales_per_model', 'number'),
            ('Market Leader %', 'market_leader_share', 'percentage'),
            ('Avg Price', 'avg_market_price', 'currency'),
            ('YoY Growth', 'yoy_growth_rate', 'percentage'),
            ('Top 3 Concentration', 'top_3_concentration', 'percentage')
        ]
        
        for label, key, format_type in key_kpis:
            if key in self.calculated_kpis:
                value = self.calculated_kpis[key]
                
                # Format value based on type
                if format_type == 'currency':
                    formatted_value = f"€{value:,.0f}"
                elif format_type == 'percentage':
                    formatted_value = f"{value:.1f}%"
                elif format_type == 'number':
                    formatted_value = f"{value:,.0f}"
                else:
                    formatted_value = str(value)
                
                dashboard_kpis.append({
                    'label': label,
                    'value': formatted_value,
                    'raw_value': value,
                    'format_type': format_type
                })
        
        return {
            'kpis': dashboard_kpis,
            'performance_ratings': self.calculated_kpis.get('performance_ratings', {}),
            'summary': self.generate_kpi_summary(self.calculated_kpis)
        }

    def export_kpis(self, format_type: str = 'dict') -> Any:
        """Export calculated KPIs in specified format."""
        if not self.calculated_kpis:
            return None
        
        if format_type == 'dict':
            return self.calculated_kpis.copy()
        elif format_type == 'dataframe':
            return pd.DataFrame([self.calculated_kpis])
        elif format_type == 'json':
            import json
            return json.dumps(self.calculated_kpis, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported format type: {format_type}")


# Global instance for use throughout the application
kpi_calculator = KPICalculator()

