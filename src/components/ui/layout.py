"""
🎨 UI Layout Component for Car Market Analysis Executive Dashboard

Professional layout components with executive-grade styling and responsive design.
Handles page configuration, headers, metric cards, and custom CSS.
"""

import streamlit as st
from typing import Dict, List, Optional, Any
import pandas as pd

# Import configuration
try:
    from ..config.app_config import APP_CONFIG, CUSTOM_CSS, COLOR_PALETTE
except ImportError:
    # Fallback configuration
    APP_CONFIG = {
        'title': 'Car Market Analysis Dashboard',
        'subtitle': 'Strategic Business Intelligence',
        'page_icon': '🚗',
        'layout': 'wide'
    }
    CUSTOM_CSS = ""
    COLOR_PALETTE = {
        'primary': '#1f77b4',
        'secondary': '#0a9396',
        'success': '#2ca02c',
        'danger': '#d62728',
        'warning': '#ff7f0e'
    }


class LayoutComponent:
    """
    🏗️ Executive-Grade Layout Component
    
    Provides professional layout functionality with responsive design,
    executive styling, and customizable components for the dashboard.
    """

    def __init__(self):
        """Initialize the LayoutComponent with configuration."""
        self.app_config = APP_CONFIG
        self.custom_css = CUSTOM_CSS
        self.color_palette = COLOR_PALETTE

    def setup_page_config(self) -> None:
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title=self.app_config['title'],
            page_icon=self.app_config['page_icon'],
            layout=self.app_config['layout'],
            initial_sidebar_state=self.app_config.get('sidebar_state', 'expanded')
        )

    def inject_custom_css(self) -> None:
        """Inject custom CSS for executive styling."""
        if self.custom_css:
            st.markdown(self.custom_css, unsafe_allow_html=True)

    def create_main_header(self, title: Optional[str] = None, subtitle: Optional[str] = None) -> None:
        """Create the main dashboard header with professional styling."""
        header_title = title or self.app_config['title']
        header_subtitle = subtitle or self.app_config['subtitle']
        
        st.markdown(f"""
        <div class="main-header">
            <h1>{header_title}</h1>
            <p>{header_subtitle}</p>
        </div>
        """, unsafe_allow_html=True)

    def create_section_header(self, title: str, description: Optional[str] = None) -> None:
        """Create a section header with optional description."""
        st.markdown(f"### {title}")
        if description:
            st.markdown(f"*{description}*")
        st.markdown("---")

    def create_metric_card(self, label: str, value: Any, delta: Optional[Any] = None, 
                          delta_color: str = "normal") -> None:
        """Create a professional metric card."""
        # Format value based on type
        if isinstance(value, (int, float)):
            if isinstance(value, float):
                formatted_value = f"{value:,.2f}"
            else:
                formatted_value = f"{value:,}"
        else:
            formatted_value = str(value)
        
        # Format delta if provided
        delta_text = ""
        if delta is not None:
            if isinstance(delta, (int, float)):
                delta_text = f" ({delta:+,.1f})"
            else:
                delta_text = f" ({delta})"
        
        # Create metric with Streamlit's built-in metric component
        st.metric(
            label=label,
            value=formatted_value,
            delta=delta_text if delta else None
        )

    def create_kpi_row(self, kpis: List[Dict[str, Any]], columns: int = 3) -> None:
        """Create a row of KPI metric cards."""
        if not kpis:
            return
        
        # Create columns
        cols = st.columns(min(columns, len(kpis)))
        
        for i, kpi in enumerate(kpis):
            with cols[i % len(cols)]:
                self.create_metric_card(
                    label=kpi.get('label', 'KPI'),
                    value=kpi.get('value', 0),
                    delta=kpi.get('delta'),
                    delta_color=kpi.get('delta_color', 'normal')
                )

    def create_info_box(self, message: str, message_type: str = "info") -> None:
        """Create an informational box with different types."""
        type_config = {
            "info": {"icon": "ℹ️", "color": self.color_palette.get('info', '#17a2b8')},
            "success": {"icon": "✅", "color": self.color_palette.get('success', '#28a745')},
            "warning": {"icon": "⚠️", "color": self.color_palette.get('warning', '#ffc107')},
            "error": {"icon": "❌", "color": self.color_palette.get('danger', '#dc3545')}
        }
        
        config = type_config.get(message_type, type_config["info"])
        
        st.markdown(f"""
        <div style="
            padding: 1rem;
            background-color: {config['color']}20;
            border-left: 4px solid {config['color']};
            border-radius: 0.5rem;
            margin: 1rem 0;
        ">
            <strong>{config['icon']} {message}</strong>
        </div>
        """, unsafe_allow_html=True)

    def create_loading_spinner(self, text: str = "Loading...") -> None:
        """Create a loading spinner with custom text."""
        with st.spinner(text):
            pass

    def create_progress_bar(self, progress: float, text: str = "Progress") -> None:
        """Create a progress bar with custom styling."""
        st.progress(progress)
        st.caption(f"{text}: {progress:.1%}")

    def create_expander(self, title: str, content: Any, expanded: bool = False) -> None:
        """Create an expandable section."""
        with st.expander(title, expanded=expanded):
            if callable(content):
                content()
            else:
                st.write(content)

    def create_tabs(self, tabs_config: List[Dict[str, Any]]) -> None:
        """Create tabs with custom configuration."""
        tab_names = [tab['name'] for tab in tabs_config]
        tab_contents = [tab['content'] for tab in tabs_config]
        
        tabs = st.tabs(tab_names)
        
        for i, (tab, content) in enumerate(zip(tabs, tab_contents)):
            with tab:
                if callable(content):
                    content()
                else:
                    st.write(content)

    def create_columns(self, num_columns: int, gap: str = "medium") -> List:
        """Create responsive columns with consistent spacing."""
        return st.columns(num_columns, gap=gap)

    def create_container(self, border: bool = False) -> Any:
        """Create a container with optional border."""
        if border:
            return st.container()
        else:
            return st.container()

    def create_spacer(self, height: int = 1) -> None:
        """Create vertical spacing."""
        for _ in range(height):
            st.markdown("")

    def create_divider(self, style: str = "thick") -> None:
        """Create a visual divider."""
        if style == "thick":
            st.markdown("---")
        elif style == "thin":
            st.markdown("***")
        elif style == "space":
            st.markdown("")

    def create_badge(self, text: str, color: str = "primary") -> None:
        """Create a colored badge."""
        color_map = {
            "primary": self.color_palette.get('primary', '#007bff'),
            "secondary": self.color_palette.get('secondary', '#6c757d'),
            "success": self.color_palette.get('success', '#28a745'),
            "danger": self.color_palette.get('danger', '#dc3545'),
            "warning": self.color_palette.get('warning', '#ffc107'),
            "info": self.color_palette.get('info', '#17a2b8')
        }
        
        badge_color = color_map.get(color, color_map["primary"])
        
        st.markdown(f"""
        <span style="
            background-color: {badge_color};
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            font-size: 0.875rem;
            font-weight: 500;
        ">{text}</span>
        """, unsafe_allow_html=True)

    def create_status_indicator(self, status: str, text: str) -> None:
        """Create a status indicator with color coding."""
        status_config = {
            "online": {"color": "#28a745", "icon": "🟢"},
            "offline": {"color": "#dc3545", "icon": "🔴"},
            "warning": {"color": "#ffc107", "icon": "🟡"},
            "info": {"color": "#17a2b8", "icon": "🔵"}
        }
        
        config = status_config.get(status, status_config["info"])
        
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem;
            background-color: {config['color']}20;
            border-radius: 0.25rem;
        ">
            <span>{config['icon']}</span>
            <span>{text}</span>
        </div>
        """, unsafe_allow_html=True)

    def create_data_table(self, data: pd.DataFrame, title: Optional[str] = None, 
                         height: int = 400) -> None:
        """Create a styled data table."""
        if title:
            st.subheader(title)
        
        if data.empty:
            st.info("No data available to display.")
            return
        
        st.dataframe(
            data,
            height=height,
            use_container_width=True,
            hide_index=True
        )

    def create_download_button(self, data: pd.DataFrame, filename: str, 
                              file_format: str = "csv") -> None:
        """Create a download button for data export."""
        if data.empty:
            st.warning("No data available for download.")
            return
        
        if file_format.lower() == "csv":
            csv_data = data.to_csv(index=False)
            st.download_button(
                label=f"Download {filename}.csv",
                data=csv_data,
                file_name=f"{filename}.csv",
                mime="text/csv"
            )
        elif file_format.lower() == "xlsx":
            # Note: This would require openpyxl or xlsxwriter
            st.info("Excel export requires additional dependencies.")
        else:
            st.warning(f"Unsupported file format: {file_format}")

    def create_filter_panel(self, filters: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a filter panel and return filter values."""
        st.sidebar.header("🔍 Filters")
        
        filter_values = {}
        
        for filter_config in filters:
            filter_type = filter_config.get('type', 'selectbox')
            filter_name = filter_config.get('name', 'filter')
            filter_label = filter_config.get('label', filter_name)
            filter_options = filter_config.get('options', [])
            filter_default = filter_config.get('default', None)
            
            if filter_type == 'selectbox':
                filter_values[filter_name] = st.sidebar.selectbox(
                    filter_label,
                    options=filter_options,
                    index=filter_options.index(filter_default) if filter_default in filter_options else 0
                )
            elif filter_type == 'multiselect':
                filter_values[filter_name] = st.sidebar.multiselect(
                    filter_label,
                    options=filter_options,
                    default=filter_default if filter_default else filter_options[:5]
                )
            elif filter_type == 'slider':
                filter_values[filter_name] = st.sidebar.slider(
                    filter_label,
                    min_value=filter_config.get('min', 0),
                    max_value=filter_config.get('max', 100),
                    value=filter_config.get('default', 50),
                    step=filter_config.get('step', 1)
                )
            elif filter_type == 'date_input':
                filter_values[filter_name] = st.sidebar.date_input(
                    filter_label,
                    value=filter_config.get('default')
                )
        
        return filter_values

    def create_navigation_menu(self, menu_items: List[Dict[str, Any]]) -> str:
        """Create a navigation menu and return selected item."""
        st.sidebar.header("🧭 Navigation")
        
        menu_options = [item['name'] for item in menu_items]
        default_index = 0
        
        # Find default selected item
        for i, item in enumerate(menu_items):
            if item.get('default', False):
                default_index = i
                break
        
        selected = st.sidebar.radio(
            "Select Dashboard",
            options=menu_options,
            index=default_index
        )
        
        return selected

    def create_sidebar_footer(self, footer_text: str = "Car Market Analysis Dashboard") -> None:
        """Create a footer for the sidebar."""
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"""
        <div style="
            text-align: center;
            color: #666;
            font-size: 0.8rem;
            padding: 1rem 0;
        ">
            {footer_text}
        </div>
        """, unsafe_allow_html=True)

    def setup_executive_layout(self) -> None:
        """Setup the complete executive layout with all components."""
        # Configure page
        self.setup_page_config()
        
        # Inject custom CSS
        self.inject_custom_css()
        
        # Create main header
        self.create_main_header()
        
        # Create status indicator
        self.create_status_indicator("online", "System Online")

    def get_layout_config(self) -> Dict[str, Any]:
        """Get the current layout configuration."""
        return {
            'app_config': self.app_config,
            'color_palette': self.color_palette,
            'has_custom_css': bool(self.custom_css)
        }


# Global instance for use throughout the application
layout_component = LayoutComponent()

