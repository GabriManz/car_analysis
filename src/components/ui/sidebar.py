"""
🧭 UI Sidebar Component for Car Market Analysis Executive Dashboard

Interactive sidebar with navigation, filters, and controls for the dashboard.
Provides user interface elements for data filtering and navigation.
"""

import streamlit as st
from typing import Dict, List, Optional, Any, Callable
import pandas as pd

# Import configuration
try:
    from ..config.app_config import DASHBOARD_MODULES, COLOR_PALETTE
except ImportError:
    # Fallback configuration
    DASHBOARD_MODULES = [
        "Executive Summary",
        "Market Analysis", 
        "Sales Analytics",
        "Price Intelligence"
    ]
    COLOR_PALETTE = {
        'primary': '#1f77b4',
        'secondary': '#0a9396',
        'success': '#2ca02c',
        'danger': '#d62728',
        'warning': '#ff7f0e'
    }


class SidebarComponent:
    """
    🎛️ Executive-Grade Sidebar Component
    
    Provides interactive sidebar functionality with navigation,
    filtering, and control elements for the dashboard.
    """

    def __init__(self):
        """Initialize the SidebarComponent with configuration."""
        self.dashboard_modules = DASHBOARD_MODULES
        self.color_palette = COLOR_PALETTE
        self.filter_state = {}

    def create_navigation(self, selected_module: Optional[str] = None) -> str:
        """Create navigation menu and return selected module."""
        st.sidebar.header("🧭 Navigation")
        
        # Create radio buttons for navigation
        selected = st.sidebar.radio(
            "Select Dashboard Module",
            options=self.dashboard_modules,
            index=self.dashboard_modules.index(selected_module) if selected_module in self.dashboard_modules else 0,
            help="Choose the dashboard module to display"
        )
        
        # Add navigation styling
        st.sidebar.markdown("""
        <style>
        .sidebar .stRadio > div > label {
            font-weight: 500;
            padding: 0.5rem;
            border-radius: 0.25rem;
            transition: all 0.3s ease;
        }
        .sidebar .stRadio > div > label:hover {
            background-color: rgba(0, 18, 25, 0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        return selected

    def create_automaker_filter(self, automaker_list: List[str], 
                               default_selection: Optional[List[str]] = None) -> List[str]:
        """Create automaker filter with multiselect."""
        st.sidebar.subheader("🚗 Automaker Filter")
        
        if not automaker_list:
            st.sidebar.info("No automakers available")
            return []
        
        # Set default selection
        if default_selection is None:
            default_selection = automaker_list[:5] if len(automaker_list) >= 5 else automaker_list
        
        # Create multiselect
        selected_automakers = st.sidebar.multiselect(
            "Select Automakers",
            options=automaker_list,
            default=default_selection,
            help="Choose one or more automakers to analyze",
            key="automaker_filter"
        )
        
        # Store in filter state
        self.filter_state['automakers'] = selected_automakers
        
        return selected_automakers

    def create_model_filter(self, model_list: List[str], 
                           default_selection: Optional[List[str]] = None) -> List[str]:
        """Create model filter with search functionality."""
        st.sidebar.subheader("🏷️ Model Filter")
        
        if not model_list:
            st.sidebar.info("No models available")
            return []
        
        # Create search box
        search_term = st.sidebar.text_input(
            "Search Models",
            placeholder="Type to search models...",
            help="Filter models by name",
            key="model_search"
        )
        
        # Filter models based on search
        filtered_models = model_list
        if search_term:
            filtered_models = [model for model in model_list if search_term.lower() in model.lower()]
        
        # Set default selection
        if default_selection is None:
            default_selection = filtered_models[:10] if len(filtered_models) >= 10 else filtered_models
        
        # Create multiselect
        selected_models = st.sidebar.multiselect(
            "Select Models",
            options=filtered_models,
            default=default_selection,
            help="Choose specific models to analyze",
            key="model_filter"
        )
        
        # Store in filter state
        self.filter_state['models'] = selected_models
        
        return selected_models

    def create_year_filter(self, year_range: tuple = (2001, 2020), 
                          default_range: Optional[tuple] = None) -> tuple:
        """Create year range filter with slider."""
        st.sidebar.subheader("📅 Year Range Filter")
        
        if default_range is None:
            default_range = year_range
        
        # Create slider for year range
        selected_range = st.sidebar.slider(
            "Select Year Range",
            min_value=year_range[0],
            max_value=year_range[1],
            value=default_range,
            step=1,
            help="Choose the year range for analysis",
            key="year_filter"
        )
        
        # Store in filter state
        self.filter_state['year_range'] = selected_range
        
        return selected_range

    def create_price_filter(self, price_range: Optional[tuple] = None) -> tuple:
        """Create price range filter with slider."""
        st.sidebar.subheader("💰 Price Range Filter")
        
        if price_range is None:
            price_range = (0, 500000)
        
        # Create slider for price range
        selected_range = st.sidebar.slider(
            "Select Price Range (€)",
            min_value=price_range[0],
            max_value=price_range[1],
            value=price_range,
            step=1000,
            help="Choose the price range for analysis",
            key="price_filter"
        )
        
        # Store in filter state
        self.filter_state['price_range'] = selected_range
        
        return selected_range

    def create_top_n_filter(self, max_items: int = 50, default_items: int = 20) -> int:
        """Create top N items filter."""
        st.sidebar.subheader("📊 Display Options")
        
        top_n = st.sidebar.slider(
            "Show Top N Items",
            min_value=5,
            max_value=max_items,
            value=default_items,
            step=5,
            help="Number of top items to display",
            key="top_n_filter"
        )
        
        # Store in filter state
        self.filter_state['top_n'] = top_n
        
        return top_n

    def create_chart_type_filter(self, chart_types: List[str] = None) -> str:
        """Create chart type selection filter."""
        st.sidebar.subheader("📈 Chart Options")
        
        if chart_types is None:
            chart_types = ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Heatmap"]
        
        selected_chart = st.sidebar.selectbox(
            "Chart Type",
            options=chart_types,
            help="Choose the type of chart to display",
            key="chart_type_filter"
        )
        
        # Store in filter state
        self.filter_state['chart_type'] = selected_chart
        
        return selected_chart

    def create_data_export_section(self) -> Dict[str, Any]:
        """Create data export controls."""
        st.sidebar.subheader("📤 Export Options")
        
        export_options = {}
        
        # Export format selection
        export_format = st.sidebar.selectbox(
            "Export Format",
            options=["CSV", "Excel", "JSON"],
            help="Choose the export format",
            key="export_format"
        )
        export_options['format'] = export_format
        
        # Export button
        if st.sidebar.button("Export Current Data", key="export_button"):
            export_options['action'] = 'export'
        
        return export_options

    def create_refresh_controls(self) -> Dict[str, Any]:
        """Create refresh and update controls."""
        st.sidebar.subheader("🔄 Refresh Controls")
        
        refresh_options = {}
        
        # Refresh data button
        if st.sidebar.button("🔄 Refresh Data", key="refresh_data"):
            refresh_options['refresh_data'] = True
        
        # Clear filters button
        if st.sidebar.button("🗑️ Clear Filters", key="clear_filters"):
            refresh_options['clear_filters'] = True
        
        # Reset to defaults button
        if st.sidebar.button("⚙️ Reset to Defaults", key="reset_defaults"):
            refresh_options['reset_defaults'] = True
        
        return refresh_options

    def create_advanced_filters(self, filter_configs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create advanced filters based on configuration."""
        st.sidebar.subheader("🔧 Advanced Filters")
        
        advanced_filters = {}
        
        for config in filter_configs:
            filter_name = config.get('name', 'filter')
            filter_type = config.get('type', 'selectbox')
            filter_label = config.get('label', filter_name)
            filter_options = config.get('options', [])
            filter_default = config.get('default')
            
            if filter_type == 'selectbox':
                advanced_filters[filter_name] = st.sidebar.selectbox(
                    filter_label,
                    options=filter_options,
                    index=filter_options.index(filter_default) if filter_default in filter_options else 0,
                    key=f"advanced_{filter_name}"
                )
            elif filter_type == 'multiselect':
                advanced_filters[filter_name] = st.sidebar.multiselect(
                    filter_label,
                    options=filter_options,
                    default=filter_default if filter_default else [],
                    key=f"advanced_{filter_name}"
                )
            elif filter_type == 'slider':
                advanced_filters[filter_name] = st.sidebar.slider(
                    filter_label,
                    min_value=config.get('min', 0),
                    max_value=config.get('max', 100),
                    value=config.get('default', 50),
                    step=config.get('step', 1),
                    key=f"advanced_{filter_name}"
                )
            elif filter_type == 'checkbox':
                advanced_filters[filter_name] = st.sidebar.checkbox(
                    filter_label,
                    value=config.get('default', False),
                    key=f"advanced_{filter_name}"
                )
        
        # Store in filter state
        self.filter_state['advanced'] = advanced_filters
        
        return advanced_filters

    def create_filter_summary(self) -> None:
        """Display a summary of current filters."""
        st.sidebar.subheader("📋 Filter Summary")
        
        if not self.filter_state:
            st.sidebar.info("No filters applied")
            return
        
        summary_items = []
        
        if 'automakers' in self.filter_state and self.filter_state['automakers']:
            summary_items.append(f"Automakers: {len(self.filter_state['automakers'])} selected")
        
        if 'models' in self.filter_state and self.filter_state['models']:
            summary_items.append(f"Models: {len(self.filter_state['models'])} selected")
        
        if 'year_range' in self.filter_state:
            year_range = self.filter_state['year_range']
            summary_items.append(f"Years: {year_range[0]}-{year_range[1]}")
        
        if 'price_range' in self.filter_state:
            price_range = self.filter_state['price_range']
            summary_items.append(f"Price: €{price_range[0]:,}-€{price_range[1]:,}")
        
        if 'top_n' in self.filter_state:
            summary_items.append(f"Top N: {self.filter_state['top_n']}")
        
        if summary_items:
            for item in summary_items:
                st.sidebar.caption(f"• {item}")
        else:
            st.sidebar.info("No filters applied")

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

    def get_filter_state(self) -> Dict[str, Any]:
        """Get the current filter state."""
        return self.filter_state.copy()

    def clear_filter_state(self) -> None:
        """Clear all filter states."""
        self.filter_state = {}

    def set_filter_state(self, filters: Dict[str, Any]) -> None:
        """Set filter state from external source."""
        self.filter_state = filters.copy()

    def create_complete_sidebar(self, automaker_list: List[str], 
                               model_list: List[str] = None,
                               year_range: tuple = (2001, 2020),
                               price_range: tuple = (0, 500000)) -> Dict[str, Any]:
        """Create a complete sidebar with all standard filters."""
        
        # Navigation
        selected_module = self.create_navigation()
        
        # Basic filters
        selected_automakers = self.create_automaker_filter(automaker_list)
        
        if model_list:
            selected_models = self.create_model_filter(model_list)
        else:
            selected_models = []
        
        selected_years = self.create_year_filter(year_range)
        selected_prices = self.create_price_filter(price_range)
        top_n = self.create_top_n_filter()
        
        # Chart options
        chart_type = self.create_chart_type_filter()
        
        # Export and refresh controls
        export_options = self.create_data_export_section()
        refresh_options = self.create_refresh_controls()
        
        # Filter summary
        self.create_filter_summary()
        
        # Footer
        self.create_sidebar_footer()
        
        # Return all filter values
        return {
            'selected_module': selected_module,
            'automakers': selected_automakers,
            'models': selected_models,
            'year_range': selected_years,
            'price_range': selected_prices,
            'top_n': top_n,
            'chart_type': chart_type,
            'export_options': export_options,
            'refresh_options': refresh_options,
            'filter_state': self.get_filter_state()
        }

    def create_minimal_sidebar(self, automaker_list: List[str]) -> Dict[str, Any]:
        """Create a minimal sidebar with essential filters only."""
        
        # Navigation
        selected_module = self.create_navigation()
        
        # Essential filters only
        selected_automakers = self.create_automaker_filter(automaker_list)
        top_n = self.create_top_n_filter()
        
        # Filter summary
        self.create_filter_summary()
        
        # Footer
        self.create_sidebar_footer()
        
        return {
            'selected_module': selected_module,
            'automakers': selected_automakers,
            'top_n': top_n,
            'filter_state': self.get_filter_state()
        }


# Global instance for use throughout the application
sidebar_component = SidebarComponent()


def render_sidebar(analyzer):
    """Renders the sidebar with filters and navigation, returns user selections."""
    with st.sidebar:
        st.markdown("## 🔧 Filters")

        try:
            automaker_list = analyzer.get_automaker_list()
        except Exception as e:
            st.error(f"Error getting automaker list: {e}")
            automaker_list = []

        if automaker_list:
            selected_automakers = st.multiselect(
                'Select Automakers (leave empty to show all)',
                options=automaker_list,
                default=[],
                key='filter_automakers'
            )
            top_n = st.slider(
                'Top N Results',
                min_value=5, max_value=50, value=15, step=5,
                key='filter_top_n'
            )
        else:
            st.warning("No automaker data available")
            selected_automakers = []
            top_n = 15

        page = st.sidebar.radio(
            "Selecciona un Dashboard",
            ["Resumen Ejecutivo", "Análisis de Mercado", "Rendimiento de Ventas"]
        )

    return selected_automakers, top_n, page
