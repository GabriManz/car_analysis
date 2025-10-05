"""
🚗 Car Market Analysis Executive Dashboard - Advanced Application

Professional executive-grade dashboard with advanced features including
export functionality, performance optimization, responsive design,
and comprehensive system monitoring.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import time
import warnings
warnings.filterwarnings('ignore')

# Import all modular components
try:
    # Configuration
    from components.config.app_config import APP_CONFIG, COLOR_PALETTE, DASHBOARD_MODULES
    
    # Core business logic
    from business_logic import analyzer
    from data_layer import data_processor
    
    # UI Components
    from components.ui.layout import layout_component
    from components.ui.sidebar import sidebar_component
    
    # Analytics Components
    from components.analytics.kpi_calculator import kpi_calculator
    from components.analytics.data_quality import data_quality
    
    # Visualization Components
    from components.visualizations.chart_factory import chart_factory
    
    # Dashboard Components
    from components.dashboards.executive_dashboard import executive_dashboard
    from components.dashboards.market_dashboard import market_dashboard
    from components.dashboards.sales_dashboard import sales_dashboard
    
    # Utility Components
    from components.utils import (
        data_manager, 
        notification_system, 
        status_indicators, 
        app_router,
        export_manager,
        performance_optimizer,
        responsive_design
    )
    
except ImportError as e:
    st.error(f"Error importing components: {str(e)}")
    st.stop()


class CarMarketAppAdvanced:
    """
    🏢 Advanced Executive-Grade Car Market Analysis Application
    
    Complete application with advanced features including export functionality,
    performance optimization, responsive design, and comprehensive monitoring.
    """

    def __init__(self):
        """Initialize the advanced application."""
        self.app_config = APP_CONFIG
        self.color_palette = COLOR_PALETTE
        self.dashboard_modules = DASHBOARD_MODULES
        
        # Core components
        self.analyzer = analyzer
        self.data_processor = data_processor
        
        # UI components
        self.layout = layout_component
        self.sidebar = sidebar_component
        
        # Analytics components
        self.kpi_calc = kpi_calculator
        self.data_quality = data_quality
        
        # Visualization components
        self.chart_factory = chart_factory
        
        # Dashboard components
        self.executive_dashboard = executive_dashboard
        self.market_dashboard = market_dashboard
        self.sales_dashboard = sales_dashboard
        
        # Utility components
        self.data_manager = data_manager
        self.notification_system = notification_system
        self.status_indicators = status_indicators
        self.app_router = app_router
        self.export_manager = export_manager
        self.performance_optimizer = performance_optimizer
        self.responsive_design = responsive_design
        
        # Application state
        self.filters = {}
        self.cached_data = {}
        self.app_initialized = False

    def setup_application(self) -> None:
        """Setup the advanced application configuration."""
        if self.app_initialized:
            return
        
        # Initialize performance monitoring
        if self.performance_optimizer:
            self.performance_optimizer.start_performance_tracking()
        
        # Configure responsive design
        if self.responsive_design:
            self.responsive_design.inject_responsive_css()
        
        # Configure Streamlit page
        if self.layout:
            self.layout.setup_page_config()
            self.layout.inject_custom_css()
        
        # Initialize session state
        self._initialize_session_state()
        
        # Initialize data manager
        if self.data_manager:
            self.data_manager.init_session_state()
        
        # Show startup notification
        if self.notification_system:
            self.notification_system.system_startup()
        
        # Run initial system check
        if self.status_indicators:
            self.status_indicators.run_full_system_check()
        
        # Set application as initialized
        self.app_initialized = True

    def _initialize_session_state(self) -> None:
        """Initialize Streamlit session state."""
        if 'app_filters' not in st.session_state:
            st.session_state.app_filters = {}
        
        if 'app_initialized' not in st.session_state:
            st.session_state.app_initialized = True
        
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'executive_summary'

    def render_application(self) -> None:
        """Render the complete advanced application."""
        # Setup application
        self.setup_application()
        
        # Render responsive dashboard
        if self.responsive_design:
            self.responsive_design.render_responsive_dashboard(self._render_dashboard_content)
        else:
            self._render_dashboard_content()

    def _render_dashboard_content(self) -> None:
        """Render dashboard content."""
        # Render header
        self._render_header()
        
        # Render sidebar with navigation
        self._render_sidebar()
        
        # Render main content using router
        self._render_main_content()
        
        # Render footer
        self._render_footer()

    def _render_header(self) -> None:
        """Render application header."""
        # Main header
        st.markdown(f"""
        <div class="main-header">
            <h1>{self.app_config.get('title', 'Car Market Analysis Dashboard')}</h1>
            <p>Advanced executive-grade market intelligence and analytics platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Status summary in expander
        with st.expander("🔍 System Status", expanded=False):
            if self.status_indicators:
                self.status_indicators.display_status_summary()
            else:
                st.info("Status indicators not available")

    def _render_sidebar(self) -> None:
        """Render application sidebar with navigation and filters."""
        with st.sidebar:
            # Navigation using router
            if self.app_router:
                self.app_router.render_navigation_sidebar()
            
            # Filters section
            self._render_filters()
            
            # System info
            self._render_system_info()
            
            # Export section
            self._render_export_section()
            
            # Performance section
            self._render_performance_section()

    def _render_filters(self) -> None:
        """Render filter controls."""
        st.markdown("## 🔧 Filters")
        
        try:
            # Load data for filters using performance optimizer
            if self.performance_optimizer:
                automaker_list = self.performance_optimizer.get_lazy_data('automaker_list')
                if not automaker_list:
                    # Fallback to direct loading
                    if self.data_manager and self.analyzer:
                        automaker_list = self.data_manager.load_data_with_cache(
                            'automaker_list',
                            lambda: sorted(self.analyzer.get_automaker_list())
                        )
            else:
                # Fallback to data manager
                if self.data_manager and self.analyzer:
                    automaker_list = self.data_manager.load_data_with_cache(
                        'automaker_list',
                        lambda: sorted(self.analyzer.get_automaker_list())
                    )
                else:
                    automaker_list = []
            
            if automaker_list:
                # Automaker filter
                selected_automakers = st.multiselect(
                    'Select Automakers',
                    options=automaker_list,
                    default=automaker_list[:5] if len(automaker_list) >= 5 else automaker_list,
                    key='filter_automakers'
                )
                
                # Top N filter
                top_n = st.slider(
                    'Top N Results',
                    min_value=5,
                    max_value=50,
                    value=15,
                    step=5,
                    key='filter_top_n'
                )
                
                # Price range filter
                if self.performance_optimizer:
                    price_data = self.performance_optimizer.get_lazy_data('price_data')
                else:
                    price_data = self.data_manager.load_price_data() if self.data_manager else pd.DataFrame()
                
                if not price_data.empty and 'price_mean' in price_data.columns:
                    min_price = float(price_data['price_mean'].min())
                    max_price = float(price_data['price_mean'].max())
                    
                    price_range = st.slider(
                        'Price Range (€)',
                        min_value=min_price,
                        max_price=max_price,
                        value=(min_price, max_price),
                        key='filter_price_range'
                    )
                
                # Update filters
                self.filters = {
                    'automakers': selected_automakers,
                    'top_n': top_n,
                    'price_range': price_range if 'price_range' in locals() else None
                }
                
                st.session_state.app_filters = self.filters
                
            else:
                st.warning("No automaker data available for filtering")
                
        except Exception as e:
            st.error(f"Error loading filter data: {str(e)}")
            if self.notification_system:
                self.notification_system.data_error(str(e))

    def _render_system_info(self) -> None:
        """Render system information."""
        st.markdown("## ℹ️ System Info")
        
        # Cache info
        if self.data_manager:
            cache_info = self.data_manager.get_cache_info()
            st.metric("Cache Size", f"{cache_info['total_size_mb']:.1f} MB")
            st.metric("Cache Utilization", f"{cache_info['utilization_percent']:.1f}%")
        
        # Notifications
        if self.notification_system:
            notification_stats = self.notification_system.get_notification_stats()
            st.metric("Active Notifications", notification_stats['total_active'])
            st.metric("Unread Notifications", notification_stats['total_unread'])
        
        # Router stats
        if self.app_router:
            router_stats = self.app_router.get_route_stats()
            st.metric("Total Routes", router_stats['total_routes'])
            st.metric("Current Page", router_stats['current_page'])

    def _render_export_section(self) -> None:
        """Render export section."""
        st.markdown("## 📤 Export")
        
        if self.export_manager:
            # Quick export buttons
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📊 Export Data", help="Export current data"):
                    self._handle_quick_export()
            
            with col2:
                if st.button("📋 Export Report", help="Export comprehensive report"):
                    self._handle_report_export()
            
            # Export manager interface
            if st.button("⚙️ Export Manager", help="Advanced export options"):
                st.session_state.show_export_manager = True

    def _render_performance_section(self) -> None:
        """Render performance section."""
        st.markdown("## ⚡ Performance")
        
        if self.performance_optimizer:
            memory_stats = self.performance_optimizer.memory_manager.get_memory_stats()
            st.metric("Memory Usage", f"{memory_stats['current_mb']:.1f} MB")
            st.metric("Available Memory", f"{memory_stats['available_mb']:.1f} MB")
            
            # Performance actions
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🧹 Clear Cache", help="Clear all caches"):
                    self.performance_optimizer.clear_lazy_cache()
                    if self.notification_system:
                        self.notification_system.info("Cache cleared successfully")
            
            with col2:
                if st.button("🗑️ Memory Cleanup", help="Perform memory cleanup"):
                    cleanup_stats = self.performance_optimizer.memory_manager.perform_cleanup()
                    if self.notification_system:
                        self.notification_system.info(f"Memory cleanup: {cleanup_stats['memory_saved_mb']:.1f}MB saved")

    def _render_main_content(self) -> None:
        """Render main content using the router."""
        # Show notifications
        if self.notification_system:
            self.notification_system.display_notifications(max_display=3)
        
        # Show export manager if requested
        if st.session_state.get('show_export_manager', False):
            self._render_export_manager()
            return
        
        # Render current page using router
        if self.app_router:
            self.app_router.render_current_page()
        else:
            st.error("Application router not available")

    def _render_export_manager(self) -> None:
        """Render export manager interface."""
        st.markdown("## 📤 Export Manager")
        
        if self.export_manager:
            self.export_manager.render_export_interface()
            
            # Close button
            if st.button("❌ Close Export Manager"):
                st.session_state.show_export_manager = False
                st.rerun()
        else:
            st.error("Export manager not available")

    def _handle_quick_export(self) -> None:
        """Handle quick data export."""
        try:
            if self.export_manager:
                # Export sales data
                result = self.export_manager.export_data(
                    'custom_analysis',
                    'csv',
                    st.session_state.get('app_filters', {}),
                    include_metadata=True
                )
                
                # Download button
                st.download_button(
                    label=f"📥 Download {result['filename']}",
                    data=result['content'],
                    file_name=result['filename'],
                    mime=result['mime_type']
                )
                
                if self.notification_system:
                    self.notification_system.success(f"Export generated: {result['filename']}")
            
        except Exception as e:
            st.error(f"Export failed: {str(e)}")
            if self.notification_system:
                self.notification_system.error(f"Export failed: {str(e)}")

    def _handle_report_export(self) -> None:
        """Handle comprehensive report export."""
        try:
            if self.export_manager:
                # Export executive summary
                result = self.export_manager.export_data(
                    'executive_summary',
                    'xlsx',
                    st.session_state.get('app_filters', {}),
                    include_metadata=True
                )
                
                # Download button
                st.download_button(
                    label=f"📥 Download {result['filename']}",
                    data=result['content'],
                    file_name=result['filename'],
                    mime=result['mime_type']
                )
                
                if self.notification_system:
                    self.notification_system.success(f"Report generated: {result['filename']}")
            
        except Exception as e:
            st.error(f"Report generation failed: {str(e)}")
            if self.notification_system:
                self.notification_system.error(f"Report generation failed: {str(e)}")

    def _render_footer(self) -> None:
        """Render application footer."""
        st.markdown("---")
        
        # Footer with app info
        footer_cols = st.columns(4)
        
        with footer_cols[0]:
            st.markdown(f"**Version:** {self.app_config.get('version', '2.0.0')}")
        
        with footer_cols[1]:
            st.markdown(f"**Author:** {self.app_config.get('author', 'Upgrade Hub')}")
        
        with footer_cols[2]:
            # Performance info
            if self.performance_optimizer:
                memory_stats = self.performance_optimizer.memory_manager.get_memory_stats()
                st.metric("Memory", f"{memory_stats['current_mb']:.1f} MB")
        
        with footer_cols[3]:
            # Debug info
            if st.button("🔧 Debug Info"):
                self._show_debug_info()

    def _show_debug_info(self) -> None:
        """Show debug information."""
        debug_info = self.get_application_status()
        st.json(debug_info)

    def get_application_status(self) -> Dict[str, Any]:
        """Get comprehensive application status."""
        status = {
            'app_config': self.app_config,
            'filters': self.filters,
            'app_initialized': self.app_initialized,
            'components_status': {
                'analyzer': self.analyzer is not None,
                'data_processor': self.data_processor is not None,
                'layout': self.layout is not None,
                'sidebar': self.sidebar is not None,
                'kpi_calculator': self.kpi_calc is not None,
                'data_quality': self.data_quality is not None,
                'chart_factory': self.chart_factory is not None,
                'executive_dashboard': self.executive_dashboard is not None,
                'market_dashboard': self.market_dashboard is not None,
                'sales_dashboard': self.sales_dashboard is not None,
                'data_manager': self.data_manager is not None,
                'notification_system': self.notification_system is not None,
                'status_indicators': self.status_indicators is not None,
                'app_router': self.app_router is not None,
                'export_manager': self.export_manager is not None,
                'performance_optimizer': self.performance_optimizer is not None,
                'responsive_design': self.responsive_design is not None
            }
        }
        
        # Add component-specific status
        if self.status_indicators:
            status['system_health'] = self.status_indicators.get_system_health()
        
        if self.data_manager:
            status['cache_info'] = self.data_manager.get_cache_info()
        
        if self.notification_system:
            status['notification_stats'] = self.notification_system.get_notification_stats()
        
        if self.app_router:
            status['router_status'] = self.app_router.get_router_status()
        
        if self.export_manager:
            status['export_stats'] = self.export_manager.get_export_stats()
        
        if self.performance_optimizer:
            status['performance_stats'] = self.performance_optimizer.get_optimizer_status()
        
        if self.responsive_design:
            status['responsive_config'] = self.responsive_design.get_responsive_config()
        
        return status


def main():
    """Main application entry point."""
    try:
        # Create and run the advanced application
        app = CarMarketAppAdvanced()
        app.render_application()
        
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    main()
