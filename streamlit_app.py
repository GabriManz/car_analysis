"""
🚗 Car Market Analysis Executive Dashboard - Streamlit Cloud Version

Professional dashboard with real data display and comprehensive features.
Optimized for Streamlit Cloud deployment with performance enhancements.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from typing import Dict, List, Optional, Any
import warnings
import sys
import os
from functools import lru_cache

warnings.filterwarnings('ignore')

# Set up page config first
st.set_page_config(
    page_title="Car Market Analysis Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Performance optimization: Cache expensive operations
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_analyzer():
    """Load and initialize the analyzer with caching."""
    try:
        from src.business_logic import analyzer
        return analyzer, None
    except ImportError as e:
        return None, str(e)

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_cached_data(analyzer, data_type: str):
    """Cache frequently used data operations."""
    try:
        if data_type == 'sales_summary':
            return analyzer.get_sales_summary()
        elif data_type == 'price_summary':
            return analyzer.get_price_range_by_model()
        elif data_type == 'automakers':
            return analyzer.get_automaker_list()
        elif data_type == 'price_segments':
            return analyzer.get_price_segments()
        elif data_type == 'sales_by_segment':
            return analyzer.get_sales_by_segment()
        elif data_type == 'sales_data':
            return analyzer.sales
    except Exception as e:
        st.error(f"Error loading {data_type}: {str(e)}")
        return pd.DataFrame()

# Load analyzer with error handling
analyzer, import_error = load_analyzer()

if analyzer is None:
    st.error(f"❌ Error importing business_logic: {import_error}")
    st.error("Please ensure business_logic.py is in the src/ directory.")
    
    # Show current directory structure for debugging
    st.write("**Current directory structure:**")
    for root, dirs, files in os.walk('.'):
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        st.write(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            st.write(f"{subindent}{file}")
    
    st.stop()
else:
    st.success("✅ Business logic loaded successfully")

# Helper functions for data validation and UI
def validate_data_not_empty(df: pd.DataFrame, data_name: str) -> bool:
    """Validate that DataFrame is not empty and show appropriate message."""
    if df.empty:
        st.info(f"No {data_name} data available")
        return False
    return True

def safe_get_data(data_type: str, selected_automakers: List[str] = None) -> pd.DataFrame:
    """Safely get cached data with error handling."""
    try:
        df = get_cached_data(analyzer, data_type)
        if selected_automakers and not df.empty and 'Automaker' in df.columns:
            df = df[df['Automaker'].isin(selected_automakers)]
        return df
    except Exception as e:
        st.error(f"Error loading {data_type}: {str(e)}")
        return pd.DataFrame()

def show_loading_spinner(operation: str):
    """Show loading spinner for long operations."""
    return st.spinner(f"Loading {operation}...")

# Application configuration
APP_CONFIG = {
    'title': 'Car Market Analysis Executive Dashboard',
    'icon': '🚗',
    'version': '2.1.0'
}

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #667eea;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: white;
        margin-bottom: 0.25rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.8);
    }
    
    .section-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    .chart-container {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown(f"""
<div class="main-header">
    {APP_CONFIG['icon']} {APP_CONFIG['title']}
</div>
""", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.markdown("## 🎛️ Dashboard Controls")

# Automaker selection with caching
with show_loading_spinner("automaker list"):
    automakers = get_cached_data(analyzer, 'automakers')

if len(automakers) > 0:
    selected_automakers = st.sidebar.multiselect(
        "Select Automakers",
        options=automakers,
        default=automakers[:5] if len(automakers) >= 5 else automakers,
        help="Select automakers to filter the analysis"
    )
else:
    selected_automakers = []
    st.sidebar.warning("No automaker data available")

# Top N selection
top_n = st.sidebar.slider("Number of Top Models", min_value=5, max_value=50, value=10)

# Performance info
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Data Info")
if not analyzer.basic.empty:
    st.sidebar.metric("Total Models", len(analyzer.basic))
if not analyzer.sales.empty:
    st.sidebar.metric("Sales Years", len([col for col in analyzer.sales.columns if col.isdigit()]))

# Tab navigation
tab1, tab2, tab3 = st.tabs(["📊 Executive Summary", "🌍 Market Analysis", "📈 Sales Performance"])

with tab1:
    st.markdown("## 📊 Executive Summary")
    
    # Get cached data with loading indicators
    with show_loading_spinner("sales data"):
        sales_summary = safe_get_data('sales_summary', selected_automakers)
    
    with show_loading_spinner("price data"):
        price_summary = safe_get_data('price_summary', selected_automakers)
    
    # Key metrics with validation
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_models = len(price_summary) if validate_data_not_empty(price_summary, "price") else 0
        st.metric("Total Models", total_models)
    
    with col2:
        if validate_data_not_empty(sales_summary, "sales"):
            total_sales = sales_summary['total_sales'].sum()
            st.metric("Total Sales", f"{int(total_sales):,}")
        else:
            st.metric("Total Sales", "0")
    
    with col3:
        if validate_data_not_empty(price_summary, "price") and 'price_mean' in price_summary.columns:
            avg_price = price_summary['price_mean'].mean()
            st.metric("Avg Price", f"€{avg_price:,.0f}")
        else:
            st.metric("Avg Price", "€0")
    
    with col4:
        if validate_data_not_empty(sales_summary, "sales"):
            automakers_count = sales_summary['Automaker'].nunique()
            st.metric("Automakers", automakers_count)
        else:
            st.metric("Automakers", "0")
    
    # Simple charts with improved validation
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Models by Sales")
        if validate_data_not_empty(sales_summary, "sales") and 'total_sales' in sales_summary.columns:
            sales_clean = sales_summary.dropna(subset=['total_sales'])
            if not sales_clean.empty:
                top_sales = sales_clean.nlargest(top_n, 'total_sales')
                fig = px.bar(top_sales, x='Genmodel', y='total_sales', title='')
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No valid sales data available")
    
    with col2:
        st.subheader("Average Price by Automaker")
        if validate_data_not_empty(price_summary, "price") and 'price_mean' in price_summary.columns:
            price_clean = price_summary.dropna(subset=['price_mean'])
            if not price_clean.empty:
                avg_price_by_maker = price_clean.groupby('Automaker')['price_mean'].mean().sort_values(ascending=False).head(10)
                fig = px.bar(x=avg_price_by_maker.index, y=avg_price_by_maker.values, title='')
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No valid price data available")
        
    # Treemap section with caching
    st.subheader("📊 Sales Volume by Market Segment")
    with show_loading_spinner("market segmentation"):
        sales_by_segment_data = safe_get_data('sales_by_segment')
    
    if validate_data_not_empty(sales_by_segment_data, "sales by segment"):
        try:
            fig_treemap = px.treemap(
                sales_by_segment_data,
                path=[px.Constant("All Segments"), 'Price_Segment'],
                values='total_sales',
                color='Price_Segment',
                title='Contribution of Each Price Segment to Total Sales',
                color_discrete_map={
                    'Budget': '#2a9d8f',
                    'Mid-Range': '#e9c46a',
                    'Premium': '#f4a261',
                    'Luxury': '#e76f51'
                }
            )
            st.plotly_chart(fig_treemap, use_container_width=True)
            
            # Segment statistics
            total_sales_all = sales_by_segment_data['total_sales'].sum()
            st.write("**Segment Contribution:**")
            for _, row in sales_by_segment_data.iterrows():
                percentage = (row['total_sales'] / total_sales_all) * 100
                st.write(f"- **{row['Price_Segment']}**: {row['total_sales']:,.0f} units ({percentage:.1f}%)")
        except Exception as e:
            st.error(f"Error rendering treemap: {str(e)}")

with tab2:
    st.markdown("## 🌍 Market Analysis")
    
    # Get cached data
    sales_summary = safe_get_data('sales_summary', selected_automakers)
    price_summary = safe_get_data('price_summary', selected_automakers)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Market Share by Automaker")
        if validate_data_not_empty(sales_summary, "sales") and 'total_sales' in sales_summary.columns:
            sales_clean = sales_summary.dropna(subset=['total_sales'])
            if not sales_clean.empty:
                market_share = sales_clean.groupby('Automaker')['total_sales'].sum().sort_values(ascending=False)
                market_share_top10 = market_share.head(10)
                fig = px.pie(values=market_share_top10.values, names=market_share_top10.index, title='')
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Price Distribution")
        if validate_data_not_empty(price_summary, "price") and 'price_mean' in price_summary.columns:
            price_clean = price_summary.dropna(subset=['price_mean'])
            if not price_clean.empty:
                fig = px.histogram(price_clean, x='price_mean', title='', nbins=50)
                st.plotly_chart(fig, use_container_width=True)
        
    # Market segmentation with caching
    st.subheader("Market Positioning by Price Segment")
    with show_loading_spinner("price segmentation"):
        segmented_data = safe_get_data('price_segments')
    
    if validate_data_not_empty(segmented_data, "price segments") and 'Price_Segment' in segmented_data.columns:
        try:
            segment_counts = segmented_data.groupby(['Automaker', 'Price_Segment']).size().reset_index(name='Model_Count')
            top_automakers = segmented_data['Automaker'].value_counts().nlargest(20).index
            segment_counts_top = segment_counts[segment_counts['Automaker'].isin(top_automakers)]
            
            fig_segment = px.bar(
                segment_counts_top,
                x='Automaker',
                y='Model_Count',
                color='Price_Segment',
                title='Number of Models per Automaker by Price Segment',
                color_discrete_map={
                    'Budget': '#2a9d8f',
                    'Mid-Range': '#e9c46a',
                    'Premium': '#f4a261',
                    'Luxury': '#e76f51'
                }
            )
            st.plotly_chart(fig_segment, use_container_width=True)
        except Exception as e:
            st.error(f"Error rendering market segmentation: {str(e)}")

with tab3:
    st.markdown("## 📈 Sales Performance")
    
    # Get cached data
    sales_summary = safe_get_data('sales_summary', selected_automakers)
    
    # Sales trends with caching
    st.subheader("Sales Trend by Automaker")
    
    with show_loading_spinner("sales trend data"):
        sales_data = safe_get_data('sales_data')
    
    if validate_data_not_empty(sales_data, "sales trend"):
        try:
            year_columns = [col for col in sales_data.columns if col.isdigit()]
            if year_columns:
                sales_long = pd.melt(
                    sales_data,
                    id_vars=['Automaker', 'Genmodel', 'Genmodel_ID'],
                    value_vars=year_columns,
                    var_name='Year',
                    value_name='Sales_Volume'
                )
                
                if selected_automakers:
                    sales_long = sales_long[sales_long['Automaker'].isin(selected_automakers)]
                
                yearly_sales_by_automaker = sales_long.groupby(['Year', 'Automaker'])['Sales_Volume'].sum().reset_index()
                yearly_sales_by_automaker['Year'] = pd.to_numeric(yearly_sales_by_automaker['Year'])
                
                # Limit to top automakers for better visualization
                top_automakers_trend = yearly_sales_by_automaker.groupby('Automaker')['Sales_Volume'].sum().nlargest(8).index
                yearly_sales_filtered = yearly_sales_by_automaker[yearly_sales_by_automaker['Automaker'].isin(top_automakers_trend)]
                
                fig_trend = px.line(
                    yearly_sales_filtered,
                    x='Year',
                    y='Sales_Volume',
                    color='Automaker',
                    title='Sales Volume Trend by Top Automakers (2001-2020)',
                    markers=True
                )
                st.plotly_chart(fig_trend, use_container_width=True)
            else:
                st.info("No yearly sales data available to display trend.")
        except Exception as e:
            st.error(f"Error rendering sales trends: {str(e)}")
        
    # Top models section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Performing Models")
        if validate_data_not_empty(sales_summary, "sales") and 'total_sales' in sales_summary.columns:
            sales_clean = sales_summary.dropna(subset=['total_sales'])
            if not sales_clean.empty:
                top_models = sales_clean.nlargest(top_n, 'total_sales')
                fig = px.bar(top_models, x='total_sales', y='Genmodel', orientation='h', title='')
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Sales Distribution")
        if validate_data_not_empty(sales_summary, "sales") and 'total_sales' in sales_summary.columns:
            sales_clean = sales_summary.dropna(subset=['total_sales'])
            if not sales_clean.empty:
                fig = px.histogram(sales_clean, x='total_sales', title='', nbins=30)
                st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    {APP_CONFIG['icon']} {APP_CONFIG['title']} v{APP_CONFIG['version']}<br>
    Professional Automotive Market Analysis Dashboard
</div>
""", unsafe_allow_html=True)
