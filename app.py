import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

# --- INSTRUCCIONES ---
# Descomenta las siguientes líneas de importación UNA POR UNA.
# Después de descomentar CADA línea, sube el cambio a GitHub y comprueba
# si la aplicación de Streamlit se carga. Si la aplicación falla y no se carga,
# la ÚLTIMA línea que descomentaste es la que contiene el error.

st.set_page_config(
    page_title="App Debugger",
    layout="wide"
)

st.title("🐞 Debugger de la Aplicación")
st.write("Revisando las importaciones del proyecto...")

try:
    # --- PASO 1: Descomenta esta línea primero ---
    from src.config.app_config import APP_CONFIG, CUSTOM_CSS
    st.success("✅ PASO 1: `app_config` importado correctamente.")

    # --- PASO 2: Después, descomenta esta línea ---
    from src.utils.state_manager import load_analyzer
    st.success("✅ PASO 2: `state_manager` importado correctamente.")

    # --- PASO 3: Finalmente, descomenta esta línea ---
    # from src.router import navigate
    # st.success("✅ PASO 3: `router` importado correctamente.")

    st.balloons()
    st.header("¡ÉXITO! Todas las importaciones principales funcionan.")
    st.info("Ahora puedes restaurar tu archivo app.py original. El problema estaba en uno de los archivos que modificaste anteriormente y que ahora está corregido.")

except ImportError as e:
    st.error(f"❌ ¡ERROR DE IMPORTACIÓN ENCONTRADO! ❌")
    st.error(f"La última importación que descomentaste ha fallado.")
    st.error(f"El error es: **{e}**")
    st.info("Revisa el archivo correspondiente a la importación fallida y corrige sus propias importaciones internas (probablemente una ruta relativa que necesita ser absoluta).")

except Exception as e:
    st.error(f"❌ ¡HA OCURRIDO UN ERROR INESPERADO! ❌")
    st.error(f"El error es: **{e}**")


