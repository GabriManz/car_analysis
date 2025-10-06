"""
Car Market Analysis Dashboard - Final Refactored Version
Based on actual data structure from notebooks analysis.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Car Market Analysis Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """
    Load all datasets with proper error handling and caching.
    Based on actual data structure from notebooks.
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

def create_automaker_analysis(basic_df, price_df):
    """Create automaker analysis with correct column names."""
    
    # Merge basic and price data
    merged_df = basic_df.merge(
        price_df, 
        left_on='Genmodel_ID', 
        right_on='Genmodel_ID', 
        how='left'
    )
    
    # Automaker statistics
    automaker_stats = merged_df.groupby('Automaker').agg({
        'Genmodel': 'nunique',  # Unique models per automaker
        'Entry_price': ['mean', 'min', 'max', 'count']  # Price statistics
    }).round(0)
    
    # Flatten column names
    automaker_stats.columns = ['Unique_Models', 'Avg_Price', 'Min_Price', 'Max_Price', 'Total_Entries']
    automaker_stats = automaker_stats.reset_index()
    
    return automaker_stats, merged_df

def create_sales_analysis(sales_df):
    """Create sales analysis with year columns."""
    
    # Get year columns (2001-2020)
    year_columns = [str(year) for year in range(2001, 2021)]
    available_years = [col for col in year_columns if col in sales_df.columns]
    
    # Calculate total sales per year
    yearly_sales = sales_df[available_years].sum().reset_index()
    yearly_sales.columns = ['Year', 'Total_Sales']
    yearly_sales['Year'] = yearly_sales['Year'].astype(int)
    
    # Top automakers by total sales
    sales_df['Total_Sales_All_Years'] = sales_df[available_years].sum(axis=1)
    top_automakers = sales_df.groupby('Maker')['Total_Sales_All_Years'].sum().sort_values(ascending=False).head(10)
    
    return yearly_sales, top_automakers, available_years

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🚗 Car Market Analysis Dashboard</h1>', unsafe_allow_html=True)
    
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
        
        if price_df is not None:
            automaker_stats, merged_df = create_automaker_analysis(basic_df, price_df)
            
            # Top automakers by model count
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Top 10 Automakers by Model Count")
                top_models = automaker_stats.nlargest(10, 'Unique_Models')
                
                fig = px.bar(
                    top_models,
                    x='Unique_Models',
                    y='Automaker',
                    orientation='h',
                    title="Models per Automaker",
                    color='Unique_Models',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Average Entry Price by Automaker")
                price_analysis = automaker_stats[automaker_stats['Avg_Price'].notna()].nlargest(10, 'Avg_Price')
                
                fig = px.bar(
                    price_analysis,
                    x='Avg_Price',
                    y='Automaker',
                    orientation='h',
                    title="Average Entry Price",
                    color='Avg_Price',
                    color_continuous_scale='Reds'
                )
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            # Automaker comparison table
            st.subheader("Automaker Comparison Table")
            st.dataframe(
                automaker_stats.sort_values('Avg_Price', ascending=False).head(15),
                use_container_width=True
            )
    
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
    
    with tab3:
        st.subheader("📈 Sales Trends Analysis")
        
        if sales_df is not None:
            yearly_sales, top_automakers, available_years = create_sales_analysis(sales_df)
            
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
    
    with tab4:
        st.subheader("🔍 Data Explorer")
        
        # Dataset selector
        dataset = st.selectbox(
            "Select Dataset to Explore:",
            ["Basic Table", "Price Table", "Sales Table"]
        )
        
        if dataset == "Basic Table":
            st.subheader("Basic Table - Car Models and Automakers")
            st.dataframe(basic_df, use_container_width=True)
            
        elif dataset == "Price Table":
            st.subheader("Price Table - Entry Prices by Model and Year")
            st.dataframe(price_df, use_container_width=True)
            
        elif dataset == "Sales Table":
            st.subheader("Sales Table - Sales Data by Model and Year")
            st.dataframe(sales_df, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>🚗 Car Market Analysis Dashboard | Built with Streamlit</p>
            <p>Data includes {:,} car models from {:,} automakers</p>
        </div>
        """.format(len(basic_df), basic_df['Automaker'].nunique()),
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
