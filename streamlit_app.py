"""
🚗 Car Market Analysis Dashboard - Simplified Version

Simplified dashboard optimized for Streamlit Cloud deployment.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')

# Set up page config
st.set_page_config(
    page_title="Car Market Analysis Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data directly without complex business logic
@st.cache_data
def load_data():
    """Load CSV data directly."""
    try:
        # Load basic data
        basic = pd.read_csv('data/Basic_table.csv')
        price = pd.read_csv('data/Price_table.csv')
        sales = pd.read_csv('data/Sales_table.csv')
        
        # Standardize column names
        for df in [price, sales]:
            if 'Maker' in df.columns:
                df.rename(columns={'Maker': 'Automaker'}, inplace=True)
        
        return basic, price, sales
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# Main header
st.markdown("""
<div style="text-align: center; font-size: 3rem; color: #667eea; margin-bottom: 2rem; font-weight: bold;">
    🚗 Car Market Analysis Dashboard
</div>
""", unsafe_allow_html=True)

# Load data
basic, price, sales = load_data()

if basic.empty or price.empty or sales.empty:
    st.error("❌ Error loading data files. Please check if the CSV files exist in the data/ folder.")
    st.stop()

st.success("✅ Data loaded successfully")

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
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_models = len(basic)
        st.metric("Total Models", total_models)
    
    with col2:
        total_automakers = len(automakers)
        st.metric("Automakers", total_automakers)
    
    with col3:
        if not price.empty and 'Entry_price' in price.columns:
            avg_price = price['Entry_price'].mean()
            st.metric("Avg Price", f"€{avg_price:,.0f}")
        else:
            st.metric("Avg Price", "N/A")
    
    with col4:
        if not sales.empty:
            year_cols = [col for col in sales.columns if col.isdigit()]
            if year_cols:
                total_sales = sales[year_cols].sum().sum()
                st.metric("Total Sales", f"{int(total_sales):,}")
            else:
                st.metric("Total Sales", "N/A")
        else:
            st.metric("Total Sales", "N/A")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Models by Automaker")
        if selected_automakers:
            filtered_basic = basic[basic['Automaker'].isin(selected_automakers)]
            model_counts = filtered_basic['Automaker'].value_counts().head(top_n)
        else:
            model_counts = basic['Automaker'].value_counts().head(top_n)
        
        if not model_counts.empty:
            fig = px.bar(x=model_counts.index, y=model_counts.values, title='')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Price Distribution")
        if not price.empty and 'Entry_price' in price.columns:
            fig = px.histogram(price, x='Entry_price', title='', nbins=30)
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("## 🌍 Market Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Market Share by Automaker")
        if not sales.empty:
            year_cols = [col for col in sales.columns if col.isdigit()]
            if year_cols:
                sales['total_sales'] = sales[year_cols].sum(axis=1)
                market_share = sales.groupby('Automaker')['total_sales'].sum().sort_values(ascending=False).head(10)
                
                if selected_automakers:
                    market_share = market_share[market_share.index.isin(selected_automakers)]
                
                if not market_share.empty:
                    fig = px.pie(values=market_share.values, names=market_share.index, title='')
                    st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Price by Automaker")
        if not price.empty and 'Entry_price' in price.columns:
            price_by_maker = price.groupby('Automaker')['Entry_price'].mean().sort_values(ascending=False).head(10)
            
            if selected_automakers:
                price_by_maker = price_by_maker[price_by_maker.index.isin(selected_automakers)]
            
            if not price_by_maker.empty:
                fig = px.bar(x=price_by_maker.index, y=price_by_maker.values, title='')
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("## 📈 Sales Performance")
    
    # Sales trends
    st.subheader("Sales Trend by Year")
    if not sales.empty:
        year_cols = [col for col in sales.columns if col.isdigit()]
        if year_cols:
            yearly_totals = sales[year_cols].sum().sort_index()
            
            fig = px.line(x=yearly_totals.index, y=yearly_totals.values, title='')
            st.plotly_chart(fig, use_container_width=True)
    
    # Top models
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Models by Sales")
        if not sales.empty:
            year_cols = [col for col in sales.columns if col.isdigit()]
            if year_cols:
                sales['total_sales'] = sales[year_cols].sum(axis=1)
                top_models = sales.nlargest(top_n, 'total_sales')[['Automaker', 'Genmodel', 'total_sales']]
                
                if selected_automakers:
                    top_models = top_models[top_models['Automaker'].isin(selected_automakers)]
                
                if not top_models.empty:
                    top_models['model_name'] = top_models['Automaker'] + ' ' + top_models['Genmodel']
                    fig = px.bar(top_models, x='total_sales', y='model_name', orientation='h', title='')
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Sales Distribution")
        if not sales.empty:
            year_cols = [col for col in sales.columns if col.isdigit()]
            if year_cols:
                sales['total_sales'] = sales[year_cols].sum(axis=1)
                fig = px.histogram(sales, x='total_sales', title='', nbins=30)
                st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    🚗 Car Market Analysis Dashboard v2.2.0<br>
    Simplified for Streamlit Cloud
</div>
""", unsafe_allow_html=True)