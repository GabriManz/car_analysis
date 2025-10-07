import streamlit as st
from src.components.dashboards.executive_dashboard import show_executive_dashboard
from src.components.dashboards.market_dashboard import show_market_dashboard
from src.components.dashboards.sales_dashboard import show_sales_dashboard


def navigate(page, analyzer):
    """Navigates to the selected dashboard."""
    if page == "Resumen Ejecutivo":
        show_executive_dashboard(analyzer)
    elif page == "Análisis de Mercado":
        show_market_dashboard(analyzer)
    elif page == "Rendimiento de Ventas":
        show_sales_dashboard(analyzer)


