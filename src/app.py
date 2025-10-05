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
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2.5rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.main-header::before {
    content: "🚗";
    position: absolute;
    top: 20px;
    right: 30px;
    font-size: 4rem;
    opacity: 0.3;
    z-index: 1;
}
.main-header h1 {
    font-size: 3rem;
    margin: 0;
    text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
    font-weight: 700;
    position: relative;
    z-index: 2;
}
.main-header p {
    font-size: 1.3rem;
    margin: 0.5rem 0 0 0;
    opacity: 0.95;
    position: relative;
    z-index: 2;
    font-weight: 300;
}
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    border: 1px solid rgba(255,255,255,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    position: relative;
    overflow: hidden;
}
.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);
}
.metric-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
    pointer-events: none;
}
.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 1rem 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    position: relative;
    z-index: 1;
}
.metric-label {
    font-size: 1.1rem;
    opacity: 0.9;
    font-weight: 500;
    position: relative;
    z-index: 1;
}
.metric-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 1;
}
.section-header {
    background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 10px;
    margin: 2rem 0 1rem 0;
    font-size: 1.5rem;
    font-weight: 600;
    text-align: center;
    box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
}
.chart-container {
    background: rgba(255,255,255,0.05);
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
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
        try:
            automaker_list = analyzer.get_automaker_list()
        except Exception as e:
            st.error(f"Error getting automaker list: {e}")
            automaker_list = []
        
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
        
        # Key metrics - Row 1
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            total_models = len(price_summary)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🚗</div>
                <div class="metric-value">{total_models}</div>
                <div class="metric-label">Total Models</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_sales = sales_summary['total_sales'].sum() if not sales_summary.empty else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">📈</div>
                <div class="metric-value">{int(total_sales):,}</div>
                <div class="metric-label">Total Sales</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_price = price_summary['price_mean'].mean() if not price_summary.empty else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">💰</div>
                <div class="metric-value">€{avg_price:,.0f}</div>
                <div class="metric-label">Avg Price</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            automakers_count = sales_summary['Automaker'].nunique() if not sales_summary.empty else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🏭</div>
                <div class="metric-value">{automakers_count}</div>
                <div class="metric-label">Automakers</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            # Market share of top automaker
            if not sales_summary.empty:
                top_automaker_sales = sales_summary.groupby('Automaker')['total_sales'].sum().max()
                total_sales_all = sales_summary['total_sales'].sum()
                market_share_top = (top_automaker_sales / total_sales_all * 100) if total_sales_all > 0 else 0
            else:
                market_share_top = 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">👑</div>
                <div class="metric-value">{market_share_top:.1f}%</div>
                <div class="metric-label">Top Market Share</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col6:
            # Price range
            if not price_summary.empty:
                price_range = price_summary['price_mean'].max() - price_summary['price_mean'].min()
            else:
                price_range = 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">📊</div>
                <div class="metric-value">€{price_range:,.0f}</div>
                <div class="metric-label">Price Range</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts
        st.markdown('<div class="section-header">📊 Sales Performance Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("🚗 Top Models by Sales")
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
                        title='',
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        template="plotly_dark"
                    )
                    fig_sales.update_layout(
                        xaxis_tickangle=-45,
                        height=450,
                        showlegend=True,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        title_font_size=16
                    )
                    st.plotly_chart(fig_sales, use_container_width=True)
                else:
                    st.info("No valid sales data available")
            else:
                st.info("No sales data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("💰 Average Price by Automaker")
            if not price_summary.empty:
                # Remove NaN values for chart
                price_clean = price_summary.dropna(subset=['price_mean'])
                if not price_clean.empty:
                    avg_price_by_maker = price_clean.groupby('Automaker')['price_mean'].mean().sort_values(ascending=False)
                    fig_price = px.bar(
                        x=avg_price_by_maker.index,
                        y=avg_price_by_maker.values,
                        title='',
                        color=avg_price_by_maker.values,
                        color_continuous_scale='Viridis',
                        template="plotly_dark"
                    )
                    fig_price.update_layout(
                        xaxis_tickangle=-45,
                        height=450,
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        title_font_size=16
                    )
                    st.plotly_chart(fig_price, use_container_width=True)
                else:
                    st.info("No valid price data available")
            else:
                st.info("No price data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
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
        st.markdown('<div class="section-header">🌍 Market Share & Distribution Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("🥧 Market Share by Automaker")
            if not sales_summary.empty:
                sales_clean = sales_summary.dropna(subset=['total_sales'])
                if not sales_clean.empty:
                    market_share = sales_clean.groupby('Automaker')['total_sales'].sum().sort_values(ascending=False)
                    # Show top 10 automakers
                    market_share_top10 = market_share.head(10)
                    fig_pie = px.pie(
                        values=market_share_top10.values,
                        names=market_share_top10.index,
                        title='',
                        template="plotly_dark",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_pie.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=450
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("No valid market data available")
            else:
                st.info("No market data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📊 Price Distribution Analysis")
            if not price_summary.empty:
                price_clean = price_summary.dropna(subset=['price_mean'])
                if not price_clean.empty:
                    fig_hist = px.histogram(
                        price_clean,
                        x='price_mean',
                        nbins=25,
                        title='',
                        template="plotly_dark",
                        color_discrete_sequence=['#667eea']
                    )
                    fig_hist.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=450,
                        xaxis_title="Price (€)",
                        yaxis_title="Number of Models"
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                else:
                    st.info("No valid price data available")
            else:
                st.info("No price data available")
            st.markdown('</div>', unsafe_allow_html=True)
            
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
        st.markdown('<div class="section-header">📈 Advanced Sales Performance Analytics</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("🏆 Top Performing Models")
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
                        title='',
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        template="plotly_dark"
                    )
                    fig_bar.update_layout(
                        height=450,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        xaxis_title="Total Sales",
                        yaxis_title="Model"
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No valid sales data available")
            else:
                st.info("No sales data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("🎯 Sales Performance by Automaker")
            if not sales_summary.empty:
                sales_clean = sales_summary.dropna(subset=['total_sales'])
                if not sales_clean.empty:
                    sales_by_maker = sales_clean.groupby('Automaker')['total_sales'].sum().sort_values(ascending=False).head(15)
                    fig_scatter = px.scatter(
                        x=sales_by_maker.index,
                        y=sales_by_maker.values,
                        title='',
                        color=sales_by_maker.values,
                        color_continuous_scale='plasma',
                        size=sales_by_maker.values,
                        template="plotly_dark"
                    )
                    fig_scatter.update_layout(
                        xaxis_tickangle=-45,
                        height=450,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        xaxis_title="Automaker",
                        yaxis_title="Total Sales"
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)
                else:
                    st.info("No valid sales data available")
            else:
                st.info("No sales data available")
            st.markdown('</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error rendering sales performance: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

if __name__ == "__main__":
    main()