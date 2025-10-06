"""
Minimal Streamlit app to test basic functionality.
"""

import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Car Analysis - Minimal", page_icon="🚗")

st.title("🚗 Car Analysis - Minimal Test")

# Test 1: Check if we can load data
st.subheader("Data Loading Test")

try:
    # Check if data directory exists
    if os.path.exists('data'):
        st.success("✅ Data directory found")
        
        # List files in data directory
        data_files = os.listdir('data')
        st.write(f"Files in data/: {data_files}")
        
        # Try to load Basic_table.csv
        if 'Basic_table.csv' in data_files:
            st.write("Loading Basic_table.csv...")
            df = pd.read_csv('data/Basic_table.csv')
            st.success(f"✅ Loaded Basic_table.csv: {df.shape[0]} rows, {df.shape[1]} columns")
            
            # Show basic info
            st.write("First 5 rows:")
            st.dataframe(df.head())
            
        else:
            st.error("❌ Basic_table.csv not found")
            
    else:
        st.error("❌ Data directory not found")
        
except Exception as e:
    st.error(f"❌ Error: {e}")
    import traceback
    st.code(traceback.format_exc())

st.write("---")
st.write("If you see this message, the basic app is working!")
