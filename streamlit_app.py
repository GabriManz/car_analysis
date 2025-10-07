"""
🚗 Car Market Analysis Dashboard - Balanced Version

Balanced dashboard with advanced features optimized for Streamlit Cloud deployment.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
from typing import Dict, List, Optional

warnings.filterwarnings('ignore')

# Set up page config
st.set_page_config(
    page_title="Car Market Analysis Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced data loading with preprocessing
@st.cache_data
def load_data():
    """Load and preprocess CSV data."""
    try:
        # Load basic data
        basic = pd.read_csv('data/Basic_table.csv')
        price = pd.read_csv('data/Price_table.csv')
        sales = pd.read_csv('data/Sales_table.csv')
        
        # Standardize column names
        for df in [price, sales]:
            if 'Maker' in df.columns:
                df.rename(columns={'Maker': 'Automaker'}, inplace=True)
        
        # Clean basic data (simple cleaning)
        if 'Automaker' in basic.columns:
            basic = basic.dropna(subset=['Automaker'])
            # Fix common automaker name issues
            basic['Automaker'] = basic['Automaker'].replace({
                'Sebring': 'Chrysler'
            })
        
        return basic, price, sales
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

@st.cache_data
def get_sales_summary(sales_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate sales summary with trends."""
    if sales_df.empty:
        return pd.DataFrame()
    
    year_cols = [col for col in sales_df.columns if col.isdigit()]
    if not year_cols:
        return pd.DataFrame()
    
    # Calculate total sales per model
    sales_summary = sales_df.copy()
    sales_summary['total_sales'] = sales_df[year_cols].sum(axis=1)
    sales_summary['avg_sales'] = sales_df[year_cols].mean(axis=1)
    sales_summary['max_sales'] = sales_df[year_cols].max(axis=1)
    sales_summary['years_active'] = (sales_df[year_cols] > 0).sum(axis=1)
    
    # Calculate trend (simplified)
    recent_years = sorted(year_cols)[-5:]  # Last 5 years
    old_years = sorted(year_cols)[:5] if len(year_cols) >= 10 else sorted(year_cols)[:3]
    
    if len(recent_years) > 0 and len(old_years) > 0:
        recent_avg = sales_df[recent_years].mean(axis=1)
        old_avg = sales_df[old_years].mean(axis=1)
        sales_summary['trend'] = np.where(
            old_avg > 0, 
            ((recent_avg - old_avg) / old_avg) * 100, 
            0
        )
    
    return sales_summary

@st.cache_data
def get_price_analysis(price_df: pd.DataFrame) -> pd.DataFrame:
    """Enhanced price analysis."""
    if price_df.empty or 'Entry_price' not in price_df.columns:
        return pd.DataFrame()
    
    price_analysis = price_df.groupby(['Automaker', 'Genmodel', 'Genmodel_ID']).agg({
        'Entry_price': ['min', 'max', 'mean', 'median', 'std', 'count']
    }).reset_index()
    
    # Flatten column names
    price_analysis.columns = [
        'Automaker', 'Genmodel', 'Genmodel_ID', 'price_min', 'price_max', 
        'price_mean', 'price_median', 'price_std', 'price_entries'
    ]
    
    # Calculate price volatility
    price_analysis['price_volatility'] = price_analysis['price_std'] / price_analysis['price_mean']
    
    # Price segments
    price_analysis['price_segment'] = pd.cut(
        price_analysis['price_mean'],
        bins=[0, 25000, 45000, 75000, float('inf')],
        labels=['Budget', 'Mid-Range', 'Premium', 'Luxury']
    )
    
    return price_analysis

@st.cache_data
def get_market_insights(basic_df: pd.DataFrame, sales_summary: pd.DataFrame, price_analysis: pd.DataFrame) -> Dict:
    """Generate market insights."""
    insights = {}
    
    if not basic_df.empty:
        insights['total_models'] = len(basic_df)
        insights['total_automakers'] = basic_df['Automaker'].nunique()
    
    if not sales_summary.empty:
        insights['total_sales'] = sales_summary['total_sales'].sum()
        insights['avg_sales_per_model'] = sales_summary['total_sales'].mean()
        
        # Market leaders
        market_share = sales_summary.groupby('Automaker')['total_sales'].sum().sort_values(ascending=False)
        insights['market_leaders'] = market_share.head(5).to_dict()
        
        # Growth trends
        if 'trend' in sales_summary.columns:
            growing_models = sales_summary[sales_summary['trend'] > 10]
            insights['growing_models'] = len(growing_models)
    
    if not price_analysis.empty:
        insights['avg_market_price'] = price_analysis['price_mean'].mean()
        insights['price_range'] = {
            'min': price_analysis['price_min'].min(),
            'max': price_analysis['price_max'].max()
        }
        
        # Segment distribution
        segment_counts = price_analysis['price_segment'].value_counts()
        insights['segment_distribution'] = segment_counts.to_dict()
    
    return insights

# Main header
st.markdown("""
<div style="text-align: center; font-size: 3rem; color: #667eea; margin-bottom: 2rem; font-weight: bold;">
    🚗 Car Market Analysis Dashboard
</div>
""", unsafe_allow_html=True)

# Load and process data
basic, price, sales = load_data()

if basic.empty or price.empty or sales.empty:
    st.error("❌ Error loading data files. Please check if the CSV files exist in the data/ folder.")
    st.stop()

st.success("✅ Data loaded successfully")

# Process data for analysis
sales_summary = get_sales_summary(sales)
price_analysis = get_price_analysis(price)
market_insights = get_market_insights(basic, sales_summary, price_analysis)

# Sidebar
st.sidebar.markdown("## 🎛️ Dashboard Controls")

# Get automakers
automakers = sorted(basic['Automaker'].unique()) if not basic.empty else []
        selected_automakers = st.sidebar.multiselect(
            "Select Automakers",
            options=automakers,
            default=automakers[:5] if len(automakers) >= 5 else automakers
        )

top_n = st.sidebar.slider("Number of Top Models", min_value=5, max_value=20, value=10)

# Main content
tab1, tab2, tab3 = st.tabs(["📊 Executive Summary", "🌍 Market Analysis", "📈 Sales Performance"])

with tab1:
    st.markdown("## 📊 Executive Summary")
    
    # Enhanced key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
        st.metric("Total Models", f"{market_insights.get('total_models', 0):,}")
        
        with col2:
        st.metric("Automakers", market_insights.get('total_automakers', 0))
    
    with col3:
        total_sales = market_insights.get('total_sales', 0)
            st.metric("Total Sales", f"{int(total_sales):,}")
        
    with col4:
        avg_price = market_insights.get('avg_market_price', 0)
            st.metric("Avg Price", f"€{avg_price:,.0f}")
        
    with col5:
        growing_models = market_insights.get('growing_models', 0)
        st.metric("Growing Models", growing_models)
    
    # Market insights section
    st.markdown("### 🎯 Key Market Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🏆 Top Market Leaders:**")
        market_leaders = market_insights.get('market_leaders', {})
        for i, (automaker, sales) in enumerate(market_leaders.items(), 1):
            percentage = (sales / total_sales) * 100 if total_sales > 0 else 0
            st.write(f"{i}. **{automaker}**: {int(sales):,} units ({percentage:.1f}%)")
    
    with col2:
        st.markdown("**💰 Price Segments:**")
        segments = market_insights.get('segment_distribution', {})
        for segment, count in segments.items():
            percentage = (count / len(price_analysis)) * 100 if not price_analysis.empty else 0
            st.write(f"• **{segment}**: {count} models ({percentage:.1f}%)")
    
    # Enhanced charts
        col1, col2 = st.columns(2)
        
        with col1:
        st.subheader("🏆 Top Models by Sales")
            if not sales_summary.empty:
            filtered_sales = sales_summary
            if selected_automakers:
                filtered_sales = sales_summary[sales_summary['Automaker'].isin(selected_automakers)]
            
            top_models = filtered_sales.nlargest(top_n, 'total_sales')[['Automaker', 'Genmodel', 'total_sales']]
            if not top_models.empty:
                top_models['model_name'] = top_models['Automaker'] + ' ' + top_models['Genmodel']
                fig = px.bar(
                    top_models, 
                    x='total_sales', 
                    y='model_name', 
                    orientation='h',
                    color='total_sales',
                    color_continuous_scale='viridis',
                    title=''
                )
                fig.update_layout(showlegend=False, height=400)
                    st.plotly_chart(fig, use_container_width=True)
        
        with col2:
        st.subheader("💰 Price Segment Distribution")
        if not price_analysis.empty:
            segment_counts = price_analysis['price_segment'].value_counts()
            if not segment_counts.empty:
                colors = ['#2E8B57', '#FFD700', '#FF6347', '#9370DB']  # Green, Gold, Tomato, Purple
                fig = px.pie(
                    values=segment_counts.values, 
                    names=segment_counts.index, 
                    title='',
                    color_discrete_sequence=colors
                )
                    st.plotly_chart(fig, use_container_width=True)
    
    # Additional insights
    st.markdown("### 📊 Advanced Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Sales Trend Analysis")
        if not sales_summary.empty and 'trend' in sales_summary.columns:
            # Show models with significant growth
            growing_models = sales_summary[sales_summary['trend'] > 20].nlargest(5, 'trend')
            if not growing_models.empty:
                growing_models['model_name'] = growing_models['Automaker'] + ' ' + growing_models['Genmodel']
                fig = px.bar(
                    growing_models, 
                    x='model_name', 
                    y='trend',
                    title='Fastest Growing Models',
                    color='trend',
                    color_continuous_scale='RdYlGn'
                )
                fig.update_layout(showlegend=False, height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No significant growth trends detected")
    
    with col2:
        st.subheader("🎯 Market Concentration")
        if not sales_summary.empty:
            market_share = sales_summary.groupby('Automaker')['total_sales'].sum().sort_values(ascending=False)
            top_5_share = market_share.head(5).sum()
            total_market = sales_summary['total_sales'].sum()
            concentration = (top_5_share / total_market) * 100 if total_market > 0 else 0
            
            st.metric("Top 5 Concentration", f"{concentration:.1f}%")
            
            # Concentration indicator
            if concentration > 60:
                st.warning("High market concentration - dominated by few players")
            elif concentration > 40:
                st.info("Moderate market concentration - balanced competition")
            else:
                st.success("Low market concentration - highly competitive")

with tab2:
    st.markdown("## 🌍 Market Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Market Share by Automaker")
        if not sales_summary.empty:
            market_share = sales_summary.groupby('Automaker')['total_sales'].sum().sort_values(ascending=False).head(10)
            
            if selected_automakers:
                market_share = market_share[market_share.index.isin(selected_automakers)]
            
            if not market_share.empty:
                # Calculate percentages
                total_market_sales = market_share.sum()
                market_share_pct = (market_share / total_market_sales * 100).round(1)
                
                fig = px.pie(
                    values=market_share.values, 
                    names=market_share.index, 
                    title='',
                    hole=0.3
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Show top 3 details
                st.markdown("**Top 3 Market Leaders:**")
                for i, (automaker, sales) in enumerate(market_share.head(3).items(), 1):
                    pct = market_share_pct[automaker]
                    st.write(f"{i}. **{automaker}**: {int(sales):,} units ({pct}%)")
    
    with col2:
        st.subheader("💰 Price Analysis by Automaker")
        if not price_analysis.empty:
            price_by_maker = price_analysis.groupby('Automaker').agg({
                'price_mean': 'mean',
                'price_min': 'min',
                'price_max': 'max'
            }).sort_values('price_mean', ascending=False).head(10)
            
        if selected_automakers:
                price_by_maker = price_by_maker[price_by_maker.index.isin(selected_automakers)]
            
            if not price_by_maker.empty:
                fig = go.Figure()
                
                # Add price range bars
                fig.add_trace(go.Bar(
                    name='Average Price',
                    x=price_by_maker.index,
                    y=price_by_maker['price_mean'],
                    marker_color='lightblue'
                ))
                
                # Add error bars for price range
                fig.update_layout(
                    title='',
                    showlegend=False,
                    yaxis_title='Price (€)',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Show price range details
                st.markdown("**Price Ranges:**")
                for automaker in price_by_maker.index[:3]:
                    avg_price = price_by_maker.loc[automaker, 'price_mean']
                    min_price = price_by_maker.loc[automaker, 'price_min']
                    max_price = price_by_maker.loc[automaker, 'price_max']
                    st.write(f"• **{automaker}**: €{avg_price:,.0f} avg (€{min_price:,.0f} - €{max_price:,.0f})")
    
    # Market segmentation analysis
    st.markdown("### 🎯 Market Segmentation Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
        st.subheader("📊 Segment Performance")
        if not sales_summary.empty and not price_analysis.empty:
            # Merge sales and price data
            merged_data = sales_summary.merge(
                price_analysis[['Automaker', 'Genmodel', 'Genmodel_ID', 'price_segment']], 
                on=['Automaker', 'Genmodel', 'Genmodel_ID'], 
                how='left'
            )
            
            if 'price_segment' in merged_data.columns:
                segment_performance = merged_data.groupby('price_segment').agg({
                    'total_sales': 'sum',
                    'avg_sales': 'mean'
                }).reset_index()
                
                if not segment_performance.empty:
                    fig = px.bar(
                        segment_performance,
                        x='price_segment',
                        y='total_sales',
                        title='Total Sales by Price Segment',
                        color='total_sales',
                        color_continuous_scale='viridis'
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        with col2:
        st.subheader("🔍 Competitive Landscape")
        if not sales_summary.empty:
            # Calculate market concentration metrics
            market_share = sales_summary.groupby('Automaker')['total_sales'].sum().sort_values(ascending=False)
            
            # Herfindahl-Hirschman Index (simplified)
            market_shares_pct = (market_share / market_share.sum()) * 100
            hhi = (market_shares_pct ** 2).sum()
            
            st.metric("Market Concentration (HHI)", f"{hhi:.0f}")
            
            # Market concentration interpretation
            if hhi > 2500:
                st.warning("🔴 Highly Concentrated Market")
                st.write("Few dominant players control the market")
            elif hhi > 1500:
                st.info("🟡 Moderately Concentrated Market")
                st.write("Some players have significant market power")
            else:
                st.success("🟢 Competitive Market")
                st.write("Market is highly competitive with many players")
            
            # Show market structure
            st.markdown("**Market Structure:**")
            top_3_share = market_shares_pct.head(3).sum()
            st.write(f"• Top 3 control: {top_3_share:.1f}% of market")
            st.write(f"• Total competitors: {len(market_share)} automakers")

with tab3:
    st.markdown("## 📈 Sales Performance")
    
    # Sales trends over time
    st.subheader("📊 Market Evolution Over Time")
    if not sales.empty:
        year_cols = [col for col in sales.columns if col.isdigit()]
        if year_cols:
            yearly_totals = sales[year_cols].sum().sort_index()
            
            # Create trend analysis
            fig = go.Figure()
            
            # Add line chart
            fig.add_trace(go.Scatter(
                x=yearly_totals.index,
                y=yearly_totals.values,
                mode='lines+markers',
                name='Total Sales',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            
            # Add trend line
            x_numeric = [int(year) for year in yearly_totals.index]
            z = np.polyfit(x_numeric, yearly_totals.values, 1)
            p = np.poly1d(z)
            trend_line = p(x_numeric)
            
            fig.add_trace(go.Scatter(
                x=yearly_totals.index,
                y=trend_line,
                mode='lines',
                name='Trend',
                line=dict(color='red', dash='dash', width=2)
            ))
            
            fig.update_layout(
                title='Market Sales Trend (2001-2020)',
                xaxis_title='Year',
                yaxis_title='Total Sales',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Trend analysis
            col1, col2, col3 = st.columns(3)
            with col1:
                peak_year = yearly_totals.idxmax()
                peak_sales = yearly_totals.max()
                st.metric("Peak Year", f"{peak_year} ({int(peak_sales):,})")
            
            with col2:
                recent_sales = yearly_totals.iloc[-1] if len(yearly_totals) > 0 else 0
                st.metric("Latest Year", f"{int(recent_sales):,}")
            
            with col3:
                growth_rate = ((recent_sales - yearly_totals.iloc[0]) / yearly_totals.iloc[0] * 100) if yearly_totals.iloc[0] > 0 else 0
                st.metric("Total Growth", f"{growth_rate:.1f}%")
    
    # Advanced sales analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top Performing Models")
        if not sales_summary.empty:
            filtered_sales = sales_summary
        if selected_automakers:
                filtered_sales = sales_summary[sales_summary['Automaker'].isin(selected_automakers)]
            
            top_models = filtered_sales.nlargest(top_n, 'total_sales')[['Automaker', 'Genmodel', 'total_sales', 'avg_sales', 'years_active']]
            
            if not top_models.empty:
                top_models['model_name'] = top_models['Automaker'] + ' ' + top_models['Genmodel']
                
                # Create multi-metric chart
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='Total Sales',
                    x=top_models['model_name'],
                    y=top_models['total_sales'],
                    marker_color='lightblue'
                ))
                
                fig.update_layout(
                    title='Top Models by Total Sales',
                    xaxis_title='Model',
                    yaxis_title='Total Sales',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Show detailed metrics
                st.markdown("**Top 3 Models Details:**")
                for i, (_, row) in enumerate(top_models.head(3).iterrows(), 1):
                    st.write(f"{i}. **{row['model_name']}**: {int(row['total_sales']):,} total sales, {int(row['avg_sales']):,} avg/year, {int(row['years_active'])} years active")
    
    with col2:
        st.subheader("📊 Sales Performance Distribution")
        if not sales_summary.empty:
            # Create performance categories
            sales_summary['performance_category'] = pd.cut(
                sales_summary['total_sales'],
                bins=[0, 1000, 10000, 100000, float('inf')],
                labels=['Low', 'Medium', 'High', 'Very High']
            )
            
            performance_counts = sales_summary['performance_category'].value_counts()
            
            if not performance_counts.empty:
                colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
                fig = px.pie(
                    values=performance_counts.values,
                    names=performance_counts.index,
                    title='Model Performance Distribution',
                    color_discrete_sequence=colors
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Performance insights
            st.markdown("**Performance Insights:**")
            high_performers = len(sales_summary[sales_summary['total_sales'] > 100000])
            total_models = len(sales_summary)
            high_perf_pct = (high_performers / total_models * 100) if total_models > 0 else 0
            
            st.write(f"• **High Performers** (>100K sales): {high_performers} models ({high_perf_pct:.1f}%)")
            st.write(f"• **Average Sales per Model**: {int(sales_summary['total_sales'].mean()):,}")
            st.write(f"• **Sales Standard Deviation**: {int(sales_summary['total_sales'].std()):,}")
    
    # Growth and decline analysis
    if not sales_summary.empty and 'trend' in sales_summary.columns:
        st.markdown("### 📈 Growth & Decline Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚀 Fastest Growing Models")
            growing_models = sales_summary[sales_summary['trend'] > 0].nlargest(5, 'trend')
            
            if not growing_models.empty:
                growing_models['model_name'] = growing_models['Automaker'] + ' ' + growing_models['Genmodel']
                fig = px.bar(
                    growing_models,
                    x='model_name',
                    y='trend',
                    title='Growth Rate (%)',
                    color='trend',
                    color_continuous_scale='RdYlGn'
                )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No significant growth trends detected")
        
        with col2:
            st.subheader("📉 Declining Models")
            declining_models = sales_summary[sales_summary['trend'] < -10].nsmallest(5, 'trend')
            
            if not declining_models.empty:
                declining_models['model_name'] = declining_models['Automaker'] + ' ' + declining_models['Genmodel']
                fig = px.bar(
                    declining_models,
                    x='model_name',
                    y='trend',
                    title='Decline Rate (%)',
                    color='trend',
                    color_continuous_scale='Reds'
                )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No significant declining trends detected")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    🚗 Car Market Analysis Dashboard v2.3.0<br>
    Advanced Analytics & Intelligence Platform
</div>
""", unsafe_allow_html=True)