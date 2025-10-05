"""
🧩 Components Package

Modular components library for the Car Market Analysis Executive Dashboard.
"""

# Import configuration first (no dependencies)
try:
    from .config.app_config import (
        APP_CONFIG,
        COLOR_PALETTE,
        COOLORS_PALETTE,
        RISK_COLORS,
        MANUFACTURER_COLORS,
        DASHBOARD_MODULES,
        DATA_CONFIG,
        CHART_CONFIG,
        KPI_THRESHOLDS,
        CORRELATION_CONFIG,
        OUTLIER_CONFIG,
        CLUSTERING_CONFIG,
        CUSTOM_CSS
    )
    from .config.data_config import (
        DATA_FILES,
        COLUMN_MAPPING,
        VALIDATION_RULES,
        SALES_YEARS,
        DATA_QUALITY_THRESHOLDS,
        MEMORY_CONFIG,
        EXPORT_CONFIG
    )
except ImportError:
    DASHBOARD_MODULES = []
    APP_CONFIG = {}
    COLOR_PALETTE = {}
    COOLORS_PALETTE = []
    RISK_COLORS = {}
    MANUFACTURER_COLORS = {}
    DATA_CONFIG = {}
    CHART_CONFIG = {}
    KPI_THRESHOLDS = {}
    CORRELATION_CONFIG = {}
    OUTLIER_CONFIG = {}
    CLUSTERING_CONFIG = {}
    CUSTOM_CSS = ""
    DATA_FILES = {}
    COLUMN_MAPPING = {}
    VALIDATION_RULES = {}
    SALES_YEARS = []
    DATA_QUALITY_THRESHOLDS = {}
    MEMORY_CONFIG = {}
    EXPORT_CONFIG = {}

# Import components with error handling
try:
    from .analytics.kpi_calculator import KPICalculator
except ImportError:
    KPICalculator = None

try:
    from .ui.layout import LayoutComponent
except ImportError:
    LayoutComponent = None

try:
    from .ui.sidebar import SidebarComponent
except ImportError:
    SidebarComponent = None

try:
    from .utils.data_manager import DataManager
except ImportError:
    DataManager = None

try:
    from .visualizations.chart_factory import ChartFactory
except ImportError:
    ChartFactory = None

try:
    from .dashboards.executive_dashboard import ExecutiveDashboard
except ImportError:
    ExecutiveDashboard = None

try:
    from .dashboards.market_dashboard import MarketDashboard
except ImportError:
    MarketDashboard = None

try:
    from .dashboards.sales_dashboard import SalesDashboard
except ImportError:
    SalesDashboard = None
