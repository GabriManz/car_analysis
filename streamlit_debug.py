"""
Debug version of the Streamlit app to identify deployment issues.
This minimal version will help us isolate the problem.
"""

import streamlit as st
import sys
import os

# Set up page config
st.set_page_config(
    page_title="Car Analysis Debug",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Car Analysis - Debug Mode")

# Test 1: Basic imports
st.subheader("Test 1: Basic Imports")
try:
    import pandas as pd
    st.success("✅ pandas imported successfully")
except Exception as e:
    st.error(f"❌ pandas import failed: {e}")

try:
    import numpy as np
    st.success("✅ numpy imported successfully")
except Exception as e:
    st.error(f"❌ numpy import failed: {e}")

try:
    import plotly.express as px
    st.success("✅ plotly imported successfully")
except Exception as e:
    st.error(f"❌ plotly import failed: {e}")

# Test 2: File structure
st.subheader("Test 2: File Structure")
try:
    current_dir = os.getcwd()
    st.write(f"Current directory: {current_dir}")
    
    files = os.listdir('.')
    st.write("Files in current directory:")
    for f in files:
        st.write(f"- {f}")
    
    if os.path.exists('data'):
        st.success("✅ data/ directory exists")
        data_files = os.listdir('data')
        st.write("Data files:")
        for f in data_files:
            st.write(f"- {f}")
    else:
        st.error("❌ data/ directory not found")
        
except Exception as e:
    st.error(f"❌ File structure test failed: {e}")

# Test 3: Business logic import
st.subheader("Test 3: Business Logic Import")
try:
    from src.business_logic import analyzer
    st.success("✅ Business logic imported successfully")
    
    # Test data loading
    automakers = analyzer.get_automaker_list()
    st.write(f"Found {len(automakers)} automakers")
    st.write("Sample automakers:", automakers[:5])
    
except Exception as e:
    st.error(f"❌ Business logic import failed: {e}")
    st.write("Full error:")
    st.code(str(e))

# Test 4: Data access
st.subheader("Test 4: Data Access")
try:
    sales_data = analyzer.get_sales_summary()
    st.success(f"✅ Sales data loaded: {sales_data.shape}")
    
    price_data = analyzer.get_price_range_by_model()
    st.success(f"✅ Price data loaded: {price_data.shape}")
    
except Exception as e:
    st.error(f"❌ Data access failed: {e}")
    st.write("Full error:")
    st.code(str(e))

st.subheader("Debug Complete")
st.write("If all tests pass, the issue might be in the main app logic.")
st.write("If any test fails, that's where we need to focus our debugging efforts.")
