"""
🛠️ Utility Components Package

Utility components for data management and system operations.
"""

# Import utility components
try:
    from .data_manager import data_manager
    from .notification_system import notification_system
    from .status_indicators import status_indicators
    from .app_router import app_router
    from .export_manager import export_manager
    from .performance_optimizer import performance_optimizer
    from .responsive_design import responsive_design
except ImportError as e:
    print(f"[WARNING] Could not import utility components: {e}")
    data_manager = None
    notification_system = None
    status_indicators = None
    app_router = None
    export_manager = None
    performance_optimizer = None
    responsive_design = None

__all__ = [
    'data_manager',
    'notification_system', 
    'status_indicators',
    'app_router',
    'export_manager',
    'performance_optimizer',
    'responsive_design'
]
