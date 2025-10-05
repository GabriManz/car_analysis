"""
📱 Responsive Design Utility Component for Car Market Analysis Executive Dashboard

Advanced responsive design system providing mobile and tablet optimization,
adaptive layouts, touch-friendly controls, and cross-device compatibility.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple, Callable
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

# Import components
try:
    from ..config.app_config import COLOR_PALETTE
except ImportError:
    COLOR_PALETTE = {
        'primary': '#1f77b4',
        'secondary': '#0a9396',
        'success': '#2ca02c',
        'danger': '#d62728',
        'warning': '#ff7f0e',
        'info': '#17a2b8'
    }


class DeviceInfo:
    """Device information and capabilities."""
    
    def __init__(self, width: int, height: int, device_type: str, touch_capable: bool = False):
        """Initialize device info."""
        self.width = width
        self.height = height
        self.device_type = device_type
        self.touch_capable = touch_capable
        self.aspect_ratio = width / height if height > 0 else 1.0

    def is_mobile(self) -> bool:
        """Check if device is mobile."""
        return self.device_type == 'mobile' or self.width < 768

    def is_tablet(self) -> bool:
        """Check if device is tablet."""
        return self.device_type == 'tablet' or (768 <= self.width < 1024)

    def is_desktop(self) -> bool:
        """Check if device is desktop."""
        return self.device_type == 'desktop' or self.width >= 1024

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'width': self.width,
            'height': self.height,
            'device_type': self.device_type,
            'touch_capable': self.touch_capable,
            'aspect_ratio': self.aspect_ratio,
            'is_mobile': self.is_mobile(),
            'is_tablet': self.is_tablet(),
            'is_desktop': self.is_desktop()
        }


class ResponsiveLayout:
    """Responsive layout configuration."""
    
    def __init__(self, device_info: DeviceInfo):
        """Initialize responsive layout."""
        self.device_info = device_info
        self.layout_config = self._get_layout_config()

    def _get_layout_config(self) -> Dict[str, Any]:
        """Get layout configuration based on device."""
        if self.device_info.is_mobile():
            return {
                'sidebar_state': 'collapsed',
                'main_content_padding': '1rem',
                'chart_height': 300,
                'chart_width': '100%',
                'columns_per_row': 1,
                'font_size_small': '0.8rem',
                'font_size_medium': '1rem',
                'font_size_large': '1.2rem',
                'button_size': 'small',
                'input_height': '2rem',
                'spacing': '0.5rem'
            }
        elif self.device_info.is_tablet():
            return {
                'sidebar_state': 'auto',
                'main_content_padding': '1.5rem',
                'chart_height': 400,
                'chart_width': '100%',
                'columns_per_row': 2,
                'font_size_small': '0.9rem',
                'font_size_medium': '1.1rem',
                'font_size_large': '1.3rem',
                'button_size': 'medium',
                'input_height': '2.2rem',
                'spacing': '0.75rem'
            }
        else:  # Desktop
            return {
                'sidebar_state': 'expanded',
                'main_content_padding': '2rem',
                'chart_height': 500,
                'chart_width': '100%',
                'columns_per_row': 3,
                'font_size_small': '1rem',
                'font_size_medium': '1.2rem',
                'font_size_large': '1.5rem',
                'button_size': 'large',
                'input_height': '2.5rem',
                'spacing': '1rem'
            }

    def get_columns(self, num_items: int) -> List[st.container]:
        """Get responsive columns for layout."""
        columns_per_row = self.layout_config['columns_per_row']
        actual_columns = min(num_items, columns_per_row)
        
        return st.columns(actual_columns)

    def get_chart_config(self) -> Dict[str, Any]:
        """Get responsive chart configuration."""
        return {
            'height': self.layout_config['chart_height'],
            'width': self.layout_config['chart_width'],
            'responsive': True,
            'showlegend': not self.device_info.is_mobile()
        }

    def get_button_config(self) -> Dict[str, Any]:
        """Get responsive button configuration."""
        return {
            'size': self.layout_config['button_size'],
            'use_container_width': self.device_info.is_mobile(),
            'type': 'primary'
        }


class ResponsiveDesign:
    """
    📱 Executive-Grade Responsive Design System
    
    Provides comprehensive responsive design capabilities including
    device detection, adaptive layouts, touch-friendly controls,
    and cross-device optimization.
    """

    def __init__(self):
        """Initialize responsive design system."""
        self.device_info = None
        self.layout = None
        self.responsive_css = ""
        
        # Device detection
        self._detect_device()
        
        # Initialize responsive layout
        if self.device_info:
            self.layout = ResponsiveLayout(self.device_info)
        
        # Generate responsive CSS
        self._generate_responsive_css()

    def _detect_device(self) -> None:
        """Detect device type and capabilities."""
        # In Streamlit, we can't directly detect device info
        # We'll use a heuristic approach based on available screen space
        
        # Default to desktop for now
        # In a real implementation, this would use JavaScript to detect
        self.device_info = DeviceInfo(
            width=1024,  # Default desktop width
            height=768,  # Default desktop height
            device_type='desktop',
            touch_capable=False
        )

    def _generate_responsive_css(self) -> None:
        """Generate responsive CSS styles."""
        self.responsive_css = f"""
        <style>
        /* Responsive Design Styles */
        
        /* Mobile Styles */
        @media (max-width: 767px) {{
            .main-header h1 {{
                font-size: 1.5rem !important;
                text-align: center;
            }}
            
            .main-header p {{
                font-size: 0.9rem !important;
                text-align: center;
            }}
            
            .stMetric {{
                margin-bottom: 0.5rem;
            }}
            
            .stMetric > div {{
                padding: 0.5rem;
                border-radius: 8px;
            }}
            
            .stMetric label {{
                font-size: 0.8rem !important;
            }}
            
            .stMetric [data-testid="metric-value"] {{
                font-size: 1.2rem !important;
            }}
            
            .stDataFrame {{
                font-size: 0.8rem;
            }}
            
            .stButton > button {{
                width: 100%;
                height: 2.5rem;
                font-size: 1rem;
                border-radius: 8px;
            }}
            
            .stSelectbox > div > div {{
                font-size: 0.9rem;
            }}
            
            .stSlider > div > div {{
                font-size: 0.9rem;
            }}
            
            .stMultiSelect > div > div {{
                font-size: 0.9rem;
            }}
            
            /* Touch-friendly spacing */
            .stElement {{
                margin-bottom: 1rem;
            }}
            
            /* Compact sidebar for mobile */
            .css-1d391kg {{
                padding-top: 1rem;
            }}
            
            /* Responsive charts */
            .js-plotly-plot {{
                height: 300px !important;
            }}
        }}
        
        /* Tablet Styles */
        @media (min-width: 768px) and (max-width: 1023px) {{
            .main-header h1 {{
                font-size: 1.8rem !important;
            }}
            
            .main-header p {{
                font-size: 1rem !important;
            }}
            
            .stMetric {{
                margin-bottom: 0.75rem;
            }}
            
            .stMetric > div {{
                padding: 0.75rem;
                border-radius: 10px;
            }}
            
            .stMetric label {{
                font-size: 0.9rem !important;
            }}
            
            .stMetric [data-testid="metric-value"] {{
                font-size: 1.4rem !important;
            }}
            
            .stButton > button {{
                height: 2.2rem;
                font-size: 1rem;
                border-radius: 8px;
            }}
            
            /* Responsive charts for tablet */
            .js-plotly-plot {{
                height: 400px !important;
            }}
        }}
        
        /* Desktop Styles */
        @media (min-width: 1024px) {{
            .main-header h1 {{
                font-size: 2.5rem !important;
            }}
            
            .main-header p {{
                font-size: 1.2rem !important;
            }}
            
            .stMetric {{
                margin-bottom: 1rem;
            }}
            
            .stMetric > div {{
                padding: 1rem;
                border-radius: 12px;
            }}
            
            .stMetric label {{
                font-size: 1rem !important;
            }}
            
            .stMetric [data-testid="metric-value"] {{
                font-size: 1.8rem !important;
            }}
            
            .stButton > button {{
                height: 2.5rem;
                font-size: 1.1rem;
                border-radius: 10px;
            }}
            
            /* Responsive charts for desktop */
            .js-plotly-plot {{
                height: 500px !important;
            }}
        }}
        
        /* Common Responsive Styles */
        
        /* Flexible grid system */
        .responsive-grid {{
            display: grid;
            gap: 1rem;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        }}
        
        /* Responsive text */
        .responsive-text {{
            font-size: clamp(0.8rem, 2.5vw, 1.2rem);
            line-height: 1.5;
        }}
        
        /* Responsive spacing */
        .responsive-spacing {{
            padding: clamp(0.5rem, 2vw, 2rem);
            margin: clamp(0.25rem, 1vw, 1rem);
        }}
        
        /* Touch-friendly buttons */
        .touch-friendly {{
            min-height: 44px;
            min-width: 44px;
            touch-action: manipulation;
        }}
        
        /* Responsive tables */
        .responsive-table {{
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }}
        
        /* Responsive images */
        .responsive-image {{
            max-width: 100%;
            height: auto;
        }}
        
        /* Responsive containers */
        .responsive-container {{
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }}
        
        /* Mobile navigation */
        @media (max-width: 767px) {{
            .mobile-nav {{
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: {COLOR_PALETTE.get('surface', '#005F73')};
                padding: 0.5rem;
                border-top: 1px solid {COLOR_PALETTE.get('primary', '#0A9396')};
                z-index: 1000;
            }}
            
            .mobile-nav button {{
                flex: 1;
                margin: 0 0.25rem;
                padding: 0.5rem;
                background: {COLOR_PALETTE.get('primary', '#0A9396')};
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 0.8rem;
            }}
            
            .mobile-nav button:hover {{
                background: {COLOR_PALETTE.get('secondary', '#94D2BD')};
            }}
            
            /* Add bottom padding to main content for mobile nav */
            .main .block-container {{
                padding-bottom: 4rem;
            }}
        }}
        
        /* Print styles */
        @media print {{
            .no-print {{
                display: none !important;
            }}
            
            .main-header {{
                page-break-after: avoid;
            }}
            
            .stMetric {{
                page-break-inside: avoid;
            }}
        }}
        
        /* Accessibility improvements */
        @media (prefers-reduced-motion: reduce) {{
            * {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}
        
        @media (prefers-color-scheme: light) {{
            .stApp {{
                background-color: #ffffff;
                color: #000000;
            }}
        }}
        
        @media (prefers-color-scheme: dark) {{
            .stApp {{
                background-color: {COLOR_PALETTE.get('background', '#001219')};
                color: {COLOR_PALETTE.get('text', '#E9D8A6')};
            }}
        }}
        </style>
        """

    def inject_responsive_css(self) -> None:
        """Inject responsive CSS into Streamlit."""
        st.markdown(self.responsive_css, unsafe_allow_html=True)

    def get_responsive_columns(self, num_items: int) -> List[st.container]:
        """Get responsive columns based on device type."""
        if self.layout:
            return self.layout.get_columns(num_items)
        else:
            # Fallback to standard columns
            return st.columns(num_items)

    def get_responsive_chart_config(self) -> Dict[str, Any]:
        """Get responsive chart configuration."""
        if self.layout:
            return self.layout.get_chart_config()
        else:
            return {'height': 400, 'width': '100%', 'responsive': True}

    def get_responsive_button_config(self) -> Dict[str, Any]:
        """Get responsive button configuration."""
        if self.layout:
            return self.layout.get_button_config()
        else:
            return {'use_container_width': False, 'type': 'primary'}

    def render_responsive_metric(self, label: str, value: str, delta: str = None) -> None:
        """Render responsive metric card."""
        if self.device_info and self.device_info.is_mobile():
            # Mobile: full width, compact design
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**{label}**")
            with col2:
                st.markdown(f"**{value}**")
            with col3:
                if delta:
                    st.markdown(f"*{delta}*")
        else:
            # Desktop/Tablet: standard metric
            st.metric(label, value, delta)

    def render_responsive_chart(self, chart_figure, chart_type: str = "plotly") -> None:
        """Render responsive chart."""
        chart_config = self.get_responsive_chart_config()
        
        if chart_type == "plotly":
            st.plotly_chart(
                chart_figure,
                use_container_width=True,
                **chart_config
            )
        else:
            st.write("Unsupported chart type")

    def render_responsive_table(self, data: pd.DataFrame, max_rows: int = None) -> None:
        """Render responsive data table."""
        if self.device_info and self.device_info.is_mobile():
            # Mobile: show fewer rows, horizontal scroll
            if max_rows is None:
                max_rows = 10
            
            st.markdown('<div class="responsive-table">', unsafe_allow_html=True)
            st.dataframe(
                data.head(max_rows),
                use_container_width=True,
                hide_index=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            if len(data) > max_rows:
                st.caption(f"Showing {max_rows} of {len(data)} rows")
        else:
            # Desktop/Tablet: full table
            st.dataframe(data, use_container_width=True)

    def render_responsive_filters(self, filter_config: Dict[str, Any]) -> None:
        """Render responsive filter controls."""
        if self.device_info and self.device_info.is_mobile():
            # Mobile: stacked layout, touch-friendly
            with st.expander("🔧 Filters", expanded=False):
                for filter_name, config in filter_config.items():
                    if config['type'] == 'multiselect':
                        st.multiselect(
                            config['label'],
                            options=config['options'],
                            default=config['default'],
                            key=f"mobile_{filter_name}",
                            help=config.get('help', '')
                        )
                    elif config['type'] == 'slider':
                        st.slider(
                            config['label'],
                            min_value=config['min_value'],
                            max_value=config['max_value'],
                            value=config['value'],
                            step=config.get('step', 1),
                            key=f"mobile_{filter_name}",
                            help=config.get('help', '')
                        )
        else:
            # Desktop/Tablet: standard layout
            for filter_name, config in filter_config.items():
                if config['type'] == 'multiselect':
                    st.multiselect(
                        config['label'],
                        options=config['options'],
                        default=config['default'],
                        key=filter_name,
                        help=config.get('help', '')
                    )
                elif config['type'] == 'slider':
                    st.slider(
                        config['label'],
                        min_value=config['min_value'],
                        max_value=config['max_value'],
                        value=config['value'],
                        step=config.get('step', 1),
                        key=filter_name,
                        help=config.get('help', '')
                    )

    def render_mobile_navigation(self, navigation_items: List[Dict[str, Any]]) -> None:
        """Render mobile bottom navigation."""
        if self.device_info and self.device_info.is_mobile():
            st.markdown("""
            <div class="mobile-nav">
                <div style="display: flex; justify-content: space-around;">
            """, unsafe_allow_html=True)
            
            for item in navigation_items:
                st.markdown(f"""
                    <button onclick="navigateTo('{item['page_id']}')">
                        {item['icon']} {item['title']}
                    </button>
                """, unsafe_allow_html=True)
            
            st.markdown("""
                </div>
            </div>
            
            <script>
            function navigateTo(pageId) {{
                // Navigation logic would go here
                console.log('Navigate to:', pageId);
            }}
            </script>
            """, unsafe_allow_html=True)

    def get_device_info(self) -> Dict[str, Any]:
        """Get current device information."""
        if self.device_info:
            return self.device_info.to_dict()
        else:
            return {
                'width': 1024,
                'height': 768,
                'device_type': 'desktop',
                'touch_capable': False,
                'aspect_ratio': 1.33,
                'is_mobile': False,
                'is_tablet': False,
                'is_desktop': True
            }

    def is_mobile_device(self) -> bool:
        """Check if current device is mobile."""
        return self.device_info.is_mobile() if self.device_info else False

    def is_tablet_device(self) -> bool:
        """Check if current device is tablet."""
        return self.device_info.is_tablet() if self.device_info else False

    def is_desktop_device(self) -> bool:
        """Check if current device is desktop."""
        return self.device_info.is_desktop() if self.device_info else True

    def render_responsive_dashboard(self, dashboard_content: Callable) -> None:
        """Render responsive dashboard with adaptive layout."""
        # Inject responsive CSS
        self.inject_responsive_css()
        
        # Add mobile navigation if needed
        if self.is_mobile_device():
            navigation_items = [
                {'page_id': 'executive', 'icon': '📊', 'title': 'Executive'},
                {'page_id': 'market', 'icon': '🌍', 'title': 'Market'},
                {'page_id': 'sales', 'icon': '📈', 'title': 'Sales'},
                {'page_id': 'settings', 'icon': '⚙️', 'title': 'Settings'}
            ]
            self.render_mobile_navigation(navigation_items)
        
        # Render dashboard content
        dashboard_content()

    def get_responsive_config(self) -> Dict[str, Any]:
        """Get responsive configuration."""
        return {
            'device_info': self.get_device_info(),
            'layout_config': self.layout.layout_config if self.layout else {},
            'is_mobile': self.is_mobile_device(),
            'is_tablet': self.is_tablet_device(),
            'is_desktop': self.is_desktop_device(),
            'css_injected': bool(self.responsive_css)
        }

    def get_responsive_status(self) -> Dict[str, Any]:
        """Get responsive design status."""
        return {
            'device_detection': self.device_info is not None,
            'responsive_layout': self.layout is not None,
            'css_generated': bool(self.responsive_css),
            'responsive_config': self.get_responsive_config()
        }


# Global instance for use throughout the application
responsive_design = ResponsiveDesign()
