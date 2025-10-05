import streamlit as st

st.title("🚗 Test App")
st.write("If you see this, Streamlit is working!")

st.header("Data Test")
try:
    from src.business_logic import analyzer
    st.success("✅ Analyzer imported successfully")
    
    automakers = analyzer.get_automaker_list()
    st.write(f"Found {len(automakers)} automakers")
    
    if automakers:
        st.write("First 10 automakers:", automakers[:10])
        
        sales = analyzer.get_sales_summary()
        st.write(f"Sales data shape: {sales.shape}")
        
        if not sales.empty:
            st.write("Sample sales data:")
            st.dataframe(sales.head())
        else:
            st.warning("Sales data is empty")
    else:
        st.error("No automakers found")
        
except Exception as e:
    st.error(f"Error: {str(e)}")
    import traceback
    st.code(traceback.format_exc())
