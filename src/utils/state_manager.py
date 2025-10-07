import streamlit as st

# Prefer relative import since this module lives under src/utils/
from ..business_logic import CarDataAnalyzer


@st.cache_data(ttl=3600)
def load_analyzer():
    """Load and cache the CarDataAnalyzer instance for 1 hour."""
    analyzer = CarDataAnalyzer()
    return analyzer


