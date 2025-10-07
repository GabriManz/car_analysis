"""
📊 Chart Factory Component for Car Market Analysis Executive Dashboard

Professional chart creation and visualization factory for automotive market analysis.
Provides executive-grade visualizations with consistent styling and interactivity.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Any, Tuple, Union
import warnings
warnings.filterwarnings('ignore')

# Import configuration and presentation layer
try:
    from src.components.config.app_config import CHART_CONFIG, COLOR_PALETTE, COOLORS_PALETTE, MANUFACTURER_COLORS
    from src.presentation_layer import presentation_layer
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
    MANUFACTURER_COLORS = {}
    presentation_layer = None


class ChartFactory:
    """
    🏭 Executive-Grade Chart Factory
    
    Creates professional, interactive visualizations with consistent styling
    and executive-grade aesthetics for automotive market analysis.
    """

    def __init__(self):
        """Initialize the ChartFactory with configuration."""
        self.chart_config = CHART_CONFIG
        self.color_palette = COLOR_PALETTE
        self.coolors_palette = COOLORS_PALETTE
        self.manufacturer_colors = MANUFACTURER_COLORS
        self.presentation_layer = presentation_layer

    # ==================== SALES CHARTS ====================

    def create_sales_bar_chart(self, data: pd.DataFrame, title: str = "Sales Analysis", 
                              chart_type: str = "horizontal") -> go.Figure:
        """Create a professional sales bar chart."""
        if data.empty:
            return self._create_empty_chart("No sales data available")
        
        # Prepare data
        chart_data = data.head(20)  # Top 20 items
        
        fig = go.Figure()
        
        if chart_type == "horizontal":
            # Horizontal bar chart
            fig.add_trace(go.Bar(
                x=chart_data['total_sales'],
                y=chart_data['Genmodel'],
                orientation='h',
                marker=dict(
                    color=self._get_automaker_colors(chart_data['Automaker']),
                    line=dict(color='rgba(0, 18, 25, 0.1)', width=1),
                    opacity=0.8
                ),
                text=chart_data['total_sales'],
                texttemplate='<b>%{text:,.0f}</b>',
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>' +
                             'Total Sales: <b>%{x:,.0f}</b><br>' +
                             'Automaker: <b>%{customdata}</b><br>' +
                             '<extra></extra>',
                customdata=chart_data['Automaker']
            ))
            
            fig.update_layout(
                xaxis_title="Total Sales (Units)",
                yaxis_title="Model",
                yaxis=dict(categoryorder='total ascending')
            )
        else:
            # Vertical bar chart
            fig.add_trace(go.Bar(
                x=chart_data['Genmodel'],
                y=chart_data['total_sales'],
                marker=dict(
                    color=self._get_automaker_colors(chart_data['Automaker']),
                    line=dict(color='rgba(0, 18, 25, 0.1)', width=1),
                    opacity=0.8
                ),
                text=chart_data['total_sales'],
                texttemplate='<b>%{text:,.0f}</b>',
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>' +
                             'Total Sales: <b>%{y:,.0f}</b><br>' +
                             'Automaker: <b>%{customdata}</b><br>' +
                             '<extra></extra>',
                customdata=chart_data['Automaker']
            ))
            
            fig.update_layout(
                xaxis_title="Model",
                yaxis_title="Total Sales (Units)",
                xaxis=dict(categoryorder='total descending')
            )
        
        return self._apply_standard_layout(fig, title)

    def create_sales_trend_chart(self, data: pd.DataFrame, title: str = "Sales Trend Over Time") -> go.Figure:
        """Create a sales trend line chart."""
        if data.empty:
            return self._create_empty_chart("No sales trend data available")
        
        # Reshape sales data if needed
        year_columns = [col for col in data.columns if col.isdigit()]
        if not year_columns:
            return self._create_empty_chart("No year data available")
        
        # Calculate total sales by year
        yearly_sales = data[year_columns].sum().sort_index()
        
        fig = go.Figure()
        
        # Create line chart with area fill
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
            name='Total Sales',
            hovertemplate='<b>Year: %{x}</b><br>' +
                         'Total Sales: <b>%{y:,.0f}</b><br>' +
                         '<extra></extra>'
        ))
        
        return self._apply_standard_layout(fig, title, x_title="Year", y_title="Total Sales (Units)")

    # ==================== PRICE CHARTS ====================

    def create_price_bar_chart(self, data: pd.DataFrame, title: str = "Price Analysis") -> go.Figure:
        """Create a professional price bar chart."""
        if data.empty or 'price_mean' not in data.columns:
            return self._create_empty_chart("No price data available")
        
        # Group by automaker and calculate average price
        price_by_maker = data.groupby('Automaker')['price_mean'].mean().sort_values(ascending=False).head(15)
        
        fig = go.Figure()
        
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
        
        return self._apply_standard_layout(fig, title, x_title="Automaker", y_title="Average Price (€)")

    def create_price_distribution_chart(self, data: pd.DataFrame, title: str = "Price Distribution") -> go.Figure:
        """Create a price distribution histogram."""
        if data.empty or 'price_mean' not in data.columns:
            return self._create_empty_chart("No price data available")
        
        price_data = data['price_mean'].dropna()
        
        fig = go.Figure()
        
        # Create histogram with custom bins
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
        
        return self._apply_standard_layout(fig, title, x_title="Price (€)", y_title="Number of Models")

    def create_price_vs_sales_scatter(self, data: pd.DataFrame, title: str = "Price vs Sales Analysis") -> go.Figure:
        """Create a scatter plot of price vs sales."""
        if data.empty:
            return self._create_empty_chart("No data available")
        
        # Merge price and sales data if needed
        if 'price_mean' not in data.columns or 'total_sales' not in data.columns:
            return self._create_empty_chart("Missing price or sales data")
        
        # Filter out missing values
        scatter_data = data.dropna(subset=['price_mean', 'total_sales'])
        
        fig = go.Figure()
        
        # Create scatter plot with automaker colors
        fig.add_trace(go.Scatter(
            x=scatter_data['price_mean'],
            y=scatter_data['total_sales'],
            mode='markers',
            marker=dict(
                size=8,
                color=self._get_automaker_colors(scatter_data['Automaker']),
                opacity=0.7,
                line=dict(color='white', width=1)
            ),
            text=scatter_data['Genmodel'],
            hovertemplate='<b>%{text}</b><br>' +
                         'Price: <b>€%{x:,.0f}</b><br>' +
                         'Sales: <b>%{y:,.0f}</b><br>' +
                         '<extra></extra>'
        ))
        
        return self._apply_standard_layout(fig, title, x_title="Average Price (€)", y_title="Total Sales (Units)")

    # ==================== MARKET SHARE CHARTS ====================

    def create_market_share_pie_chart(self, data: pd.DataFrame, title: str = "Market Share Distribution") -> go.Figure:
        """Create a market share pie chart."""
        if data.empty or 'market_share_percent' not in data.columns:
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
        
        # Create donut chart
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
        
        return self._apply_standard_layout(fig, title)

    def create_market_share_bar_chart(self, data: pd.DataFrame, title: str = "Market Share by Automaker") -> go.Figure:
        """Create a market share bar chart."""
        if data.empty or 'market_share_percent' not in data.columns:
            return self._create_empty_chart("No market share data available")
        
        # Show top 15 automakers
        chart_data = data.head(15)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=chart_data['Automaker'],
            y=chart_data['market_share_percent'],
            marker=dict(
                color=self._get_automaker_colors(chart_data['Automaker']),
                line=dict(color='rgba(0, 18, 25, 0.1)', width=1),
                opacity=0.8
            ),
            text=[f"{val:.1f}%" for val in chart_data['market_share_percent'].values],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>' +
                         'Market Share: <b>%{y:.1f}%</b><br>' +
                         '<extra></extra>'
        ))
        
        return self._apply_standard_layout(fig, title, x_title="Automaker", y_title="Market Share (%)")

    # ==================== ANALYTICS CHARTS ====================

    def create_correlation_heatmap(self, correlation_matrix: pd.DataFrame, title: str = "Feature Correlation Matrix") -> go.Figure:
        """Create a correlation heatmap."""
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
        
        return self._apply_standard_layout(fig, title)

    def create_clustering_scatter_chart(self, data: pd.DataFrame, title: str = "Model Clustering Analysis") -> go.Figure:
        """Create a clustering scatter plot."""
        if data.empty or 'cluster' not in data.columns:
            return self._create_empty_chart("No clustering data available")
        
        # Filter out missing values
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
        
        return self._apply_standard_layout(fig, title, x_title="Average Price (€)", y_title="Total Sales (Units)")

    def create_trend_analysis_chart(self, data: pd.DataFrame, metric_column: str, 
                                   title: str = "Trend Analysis") -> go.Figure:
        """Create a trend analysis chart."""
        if data.empty or metric_column not in data.columns:
            return self._create_empty_chart(f"No {metric_column} data available")
        
        metric_data = data[metric_column].dropna()
        
        if len(metric_data) < 2:
            return self._create_empty_chart("Insufficient data for trend analysis")
        
        fig = go.Figure()
        
        # Create line chart with trend
        x_values = list(range(len(metric_data)))
        fig.add_trace(go.Scatter(
            x=x_values,
            y=metric_data.values,
            mode='lines+markers',
            name='Actual',
            line=dict(color=self.color_palette['primary'], width=3),
            marker=dict(size=6, color=self.color_palette['primary'])
        ))
        
        # Add trend line
        slope, intercept = np.polyfit(x_values, metric_data.values, 1)
        trend_line = [slope * x + intercept for x in x_values]
        
        fig.add_trace(go.Scatter(
            x=x_values,
            y=trend_line,
            mode='lines',
            name='Trend',
            line=dict(color=self.color_palette['danger'], width=2, dash='dash'),
            hovertemplate='Trend Line<br>' +
                         'Value: <b>%{y:.2f}</b><br>' +
                         '<extra></extra>'
        ))
        
        return self._apply_standard_layout(fig, title, x_title="Time Period", y_title=metric_column)

    # ==================== EXECUTIVE DASHBOARD CHARTS ====================

    def create_kpi_gauge_chart(self, kpi_data: Dict[str, float], title: str = "KPI Dashboard") -> go.Figure:
        """Create KPI gauge charts."""
        if not kpi_data:
            return self._create_empty_chart("No KPI data available")
        
        # Select key KPIs for gauges
        kpi_keys = ['total_market_sales', 'avg_market_price', 'market_leader_share', 'yoy_growth_rate']
        kpi_labels = ['Total Sales', 'Avg Price (€)', 'Market Leader (%)', 'YoY Growth (%)']
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{'type': 'indicator'}, {'type': 'indicator'}],
                   [{'type': 'indicator'}, {'type': 'indicator'}]],
            subplot_titles=kpi_labels
        )
        
        positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
        colors = [self.coolors_palette[i] for i in range(4)]
        
        for i, (key, label, pos, color) in enumerate(zip(kpi_keys, kpi_labels, positions, colors)):
            if key in kpi_data:
                value = kpi_data[key]
                max_value = max(value * 1.5, 100) if value > 0 else 100
                
                fig.add_trace(go.Indicator(
                    mode="gauge+number",
                    value=value,
                    title={'text': label},
                    gauge={
                        'axis': {'range': [None, max_value]},
                        'bar': {'color': color},
                        'steps': [
                            {'range': [0, max_value * 0.5], 'color': "lightgray"},
                            {'range': [max_value * 0.5, max_value * 0.8], 'color': "gray"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': value * 0.9
                        }
                    }
                ), row=pos[0], col=pos[1])
        
        fig.update_layout(
            title=title,
            height=600,
            font=dict(family=self.chart_config['font_family']),
            paper_bgcolor=self.chart_config['paper_bgcolor']
        )
        
        return fig

    def create_executive_summary_chart(self, summary_data: Dict[str, Any], 
                                     title: str = "Executive Summary") -> go.Figure:
        """Create an executive summary chart."""
        if not summary_data:
            return self._create_empty_chart("No summary data available")
        
        # Create a multi-metric chart
        fig = make_subplots(
            rows=1, cols=3,
            specs=[[{'type': 'bar'}, {'type': 'pie'}, {'type': 'scatter'}]],
            subplot_titles=['Top Models', 'Market Share', 'Price vs Sales']
        )
        
        # Add charts based on available data
        if 'top_models' in summary_data:
            # Bar chart for top models
            models_data = summary_data['top_models'].head(10)
            fig.add_trace(go.Bar(
                x=models_data['total_sales'],
                y=models_data['Genmodel'],
                orientation='h',
                name='Sales',
                marker_color=self.color_palette['primary']
            ), row=1, col=1)
        
        if 'market_share' in summary_data:
            # Pie chart for market share
            share_data = summary_data['market_share'].head(5)
            fig.add_trace(go.Pie(
                labels=share_data['Automaker'],
                values=share_data['market_share_percent'],
                name='Market Share'
            ), row=1, col=2)
        
        if 'price_sales' in summary_data:
            # Scatter plot for price vs sales
            scatter_data = summary_data['price_sales']
            fig.add_trace(go.Scatter(
                x=scatter_data['price_mean'],
                y=scatter_data['total_sales'],
                mode='markers',
                name='Models',
                marker_color=self.color_palette['secondary']
            ), row=1, col=3)
        
        fig.update_layout(
            title=title,
            height=400,
            showlegend=False,
            font=dict(family=self.chart_config['font_family']),
            paper_bgcolor=self.chart_config['paper_bgcolor']
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

    def _apply_standard_layout(self, fig: go.Figure, title: str, 
                             x_title: str = None, y_title: str = None) -> go.Figure:
        """Apply standard layout to a chart."""
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=self.chart_config['title_font_size'], 
                         color=self.chart_config['title_color']),
                x=0.5
            ),
            plot_bgcolor=self.chart_config['plot_bgcolor'],
            paper_bgcolor=self.chart_config['paper_bgcolor'],
            font=dict(family=self.chart_config['font_family']),
            height=self.chart_config['default_height'],
            margin=dict(l=60, r=40, t=80, b=60),
            showlegend=True if len(fig.data) > 1 else False
        )
        
        if x_title:
            fig.update_xaxes(title=x_title, gridcolor='rgba(0, 0, 0, 0.1)')
        
        if y_title:
            fig.update_yaxes(title=y_title, gridcolor='rgba(0, 0, 0, 0.1)')
        
        return fig

    def _get_automaker_colors(self, automakers: Union[pd.Series, List[str]]) -> List[str]:
        """Get colors for automakers."""
        if isinstance(automakers, pd.Series):
            automakers = automakers.tolist()
        
        colors = []
        for automaker in automakers:
            if automaker in self.manufacturer_colors:
                colors.append(self.manufacturer_colors[automaker])
            else:
                # Generate color based on automaker name
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

    # ==================== CHART SELECTION METHODS ====================

    def create_chart_by_type(self, chart_type: str, data: pd.DataFrame, 
                           title: str = None, **kwargs) -> go.Figure:
        """Create a chart based on type string."""
        chart_methods = {
            'sales_bar': self.create_sales_bar_chart,
            'sales_trend': self.create_sales_trend_chart,
            'price_bar': self.create_price_bar_chart,
            'price_distribution': self.create_price_distribution_chart,
            'price_vs_sales': self.create_price_vs_sales_scatter,
            'market_share_pie': self.create_market_share_pie_chart,
            'market_share_bar': self.create_market_share_bar_chart,
            'correlation_heatmap': self.create_correlation_heatmap,
            'clustering_scatter': self.create_clustering_scatter_chart,
            'trend_analysis': self.create_trend_analysis_chart,
            'kpi_gauges': self.create_kpi_gauge_chart,
            'executive_summary': self.create_executive_summary_chart
        }
        
        if chart_type in chart_methods:
            method = chart_methods[chart_type]
            if title:
                kwargs['title'] = title
            return method(data, **kwargs)
        else:
            return self._create_empty_chart(f"Unknown chart type: {chart_type}")

    def get_available_chart_types(self) -> List[str]:
        """Get list of available chart types."""
        return [
            'sales_bar', 'sales_trend', 'price_bar', 'price_distribution',
            'price_vs_sales', 'market_share_pie', 'market_share_bar',
            'correlation_heatmap', 'clustering_scatter', 'trend_analysis',
            'kpi_gauges', 'executive_summary'
        ]

    def get_chart_config(self) -> Dict[str, Any]:
        """Get the current chart configuration."""
        return {
            'chart_config': self.chart_config,
            'color_palette': self.color_palette,
            'coolors_palette': self.coolors_palette,
            'available_charts': self.get_available_chart_types()
        }


# Global instance for use throughout the application
chart_factory = ChartFactory()

