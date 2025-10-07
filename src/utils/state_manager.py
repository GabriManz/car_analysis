import streamlit as st

# Prefer relative import since this module lives under src/utils/
from ..business_logic import CarDataAnalyzer


@st.cache_resource
def load_analyzer():
    """Create and cache the CarDataAnalyzer instance as a resource."""
    analyzer = CarDataAnalyzer()
    return analyzer


