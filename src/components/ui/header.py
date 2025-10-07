import streamlit as st
from src.config.app_config import APP_CONFIG


def render_header():
    """Renders the main header of the application."""
    st.markdown(f"""
    <div class="main-header">
        <h1>{APP_CONFIG['title']}</h1>
        <p>Professional market intelligence and analytics platform</p>
    </div>
    """, unsafe_allow_html=True)


