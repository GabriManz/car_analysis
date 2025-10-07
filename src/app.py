"""
🚗 Car Market Analysis Executive Dashboard - Working Version

Professional dashboard with real data display and comprehensive features.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from typing import Dict, List, Optional, Any
import warnings
warnings.filterwarnings('ignore')

# Import core components
import sys
import os

# Add the src directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    # Prefer package-relative import when running as a module
    from .utils.state_manager import load_analyzer
except ImportError:
    try:
        # Fallback for direct execution contexts
        from utils.state_manager import load_analyzer
    except ImportError as e:
        st.error(f"❌ Error importing state manager: {e}")
        st.error("Please ensure src/utils/state_manager.py exists and is importable.")
        st.stop()

# Import dashboard renderers
try:
    from .components.dashboards.executive_dashboard import show_executive_dashboard
    from .components.dashboards.market_dashboard import show_market_dashboard
    from .components.dashboards.sales_dashboard import show_sales_dashboard
except ImportError:
    try:
        from components.dashboards.executive_dashboard import show_executive_dashboard
        from components.dashboards.market_dashboard import show_market_dashboard
        from components.dashboards.sales_dashboard import show_sales_dashboard
except ImportError as e:
        st.error(f"❌ Error importing executive dashboard: {e}")
    st.stop()

# Application configuration
APP_CONFIG = {
    'title': 'Car Market Analysis Executive Dashboard',
    'icon': '🚗',
    'version': '2.0.0'
}

st.set_page_config(
    page_title=APP_CONFIG['title'],
    page_icon=APP_CONFIG['icon'],
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2.5rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.main-header::before {
    content: "🚗";
    position: absolute;
    top: 20px;
    right: 30px;
    font-size: 4rem;
    opacity: 0.3;
    z-index: 1;
}
.main-header h1 {
    font-size: 3rem;
    margin: 0;
    text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
    font-weight: 700;
    position: relative;
    z-index: 2;
}
.main-header p {
    font-size: 1.3rem;
    margin: 0.5rem 0 0 0;
    opacity: 0.95;
    position: relative;
    z-index: 2;
    font-weight: 300;
}
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    border: 1px solid rgba(255,255,255,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    position: relative;
    overflow: hidden;
}
.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);
}
.metric-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
    pointer-events: none;
}
.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 1rem 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    position: relative;
    z-index: 1;
}
.metric-label {
    font-size: 1.1rem;
    opacity: 0.9;
    font-weight: 500;
    position: relative;
    z-index: 1;
}
.metric-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 1;
}
.section-header {
    background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 10px;
    margin: 2rem 0 1rem 0;
    font-size: 1.5rem;
    font-weight: 600;
    text-align: center;
    box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
}
.chart-container {
    background: rgba(255,255,255,0.05);
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
}
</style>
""", unsafe_allow_html=True)

# Initialize analyzer via cached state manager
analyzer = load_analyzer()

def main():
    """Main application."""
    
    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>{APP_CONFIG['title']}</h1>
        <p>Professional market intelligence and analytics platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar filters
    with st.sidebar:
        st.markdown("## 🔧 Filters")
        
        # Get automaker list
        try:
            automaker_list = analyzer.get_automaker_list()
        except Exception as e:
            st.error(f"Error getting automaker list: {e}")
            automaker_list = []
        
        if automaker_list:
            selected_automakers = st.multiselect(
                'Select Automakers (leave empty to show all)',
                options=automaker_list,
                default=[],
                key='filter_automakers'
            )
            
            top_n = st.slider(
                'Top N Results',
                min_value=5,
                max_value=50,
                value=15,
                step=5,
                key='filter_top_n'
            )
        else:
            st.warning("No automaker data available")
            selected_automakers = []
            top_n = 15
    
    # Router navigation (sidebar)
    page = st.sidebar.radio(
        "Selecciona un Dashboard",
        ["Resumen Ejecutivo", "Análisis de Mercado", "Rendimiento de Ventas"]
    )

    # Persist filters in session_state for dashboard functions
    st.session_state['filter_automakers'] = selected_automakers
    st.session_state['filter_top_n'] = top_n

    if page == "Resumen Ejecutivo":
        show_executive_dashboard(analyzer)
    elif page == "Análisis de Mercado":
        show_market_dashboard(analyzer)
    elif page == "Rendimiento de Ventas":
        show_sales_dashboard(analyzer)

if __name__ == "__main__":
    main()