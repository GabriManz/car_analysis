"""
🚗 Car Market Analysis Executive Dashboard - Streamlit Cloud Optimized Version

Optimized for Streamlit Cloud deployment with memory and performance optimizations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from typing import Dict, List, Optional, Any
import warnings
import sys
import os

warnings.filterwarnings('ignore')

# Set up page config first
st.set_page_config(
    page_title="Car Market Analysis Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# Import business logic with error handling
try:
    from business_logic import analyzer
    st.success("✅ Business logic loaded successfully")
except ImportError as e:
    st.error(f"❌ Error importing business_logic: {e}")
    st.error("Please ensure business_logic.py is in the src/ directory.")
    st.stop()

# Application configuration
APP_CONFIG = {
    'title': 'Car Market Analysis Executive Dashboard',
    'icon': '🚗',
    'version': '2.0.0'
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
@st.cache_data
def get_automaker_list():
    try:
        return analyzer.get_automaker_list()
    except:
        return []

automakers = get_automaker_list()
if len(automakers) > 0:
    selected_automakers = st.sidebar.multiselect(
        "Select Automakers",
        options=automakers,
        default=automakers[:5] if len(automakers) >= 5 else automakers
    )
else:
    selected_automakers = []
    st.sidebar.warning("No automaker data available")

# Top N selection
top_n = st.sidebar.slider("Number of Top Models", min_value=5, max_value=20, value=10)

# Tab navigation
tab1, tab2, tab3 = st.tabs(["📊 Executive Summary", "🌍 Market Analysis", "📈 Sales Performance"])

with tab1:
    st.markdown("## 📊 Executive Summary")
    
    try:
        # Get data with caching
        @st.cache_data
        def get_cached_data():
            sales_summary = analyzer.get_sales_summary()
            price_summary = analyzer.get_price_range_by_model()
            return sales_summary, price_summary
        
        sales_summary, price_summary = get_cached_data()
        
        # Apply filters
        if selected_automakers:
            sales_summary = sales_summary[sales_summary['Automaker'].isin(selected_automakers)]
            price_summary = price_summary[price_summary['Automaker'].isin(selected_automakers)]
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_models = len(price_summary)
            st.metric("Total Models", total_models)
        
        with col2:
            total_sales = sales_summary['total_sales'].sum() if not sales_summary.empty else 0
            st.metric("Total Sales", f"{int(total_sales):,}")
        
        with col3:
            avg_price = price_summary['price_mean'].mean() if not price_summary.empty else 0
            st.metric("Avg Price", f"€{avg_price:,.0f}")
        
        with col4:
            automakers_count = sales_summary['Automaker'].nunique() if not sales_summary.empty else 0
            st.metric("Automakers", automakers_count)
        
        # Simple charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Models by Sales")
            if not sales_summary.empty:
                sales_clean = sales_summary.dropna(subset=['total_sales'])
                if not sales_clean.empty:
                    top_sales = sales_clean.nlargest(top_n, 'total_sales')
                    fig = px.bar(top_sales, x='Genmodel', y='total_sales', title='')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No sales data available")
            else:
                st.info("No sales data available")
        
        with col2:
            st.subheader("Average Price by Automaker")
            if not price_summary.empty:
                price_clean = price_summary.dropna(subset=['price_mean'])
                if not price_clean.empty:
                    avg_price_by_maker = price_clean.groupby('Automaker')['price_mean'].mean().sort_values(ascending=False)
                    fig = px.bar(x=avg_price_by_maker.index, y=avg_price_by_maker.values, title='')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No price data available")
            else:
                st.info("No price data available")
    
    except Exception as e:
        st.error(f"Error in Executive Summary: {str(e)}")

with tab2:
    st.markdown("## 🌍 Market Analysis")
    
    try:
        # Get cached data
        @st.cache_data
        def get_cached_market_data():
            sales_summary = analyzer.get_sales_summary()
            price_summary = analyzer.get_price_range_by_model()
            return sales_summary, price_summary
        
        sales_summary, price_summary = get_cached_market_data()
        
        # Apply filters
        if selected_automakers:
            sales_summary = sales_summary[sales_summary['Automaker'].isin(selected_automakers)]
            price_summary = price_summary[price_summary['Automaker'].isin(selected_automakers)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Market Share by Automaker")
            if not sales_summary.empty:
                sales_clean = sales_summary.dropna(subset=['total_sales'])
                if not sales_clean.empty:
                    market_share = sales_clean.groupby('Automaker')['total_sales'].sum().sort_values(ascending=False)
                    market_share_top10 = market_share.head(10)
                    fig = px.pie(values=market_share_top10.values, names=market_share_top10.index, title='')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No market data available")
            else:
                st.info("No market data available")
        
        with col2:
            st.subheader("Price Distribution")
            if not price_summary.empty:
                price_clean = price_summary.dropna(subset=['price_mean'])
                if not price_clean.empty:
                    fig = px.histogram(price_clean, x='price_mean', title='', nbins=50)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No price data available")
            else:
                st.info("No price data available")
    
    except Exception as e:
        st.error(f"Error in Market Analysis: {str(e)}")

with tab3:
    st.markdown("## 📈 Sales Performance")
    
    try:
        # Get cached data
        @st.cache_data
        def get_cached_sales_data():
            return analyzer.get_sales_summary()
        
        sales_summary = get_cached_sales_data()
        
        # Apply filters
        if selected_automakers:
            sales_summary = sales_summary[sales_summary['Automaker'].isin(selected_automakers)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Performing Models")
            if not sales_summary.empty:
                sales_clean = sales_summary.dropna(subset=['total_sales'])
                if not sales_clean.empty:
                    top_models = sales_clean.nlargest(top_n, 'total_sales')
                    fig = px.bar(top_models, x='total_sales', y='Genmodel', orientation='h', title='')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No valid sales data available")
            else:
                st.info("No sales data available")
        
        with col2:
            st.subheader("Sales Distribution")
            if not sales_summary.empty:
                sales_clean = sales_summary.dropna(subset=['total_sales'])
                if not sales_clean.empty:
                    fig = px.histogram(sales_clean, x='total_sales', title='', nbins=30)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No sales data available")
            else:
                st.info("No sales data available")
    
    except Exception as e:
        st.error(f"Error in Sales Performance: {str(e)}")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    {APP_CONFIG['icon']} {APP_CONFIG['title']} v{APP_CONFIG['version']}<br>
    Professional Automotive Market Analysis Dashboard
</div>
""", unsafe_allow_html=True)
