"""
Debug version to check column names in the data.
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Debug Columns", page_icon="🔍")

st.title("🔍 Debug: Check Column Names")

# Load data
try:
    basic_df = pd.read_csv('data/Basic_table.csv')
    price_df = pd.read_csv('data/Price_table.csv')
    sales_df = pd.read_csv('data/Sales_table.csv')
    
    st.success("✅ Data loaded successfully")
    
    # Show column names for each dataset
    st.subheader("📋 Basic_table.csv columns:")
    st.write(basic_df.columns.tolist())
    st.write("Shape:", basic_df.shape)
    st.write("First few rows:")
    st.dataframe(basic_df.head())
    
    st.subheader("💰 Price_table.csv columns:")
    st.write(price_df.columns.tolist())
    st.write("Shape:", price_df.shape)
    st.write("First few rows:")
    st.dataframe(price_df.head())
    
    st.subheader("📊 Sales_table.csv columns:")
    st.write(sales_df.columns.tolist())
    st.write("Shape:", sales_df.shape)
    st.write("First few rows:")
    st.dataframe(sales_df.head())
    
except Exception as e:
    st.error(f"Error: {e}")
    import traceback
    st.code(traceback.format_exc())
