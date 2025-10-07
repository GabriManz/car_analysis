import streamlit as st

# Envuelve TODA la aplicación en un bloque try/except para garantizar la captura de cualquier error.
try:
    # ===================================================================
    # 1. IMPORTACIONES DEL PROYECTO
    # ===================================================================
    import pandas as pd
    import numpy as np
    from typing import Dict, List, Optional, Any
    import warnings
    warnings.filterwarnings('ignore')

    from src.utils.state_manager import load_analyzer
    from src.components.ui.header import render_header
    from src.components.ui.sidebar import render_sidebar
    from src.router import navigate
    from src.config.app_config import APP_CONFIG, CUSTOM_CSS

    # ===================================================================
    # 2. CONFIGURACIÓN E INICIALIZACIÓN DE LA APP
    # ===================================================================
    st.set_page_config(
        page_title=APP_CONFIG['title'],
        page_icon=APP_CONFIG['icon'],
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Inicializa el analizador (el punto más probable de fallo en ejecución)
    analyzer = load_analyzer()

    # ===================================================================
    # 3. LÓGICA PRINCIPAL DE LA APLICACIÓN
    # ===================================================================
    def main():
        """Aplicación principal."""
        render_header()
        _, _, page = render_sidebar(analyzer)
        navigate(page, analyzer)

    if __name__ == "__main__":
        main()

except Exception as e:
    # ===================================================================
    # 4. BLOQUE DE CAPTURA DE ERRORES
    # Si la aplicación llega aquí, hemos encontrado el error definitivo.
    # ===================================================================
    st.error("💥 Se ha producido un error fatal al iniciar la aplicación.")
    st.error("Este es el error definitivo que está causando el fallo. El traceback a continuación muestra el archivo y la línea exactos del problema:")
    st.exception(e) # Muestra el traceback completo del error en la pantalla.


