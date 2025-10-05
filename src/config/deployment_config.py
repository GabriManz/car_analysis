"""
🚀 Deployment Configuration for Car Market Analysis Executive Dashboard

Configuration settings for different deployment environments including
development, staging, and production configurations.
"""

import os
from typing import Dict, Any, Optional

# Environment configurations
ENVIRONMENTS = {
    'development': {
        'debug': True,
        'log_level': 'DEBUG',
        'cache_ttl': 300,  # 5 minutes
        'max_cache_size_mb': 50,
        'enable_notifications': True,
        'enable_system_monitoring': True,
        'data_refresh_interval': 60,  # 1 minute
        'performance_monitoring': True
    },
    'staging': {
        'debug': False,
        'log_level': 'INFO',
        'cache_ttl': 1800,  # 30 minutes
        'max_cache_size_mb': 100,
        'enable_notifications': True,
        'enable_system_monitoring': True,
        'data_refresh_interval': 300,  # 5 minutes
        'performance_monitoring': True
    },
    'production': {
        'debug': False,
        'log_level': 'WARNING',
        'cache_ttl': 3600,  # 1 hour
        'max_cache_size_mb': 200,
        'enable_notifications': True,
        'enable_system_monitoring': True,
        'data_refresh_interval': 600,  # 10 minutes
        'performance_monitoring': False
    }
}

# Streamlit Cloud specific configurations
STREAMLIT_CLOUD_CONFIG = {
    'page_config': {
        'page_title': "Car Market Analysis Executive Dashboard",
        'page_icon': "🚗",
        'layout': "wide",
        'initial_sidebar_state': "expanded"
    },
    'theme': {
        'primaryColor': '#0A9396',
        'backgroundColor': '#001219',
        'secondaryBackgroundColor': '#005F73',
        'textColor': '#E9D8A6'
    },
    'server': {
        'port': 8501,
        'address': '0.0.0.0',
        'maxUploadSize': 200
    },
    'browser': {
        'gatherUsageStats': False
    }
}

# Data source configurations
DATA_CONFIG = {
    'local': {
        'data_path': 'data/',
        'cache_enabled': True,
        'auto_reload': True
    },
    'cloud': {
        'data_path': 'https://raw.githubusercontent.com/user/repo/main/data/',
        'cache_enabled': True,
        'auto_reload': False
    }
}

# Security configurations
SECURITY_CONFIG = {
    'development': {
        'enable_auth': False,
        'enable_cors': True,
        'allowed_origins': ['*'],
        'session_timeout': 3600
    },
    'production': {
        'enable_auth': True,
        'enable_cors': False,
        'allowed_origins': ['https://yourdomain.com'],
        'session_timeout': 1800
    }
}

# Performance configurations
PERFORMANCE_CONFIG = {
    'development': {
        'max_workers': 1,
        'chunk_size': 1000,
        'enable_profiling': True
    },
    'production': {
        'max_workers': 4,
        'chunk_size': 10000,
        'enable_profiling': False
    }
}

def get_environment() -> str:
    """Get current environment from environment variable."""
    return os.getenv('ENVIRONMENT', 'development')

def get_config(environment: Optional[str] = None) -> Dict[str, Any]:
    """Get configuration for specified environment."""
    if environment is None:
        environment = get_environment()
    
    return ENVIRONMENTS.get(environment, ENVIRONMENTS['development'])

def get_streamlit_config() -> Dict[str, Any]:
    """Get Streamlit configuration."""
    return STREAMLIT_CLOUD_CONFIG

def get_data_config() -> Dict[str, Any]:
    """Get data configuration based on environment."""
    environment = get_environment()
    
    if environment == 'production':
        return DATA_CONFIG['cloud']
    else:
        return DATA_CONFIG['local']

def get_security_config() -> Dict[str, Any]:
    """Get security configuration based on environment."""
    environment = get_environment()
    return SECURITY_CONFIG.get(environment, SECURITY_CONFIG['development'])

def get_performance_config() -> Dict[str, Any]:
    """Get performance configuration based on environment."""
    environment = get_environment()
    return PERFORMANCE_CONFIG.get(environment, PERFORMANCE_CONFIG['development'])

def get_full_config() -> Dict[str, Any]:
    """Get complete configuration for current environment."""
    return {
        'environment': get_environment(),
        'app_config': get_config(),
        'streamlit_config': get_streamlit_config(),
        'data_config': get_data_config(),
        'security_config': get_security_config(),
        'performance_config': get_performance_config()
    }

