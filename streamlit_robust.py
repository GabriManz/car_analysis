"""
Car Market Analysis Dashboard - Robust Version
Simplified and error-proof based on actual data structure.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Car Market Analysis Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    """
    Load all datasets with proper error handling and caching.
    """
    try:
        # Load Basic table (1011 rows, 4 columns)
        basic_df = pd.read_csv('data/Basic_table.csv')
        
        # Load Price table (6333 rows, 5 columns) 
        price_df = pd.read_csv('data/Price_table.csv')
        
        # Load Sales table (773 rows, 23 columns)
        sales_df = pd.read_csv('data/Sales_table.csv')
        
        return basic_df, price_df, sales_df, None
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, str(e)

def main():
    """Main application function."""
    
    # Header
    st.title("🚗 Car Market Analysis Dashboard")
    st.markdown("---")
    
    # Load data
    with st.spinner("Loading data..."):
        basic_df, price_df, sales_df, error = load_data()
    
    if error:
        st.error(f"Failed to load data: {error}")
        return
    
    # Data overview metrics
    st.subheader("📊 Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Car Models", 
            value=f"{len(basic_df):,}",
            help="Unique car models in Basic table"
        )
    
    with col2:
        st.metric(
            label="Unique Automakers", 
            value=f"{basic_df['Automaker'].nunique():,}",
            help="Number of unique car manufacturers"
        )
    
    with col3:
        if price_df is not None:
            avg_price = price_df['Entry_price'].mean()
            st.metric(
                label="Average Entry Price", 
                value=f"${avg_price:,.0f}",
                help="Average entry price across all models"
            )
    
    with col4:
        if sales_df is not None:
            year_columns = [str(year) for year in range(2001, 2021) if str(year) in sales_df.columns]
            total_sales = sales_df[year_columns].sum().sum()
            st.metric(
                label="Total Sales (2001-2020)", 
                value=f"{total_sales:,.0f}",
                help="Total sales across all years and models"
            )
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(["🏭 Automaker Analysis", "💰 Price Analysis", "📈 Sales Trends", "🔍 Data Explorer"])
    
    with tab1:
        st.subheader("🏭 Automaker Performance Analysis")
        
        # Simple automaker analysis from basic table
        automaker_counts = basic_df['Automaker'].value_counts().head(15)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 15 Automakers by Model Count")
            fig = px.bar(
                x=automaker_counts.values,
                y=automaker_counts.index,
                orientation='h',
                title="Models per Automaker",
                labels={'x': 'Number of Models', 'y': 'Automaker'},
                color=automaker_counts.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Automaker Distribution")
            fig = px.pie(
                values=automaker_counts.head(10).values,
                names=automaker_counts.head(10).index,
                title="Top 10 Automakers Distribution"
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        # Automaker table
        st.subheader("Automaker Statistics")
        automaker_stats = basic_df.groupby('Automaker').agg({
            'Genmodel': 'nunique',
            'Automaker_ID': 'first'
        }).rename(columns={'Genmodel': 'Model_Count'}).sort_values('Model_Count', ascending=False)
        
        st.dataframe(automaker_stats.head(20), use_container_width=True)
    
    with tab2:
        st.subheader("💰 Price Analysis")
        
        if price_df is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                # Price distribution
                st.subheader("Entry Price Distribution")
                fig = px.histogram(
                    price_df,
                    x='Entry_price',
                    nbins=50,
                    title="Distribution of Entry Prices",
                    labels={'Entry_price': 'Entry Price ($)', 'count': 'Number of Models'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Price by year
                st.subheader("Average Price Trends by Year")
                yearly_prices = price_df.groupby('Year')['Entry_price'].mean().reset_index()
                
                fig = px.line(
                    yearly_prices,
                    x='Year',
                    y='Entry_price',
                    title="Average Entry Price by Year",
                    markers=True
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            # Price statistics
            st.subheader("Price Statistics")
            price_stats = price_df['Entry_price'].describe()
            st.write(price_stats)
            
            # Top expensive models
            st.subheader("Most Expensive Models")
            expensive_models = price_df.nlargest(10, 'Entry_price')[['Maker', 'Genmodel', 'Year', 'Entry_price']]
            st.dataframe(expensive_models, use_container_width=True)
    
    with tab3:
        st.subheader("📈 Sales Trends Analysis")
        
        if sales_df is not None:
            # Get year columns (2001-2020)
            year_columns = [str(year) for year in range(2001, 2021)]
            available_years = [col for col in year_columns if col in sales_df.columns]
            
            # Calculate total sales per year
            yearly_sales = sales_df[available_years].sum().reset_index()
            yearly_sales.columns = ['Year', 'Total_Sales']
            yearly_sales['Year'] = yearly_sales['Year'].astype(int)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Sales trend over time
                st.subheader("Total Sales Trend (2001-2020)")
                fig = px.line(
                    yearly_sales,
                    x='Year',
                    y='Total_Sales',
                    title="Total Sales by Year",
                    markers=True
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Top automakers by sales
                st.subheader("Top 10 Automakers by Total Sales")
                sales_df['Total_Sales_All_Years'] = sales_df[available_years].sum(axis=1)
                top_automakers = sales_df.groupby('Maker')['Total_Sales_All_Years'].sum().sort_values(ascending=False).head(10)
                
                fig = px.bar(
                    x=top_automakers.values,
                    y=top_automakers.index,
                    orientation='h',
                    title="Total Sales by Automaker",
                    color=top_automakers.values,
                    color_continuous_scale='Greens'
                )
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            # Sales statistics
            st.subheader("Sales Statistics by Year")
            yearly_stats = yearly_sales.describe()
            st.write(yearly_stats)
    
    with tab4:
        st.subheader("🔍 Data Explorer")
        
        # Dataset selector
        dataset = st.selectbox(
            "Select Dataset to Explore:",
            ["Basic Table", "Price Table", "Sales Table"]
        )
        
        if dataset == "Basic Table":
            st.subheader("Basic Table - Car Models and Automakers")
            st.write(f"Shape: {basic_df.shape}")
            st.dataframe(basic_df, use_container_width=True)
            
        elif dataset == "Price Table":
            st.subheader("Price Table - Entry Prices by Model and Year")
            st.write(f"Shape: {price_df.shape}")
            st.dataframe(price_df, use_container_width=True)
            
        elif dataset == "Sales Table":
            st.subheader("Sales Table - Sales Data by Model and Year")
            st.write(f"Shape: {sales_df.shape}")
            st.dataframe(sales_df, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"""
        <div style='text-align: center; color: #666;'>
            <p>🚗 Car Market Analysis Dashboard | Built with Streamlit</p>
            <p>Data includes {len(basic_df):,} car models from {basic_df['Automaker'].nunique():,} automakers</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
