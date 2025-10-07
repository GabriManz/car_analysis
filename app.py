import streamlit as st
import warnings
warnings.filterwarnings('ignore')

# Configuration and styles
from src.config.app_config import APP_CONFIG, CUSTOM_CSS

# Core modules
from src.utils.state_manager import load_analyzer
from src.components.ui.header import render_header
from src.components.ui.sidebar import render_sidebar

st.set_page_config(
    page_title=APP_CONFIG['title'],
    page_icon=APP_CONFIG.get('icon', '🚗'),
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize analyzer (cached)
analyzer = load_analyzer()

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


