"""
Debug version of the app to identify errors
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Dict, List, Optional, Any
import traceback

# Import core components
try:
    from src.business_logic import analyzer
    from src.components.config.app_config import APP_CONFIG, COLOR_PALETTE
    st.success("✅ All imports successful")
except ImportError as e:
    st.error(f"❌ Import error: {str(e)}")
    st.stop()

def debug_app():
    """Debug version of the app"""
    st.set_page_config(
        page_title="Debug - Car Market Analysis Dashboard",
        page_icon="🚗",
        layout="wide"
    )
    
    st.title("🔍 Debug - Car Market Analysis Dashboard")
    
    # Test data loading
    st.header("1. Data Loading Test")
    try:
        st.write("Testing analyzer...")
        automaker_list = analyzer.get_automaker_list()
        st.success(f"✅ Automaker list loaded: {len(automaker_list)} items")
        st.write(f"First 10 automakers: {automaker_list[:10]}")
        
        sales_summary = analyzer.get_sales_summary()
        st.success(f"✅ Sales summary loaded: {sales_summary.shape}")
        st.write(f"Sales columns: {list(sales_summary.columns)}")
        
        price_summary = analyzer.get_price_range_by_model()
        st.success(f"✅ Price summary loaded: {price_summary.shape}")
        
    except Exception as e:
        st.error(f"❌ Data loading error: {str(e)}")
        st.code(traceback.format_exc())
        return
    
    # Test filters
    st.header("2. Filters Test")
    try:
        with st.sidebar:
            st.markdown("## 🔧 Filters")
            
            if automaker_list:
                selected_automakers = st.multiselect(
                    'Select Automakers (leave empty to show all)',
                    options=automaker_list,
                    default=[],
                    key='debug_filter_automakers'
                )
                
                st.write(f"Selected automakers: {selected_automakers}")
                
                # Test filtering logic
                if selected_automakers:
                    filtered_sales = sales_summary[sales_summary['Automaker'].isin(selected_automakers)]
                    st.write(f"Filtered sales shape: {filtered_sales.shape}")
                else:
                    st.write("No filters applied - showing all data")
                    filtered_sales = sales_summary
                
                st.write(f"Final data shape: {filtered_sales.shape}")
                
            else:
                st.warning("No automaker data available")
                
    except Exception as e:
        st.error(f"❌ Filters error: {str(e)}")
        st.code(traceback.format_exc())
        return
    
    # Test metrics calculation
    st.header("3. Metrics Test")
    try:
        # Calculate metrics
        total_models = len(price_summary)
        total_sales = sales_summary['total_sales'].sum() if not sales_summary.empty else 0
        avg_price = price_summary['price_mean'].mean() if not price_summary.empty else 0
        automakers_count = sales_summary['Automaker'].nunique() if not sales_summary.empty else 0
        
        st.write(f"Total Models: {total_models}")
        st.write(f"Total Sales: {total_sales}")
        st.write(f"Avg Price: €{avg_price:,.0f}")
        st.write(f"Automakers: {automakers_count}")
        
        # Test if data has NaN values
        st.write(f"Sales data has NaN: {sales_summary['total_sales'].isna().sum()}")
        st.write(f"Price data has NaN: {price_summary['price_mean'].isna().sum()}")
        
    except Exception as e:
        st.error(f"❌ Metrics error: {str(e)}")
        st.code(traceback.format_exc())
        return
    
    # Test charts
    st.header("4. Charts Test")
    try:
        if not sales_summary.empty:
            # Test bar chart
            top_sales = sales_summary.nlargest(10, 'total_sales')
            fig_sales = px.bar(
                top_sales,
                x='Genmodel',
                y='total_sales',
                color='Automaker',
                title='Top Models by Sales (Debug)'
            )
            st.plotly_chart(fig_sales, use_container_width=True)
            st.success("✅ Bar chart created successfully")
        else:
            st.warning("No sales data for charts")
            
    except Exception as e:
        st.error(f"❌ Charts error: {str(e)}")
        st.code(traceback.format_exc())
        return
    
    # Test data table
    st.header("5. Data Table Test")
    try:
        if not sales_summary.empty:
            st.dataframe(sales_summary.head(10), use_container_width=True)
            st.success("✅ Data table displayed successfully")
        else:
            st.warning("No data to display in table")
            
    except Exception as e:
        st.error(f"❌ Data table error: {str(e)}")
        st.code(traceback.format_exc())
        return
    
    st.success("🎉 All tests passed! The app should be working.")

if __name__ == "__main__":
    debug_app()
