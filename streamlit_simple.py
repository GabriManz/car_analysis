"""
Ultra-simple version of the Streamlit app for debugging.
This version will help us identify the exact issue.
"""

import streamlit as st
import sys
import os

# Set up page config
st.set_page_config(
    page_title="Car Analysis - Simple",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Car Analysis - Simple Version")

st.write("This is a simple test to verify Streamlit Cloud is working.")

# Test basic imports
st.subheader("Testing Basic Imports")

try:
    import pandas as pd
    st.success("✅ pandas imported successfully")
    st.write(f"Pandas version: {pd.__version__}")
except Exception as e:
    st.error(f"❌ pandas import failed: {e}")

try:
    import numpy as np
    st.success("✅ numpy imported successfully")
    st.write(f"NumPy version: {np.__version__}")
except Exception as e:
    st.error(f"❌ numpy import failed: {e}")

try:
    import plotly.express as px
    st.success("✅ plotly imported successfully")
except Exception as e:
    st.error(f"❌ plotly import failed: {e}")

# Test file structure
st.subheader("Testing File Structure")

try:
    current_dir = os.getcwd()
    st.write(f"Current directory: {current_dir}")
    
    # List files
    files = os.listdir('.')
    st.write("Files in current directory:")
    for f in files[:10]:  # Show first 10 files
        st.write(f"- {f}")
    
    # Check data directory
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

# Test business logic import
st.subheader("Testing Business Logic Import")

try:
    st.write("Attempting to import business_logic...")
    from src.business_logic import analyzer
    st.success("✅ Business logic imported successfully")
    
    # Test data loading
    st.write("Testing data access...")
    automakers = analyzer.get_automaker_list()
    st.success(f"✅ Data access successful - Found {len(automakers)} automakers")
    
    if len(automakers) > 0:
        st.write("Sample automakers:", automakers[:5])
    
except Exception as e:
    st.error(f"❌ Business logic import failed: {e}")
    st.write("Full error details:")
    st.code(str(e))
    
    # Show more details
    import traceback
    st.write("Traceback:")
    st.code(traceback.format_exc())

st.subheader("Test Complete")
st.write("If you see this message, the basic Streamlit app is working.")
st.write("Any errors above will help us identify the specific issue.")
