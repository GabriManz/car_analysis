"""
🚗 Car Market Analysis Executive Dashboard - Working Version

Professional dashboard with real data display and comprehensive features.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Dict, List, Optional, Any
import warnings
warnings.filterwarnings('ignore')

# Import core components
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.business_logic import analyzer
except ImportError:
    try:
        from business_logic import analyzer
    except ImportError:
        # Fallback for Streamlit Cloud
        import importlib.util
        spec = importlib.util.spec_from_file_location("business_logic", "src/business_logic.py")
        business_logic = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(business_logic)
        analyzer = business_logic.analyzer

# Application configuration
APP_CONFIG = {
    'title': 'Car Market Analysis Executive Dashboard',
    'icon': '🚗',
    'version': '2.0.0'
}

st.set_page_config(
    page_title=APP_CONFIG['title'],
    page_icon=APP_CONFIG['icon'],
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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

def main():
    """Main application."""
    
    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>{APP_CONFIG['title']}</h1>
        <p>Professional market intelligence and analytics platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar filters
    with st.sidebar:
        st.markdown("## 🔧 Filters")
        
        # Get automaker list
        automaker_list = analyzer.get_automaker_list()
        
        if automaker_list:
            selected_automakers = st.multiselect(
                'Select Automakers (leave empty to show all)',
                options=automaker_list,
                default=[],
                key='filter_automakers'
            )
            
            top_n = st.slider(
                'Top N Results',
                min_value=5,
                max_value=50,
                value=15,
                step=5,
                key='filter_top_n'
            )
        else:
            st.warning("No automaker data available")
            selected_automakers = []
            top_n = 15
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📊 Executive Summary", "🌍 Market Analysis", "📈 Sales Performance"])
    
    with tab1:
        render_executive_summary(selected_automakers, top_n)
    
    with tab2:
        render_market_analysis(selected_automakers)
    
    with tab3:
        render_sales_performance(selected_automakers, top_n)

def render_executive_summary(selected_automakers, top_n):
    """Render executive summary dashboard."""
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
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Models</div>
                <div class="metric-value">{total_models}</div>
            </div>
            """, unsafe_allow_html=True)
        
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
                # Remove NaN values for chart
                sales_clean = sales_summary.dropna(subset=['total_sales'])
                if not sales_clean.empty:
                    top_sales = sales_clean.nlargest(top_n, 'total_sales')
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
                    st.info("No valid sales data available")
            else:
                st.info("No sales data available")
        
        with col2:
            st.subheader("Price Distribution by Automaker")
            if not price_summary.empty:
                # Remove NaN values for chart
                price_clean = price_summary.dropna(subset=['price_mean'])
                if not price_clean.empty:
                    avg_price_by_maker = price_clean.groupby('Automaker')['price_mean'].mean().sort_values(ascending=False)
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
                    st.info("No valid price data available")
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
        import traceback
        st.code(traceback.format_exc())

def render_market_analysis(selected_automakers):
    """Render market analysis dashboard."""
    st.markdown("## 🌍 Market Analysis")
    
    try:
        # Get data
        sales_summary = analyzer.get_sales_summary()
        price_summary = analyzer.get_price_range_by_model()
        
        # Apply filters
        if selected_automakers:
            sales_summary = sales_summary[sales_summary['Automaker'].isin(selected_automakers)]
            price_summary = price_summary[price_summary['Automaker'].isin(selected_automakers)]
        
        # Market share analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Market Share by Automaker")
            if not sales_summary.empty:
                sales_clean = sales_summary.dropna(subset=['total_sales'])
                if not sales_clean.empty:
                    market_share = sales_clean.groupby('Automaker')['total_sales'].sum().sort_values(ascending=False)
                    fig_pie = px.pie(
                        values=market_share.values,
                        names=market_share.index,
                        title='Market Share Distribution'
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("No valid market data available")
            else:
                st.info("No market data available")
        
        with col2:
            st.subheader("Price Range Analysis")
            if not price_summary.empty:
                price_clean = price_summary.dropna(subset=['price_mean'])
                if not price_clean.empty:
                    fig_hist = px.histogram(
                        price_clean,
                        x='price_mean',
                        nbins=20,
                        title='Price Distribution',
                        color_discrete_sequence=['#0A9396']
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                else:
                    st.info("No valid price data available")
            else:
                st.info("No price data available")
            
    except Exception as e:
        st.error(f"Error rendering market analysis: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

def render_sales_performance(selected_automakers, top_n):
    """Render sales performance dashboard."""
    st.markdown("## 📈 Sales Performance")
    
    try:
        # Get data
        sales_summary = analyzer.get_sales_summary()
        
        # Apply filters
        if selected_automakers:
            sales_summary = sales_summary[sales_summary['Automaker'].isin(selected_automakers)]
        
        # Sales trends
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Performing Models")
            if not sales_summary.empty:
                sales_clean = sales_summary.dropna(subset=['total_sales'])
                if not sales_clean.empty:
                    top_models = sales_clean.nlargest(top_n, 'total_sales')
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
                    st.info("No valid sales data available")
            else:
                st.info("No sales data available")
        
        with col2:
            st.subheader("Sales by Automaker")
            if not sales_summary.empty:
                sales_clean = sales_summary.dropna(subset=['total_sales'])
                if not sales_clean.empty:
                    sales_by_maker = sales_clean.groupby('Automaker')['total_sales'].sum().sort_values(ascending=False)
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
                    st.info("No valid sales data available")
            else:
                st.info("No sales data available")
            
    except Exception as e:
        st.error(f"Error rendering sales performance: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

if __name__ == "__main__":
    main()