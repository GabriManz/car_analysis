import streamlit as st

# --- INSTRUCCIONES ---
# Descomenta las siguientes líneas de importación UNA POR UNA, de arriba abajo.
# Guarda y sube el cambio a GitHub después de descomentar CADA LÍNEA.
# La ÚLTIMA línea que descomentes antes de que la app falle es la que contiene el error.

# --- PASO 1: Descomenta esta línea primero ---
from src.components.dashboards.executive_dashboard import show_executive_dashboard
st.success("✅ ROUTER PASO 1: 'executive_dashboard' importado correctamente.")

# --- PASO 2: Descomenta esta línea después ---
# from src.components.dashboards.market_dashboard import show_market_dashboard
# st.success("✅ ROUTER PASO 2: 'market_dashboard' importado correctamente.")

# --- PASO 3: Descomenta esta línea al final ---
# from src.components.dashboards.sales_dashboard import show_sales_dashboard
# st.success("✅ ROUTER PASO 3: 'sales_dashboard' importado correctamente.")


def navigate(page, analyzer):
    """Función de navegación de depuración. No se utiliza en este modo."""
    st.info("Modo de depuración del router activo.")
    st.write("Descomenta las importaciones en `src/router.py` una por una para encontrar el error.")