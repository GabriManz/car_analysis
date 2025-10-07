import streamlit as st
import warnings
warnings.filterwarnings('ignore')

try:
    from src.config.app_config import APP_CONFIG, CUSTOM_CSS
    st.set_page_config(
        page_title=APP_CONFIG['title'],
        page_icon=APP_CONFIG.get('icon', '🚗'),
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
except Exception as e:
    # Fallback minimal config to ensure UI renders error
    st.set_page_config(page_title="App", layout="wide")
    st.error("❌ Error importando configuración (src.config.app_config)")
    st.exception(e)
    st.stop()

try:
    from src.utils.state_manager import load_analyzer
    analyzer = load_analyzer()
except Exception as e:
    st.error("❌ Error inicializando el analizador (src.utils.state_manager)")
    st.exception(e)
    st.stop()

try:
    from src.components.ui.header import render_header
    from src.components.ui.sidebar import render_sidebar
except Exception as e:
    st.error("❌ Error importando componentes de UI (header/sidebar)")
    st.exception(e)
    st.stop()

def main():
    """Main application."""
    render_header()
    _, _, page = render_sidebar(analyzer)

    # Deferred import of router to surface precise import errors in UI
    try:
        from src.router import navigate
    except Exception as e:
        st.error("❌ Error importando el enrutador (src.router). Revisa las importaciones internas.")
        st.exception(e)
        st.stop()

    navigate(page, analyzer)

if __name__ == "__main__":
    main()


