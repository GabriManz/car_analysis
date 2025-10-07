"""
📈 Presentation Layer for Car Market Analysis Executive Dashboard

Professional chart creation, interactive visualizations, and executive-grade styling.
Handles all visualization components with advanced hover systems and responsive design.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Any, Tuple, Union
import warnings
warnings.filterwarnings('ignore')

# Import configuration (absolute)
try:
    from src.components.config.app_config import (
        CHART_CONFIG, COLOR_PALETTE, COOLORS_PALETTE, RISK_COLORS,
        MANUFACTURER_COLORS, CUSTOM_CSS
    )
except ImportError:
    # Fallback configuration
    CHART_CONFIG = {
        'default_height': 500,
        'plot_bgcolor': 'rgba(255, 255, 255, 0.95)',
        'paper_bgcolor': 'rgba(255, 255, 255, 0.95)',
        'font_family': 'Arial, sans-serif',
        'title_font_size': 18,
        'title_color': '#2c3e50'
    }
    COLOR_PALETTE = {
        'primary': '#1f77b4',
        'secondary': '#0a9396',
        'success': '#2ca02c',
        'danger': '#d62728',
        'warning': '#ff7f0e'
    }
    COOLORS_PALETTE = ['#001219', '#005f73', '#0a9396', '#94d2bd', '#e9d8a6']
    RISK_COLORS = {'low': '#28a745', 'medium': '#ffc107', 'high': '#fd7e14', 'critical': '#dc3545'}
    MANUFACTURER_COLORS = {}
    CUSTOM_CSS = ""


class PresentationLayer:
    """
    🎨 Executive-Grade Presentation Engine
    
    Creates professional, interactive visualizations with advanced styling,
    responsive design, and executive-grade aesthetics for automotive market analysis.
    """

    def __init__(self):
        """Initialize the PresentationLayer with configuration and styling."""
        self.chart_config = CHART_CONFIG
        self.color_palette = COLOR_PALETTE
        self.coolors_palette = COOLORS_PALETTE
        self.risk_colors = RISK_COLORS
        self.manufacturer_colors = MANUFACTURER_COLORS
        self.custom_css = CUSTOM_CSS
        
        # Chart templates
        self.templates = {
            'executive': 'plotly_white',
            'dark': 'plotly_dark',
            'minimal': 'simple_white'
        }

    # ==================== CHART CREATION METHODS ====================

    def create_sales_by_model_bar(self, data: pd.DataFrame, title: str = "Top Models by Sales") -> go.Figure:
        """Create a professional bar chart for sales by model."""
        if data.empty:
            return self._create_empty_chart("No sales data available")
        
        # Prepare data
        chart_data = data.head(20)  # Top 20 models
        
        fig = go.Figure()
        
        # Create bar chart with professional styling
        fig.add_trace(go.Bar(
            x=chart_data['total_sales'],
            y=chart_data['Genmodel'],
            orientation='h',
            marker=dict(
                color=self._get_manufacturer_colors(chart_data['Automaker']),
                line=dict(color='rgba(0, 18, 25, 0.1)', width=1),
                opacity=0.8
            ),
            text=chart_data['total_sales'],
            texttemplate='<b>%{text:,.0f}</b>',
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>' +
                         'Total Sales: <b>%{x:,.0f}</b><br>' +
                         '<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=self.chart_config['title_font_size'], color=self.chart_config['title_color']),
                x=0.5
            ),
            xaxis=dict(
                title="Total Sales (Units)",
                gridcolor='rgba(0, 0, 0, 0.1)',
                zeroline=False,
                showline=True,
                linecolor='rgba(0, 0, 0, 0.2)'
            ),
            yaxis=dict(
                title="Model",
                gridcolor='rgba(0, 0, 0, 0.1)',
                showline=True,
                linecolor='rgba(0, 0, 0, 0.2)',
                categoryorder='total ascending'
            ),
            plot_bgcolor=self.chart_config['plot_bgcolor'],
            paper_bgcolor=self.chart_config['paper_bgcolor'],
            font=dict(family=self.chart_config['font_family']),
            height=self.chart_config['default_height'],
            margin=dict(l=80, r=40, t=80, b=60),
            showlegend=False
        )
        
        return fig

    def create_price_by_automaker_bar(self, data: pd.DataFrame, title: str = "Average Price by Automaker") -> go.Figure:
        """Create a professional bar chart for average price by automaker."""
        if data.empty:
            return self._create_empty_chart("No price data available")
        
        # Prepare data
        price_by_maker = data.groupby('Automaker')['price_mean'].mean().sort_values(ascending=False).head(15)
        
        fig = go.Figure()
        
        # Create bar chart
        fig.add_trace(go.Bar(
            x=price_by_maker.index,
            y=price_by_maker.values,
            marker=dict(
                color=self._get_automaker_colors(price_by_maker.index),
                line=dict(color='rgba(0, 18, 25, 0.1)', width=1),
                opacity=0.8
            ),
            text=[f"€{val:,.0f}" for val in price_by_maker.values],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>' +
                         'Average Price: <b>€%{y:,.0f}</b><br>' +
                         '<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=self.chart_config['title_font_size'], color=self.chart_config['title_color']),
                x=0.5
            ),
            xaxis=dict(
                title="Automaker",
                gridcolor='rgba(0, 0, 0, 0.1)',
                zeroline=False,
                showline=True,
                linecolor='rgba(0, 0, 0, 0.2)'
            ),
            yaxis=dict(
                title="Average Price (€)",
                gridcolor='rgba(0, 0, 0, 0.1)',
                showline=True,
                linecolor='rgba(0, 0, 0, 0.2)',
                tickformat='€,.0f'
            ),
            plot_bgcolor=self.chart_config['plot_bgcolor'],
            paper_bgcolor=self.chart_config['paper_bgcolor'],
            font=dict(family=self.chart_config['font_family']),
            height=self.chart_config['default_height'],
            margin=dict(l=80, r=40, t=80, b=60),
            showlegend=False
        )
        
        return fig

    def create_market_share_pie(self, data: pd.DataFrame, title: str = "Market Share by Automaker") -> go.Figure:
        """Create a professional pie chart for market share."""
        if data.empty:
            return self._create_empty_chart("No market share data available")
        
        # Prepare data - show top 10 and group others
        top_10 = data.head(10)
        others_sum = data.iloc[10:]['market_share_percent'].sum()
        
        if others_sum > 0:
            top_10 = pd.concat([top_10, pd.DataFrame({
                'Automaker': ['Others'],
                'market_share_percent': [others_sum]
            })], ignore_index=True)
        
        fig = go.Figure()
        
        # Create pie chart
        fig.add_trace(go.Pie(
            labels=top_10['Automaker'],
            values=top_10['market_share_percent'],
            marker=dict(
                colors=self._get_automaker_colors(top_10['Automaker']),
                line=dict(color='white', width=2)
            ),
            textinfo='label+percent',
            texttemplate='<b>%{label}</b><br>%{percent}<br>(%{value:.1f}%)',
            hovertemplate='<b>%{label}</b><br>' +
                         'Market Share: <b>%{value:.1f}%</b><br>' +
                         '<extra></extra>',
            hole=0.3  # Donut chart
        ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=self.chart_config['title_font_size'], color=self.chart_config['title_color']),
                x=0.5
            ),
            plot_bgcolor=self.chart_config['plot_bgcolor'],
            paper_bgcolor=self.chart_config['paper_bgcolor'],
            font=dict(family=self.chart_config['font_family']),
            height=self.chart_config['default_height'],
            margin=dict(l=40, r=40, t=80, b=40),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.02
            )
        )
        
        return fig

    def create_sales_trend_line(self, data: pd.DataFrame, title: str = "Sales Trend Over Time") -> go.Figure:
        """Create a professional line chart for sales trends."""
        if data.empty:
            return self._create_empty_chart("No sales trend data available")
        
        # Prepare data - reshape sales data
        year_columns = [col for col in data.columns if col.isdigit()]
        if not year_columns:
            return self._create_empty_chart("No year data available")
        
        # Calculate total sales by year
        yearly_sales = data[year_columns].sum().sort_index()
        
        fig = go.Figure()
        
        # Create line chart
        fig.add_trace(go.Scatter(
            x=yearly_sales.index,
            y=yearly_sales.values,
            mode='lines+markers',
            line=dict(
                color=self.color_palette['primary'],
                width=4,
                shape='spline'
            ),
            marker=dict(
                size=8,
                color=self.color_palette['primary'],
                line=dict(color='white', width=2)
            ),
            fill='tonexty',
            fillcolor=f"rgba({self._hex_to_rgb(self.color_palette['primary'])}, 0.1)",
            hovertemplate='<b>Year: %{x}</b><br>' +
                         'Total Sales: <b>%{y:,.0f}</b><br>' +
                         '<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=self.chart_config['title_font_size'], color=self.chart_config['title_color']),
                x=0.5
            ),
            xaxis=dict(
                title="Year",
                gridcolor='rgba(0, 0, 0, 0.1)',
                zeroline=False,
                showline=True,
                linecolor='rgba(0, 0, 0, 0.2)'
            ),
            yaxis=dict(
                title="Total Sales (Units)",
                gridcolor='rgba(0, 0, 0, 0.1)',
                showline=True,
                linecolor='rgba(0, 0, 0, 0.2)',
                tickformat=',.0f'
            ),
            plot_bgcolor=self.chart_config['plot_bgcolor'],
            paper_bgcolor=self.chart_config['paper_bgcolor'],
            font=dict(family=self.chart_config['font_family']),
            height=self.chart_config['default_height'],
            margin=dict(l=80, r=40, t=80, b=60),
            showlegend=False
        )
        
        return fig

    def create_price_distribution_histogram(self, data: pd.DataFrame, title: str = "Price Distribution") -> go.Figure:
        """Create a professional histogram for price distribution."""
        if data.empty or 'price_mean' not in data.columns:
            return self._create_empty_chart("No price data available")
        
        # Prepare data
        price_data = data['price_mean'].dropna()
        
        fig = go.Figure()
        
        # Create histogram
        fig.add_trace(go.Histogram(
            x=price_data,
            nbinsx=30,
            marker=dict(
                color=self.color_palette['secondary'],
                opacity=0.7,
                line=dict(color='white', width=1)
            ),
            hovertemplate='<b>Price Range: €%{x:,.0f}</b><br>' +
                         'Count: <b>%{y}</b><br>' +
                         '<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=self.chart_config['title_font_size'], color=self.chart_config['title_color']),
                x=0.5
            ),
            xaxis=dict(
                title="Price (€)",
                gridcolor='rgba(0, 0, 0, 0.1)',
                zeroline=False,
                showline=True,
                linecolor='rgba(0, 0, 0, 0.2)',
                tickformat='€,.0f'
            ),
            yaxis=dict(
                title="Number of Models",
                gridcolor='rgba(0, 0, 0, 0.1)',
                showline=True,
                linecolor='rgba(0, 0, 0, 0.2)'
            ),
            plot_bgcolor=self.chart_config['plot_bgcolor'],
            paper_bgcolor=self.chart_config['paper_bgcolor'],
            font=dict(family=self.chart_config['font_family']),
            height=self.chart_config['default_height'],
            margin=dict(l=80, r=40, t=80, b=60),
            showlegend=False
        )
        
        return fig

    def create_correlation_heatmap(self, correlation_matrix: pd.DataFrame, title: str = "Feature Correlation Matrix") -> go.Figure:
        """Create a professional heatmap for correlation analysis."""
        if correlation_matrix.empty:
            return self._create_empty_chart("No correlation data available")
        
        fig = go.Figure()
        
        # Create heatmap
        fig.add_trace(go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=np.round(correlation_matrix.values, 2),
            texttemplate='%{text}',
            textfont={"size": 10},
            hovertemplate='<b>%{y} vs %{x}</b><br>' +
                         'Correlation: <b>%{z:.3f}</b><br>' +
                         '<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=self.chart_config['title_font_size'], color=self.chart_config['title_color']),
                x=0.5
            ),
            xaxis=dict(
                title="Features",
                gridcolor='rgba(0, 0, 0, 0.1)',
                showline=True,
                linecolor='rgba(0, 0, 0, 0.2)'
            ),
            yaxis=dict(
                title="Features",
                gridcolor='rgba(0, 0, 0, 0.1)',
                showline=True,
                linecolor='rgba(0, 0, 0, 0.2)'
            ),
            plot_bgcolor=self.chart_config['plot_bgcolor'],
            paper_bgcolor=self.chart_config['paper_bgcolor'],
            font=dict(family=self.chart_config['font_family']),
            height=self.chart_config['default_height'],
            margin=dict(l=80, r=40, t=80, b=60)
        )
        
        return fig

    def create_clustering_scatter(self, data: pd.DataFrame, title: str = "Model Clustering Analysis") -> go.Figure:
        """Create a professional scatter plot for clustering analysis."""
        if data.empty or 'cluster' not in data.columns:
            return self._create_empty_chart("No clustering data available")
        
        # Prepare data
        cluster_data = data.dropna(subset=['cluster'])
        
        fig = go.Figure()
        
        # Create scatter plot with clusters
        for cluster_id in sorted(cluster_data['cluster'].unique()):
            cluster_subset = cluster_data[cluster_data['cluster'] == cluster_id]
            
            fig.add_trace(go.Scatter(
                x=cluster_subset.get('price_mean', cluster_subset.iloc[:, 0]),
                y=cluster_subset.get('total_sales', cluster_subset.iloc[:, 1]),
                mode='markers',
                name=f'Cluster {cluster_id}',
                marker=dict(
                    size=8,
                    color=self.coolors_palette[cluster_id % len(self.coolors_palette)],
                    opacity=0.7,
                    line=dict(color='white', width=1)
                ),
                hovertemplate='<b>%{text}</b><br>' +
                             'Price: <b>€%{x:,.0f}</b><br>' +
                             'Sales: <b>%{y:,.0f}</b><br>' +
                             '<extra></extra>',
                text=cluster_subset.get('Genmodel', cluster_subset.index)
            ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=self.chart_config['title_font_size'], color=self.chart_config['title_color']),
                x=0.5
            ),
            xaxis=dict(
                title="Average Price (€)",
                gridcolor='rgba(0, 0, 0, 0.1)',
                zeroline=False,
                showline=True,
                linecolor='rgba(0, 0, 0, 0.2)',
                tickformat='€,.0f'
            ),
            yaxis=dict(
                title="Total Sales (Units)",
                gridcolor='rgba(0, 0, 0, 0.1)',
                showline=True,
                linecolor='rgba(0, 0, 0, 0.2)',
                tickformat=',.0f'
            ),
            plot_bgcolor=self.chart_config['plot_bgcolor'],
            paper_bgcolor=self.chart_config['paper_bgcolor'],
            font=dict(family=self.chart_config['font_family']),
            height=self.chart_config['default_height'],
            margin=dict(l=80, r=40, t=80, b=60),
            showlegend=True
        )
        
        return fig

    # ==================== UTILITY METHODS ====================

    def _create_empty_chart(self, message: str = "No data available") -> go.Figure:
        """Create an empty chart with a message."""
        fig = go.Figure()
        
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color=self.color_palette['secondary'])
        )
        
        fig.update_layout(
            plot_bgcolor=self.chart_config['plot_bgcolor'],
            paper_bgcolor=self.chart_config['paper_bgcolor'],
            font=dict(family=self.chart_config['font_family']),
            height=self.chart_config['default_height'],
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        
        return fig

    def _get_manufacturer_colors(self, manufacturers: pd.Series) -> List[str]:
        """Get colors for manufacturers."""
        colors = []
        for manufacturer in manufacturers:
            if manufacturer in self.manufacturer_colors:
                colors.append(self.manufacturer_colors[manufacturer])
            else:
                # Generate color based on manufacturer name
                colors.append(self._generate_color_from_name(manufacturer))
        return colors

    def _get_automaker_colors(self, automakers: Union[pd.Series, List[str]]) -> List[str]:
        """Get colors for automakers."""
        if isinstance(automakers, pd.Series):
            automakers = automakers.tolist()
        
        colors = []
        for automaker in automakers:
            if automaker in self.manufacturer_colors:
                colors.append(self.manufacturer_colors[automaker])
            else:
                colors.append(self._generate_color_from_name(automaker))
        return colors

    def _generate_color_from_name(self, name: str) -> str:
        """Generate a consistent color from a name."""
        # Simple hash-based color generation
        hash_value = hash(name) % len(self.coolors_palette)
        return self.coolors_palette[abs(hash_value)]

    def _hex_to_rgb(self, hex_color: str) -> str:
        """Convert hex color to RGB string for rgba."""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"{rgb[0]}, {rgb[1]}, {rgb[2]}"

    # ==================== EXECUTIVE DASHBOARD CHARTS ====================

    def create_executive_summary_chart(self, kpi_data: Dict[str, float]) -> go.Figure:
        """Create an executive summary chart with key metrics."""
        # Extract key metrics
        metrics = ['total_models', 'total_market_sales', 'avg_market_price', 'market_leader_share']
        values = [kpi_data.get(metric, 0) for metric in metrics]
        labels = ['Total Models', 'Total Sales', 'Avg Price (€)', 'Market Leader (%)']
        
        fig = go.Figure()
        
        # Create gauge-style indicators
        for i, (label, value) in enumerate(zip(labels, values)):
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=value,
                domain={'x': [i/4, (i+1)/4], 'y': [0, 1]},
                title={'text': label},
                gauge={
                    'axis': {'range': [None, max(value * 1.5, 100)]},
                    'bar': {'color': self.coolors_palette[i % len(self.coolors_palette)]},
                    'steps': [
                        {'range': [0, max(value * 1.5, 100) * 0.5], 'color': "lightgray"},
                        {'range': [max(value * 1.5, 100) * 0.5, max(value * 1.5, 100) * 0.8], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': value * 0.9
                    }
                }
            ))
        
        fig.update_layout(
            title="Executive Dashboard - Key Performance Indicators",
            font=dict(family=self.chart_config['font_family']),
            height=400,
            paper_bgcolor=self.chart_config['paper_bgcolor']
        )
        
        return fig

    def create_market_analysis_dashboard(self, market_data: Dict[str, pd.DataFrame]) -> Dict[str, go.Figure]:
        """Create a comprehensive market analysis dashboard."""
        dashboard_charts = {}
        
        # Market share pie chart
        if 'market_share' in market_data:
            dashboard_charts['market_share'] = self.create_market_share_pie(
                market_data['market_share'], 
                "Market Share Distribution"
            )
        
        # Sales by model bar chart
        if 'sales_summary' in market_data:
            dashboard_charts['top_models'] = self.create_sales_by_model_bar(
                market_data['sales_summary'], 
                "Top 20 Models by Sales Volume"
            )
        
        # Price distribution histogram
        if 'price_data' in market_data:
            dashboard_charts['price_distribution'] = self.create_price_distribution_histogram(
                market_data['price_data'], 
                "Price Distribution Analysis"
            )
        
        # Sales trend line chart
        if 'sales_data' in market_data:
            dashboard_charts['sales_trend'] = self.create_sales_trend_line(
                market_data['sales_data'], 
                "Market Sales Trend (2001-2020)"
            )
        
        return dashboard_charts

    def create_analytics_dashboard(self, analytics_data: Dict[str, Any]) -> Dict[str, go.Figure]:
        """Create an advanced analytics dashboard."""
        analytics_charts = {}
        
        # Correlation heatmap
        if 'correlation_matrix' in analytics_data:
            analytics_charts['correlation'] = self.create_correlation_heatmap(
                analytics_data['correlation_matrix'],
                "Feature Correlation Analysis"
            )
        
        # Clustering scatter plot
        if 'clustering_data' in analytics_data:
            analytics_charts['clustering'] = self.create_clustering_scatter(
                analytics_data['clustering_data'],
                "Market Segment Clustering"
            )
        
        # Price elasticity analysis
        if 'price_elasticity' in analytics_data:
            analytics_charts['price_elasticity'] = self.create_price_elasticity_chart(
                analytics_data['price_elasticity']
            )
        
        return analytics_charts

    def create_price_elasticity_chart(self, elasticity_data: pd.DataFrame) -> go.Figure:
        """Create a chart for price elasticity analysis."""
        if elasticity_data.empty:
            return self._create_empty_chart("No price elasticity data available")
        
        fig = go.Figure()
        
        # Create scatter plot with elasticity categories
        for category in elasticity_data['elasticity_category'].unique():
            category_data = elasticity_data[elasticity_data['elasticity_category'] == category]
            
            fig.add_trace(go.Scatter(
                x=category_data['price_mean'],
                y=category_data['total_sales'],
                mode='markers',
                name=category,
                marker=dict(
                    size=8,
                    opacity=0.7
                ),
                hovertemplate='<b>%{text}</b><br>' +
                             'Price: <b>€%{x:,.0f}</b><br>' +
                             'Sales: <b>%{y:,.0f}</b><br>' +
                             '<extra></extra>',
                text=category_data['Genmodel']
            ))
        
        # Update layout
        fig.update_layout(
            title="Price Elasticity Analysis",
            xaxis_title="Average Price (€)",
            yaxis_title="Total Sales (Units)",
            plot_bgcolor=self.chart_config['plot_bgcolor'],
            paper_bgcolor=self.chart_config['paper_bgcolor'],
            font=dict(family=self.chart_config['font_family']),
            height=self.chart_config['default_height'],
            showlegend=True
        )
        
        return fig

    # ==================== RESPONSIVE DESIGN METHODS ====================

    def get_responsive_config(self, screen_size: str = 'desktop') -> Dict[str, Any]:
        """Get responsive configuration for different screen sizes."""
        configs = {
            'mobile': {
                'height': 300,
                'font_size': 12,
                'margin': dict(l=40, r=20, t=60, b=40)
            },
            'tablet': {
                'height': 400,
                'font_size': 14,
                'margin': dict(l=60, r=30, t=70, b=50)
            },
            'desktop': {
                'height': 500,
                'font_size': 16,
                'margin': dict(l=80, r=40, t=80, b=60)
            }
        }
        
        return configs.get(screen_size, configs['desktop'])

    def make_chart_responsive(self, fig: go.Figure, screen_size: str = 'desktop') -> go.Figure:
        """Make a chart responsive for different screen sizes."""
        responsive_config = self.get_responsive_config(screen_size)
        
        fig.update_layout(
            height=responsive_config['height'],
            font=dict(size=responsive_config['font_size']),
            margin=responsive_config['margin']
        )
        
        return fig


# Global instance for use throughout the application
presentation_layer = PresentationLayer()

