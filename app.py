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

# Import core modules from src using absolute imports
from src.utils.state_manager import load_analyzer
from src.components.ui.header import render_header
from src.components.ui.sidebar import render_sidebar

# Import dashboard renderers
from src.router import navigate

# Configuration and styles
from src.config.app_config import APP_CONFIG, CUSTOM_CSS

st.set_page_config(
    page_title=APP_CONFIG['title'],
    page_icon=APP_CONFIG['icon'],
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize analyzer via cached state manager
analyzer = load_analyzer()

def main():
    """Main application."""
    
    # Header
    render_header()

    # Sidebar (filters and navigation)
    selected_automakers, top_n, page = render_sidebar(analyzer)

    # Persist filters in session_state for dashboard functions
    st.session_state['filter_automakers'] = selected_automakers
    st.session_state['filter_top_n'] = top_n

    # Navigate to the selected page
    navigate(page, analyzer)

if __name__ == "__main__":
    main()


