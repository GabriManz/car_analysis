"""
🧭 Application Router Utility Component for Car Market Analysis Executive Dashboard

Advanced routing and navigation system providing page management, 
component loading, and state management for the dashboard application.
"""

import streamlit as st
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import json

# Import dashboard components
try:
    from src.components.dashboards.executive_dashboard import executive_dashboard
    from src.components.dashboards.market_dashboard import market_dashboard
    from src.components.dashboards.sales_dashboard import sales_dashboard
except ImportError:
    executive_dashboard = None
    market_dashboard = None
    sales_dashboard = None


class PageRoute:
    """Individual page route configuration."""
    
    def __init__(self, page_id: str, title: str, icon: str, component: Callable = None,
                 description: str = "", category: str = "main", 
                 requires_auth: bool = False, permissions: List[str] = None,
                 metadata: Dict[str, Any] = None):
        """Initialize page route."""
        self.page_id = page_id
        self.title = title
        self.icon = icon
        self.component = component
        self.description = description
        self.category = category
        self.requires_auth = requires_auth
        self.permissions = permissions or []
        self.metadata = metadata or {}
        self.last_accessed = None
        self.access_count = 0

    def access_page(self) -> None:
        """Record page access."""
        self.last_accessed = datetime.now()
        self.access_count += 1

    def can_access(self, user_permissions: List[str] = None) -> bool:
        """Check if user can access this page."""
        if not self.requires_auth:
            return True
        
        if not user_permissions:
            return False
        
        return any(perm in user_permissions for perm in self.permissions)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'page_id': self.page_id,
            'title': self.title,
            'icon': self.icon,
            'description': self.description,
            'category': self.category,
            'requires_auth': self.requires_auth,
            'permissions': self.permissions,
            'metadata': self.metadata,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None,
            'access_count': self.access_count
        }


class AppRouter:
    """
    🗺️ Executive-Grade Application Router
    
    Provides comprehensive routing, navigation, and page management
    for the car market analysis dashboard application.
    """

    def __init__(self):
        """Initialize the application router."""
        self.routes: Dict[str, PageRoute] = {}
        self.current_page = "executive_summary"
        self.navigation_history = []
        self.user_permissions = []  # In a real app, this would come from authentication
        
        # Initialize default routes
        self._initialize_default_routes()

    def _initialize_default_routes(self) -> None:
        """Initialize default application routes."""
        
        # Executive Dashboard
        self.add_route(
            page_id="executive_summary",
            title="Executive Summary",
            icon="📊",
            component=self._render_executive_dashboard,
            description="High-level strategic insights and executive KPIs",
            category="executive"
        )
        
        # Market Analysis
        self.add_route(
            page_id="market_analysis",
            title="Market Analysis",
            icon="🌍",
            component=self._render_market_dashboard,
            description="Comprehensive market intelligence and competitive analysis",
            category="analytics"
        )
        
        # Sales Performance
        self.add_route(
            page_id="sales_performance",
            title="Sales Performance",
            icon="📈",
            component=self._render_sales_dashboard,
            description="Sales analysis, trends, and performance metrics",
            category="analytics"
        )
        
        # Advanced Analytics
        self.add_route(
            page_id="advanced_analytics",
            title="Advanced Analytics",
            icon="🧠",
            component=self._render_advanced_analytics,
            description="Advanced statistical analysis and machine learning insights",
            category="analytics"
        )
        
        # Data Quality Report
        self.add_route(
            page_id="data_quality_report",
            title="Data Quality Report",
            icon="🔍",
            component=self._render_data_quality_report,
            description="Data quality assessment and validation metrics",
            category="administration"
        )
        
        # System Monitoring
        self.add_route(
            page_id="system_monitoring",
            title="System Monitoring",
            icon="⚙️",
            component=self._render_system_monitoring,
            description="System health, performance monitoring, and diagnostics",
            category="administration"
        )
        
        # Settings
        self.add_route(
            page_id="settings",
            title="Settings",
            icon="⚙️",
            component=self._render_settings,
            description="Application configuration and preferences",
            category="administration",
            requires_auth=True,
            permissions=["admin", "settings"]
        )

    def add_route(self, page_id: str, title: str, icon: str, component: Callable = None,
                 description: str = "", category: str = "main", 
                 requires_auth: bool = False, permissions: List[str] = None,
                 metadata: Dict[str, Any] = None) -> None:
        """Add a new page route."""
        route = PageRoute(
            page_id=page_id,
            title=title,
            icon=icon,
            component=component,
            description=description,
            category=category,
            requires_auth=requires_auth,
            permissions=permissions,
            metadata=metadata
        )
        
        self.routes[page_id] = route

    def navigate_to(self, page_id: str) -> bool:
        """Navigate to a specific page."""
        if page_id in self.routes:
            route = self.routes[page_id]
            
            # Check permissions
            if not route.can_access(self.user_permissions):
                st.error(f"Access denied to {route.title}")
                return False
            
            # Update navigation history
            if self.current_page != page_id:
                self.navigation_history.append({
                    'from': self.current_page,
                    'to': page_id,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Limit history size
                if len(self.navigation_history) > 50:
                    self.navigation_history = self.navigation_history[-50:]
            
            # Update current page and record access
            self.current_page = page_id
            route.access_page()
            
            return True
        
        return False

    def get_current_route(self) -> Optional[PageRoute]:
        """Get current page route."""
        return self.routes.get(self.current_page)

    def get_routes_by_category(self, category: str) -> List[PageRoute]:
        """Get all routes in a specific category."""
        return [route for route in self.routes.values() if route.category == category]

    def get_accessible_routes(self) -> List[PageRoute]:
        """Get all routes accessible to current user."""
        return [route for route in self.routes.values() if route.can_access(self.user_permissions)]

    def render_navigation_sidebar(self) -> None:
        """Render navigation sidebar."""
        st.sidebar.markdown("## 🧭 Navigation")
        
        # Get accessible routes
        accessible_routes = self.get_accessible_routes()
        
        # Group by category
        categories = {}
        for route in accessible_routes:
            if route.category not in categories:
                categories[route.category] = []
            categories[route.category].append(route)
        
        # Render navigation by category
        for category, routes in categories.items():
            st.sidebar.markdown(f"### {category.title()}")
            
            for route in routes:
                # Determine button style based on current page
                button_type = "primary" if route.page_id == self.current_page else "secondary"
                
                if st.sidebar.button(
                    f"{route.icon} {route.title}",
                    key=f"nav_{route.page_id}",
                    help=route.description
                ):
                    if self.navigate_to(route.page_id):
                        st.rerun()

    def render_navigation_tabs(self) -> str:
        """Render navigation as tabs and return selected page."""
        accessible_routes = self.get_accessible_routes()
        
        # Create tab labels and page mapping
        tab_labels = []
        page_mapping = {}
        
        for route in accessible_routes:
            tab_label = f"{route.icon} {route.title}"
            tab_labels.append(tab_label)
            page_mapping[tab_label] = route.page_id
        
        # Create tabs
        selected_tab = st.tabs(tab_labels)
        
        # Find which tab is selected (this is a limitation of Streamlit tabs)
        # We'll use a different approach with selectbox
        page_options = {route.page_id: f"{route.icon} {route.title}" for route in accessible_routes}
        
        selected_page = st.selectbox(
            "Select Dashboard",
            options=list(page_options.keys()),
            format_func=lambda x: page_options[x],
            index=list(page_options.keys()).index(self.current_page) if self.current_page in page_options else 0,
            key="page_selector"
        )
        
        if selected_page != self.current_page:
            self.navigate_to(selected_page)
        
        return selected_page

    def render_current_page(self) -> None:
        """Render the current page."""
        current_route = self.get_current_route()
        
        if current_route and current_route.component:
            try:
                # Add page header
                st.markdown(f"## {current_route.icon} {current_route.title}")
                st.markdown(f"*{current_route.description}*")
                st.markdown("---")
                
                # Render page component
                current_route.component()
                
            except Exception as e:
                st.error(f"Error rendering {current_route.title}: {str(e)}")
                st.exception(e)
        else:
            st.error(f"Page '{self.current_page}' not found or has no component")

    # ==================== PAGE COMPONENTS ====================

    def _render_executive_dashboard(self) -> None:
        """Render executive dashboard page."""
        if executive_dashboard:
            try:
                executive_dashboard.render_executive_dashboard()
            except Exception as e:
                st.error(f"Executive dashboard error: {str(e)}")
        else:
            st.error("Executive dashboard component not available")

    def _render_market_dashboard(self) -> None:
        """Render market dashboard page."""
        if market_dashboard:
            try:
                market_dashboard.render_market_dashboard()
            except Exception as e:
                st.error(f"Market dashboard error: {str(e)}")
        else:
            st.error("Market dashboard component not available")

    def _render_sales_dashboard(self) -> None:
        """Render sales dashboard page."""
        if sales_dashboard:
            try:
                sales_dashboard.render_sales_dashboard()
            except Exception as e:
                st.error(f"Sales dashboard error: {str(e)}")
        else:
            st.error("Sales dashboard component not available")

    def _render_advanced_analytics(self) -> None:
        """Render advanced analytics page."""
        st.markdown("### Advanced Statistical Analysis")
        
        # Advanced analytics content would go here
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Correlation Analysis")
            st.info("Advanced correlation analysis between price, sales, and market factors")
        
        with col2:
            st.markdown("#### Clustering Analysis")
            st.info("Market segment clustering and classification analysis")
        
        # Placeholder for advanced analytics
        st.markdown("#### Machine Learning Insights")
        st.info("Advanced machine learning models for market prediction and analysis")

    def _render_data_quality_report(self) -> None:
        """Render data quality report page."""
        st.markdown("### Data Quality Assessment")
        
        # Data quality content would go here
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Data Completeness", "95.2%")
            st.metric("Data Accuracy", "98.7%")
        
        with col2:
            st.metric("Missing Values", "1,234")
            st.metric("Duplicate Records", "56")
        
        with col3:
            st.metric("Data Freshness", "2 hours")
            st.metric("Quality Score", "A+")
        
        st.markdown("#### Data Quality Trends")
        st.info("Data quality metrics and trends over time")

    def _render_system_monitoring(self) -> None:
        """Render system monitoring page."""
        st.markdown("### System Health Monitoring")
        
        # System monitoring content would go here
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("System Uptime", "99.9%")
            st.metric("Response Time", "120ms")
        
        with col2:
            st.metric("Memory Usage", "2.1GB")
            st.metric("CPU Usage", "15%")
        
        with col3:
            st.metric("Active Users", "24")
            st.metric("Cache Hit Rate", "94%")
        
        st.markdown("#### System Performance")
        st.info("Real-time system performance metrics and alerts")

    def _render_settings(self) -> None:
        """Render settings page."""
        st.markdown("### Application Settings")
        
        # Settings content would go here
        st.markdown("#### General Settings")
        st.selectbox("Theme", ["Light", "Dark", "Auto"])
        st.selectbox("Language", ["English", "Spanish", "French"])
        
        st.markdown("#### Data Settings")
        st.number_input("Cache Size (MB)", min_value=50, max_value=1000, value=100)
        st.number_input("Refresh Interval (seconds)", min_value=30, max_value=3600, value=300)
        
        st.markdown("#### Notification Settings")
        st.checkbox("Email Notifications", value=True)
        st.checkbox("System Alerts", value=True)

    # ==================== UTILITY METHODS ====================

    def get_navigation_history(self) -> List[Dict[str, Any]]:
        """Get navigation history."""
        return self.navigation_history.copy()

    def get_route_stats(self) -> Dict[str, Any]:
        """Get route access statistics."""
        total_accesses = sum(route.access_count for route in self.routes.values())
        most_accessed = max(self.routes.values(), key=lambda x: x.access_count) if self.routes else None
        
        return {
            'total_routes': len(self.routes),
            'total_accesses': total_accesses,
            'current_page': self.current_page,
            'most_accessed_page': most_accessed.page_id if most_accessed else None,
            'most_accessed_count': most_accessed.access_count if most_accessed else 0,
            'navigation_history_length': len(self.navigation_history)
        }

    def export_route_config(self) -> str:
        """Export route configuration."""
        config = {
            'routes': {route_id: route.to_dict() for route_id, route in self.routes.items()},
            'current_page': self.current_page,
            'navigation_history': self.navigation_history,
            'user_permissions': self.user_permissions,
            'export_timestamp': datetime.now().isoformat()
        }
        
        return json.dumps(config, indent=2, default=str)

    def get_router_status(self) -> Dict[str, Any]:
        """Get router status and statistics."""
        return {
            'current_page': self.current_page,
            'total_routes': len(self.routes),
            'accessible_routes': len(self.get_accessible_routes()),
            'navigation_history_length': len(self.navigation_history),
            'route_stats': self.get_route_stats()
        }


# Global instance for use throughout the application
app_router = AppRouter()

