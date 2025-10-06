"""
Simplified Car Analysis Dashboard - Working Version
Based on the successful minimal test.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Car Analysis Dashboard",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Car Market Analysis Dashboard")

# Load data directly (we know this works from minimal test)
@st.cache_data
def load_data():
    """Load all datasets with caching."""
    try:
        basic_df = pd.read_csv('data/Basic_table.csv')
        price_df = pd.read_csv('data/Price_table.csv')
        sales_df = pd.read_csv('data/Sales_table.csv')
        
        return basic_df, price_df, sales_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

# Load data
basic_df, price_df, sales_df = load_data()

if basic_df is not None:
    st.success(f"✅ Data loaded successfully: {len(basic_df)} cars")
    
    # Basic metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Cars", len(basic_df))
    
    with col2:
        st.metric("Unique Brands", basic_df['Brand'].nunique())
    
    with col3:
        st.metric("Unique Models", basic_df['Model'].nunique())
    
    with col4:
        if price_df is not None:
            avg_price = price_df['Price'].mean()
            st.metric("Avg Price", f"${avg_price:,.0f}")
    
    # Brand distribution
    st.subheader("📊 Brand Distribution")
    brand_counts = basic_df['Brand'].value_counts().head(10)
    
    fig = px.bar(
        x=brand_counts.values,
        y=brand_counts.index,
        orientation='h',
        title="Top 10 Car Brands",
        labels={'x': 'Number of Cars', 'y': 'Brand'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Model distribution
    st.subheader("🚙 Model Distribution")
    model_counts = basic_df['Model'].value_counts().head(10)
    
    fig2 = px.bar(
        x=model_counts.values,
        y=model_counts.index,
        orientation='h',
        title="Top 10 Car Models",
        labels={'x': 'Number of Cars', 'y': 'Model'}
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Data table
    st.subheader("📋 Data Overview")
    st.dataframe(basic_df.head(20), use_container_width=True)
    
else:
    st.error("❌ Failed to load data")

st.write("---")
st.write("🎉 Dashboard loaded successfully!")
