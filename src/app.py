"""
🚗 Car Market Analysis Executive Dashboard - Simple Version

Simplified dashboard that works without complex routing.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Dict, List, Optional, Any
import time
import warnings
warnings.filterwarnings('ignore')

# Import core components
try:
    from business_logic import analyzer
    from components.config.app_config import APP_CONFIG, COLOR_PALETTE
    from components.ui.layout import layout_component
    from components.visualizations.chart_factory import chart_factory
except ImportError as e:
    st.error(f"Error importing components: {str(e)}")
    st.stop()


class SimpleCarMarketApp:
    """
    🏢 Simple Car Market Analysis Application
    
    Streamlined version that focuses on core functionality.
    """

    def __init__(self):
        """Initialize the simple application."""
        self.app_config = APP_CONFIG
        self.analyzer = analyzer
        self.chart_factory = chart_factory
        self.filters = {}

    def setup_application(self) -> None:
        """Setup the application configuration."""
        # Configure Streamlit page
        st.set_page_config(
            page_title=self.app_config.get('title', 'Car Market Analysis Dashboard'),
            page_icon=self.app_config.get('icon', '🚗'),
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Inject custom CSS
        self._inject_custom_css()

    def _inject_custom_css(self) -> None:
        """Inject custom CSS styling."""
        st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #0A9396 0%, #005F73 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
            color: white;
        }
        .main-header h1 {
            font-size: 2.5rem;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .main-header p {
            font-size: 1.2rem;
            margin: 0.5rem 0 0 0;
            opacity: 0.9;
        }
        .metric-card {
            background: linear-gradient(135deg, #005F73 0%, #0A9396 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            margin: 0.5rem 0;
        }
        .metric-label {
            font-size: 1rem;
            opacity: 0.9;
        }
        </style>
        """, unsafe_allow_html=True)

    def render_application(self) -> None:
        """Render the complete application."""
        self.setup_application()
        
        # Render header
        self._render_header()
        
        # Render sidebar
        self._render_sidebar()
        
        # Render main content
        self._render_main_content()

    def _render_header(self) -> None:
        """Render application header."""
        st.markdown(f"""
        <div class="main-header">
            <h1>{self.app_config.get('title', 'Car Market Analysis Dashboard')}</h1>
            <p>Professional market intelligence and analytics platform</p>
        </div>
        """, unsafe_allow_html=True)

    def _render_sidebar(self) -> None:
        """Render sidebar with filters."""
        with st.sidebar:
            st.markdown("## 🔧 Filters")
            
            try:
                # Get automaker list
                automaker_list = sorted(self.analyzer.get_automaker_list())
                
                if automaker_list:
                    # Automaker filter
                    selected_automakers = st.multiselect(
                        'Select Automakers',
                        options=automaker_list,
                        default=automaker_list[:5] if len(automaker_list) >= 5 else automaker_list,
                        key='filter_automakers'
                    )
                    
                    # Top N filter
                    top_n = st.slider(
                        'Top N Results',
                        min_value=5,
                        max_value=50,
                        value=15,
                        step=5,
                        key='filter_top_n'
                    )
                    
                    # Update filters
                    self.filters = {
                        'automakers': selected_automakers,
                        'top_n': top_n
                    }
                else:
                    st.warning("No automaker data available")
                    
            except Exception as e:
                st.error(f"Error loading filter data: {str(e)}")

    def _render_main_content(self) -> None:
        """Render main content."""
        # Dashboard tabs
        tab1, tab2, tab3 = st.tabs(["📊 Executive Summary", "🌍 Market Analysis", "📈 Sales Performance"])
        
        with tab1:
            self._render_executive_summary()
        
        with tab2:
            self._render_market_analysis()
        
        with tab3:
            self._render_sales_performance()

    def _render_executive_summary(self) -> None:
        """Render executive summary dashboard."""
        st.markdown("## 📊 Executive Summary")
        
        try:
            # Get data summaries
            sales_summary = self.analyzer.get_sales_summary()
            price_summary = self.analyzer.get_price_range_by_model()
            
            # Apply filters
            if self.filters.get('automakers'):
                sales_summary = sales_summary[sales_summary['Automaker'].isin(self.filters['automakers'])]
                price_summary = price_summary[price_summary['Automaker'].isin(self.filters['automakers'])]
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">Total Models</div>
                    <div class="metric-value">{}</div>
                </div>
                """.format(len(price_summary)), unsafe_allow_html=True)
            
            with col2:
                total_sales = sales_summary['total_sales'].sum() if not sales_summary.empty else 0
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Total Sales</div>
                    <div class="metric-value">{int(total_sales):,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                avg_price = price_summary['price_mean'].mean() if not price_summary.empty else 0
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Avg Price</div>
                    <div class="metric-value">€{avg_price:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                automakers_count = sales_summary['Automaker'].nunique() if not sales_summary.empty else 0
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Automakers</div>
                    <div class="metric-value">{automakers_count}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Top Models by Sales")
                if not sales_summary.empty:
                    top_sales = sales_summary.nlargest(self.filters.get('top_n', 15), 'total_sales')
                    fig_sales = px.bar(
                        top_sales,
                        x='Genmodel',
                        y='total_sales',
                        color='Automaker',
                        title='Top Models by Sales',
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_sales.update_layout(
                        xaxis_tickangle=-45,
                        height=400,
                        showlegend=True
                    )
                    st.plotly_chart(fig_sales, use_container_width=True)
                else:
                    st.info("No sales data available")
            
            with col2:
                st.subheader("Price Distribution by Automaker")
                if not price_summary.empty:
                    avg_price_by_maker = price_summary.groupby('Automaker')['price_mean'].mean().sort_values(ascending=False)
                    fig_price = px.bar(
                        x=avg_price_by_maker.index,
                        y=avg_price_by_maker.values,
                        title='Average Price by Automaker',
                        color=avg_price_by_maker.values,
                        color_continuous_scale='Viridis'
                    )
                    fig_price.update_layout(
                        xaxis_tickangle=-45,
                        height=400,
                        showlegend=False
                    )
                    st.plotly_chart(fig_price, use_container_width=True)
                else:
                    st.info("No price data available")
            
            # Data table
            st.subheader("Detailed Data")
            if not sales_summary.empty:
                st.dataframe(sales_summary, use_container_width=True)
            else:
                st.info("No data to display")
                
        except Exception as e:
            st.error(f"Error rendering executive summary: {str(e)}")

    def _render_market_analysis(self) -> None:
        """Render market analysis dashboard."""
        st.markdown("## 🌍 Market Analysis")
        
        try:
            # Get market data
            sales_summary = self.analyzer.get_sales_summary()
            price_summary = self.analyzer.get_price_range_by_model()
            
            # Apply filters
            if self.filters.get('automakers'):
                sales_summary = sales_summary[sales_summary['Automaker'].isin(self.filters['automakers'])]
                price_summary = price_summary[price_summary['Automaker'].isin(self.filters['automakers'])]
            
            # Market share analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Market Share by Automaker")
                if not sales_summary.empty:
                    market_share = sales_summary.groupby('Automaker')['total_sales'].sum().sort_values(ascending=False)
                    fig_pie = px.pie(
                        values=market_share.values,
                        names=market_share.index,
                        title='Market Share Distribution'
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("No market data available")
            
            with col2:
                st.subheader("Price Range Analysis")
                if not price_summary.empty:
                    fig_hist = px.histogram(
                        price_summary,
                        x='price_mean',
                        nbins=20,
                        title='Price Distribution',
                        color_discrete_sequence=['#0A9396']
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                else:
                    st.info("No price data available")
            
        except Exception as e:
            st.error(f"Error rendering market analysis: {str(e)}")

    def _render_sales_performance(self) -> None:
        """Render sales performance dashboard."""
        st.markdown("## 📈 Sales Performance")
        
        try:
            # Get sales data
            sales_summary = self.analyzer.get_sales_summary()
            
            # Apply filters
            if self.filters.get('automakers'):
                sales_summary = sales_summary[sales_summary['Automaker'].isin(self.filters['automakers'])]
            
            # Sales trends
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Top Performing Models")
                if not sales_summary.empty:
                    top_models = sales_summary.nlargest(self.filters.get('top_n', 15), 'total_sales')
                    fig_bar = px.bar(
                        top_models,
                        x='total_sales',
                        y='Genmodel',
                        orientation='h',
                        color='Automaker',
                        title='Top Performing Models',
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_bar.update_layout(height=400)
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No sales data available")
            
            with col2:
                st.subheader("Sales by Automaker")
                if not sales_summary.empty:
                    sales_by_maker = sales_summary.groupby('Automaker')['total_sales'].sum().sort_values(ascending=False)
                    fig_scatter = px.scatter(
                        x=sales_by_maker.index,
                        y=sales_by_maker.values,
                        title='Total Sales by Automaker',
                        color=sales_by_maker.values,
                        color_continuous_scale='Viridis',
                        size=sales_by_maker.values
                    )
                    fig_scatter.update_layout(
                        xaxis_tickangle=-45,
                        height=400
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)
                else:
                    st.info("No sales data available")
            
        except Exception as e:
            st.error(f"Error rendering sales performance: {str(e)}")


def main():
    """Main application entry point."""
    try:
        # Create and run the simple application
        app = SimpleCarMarketApp()
        app.render_application()
        
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    main()
