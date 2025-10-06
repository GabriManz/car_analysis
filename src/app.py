"""
🚗 Car Market Analysis Executive Dashboard - Working Version

Professional dashboard with real data display and comprehensive features.
"""

import streamlit as st
import pandas as pd
import numpy as np
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
        
        st.markdown("---")  # Separador visual
        
        # --- NUEVA SECCIÓN PARA EL TREEMAP ---
        st.subheader("📊 Sales Volume by Market Segment")
        try:
            sales_by_segment_data = analyzer.get_sales_by_segment()
            if not sales_by_segment_data.empty:
                # Crear el Treemap
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
                        'Luxury': '#e76f51',
                        '(?)': '#a9a9a9'  # Color para el total
                    },
                    template="plotly_dark"
                )
                fig_treemap.update_layout(
                    margin=dict(t=50, l=25, r=25, b=25),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=500
                )
                st.plotly_chart(fig_treemap, use_container_width=True)
                
                # Añadir información contextual sobre el Treemap
                st.markdown("""
                **📊 Market Segment Analysis:**
                - **Size of rectangles**: Represents total sales volume for each segment
                - **Color coding**: Consistent with market segmentation visualization
                - **Market dominance**: Larger segments drive the majority of sales volume
                """)
                
                # Mostrar estadísticas del Treemap
                total_sales_all_segments = sales_by_segment_data['total_sales'].sum()
                st.markdown("**🎯 Segment Contribution:**")
                for _, row in sales_by_segment_data.iterrows():
                    percentage = (row['total_sales'] / total_sales_all_segments) * 100
                    st.markdown(f"- **{row['Price_Segment']}**: {row['total_sales']:,.0f} units ({percentage:.1f}%)")
            else:
                st.info("Sales by segment data is not available.")
        except Exception as e:
            st.error(f"Error rendering sales by segment treemap: {str(e)}")
        # ------------------------------------
        
        # Additional Charts Section
        st.markdown('<div class="section-header">🔍 Advanced Analytics</div>', unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("💹 Price vs Sales Correlation")
            if not sales_summary.empty and not price_summary.empty:
                # Merge sales and price data for correlation analysis
                correlation_data = sales_summary.merge(
                    price_summary[['Genmodel', 'price_mean']], 
                    on='Genmodel', 
                    how='inner'
                ).dropna(subset=['total_sales', 'price_mean'])
                
                if not correlation_data.empty:
                    fig_scatter = px.scatter(
                        correlation_data,
                        x='price_mean',
                        y='total_sales',
                        color='Automaker',
                        size='total_sales',
                        title='',
                        template="plotly_dark",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_scatter.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=450,
                        xaxis_title="Average Price (€)",
                        yaxis_title="Total Sales"
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)
                else:
                    st.info("No correlation data available")
            else:
                st.info("No data available for correlation analysis")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📊 Price Distribution by Category")
            if not price_summary.empty:
                # Create price categories
                price_clean = price_summary.dropna(subset=['price_mean'])
                if not price_clean.empty:
                    # Define price categories
                    price_clean_copy = price_clean.copy()
                    price_clean_copy['Price Category'] = pd.cut(
                        price_clean_copy['price_mean'],
                        bins=[0, 20000, 40000, 60000, 100000, float('inf')],
                        labels=['Budget (<€20K)', 'Mid-range (€20K-€40K)', 'Premium (€40K-€60K)', 'Luxury (€60K-€100K)', 'Super Luxury (>€100K)']
                    )
                    
                    category_counts = price_clean_copy['Price Category'].value_counts()
                    
                    fig_pie = px.pie(
                        values=category_counts.values,
                        names=category_counts.index,
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
                    st.info("No price data available")
            else:
                st.info("No price data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Third Row - Box Plot and Heatmap
        col5, col6 = st.columns(2)
        
        with col5:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📦 Price Distribution by Automaker")
            if not price_summary.empty:
                price_clean = price_summary.dropna(subset=['price_mean'])
                if not price_clean.empty:
                    # Get top 10 automakers by model count
                    top_automakers = price_clean['Automaker'].value_counts().head(10).index
                    price_filtered = price_clean[price_clean['Automaker'].isin(top_automakers)]
                    
                    fig_box = px.box(
                        price_filtered,
                        x='Automaker',
                        y='price_mean',
                        title='',
                        template="plotly_dark",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_box.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=450,
                        xaxis_tickangle=-45,
                        xaxis_title="Automaker",
                        yaxis_title="Price (€)"
                    )
                    st.plotly_chart(fig_box, use_container_width=True)
                else:
                    st.info("No price data available")
            else:
                st.info("No price data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col6:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("🔥 Sales Heatmap by Year")
            if not sales_summary.empty:
                # Create a correlation matrix for sales data
                sales_numeric = sales_summary.select_dtypes(include=[np.number])
                if not sales_numeric.empty and len(sales_numeric.columns) > 1:
                    correlation_matrix = sales_numeric.corr()
                    
                    fig_heatmap = px.imshow(
                        correlation_matrix,
                        title='',
                        template="plotly_dark",
                        color_continuous_scale='RdBu',
                        aspect="auto"
                    )
                    fig_heatmap.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=450,
                        xaxis_title="Variables",
                        yaxis_title="Variables"
                    )
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                else:
                    st.info("Insufficient numeric data for heatmap")
            else:
                st.info("No sales data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Data table
        st.subheader("📋 Detailed Data")
        if not sales_summary.empty:
            st.dataframe(
                sales_summary.style.format(
                    {
                        'price_mean': "€{:,.0f}",
                        'price_min': "€{:,.0f}",
                        'price_max': "€{:,.0f}",
                        'total_sales': "{:,.0f}",
                        'avg_sales': "{:,.1f}"
                    },
                    na_rep="N/A"
                ),
                use_container_width=True
            )
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
        
        # Additional Market Analytics
        st.markdown('<div class="section-header">📈 Market Trends & Analytics</div>', unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📊 Market Share vs Average Price")
            if not sales_summary.empty and not price_summary.empty:
                # Calculate market share by automaker
                market_share = sales_summary.groupby('Automaker')['total_sales'].sum()
                total_sales_all = market_share.sum()
                market_share_pct = (market_share / total_sales_all * 100).head(10)
                
                # Get average prices by automaker
                avg_prices = price_summary.groupby('Automaker')['price_mean'].mean()
                
                # Merge data
                market_analysis = pd.DataFrame({
                    'Market Share (%)': market_share_pct,
                    'Avg Price (€)': avg_prices
                }).dropna()
                
                if not market_analysis.empty:
                    fig_bubble = px.scatter(
                        market_analysis,
                        x='Avg Price (€)',
                        y='Market Share (%)',
                        size='Market Share (%)',
                        color='Market Share (%)',
                        title='',
                        template="plotly_dark",
                        color_continuous_scale='Viridis',
                        hover_data={'Market Share (%)': ':.1f', 'Avg Price (€)': ':,.0f'}
                    )
                    fig_bubble.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=450,
                        xaxis_title="Average Price (€)",
                        yaxis_title="Market Share (%)"
                    )
                    st.plotly_chart(fig_bubble, use_container_width=True)
                else:
                    st.info("No market analysis data available")
            else:
                st.info("No market data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📉 Price Range Distribution")
            if not price_summary.empty:
                price_clean = price_summary.dropna(subset=['price_mean'])
                if not price_clean.empty:
                    # Create price bins for histogram
                    fig_hist = px.histogram(
                        price_clean,
                        x='price_mean',
                        nbins=30,
                        title='',
                        template="plotly_dark",
                        color_discrete_sequence=['#667eea'],
                        marginal="box"
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
                    st.info("No price data available")
            else:
                st.info("No price data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Market Positioning by Price Segment
        st.markdown("---")  # Separador visual
        st.subheader("Market Positioning by Price Segment")

        try:
            # Obtener datos segmentados desde la lógica de negocio
            segmented_data = analyzer.get_price_segments()

            if not segmented_data.empty and 'Price_Segment' in segmented_data.columns:
                # Contar modelos por fabricante y segmento
                segment_counts = segmented_data.groupby(['Automaker', 'Price_Segment']).size().reset_index(name='Model_Count')
                
                # Ordenar fabricantes por número total de modelos para una mejor visualización
                top_automakers = segmented_data['Automaker'].value_counts().nlargest(20).index
                segment_counts_top = segment_counts[segment_counts['Automaker'].isin(top_automakers)]

                # Crear el gráfico de barras apiladas
                fig_segment = px.bar(
                    segment_counts_top,
                    x='Automaker',
                    y='Model_Count',
                    color='Price_Segment',
                    title='Number of Models per Automaker by Price Segment (Top 20)',
                    labels={'Model_Count': 'Number of Models', 'Automaker': 'Automaker'},
                    category_orders={
                        "Price_Segment": ["Budget", "Mid-Range", "Premium", "Luxury"]
                    },
                    color_discrete_map={
                        'Budget': '#2a9d8f',
                        'Mid-Range': '#e9c46a',
                        'Premium': '#f4a261',
                        'Luxury': '#e76f51'
                    },
                    template="plotly_dark"
                )
                
                fig_segment.update_layout(
                    xaxis_tickangle=-45, 
                    height=500,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis_title="Automaker",
                    yaxis_title="Number of Models",
                    legend_title="Price Segment"
                )
                
                st.plotly_chart(fig_segment, use_container_width=True)
                
                # Añadir información adicional sobre la segmentación
                st.markdown("""
                **📊 Market Segmentation Insights:**
                - **Budget**: Bottom 25% of price range (most affordable models)
                - **Mid-Range**: 25th-75th percentile (mainstream market)
                - **Premium**: 75th-95th percentile (higher-end positioning)
                - **Luxury**: Top 5% of price range (ultra-luxury models)
                """)
                
                # Mostrar estadísticas de segmentación
                if not segment_counts_top.empty:
                    st.markdown("**🎯 Segment Distribution:**")
                    segment_totals = segment_counts_top.groupby('Price_Segment')['Model_Count'].sum().sort_values(ascending=False)
                    for segment, count in segment_totals.items():
                        percentage = (count / segment_totals.sum()) * 100
                        st.markdown(f"- **{segment}**: {count} models ({percentage:.1f}%)")
            else:
                st.info("Price segmentation data is not available.")
                
        except Exception as e:
            st.error(f"Error rendering market segmentation: {str(e)}")
            
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
        
        # Sales Trend by Automaker
        st.subheader("📈 Sales Trend by Automaker")
        
        # Preparamos los datos para el gráfico de tendencias competitivas
        if not sales_summary.empty:
            # Necesitamos obtener los datos originales de ventas para el análisis temporal
            sales_data = analyzer.sales  # Acceso directo a los datos de ventas
            
            if not sales_data.empty:
                # Transformamos los datos de ventas de formato ancho a largo
                year_columns = [col for col in sales_data.columns if col.isdigit()]
                
                if year_columns:
                    sales_long = pd.melt(
                        sales_data,
                        id_vars=['Automaker', 'Genmodel', 'Genmodel_ID'],
                        value_vars=year_columns,
                        var_name='Year',
                        value_name='Sales_Volume'
                    )
                    
                    # Aplicamos filtros si están seleccionados
                    if selected_automakers:
                        sales_long = sales_long[sales_long['Automaker'].isin(selected_automakers)]
                    
                    # Agrupamos por año y fabricante para obtener las ventas por fabricante
                    yearly_sales_by_automaker = sales_long.groupby(['Year', 'Automaker'])['Sales_Volume'].sum().reset_index()
                    yearly_sales_by_automaker['Year'] = pd.to_numeric(yearly_sales_by_automaker['Year'])  # Aseguramos que el año sea numérico

                    # Creamos el gráfico de líneas competitivo con Plotly Express
                    fig_trend = px.line(
                        yearly_sales_by_automaker,
                        x='Year',
                        y='Sales_Volume',
                        color='Automaker',  # ¡Esta es la línea clave para múltiples líneas!
                        title='Sales Volume Trend by Automaker (2001-2020)',
                        markers=True,  # Añade puntos en cada dato anual
                        labels={'Sales_Volume': 'Total Sales', 'Year': 'Year'},
                        template="plotly_dark",
                        color_discrete_sequence=px.colors.qualitative.Set3  # Paleta de colores distintiva
                    )
                    
                    fig_trend.update_layout(
                        xaxis_title='Year',
                        yaxis_title='Total Sales Volume',
                        showlegend=True,  # Mostramos la leyenda para identificar fabricantes
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1,
                            font=dict(color="white", size=10)
                        ),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=500  # Aumentamos altura para acomodar la leyenda
                    )
                    
                    # Añadimos anotaciones para eventos importantes (solo si hay datos)
                    if 2016 in yearly_sales_by_automaker['Year'].values:
                        # Calculamos el promedio de ventas en 2016 para posicionar la anotación
                        sales_2016 = yearly_sales_by_automaker[yearly_sales_by_automaker['Year'] == 2016]['Sales_Volume'].mean()
                        fig_trend.add_annotation(
                            x=2016,
                            y=sales_2016,
                            text="Peak Year (2016)",
                            showarrow=True,
                            arrowhead=2,
                            arrowcolor="red",
                            bgcolor="rgba(255,255,255,0.8)",
                            bordercolor="red",
                            font=dict(color="black", size=12)
                        )
                    
                    # Mostramos el gráfico
                    st.plotly_chart(fig_trend, use_container_width=True)
                    
                    # Añadimos información adicional sobre las tendencias competitivas
                    st.markdown("""
                    **📊 Competitive Analysis Insights:**
                    - **Market Leaders**: Compare performance of different automakers over time
                    - **Growth Patterns**: Identify which brands show consistent growth vs volatility
                    - **Market Share Evolution**: See how brand positions changed from 2001-2020
                    - **Crisis Impact**: Observe how different brands responded to market challenges
                    - **Peak Performance**: 2016 marked the highest overall market volume
                    """)
                    
                    # Añadimos estadísticas rápidas si hay datos filtrados
                    if selected_automakers:
                        st.markdown("**🎯 Selected Automakers Analysis:**")
                        for automaker in selected_automakers:
                            automaker_data = yearly_sales_by_automaker[yearly_sales_by_automaker['Automaker'] == automaker]
                            if not automaker_data.empty:
                                peak_year = automaker_data.loc[automaker_data['Sales_Volume'].idxmax(), 'Year']
                                peak_sales = automaker_data['Sales_Volume'].max()
                                total_sales = automaker_data['Sales_Volume'].sum()
                                st.markdown(f"- **{automaker}**: Peak in {peak_year} ({peak_sales:,.0f} units), Total: {total_sales:,.0f} units")
                    
                    st.markdown("---")  # Añadimos un separador visual
                else:
                    st.info("No yearly sales data available to display trend.")
            else:
                st.info("No sales data available for trend analysis.")
        else:
            st.info("No filtered sales data available to display trend.")
        
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
        
        # Additional Sales Analytics
        st.markdown('<div class="section-header">🎯 Advanced Sales Analytics</div>', unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📊 Sales Distribution Analysis")
            if not sales_summary.empty:
                sales_clean = sales_summary.dropna(subset=['total_sales'])
                if not sales_clean.empty:
                    # Create sales categories
                    sales_clean_copy = sales_clean.copy()
                    sales_clean_copy['Sales Category'] = pd.cut(
                        sales_clean_copy['total_sales'],
                        bins=[0, 1000, 5000, 10000, 50000, float('inf')],
                        labels=['Low (<1K)', 'Medium (1K-5K)', 'High (5K-10K)', 'Very High (10K-50K)', 'Exceptional (>50K)']
                    )
                    
                    category_counts = sales_clean_copy['Sales Category'].value_counts()
                    
                    fig_bar = px.bar(
                        x=category_counts.index,
                        y=category_counts.values,
                        title='',
                        template="plotly_dark",
                        color=category_counts.values,
                        color_continuous_scale='plasma'
                    )
                    fig_bar.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=450,
                        xaxis_title="Sales Category",
                        yaxis_title="Number of Models",
                        xaxis_tickangle=-45
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No sales data available")
            else:
                st.info("No sales data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📈 Sales Performance Matrix")
            if not sales_summary.empty:
                sales_clean = sales_summary.dropna(subset=['total_sales'])
                if not sales_clean.empty:
                    # Create performance matrix by automaker
                    performance_matrix = sales_clean.groupby('Automaker').agg({
                        'total_sales': ['sum', 'mean', 'count']
                    }).round(0)
                    
                    performance_matrix.columns = ['Total Sales', 'Avg Sales per Model', 'Model Count']
                    performance_matrix = performance_matrix.sort_values('Total Sales', ascending=False).head(15)
                    
                    # Create scatter plot for performance matrix
                    fig_scatter = px.scatter(
                        performance_matrix,
                        x='Model Count',
                        y='Avg Sales per Model',
                        size='Total Sales',
                        color='Total Sales',
                        title='',
                        template="plotly_dark",
                        color_continuous_scale='viridis',
                        hover_data={'Total Sales': ':,.0f', 'Model Count': ':.0f', 'Avg Sales per Model': ':,.0f'}
                    )
                    fig_scatter.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=450,
                        xaxis_title="Number of Models",
                        yaxis_title="Average Sales per Model"
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)
                else:
                    st.info("No sales data available")
            else:
                st.info("No sales data available")
            st.markdown('</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error rendering sales performance: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

if __name__ == "__main__":
    main()