"""
📊 Status Indicators Utility Component for Car Market Analysis Executive Dashboard

Advanced status indicator system providing real-time system monitoring,
component health checks, data quality indicators, and performance metrics.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
from enum import Enum
import time
import psutil
import json

# Import components
try:
    from ...business_logic import analyzer
    from ...data_layer import data_processor
    from .data_manager import data_manager
    from .notification_system import notification_system
except ImportError:
    # Fallback imports
    analyzer = None
    data_processor = None
    data_manager = None
    notification_system = None

# Import configuration
try:
    from ..config.app_config import COLOR_PALETTE, RISK_COLORS
except ImportError:
    # Fallback configuration
    COLOR_PALETTE = {
        'primary': '#1f77b4',
        'secondary': '#0a9396',
        'success': '#2ca02c',
        'danger': '#d62728',
        'warning': '#ff7f0e',
        'info': '#17a2b8'
    }
    RISK_COLORS = {
        'Low': '#2ca02c',
        'Medium': '#ff7f0e',
        'High': '#d62728',
        'Critical': '#8b0000'
    }


class StatusLevel(Enum):
    """Status level enumeration."""
    EXCELLENT = "excellent"
    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class ComponentType(Enum):
    """Component type enumeration."""
    DATA_SOURCE = "data_source"
    BUSINESS_LOGIC = "business_logic"
    CACHE = "cache"
    UI_COMPONENT = "ui_component"
    EXTERNAL_API = "external_api"
    DATABASE = "database"
    FILE_SYSTEM = "file_system"
    SYSTEM = "system"


class StatusIndicator:
    """Individual status indicator class."""
    
    def __init__(self, component_name: str, component_type: ComponentType = ComponentType.DATA_SOURCE,
                 status: StatusLevel = StatusLevel.UNKNOWN, message: str = "",
                 value: Any = None, unit: str = "", threshold: float = None,
                 last_updated: datetime = None, metadata: Dict[str, Any] = None):
        """Initialize status indicator."""
        self.component_name = component_name
        self.component_type = component_type
        self.status = status
        self.message = message
        self.value = value
        self.unit = unit
        self.threshold = threshold
        self.last_updated = last_updated or datetime.now()
        self.metadata = metadata or {}
        self.history: List[Tuple[datetime, StatusLevel, str]] = []

    def update_status(self, status: StatusLevel, message: str = "", value: Any = None) -> None:
        """Update status indicator."""
        # Add to history
        self.history.append((self.last_updated, self.status, self.message))
        
        # Update current status
        self.status = status
        self.message = message
        self.value = value
        self.last_updated = datetime.now()
        
        # Limit history
        if len(self.history) > 50:
            self.history = self.history[-50:]

    def get_status_color(self) -> str:
        """Get color for current status."""
        color_map = {
            StatusLevel.EXCELLENT: COLOR_PALETTE['success'],
            StatusLevel.GOOD: COLOR_PALETTE['info'],
            StatusLevel.WARNING: COLOR_PALETTE['warning'],
            StatusLevel.CRITICAL: COLOR_PALETTE['danger'],
            StatusLevel.UNKNOWN: '#6c757d'
        }
        return color_map.get(self.status, '#6c757d')

    def get_status_icon(self) -> str:
        """Get icon for current status."""
        icon_map = {
            StatusLevel.EXCELLENT: '🟢',
            StatusLevel.GOOD: '🟡',
            StatusLevel.WARNING: '🟠',
            StatusLevel.CRITICAL: '🔴',
            StatusLevel.UNKNOWN: '⚪'
        }
        return icon_map.get(self.status, '⚪')

    def is_healthy(self) -> bool:
        """Check if component is healthy."""
        return self.status in [StatusLevel.EXCELLENT, StatusLevel.GOOD]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'component_name': self.component_name,
            'component_type': self.component_type.value,
            'status': self.status.value,
            'message': self.message,
            'value': self.value,
            'unit': self.unit,
            'threshold': self.threshold,
            'last_updated': self.last_updated.isoformat(),
            'metadata': self.metadata,
            'is_healthy': self.is_healthy()
        }


class StatusIndicators:
    """
    📈 Executive-Grade Status Indicator System
    
    Provides comprehensive system monitoring with real-time status indicators,
    component health checks, performance metrics, and system diagnostics.
    """

    def __init__(self):
        """Initialize the StatusIndicators system."""
        self.indicators: Dict[str, StatusIndicator] = {}
        self.system_metrics = {}
        self.last_system_check = None
        
        # Initialize default indicators
        self._initialize_default_indicators()

    def _initialize_default_indicators(self) -> None:
        """Initialize default system indicators."""
        # Data source indicators
        self.add_indicator(
            'basic_data', ComponentType.DATA_SOURCE,
            "Basic car data table"
        )
        self.add_indicator(
            'sales_data', ComponentType.DATA_SOURCE,
            "Sales data table"
        )
        self.add_indicator(
            'price_data', ComponentType.DATA_SOURCE,
            "Price data table"
        )
        
        # Business logic indicators
        self.add_indicator(
            'analyzer', ComponentType.BUSINESS_LOGIC,
            "Car data analyzer"
        )
        self.add_indicator(
            'data_processor', ComponentType.BUSINESS_LOGIC,
            "Data processor"
        )
        
        # Cache indicators
        self.add_indicator(
            'data_cache', ComponentType.CACHE,
            "Data cache system"
        )
        
        # System indicators
        self.add_indicator(
            'memory_usage', ComponentType.SYSTEM,
            "System memory usage",
            unit="MB"
        )
        self.add_indicator(
            'cpu_usage', ComponentType.SYSTEM,
            "CPU usage",
            unit="%"
        )

    def add_indicator(self, component_name: str, component_type: ComponentType,
                     description: str = "", status: StatusLevel = StatusLevel.UNKNOWN,
                     message: str = "", value: Any = None, unit: str = "",
                     threshold: float = None, metadata: Dict[str, Any] = None) -> None:
        """Add a new status indicator."""
        indicator = StatusIndicator(
            component_name=component_name,
            component_type=component_type,
            status=status,
            message=message,
            value=value,
            unit=unit,
            threshold=threshold,
            metadata=metadata or {}
        )
        
        self.indicators[component_name] = indicator

    def update_indicator(self, component_name: str, status: StatusLevel,
                        message: str = "", value: Any = None) -> bool:
        """Update an existing status indicator."""
        if component_name in self.indicators:
            self.indicators[component_name].update_status(status, message, value)
            return True
        return False

    def check_data_sources(self) -> None:
        """Check data source indicators."""
        # Check basic data
        if analyzer and hasattr(analyzer, 'basic') and not analyzer.basic.empty:
            self.update_indicator(
                'basic_data', StatusLevel.EXCELLENT,
                f"Loaded {len(analyzer.basic)} records",
                len(analyzer.basic)
            )
        else:
            self.update_indicator(
                'basic_data', StatusLevel.CRITICAL,
                "No basic data available"
            )
        
        # Check sales data
        try:
            if analyzer:
                sales_data = analyzer.get_sales_summary()
                if not sales_data.empty:
                    self.update_indicator(
                        'sales_data', StatusLevel.EXCELLENT,
                        f"Loaded {len(sales_data)} sales records",
                        len(sales_data)
                    )
                else:
                    self.update_indicator(
                        'sales_data', StatusLevel.WARNING,
                        "Sales data is empty"
                    )
            else:
                self.update_indicator(
                    'sales_data', StatusLevel.CRITICAL,
                    "Analyzer not available"
                )
        except Exception as e:
            self.update_indicator(
                'sales_data', StatusLevel.CRITICAL,
                f"Error loading sales data: {str(e)}"
            )
        
        # Check price data
        try:
            if analyzer:
                price_data = analyzer.get_price_range_by_model()
                if not price_data.empty:
                    self.update_indicator(
                        'price_data', StatusLevel.EXCELLENT,
                        f"Loaded {len(price_data)} price records",
                        len(price_data)
                    )
                else:
                    self.update_indicator(
                        'price_data', StatusLevel.WARNING,
                        "Price data is empty"
                    )
            else:
                self.update_indicator(
                    'price_data', StatusLevel.CRITICAL,
                    "Analyzer not available"
                )
        except Exception as e:
            self.update_indicator(
                'price_data', StatusLevel.CRITICAL,
                f"Error loading price data: {str(e)}"
            )

    def check_business_logic(self) -> None:
        """Check business logic components."""
        # Check analyzer
        if analyzer:
            try:
                # Test basic functionality
                automaker_list = analyzer.get_automaker_list()
                if automaker_list:
                    self.update_indicator(
                        'analyzer', StatusLevel.EXCELLENT,
                        f"Analyzer working with {len(automaker_list)} automakers",
                        len(automaker_list)
                    )
                else:
                    self.update_indicator(
                        'analyzer', StatusLevel.WARNING,
                        "Analyzer working but no automakers found"
                    )
            except Exception as e:
                self.update_indicator(
                    'analyzer', StatusLevel.CRITICAL,
                    f"Analyzer error: {str(e)}"
                )
        else:
            self.update_indicator(
                'analyzer', StatusLevel.CRITICAL,
                "Analyzer not available"
            )
        
        # Check data processor
        if data_processor:
            try:
                # Test data processor functionality
                datasets = getattr(data_processor, 'datasets', {})
                if datasets:
                    self.update_indicator(
                        'data_processor', StatusLevel.EXCELLENT,
                        f"Data processor loaded {len(datasets)} datasets",
                        len(datasets)
                    )
                else:
                    self.update_indicator(
                        'data_processor', StatusLevel.WARNING,
                        "Data processor available but no datasets loaded"
                    )
            except Exception as e:
                self.update_indicator(
                    'data_processor', StatusLevel.CRITICAL,
                    f"Data processor error: {str(e)}"
                )
        else:
            self.update_indicator(
                'data_processor', StatusLevel.CRITICAL,
                "Data processor not available"
            )

    def check_cache_system(self) -> None:
        """Check cache system status."""
        if data_manager:
            try:
                cache_info = data_manager.get_cache_info()
                cache_size = cache_info.get('total_size_mb', 0)
                cache_utilization = cache_info.get('utilization_percent', 0)
                
                if cache_utilization < 80:
                    self.update_indicator(
                        'data_cache', StatusLevel.EXCELLENT,
                        f"Cache healthy: {cache_size:.1f}MB ({cache_utilization:.1f}% used)",
                        cache_size
                    )
                elif cache_utilization < 95:
                    self.update_indicator(
                        'data_cache', StatusLevel.WARNING,
                        f"Cache nearly full: {cache_size:.1f}MB ({cache_utilization:.1f}% used)",
                        cache_size
                    )
                else:
                    self.update_indicator(
                        'data_cache', StatusLevel.CRITICAL,
                        f"Cache full: {cache_size:.1f}MB ({cache_utilization:.1f}% used)",
                        cache_size
                    )
            except Exception as e:
                self.update_indicator(
                    'data_cache', StatusLevel.CRITICAL,
                    f"Cache error: {str(e)}"
                )
        else:
            self.update_indicator(
                'data_cache', StatusLevel.CRITICAL,
                "Data manager not available"
            )

    def check_system_resources(self) -> None:
        """Check system resource usage."""
        try:
            # Memory usage
            memory = psutil.virtual_memory()
            memory_usage_mb = memory.used / (1024 * 1024)
            memory_percent = memory.percent
            
            if memory_percent < 70:
                self.update_indicator(
                    'memory_usage', StatusLevel.EXCELLENT,
                    f"Memory usage: {memory_percent:.1f}%",
                    memory_usage_mb
                )
            elif memory_percent < 85:
                self.update_indicator(
                    'memory_usage', StatusLevel.WARNING,
                    f"Memory usage high: {memory_percent:.1f}%",
                    memory_usage_mb
                )
            else:
                self.update_indicator(
                    'memory_usage', StatusLevel.CRITICAL,
                    f"Memory usage critical: {memory_percent:.1f}%",
                    memory_usage_mb
                )
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            if cpu_percent < 50:
                self.update_indicator(
                    'cpu_usage', StatusLevel.EXCELLENT,
                    f"CPU usage: {cpu_percent:.1f}%",
                    cpu_percent
                )
            elif cpu_percent < 80:
                self.update_indicator(
                    'cpu_usage', StatusLevel.WARNING,
                    f"CPU usage high: {cpu_percent:.1f}%",
                    cpu_percent
                )
            else:
                self.update_indicator(
                    'cpu_usage', StatusLevel.CRITICAL,
                    f"CPU usage critical: {cpu_percent:.1f}%",
                    cpu_percent
                )
                
        except Exception as e:
            self.update_indicator(
                'memory_usage', StatusLevel.CRITICAL,
                f"System check error: {str(e)}"
            )

    def run_full_system_check(self) -> None:
        """Run complete system health check."""
        self.last_system_check = datetime.now()
        
        # Check all components
        self.check_data_sources()
        self.check_business_logic()
        self.check_cache_system()
        self.check_system_resources()
        
        # Update system metrics
        self._update_system_metrics()

    def _update_system_metrics(self) -> None:
        """Update system metrics."""
        total_indicators = len(self.indicators)
        healthy_indicators = sum(1 for ind in self.indicators.values() if ind.is_healthy())
        critical_indicators = sum(1 for ind in self.indicators.values() if ind.status == StatusLevel.CRITICAL)
        
        self.system_metrics = {
            'total_components': total_indicators,
            'healthy_components': healthy_indicators,
            'critical_components': critical_indicators,
            'health_percentage': (healthy_indicators / total_indicators * 100) if total_indicators > 0 else 0,
            'last_check': self.last_system_check.isoformat() if self.last_system_check else None
        }

    # ==================== DISPLAY METHODS ====================

    def display_status_dashboard(self, container=None) -> None:
        """Display comprehensive status dashboard."""
        if container is None:
            container = st
        
        # Run system check if needed
        if not self.last_system_check or (datetime.now() - self.last_system_check).seconds > 60:
            self.run_full_system_check()
        
        # System overview
        self._display_system_overview(container)
        
        # Component status grid
        self._display_component_grid(container)
        
        # System metrics
        self._display_system_metrics(container)

    def _display_system_overview(self, container) -> None:
        """Display system overview section."""
        container.markdown("## 🔍 System Health Overview")
        
        # Calculate system health
        total_components = len(self.indicators)
        healthy_components = sum(1 for ind in self.indicators.values() if ind.is_healthy())
        critical_components = sum(1 for ind in self.indicators.values() if ind.status == StatusLevel.CRITICAL)
        
        health_percentage = (healthy_components / total_components * 100) if total_components > 0 else 0
        
        # System health indicator
        if health_percentage >= 90:
            health_status = StatusLevel.EXCELLENT
            health_message = "All systems operational"
        elif health_percentage >= 75:
            health_status = StatusLevel.GOOD
            health_message = "Most systems operational"
        elif health_percentage >= 50:
            health_status = StatusLevel.WARNING
            health_message = "Some systems need attention"
        else:
            health_status = StatusLevel.CRITICAL
            health_message = "Multiple systems critical"
        
        # Display health metrics
        col1, col2, col3, col4 = container.columns(4)
        
        with col1:
            container.metric(
                "System Health",
                f"{health_percentage:.1f}%",
                delta=f"{healthy_components}/{total_components} healthy"
            )
        
        with col2:
            container.metric(
                "Critical Issues",
                critical_components,
                delta="Need immediate attention" if critical_components > 0 else "None"
            )
        
        with col3:
            container.metric(
                "Total Components",
                total_components,
                delta="Monitored"
            )
        
        with col4:
            last_check = self.last_system_check.strftime('%H:%M:%S') if self.last_system_check else "Never"
            container.metric(
                "Last Check",
                last_check,
                delta="System check"
            )

    def _display_component_grid(self, container) -> None:
        """Display component status grid."""
        container.markdown("## 📊 Component Status")
        
        # Group indicators by type
        indicators_by_type = {}
        for indicator in self.indicators.values():
            component_type = indicator.component_type
            if component_type not in indicators_by_type:
                indicators_by_type[component_type] = []
            indicators_by_type[component_type].append(indicator)
        
        # Display each component type
        for component_type, indicators in indicators_by_type.items():
            container.markdown(f"### {component_type.value.replace('_', ' ').title()}")
            
            # Create columns for indicators
            cols = container.columns(min(3, len(indicators)))
            
            for i, indicator in enumerate(indicators):
                with cols[i % len(cols)]:
                    self._display_single_indicator(indicator, container)

    def _display_single_indicator(self, indicator: StatusIndicator, container) -> None:
        """Display a single status indicator."""
        # Create indicator card
        status_color = indicator.get_status_color()
        status_icon = indicator.get_status_icon()
        
        # Format value
        value_text = ""
        if indicator.value is not None:
            if indicator.unit:
                value_text = f"{indicator.value:,.0f} {indicator.unit}"
            else:
                value_text = str(indicator.value)
        
        # Create HTML for indicator card
        indicator_html = f"""
        <div style="
            border: 2px solid {status_color};
            border-radius: 8px;
            padding: 12px;
            margin: 8px 0;
            background-color: {status_color}10;
        ">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span style="font-size: 18px;">{status_icon}</span>
                <strong style="color: {status_color};">
                    {indicator.component_name.replace('_', ' ').title()}
                </strong>
            </div>
            <div style="font-size: 14px; color: #666; margin-bottom: 4px;">
                {indicator.message}
            </div>
            {f"<div style='font-size: 12px; color: #888;'>{value_text}</div>" if value_text else ""}
            <div style="font-size: 11px; color: #999; margin-top: 4px;">
                {indicator.last_updated.strftime('%H:%M:%S')}
            </div>
        </div>
        """
        
        container.markdown(indicator_html, unsafe_allow_html=True)

    def _display_system_metrics(self, container) -> None:
        """Display system metrics section."""
        container.markdown("## 📈 System Metrics")
        
        if not self.system_metrics:
            container.info("No system metrics available")
            return
        
        # Display metrics in columns
        col1, col2, col3 = container.columns(3)
        
        with col1:
            container.metric(
                "Health Percentage",
                f"{self.system_metrics.get('health_percentage', 0):.1f}%"
            )
        
        with col2:
            container.metric(
                "Healthy Components",
                self.system_metrics.get('healthy_components', 0)
            )
        
        with col3:
            container.metric(
                "Critical Components",
                self.system_metrics.get('critical_components', 0)
            )

    def display_status_summary(self, container=None) -> None:
        """Display compact status summary."""
        if container is None:
            container = st
        
        # Run quick check if needed
        if not self.last_system_check or (datetime.now() - self.last_system_check).seconds > 300:
            self.run_full_system_check()
        
        # Get summary data
        total_components = len(self.indicators)
        healthy_components = sum(1 for ind in self.indicators.values() if ind.is_healthy())
        critical_components = sum(1 for ind in self.indicators.values() if ind.status == StatusLevel.CRITICAL)
        
        health_percentage = (healthy_components / total_components * 100) if total_components > 0 else 0
        
        # Display summary
        if critical_components > 0:
            container.error(f"🚨 {critical_components} critical issues detected")
        elif health_percentage < 80:
            container.warning(f"⚠️ System health: {health_percentage:.1f}%")
        else:
            container.success(f"✅ System health: {health_percentage:.1f}%")

    # ==================== UTILITY METHODS ====================

    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health information."""
        total_components = len(self.indicators)
        healthy_components = sum(1 for ind in self.indicators.values() if ind.is_healthy())
        critical_components = sum(1 for ind in self.indicators.values() if ind.status == StatusLevel.CRITICAL)
        
        health_percentage = (healthy_components / total_components * 100) if total_components > 0 else 0
        
        return {
            'health_percentage': health_percentage,
            'total_components': total_components,
            'healthy_components': healthy_components,
            'critical_components': critical_components,
            'last_check': self.last_system_check.isoformat() if self.last_system_check else None,
            'overall_status': 'healthy' if health_percentage >= 80 else 'warning' if health_percentage >= 50 else 'critical'
        }

    def get_component_status(self, component_name: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific component."""
        if component_name in self.indicators:
            return self.indicators[component_name].to_dict()
        return None

    def get_all_indicators(self) -> Dict[str, Dict[str, Any]]:
        """Get all status indicators."""
        return {name: indicator.to_dict() for name, indicator in self.indicators.items()}

    def export_status_report(self, format: str = 'json') -> str:
        """Export status report."""
        report_data = {
            'system_health': self.get_system_health(),
            'indicators': self.get_all_indicators(),
            'system_metrics': self.system_metrics,
            'export_timestamp': datetime.now().isoformat()
        }
        
        if format.lower() == 'json':
            return json.dumps(report_data, indent=2, default=str)
        else:
            return str(report_data)

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return {
            'system_health': self.get_system_health(),
            'indicators': self.get_all_indicators(),
            'system_metrics': self.system_metrics,
            'last_check': self.last_system_check.isoformat() if self.last_system_check else None
        }


# Global instance for use throughout the application
status_indicators = StatusIndicators()

