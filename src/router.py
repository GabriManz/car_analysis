import streamlit as st
from src.components.dashboards.executive_dashboard import show_executive_dashboard
from src.components.dashboards.market_dashboard import show_market_dashboard
from src.components.dashboards.sales_dashboard import show_sales_dashboard
from src.components.dashboards.statistical_dashboard import show_statistical_dashboard


def navigate(page, analyzer):
    """Navigates to the selected dashboard."""
    if page == "Executive Summary":
        show_executive_dashboard(analyzer)
    elif page == "Market Analysis":
        show_market_dashboard(analyzer)
    elif page == "Sales Performance":
        show_sales_dashboard(analyzer)
    elif page == "Statistical Analysis":
        show_statistical_dashboard(analyzer)