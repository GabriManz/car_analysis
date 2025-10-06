"""
🚗 Car Market Analysis Executive Dashboard - Streamlit Cloud Version

Professional dashboard with real data display and comprehensive features.
Optimized for Streamlit Cloud deployment.
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

# Import business logic with error handling
try:
    from src.business_logic import analyzer
    st.success("✅ Business logic loaded successfully")
except ImportError as e:
    st.error(f"❌ Error importing business_logic: {e}")
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

# Automaker selection
try:
    automakers = analyzer.basic['Automaker'].unique() if not analyzer.basic.empty else []
    if len(automakers) > 0:
        selected_automakers = st.sidebar.multiselect(
            "Select Automakers",
            options=automakers,
            default=automakers[:5] if len(automakers) >= 5 else automakers
        )
    else:
        selected_automakers = []
        st.sidebar.warning("No automaker data available")
except Exception as e:
    st.sidebar.error(f"Error loading automakers: {e}")
    selected_automakers = []

# Top N selection
top_n = st.sidebar.slider("Number of Top Models", min_value=5, max_value=50, value=10)

# Tab navigation
tab1, tab2, tab3 = st.tabs(["📊 Executive Summary", "🌍 Market Analysis", "📈 Sales Performance"])

with tab1:
    st.markdown("## 📊 Executive Summary")
    
    try:
        # Get data
        sales_summary = analyzer.get_sales_summary()
        price_summary = analyzer.get_price_range_by_model()
        
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
        
        # Treemap section
        st.subheader("📊 Sales Volume by Market Segment")
        try:
            sales_by_segment_data = analyzer.get_sales_by_segment()
            if not sales_by_segment_data.empty:
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
            else:
                st.info("Sales by segment data is not available.")
        except Exception as e:
            st.error(f"Error rendering treemap: {str(e)}")
    
    except Exception as e:
        st.error(f"Error in Executive Summary: {str(e)}")

with tab2:
    st.markdown("## 🌍 Market Analysis")
    
    try:
        # Get data
        sales_summary = analyzer.get_sales_summary()
        price_summary = analyzer.get_price_range_by_model()
        
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
        
        # Market segmentation
        st.subheader("Market Positioning by Price Segment")
        try:
            segmented_data = analyzer.get_price_segments()
            if not segmented_data.empty and 'Price_Segment' in segmented_data.columns:
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
            else:
                st.info("Price segmentation data is not available.")
        except Exception as e:
            st.error(f"Error rendering market segmentation: {str(e)}")
    
    except Exception as e:
        st.error(f"Error in Market Analysis: {str(e)}")

with tab3:
    st.markdown("## 📈 Sales Performance")
    
    try:
        # Get data
        sales_summary = analyzer.get_sales_summary()
        
        # Apply filters
        if selected_automakers:
            sales_summary = sales_summary[sales_summary['Automaker'].isin(selected_automakers)]
        
        # Sales trends
        st.subheader("Sales Trend by Automaker")
        
        try:
            sales_data = analyzer.sales
            if not sales_data.empty:
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
                    
                    fig_trend = px.line(
                        yearly_sales_by_automaker,
                        x='Year',
                        y='Sales_Volume',
                        color='Automaker',
                        title='Sales Volume Trend by Automaker (2001-2020)',
                        markers=True
                    )
                    st.plotly_chart(fig_trend, use_container_width=True)
                else:
                    st.info("No yearly sales data available to display trend.")
            else:
                st.info("No sales data available for trend analysis.")
        except Exception as e:
            st.error(f"Error rendering sales trends: {str(e)}")
        
        # Top models
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
