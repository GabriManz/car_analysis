"""
⚙️ Application Configuration Module

Centralized configuration management for the Car Market Analysis Executive Dashboard.
Contains all constants, color schemes, and application settings.
"""

# Application Metadata
APP_CONFIG = {
    'title': '🚗 Car Market Analysis Executive Dashboard',
    'subtitle': 'Strategic Business Intelligence for Automotive Market Analysis & Decision Making',
    'version': '2.0.0-Executive',
    'page_icon': '🚗',
    'layout': 'wide',
    'sidebar_state': 'expanded'
}

# Professional Color Palettes
COLOR_PALETTE = {
    'primary': '#1f77b4',
    'secondary': '#0a9396',
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ff7f0e',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40'
}

# Risk Colors for automotive market analysis
RISK_COLORS = {
    'low': '#28a745',      # Green
    'medium': '#ffc107',   # Yellow
    'high': '#fd7e14',     # Orange
    'critical': '#dc3545'  # Red
}

# Automotive manufacturer colors
MANUFACTURER_COLORS = {
    'BMW': '#1f77b4',
    'Mercedes-Benz': '#ff7f0e',
    'Audi': '#2ca02c',
    'Volkswagen': '#d62728',
    'Toyota': '#9467bd',
    'Honda': '#8c564b',
    'Ford': '#e377c2',
    'Nissan': '#17becf',
    'Hyundai': '#bcbd22',
    'Kia': '#7f7f7f'
}

# Coolors.co Palette for Charts (adapted for automotive theme)
COOLORS_PALETTE = [
    '#001219',  # Rich Black
    '#005f73',  # Dark Cyan
    '#0a9396',  # Teal
    '#94d2bd',  # Light Teal
    '#e9d8a6',  # Beige
    '#ee9b00',  # Orange
    '#ca6702',  # Dark Orange
    '#bb3e03',  # Red Orange
    '#ae2012',  # Dark Red
    '#9b2226'   # Burgundy
]

# Dashboard Module Configuration
DASHBOARD_MODULES = [
    "🏢 Executive Summary",
    "🚗 Market Analysis",
    "📈 Sales Analytics",
    "💰 Price Intelligence",
    "🌍 Geographic Distribution",
    "📊 Performance Metrics",
    "🔮 Forecasting & Trends"
]

# Data Configuration
DATA_CONFIG = {
    'primary_data_path': 'data/',
    'basic_table': 'Basic_table.csv',
    'trim_table': 'Trim_table.csv',
    'price_table': 'Price_table.csv',
    'sales_table': 'Sales_table.csv',
    'year_range': (2001, 2020),  # Based on sales data
    'price_range': (1000, 500000),  # Estimated price range in EUR
}

# Event Types for car market analysis
VEHICLE_TYPES = [
    "All Types", "Sedan", "SUV", "Hatchback", "Coupe",
    "Convertible", "Wagon", "Truck", "Van", "Hybrid", "Electric"
]

# Professional CSS Styles
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&family=JetBrains+Mono:wght@100;200;300;400;500;600;700;800&family=Playfair+Display:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

:root {
    /* Automotive-themed Gradient Palette */
    --primary-gradient: linear-gradient(135deg, #001219 0%, #005f73 100%);
    --secondary-gradient: linear-gradient(135deg, #0a9396 0%, #11998e 100%);
    --success-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    --warning-gradient: linear-gradient(135deg, #ee9b00 0%, #ffc107 100%);
    --danger-gradient: linear-gradient(135deg, #bb3e03 0%, #dc3545 100%);
    --info-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    --neutral-gradient: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);

    /* Executive Color Palette */
    --executive-blue: #1e3a8a;
    --executive-navy: #1e293b;
    --executive-gold: #0a9396;
    --executive-silver: #64748b;
    --executive-platinum: #f8fafc;

    /* Glass Morphism */
    --glass-light: rgba(255, 255, 255, 0.25);
    --glass-dark: rgba(255, 255, 255, 0.1);
    --glass-border: rgba(255, 255, 255, 0.18);
    --shadow-elevation-1: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-elevation-2: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --shadow-elevation-3: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    --shadow-glow: 0 0 20px rgba(0, 18, 25, 0.3);

    /* Professional Typography */
    --font-heading: 'Playfair Display', serif;
    --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
    --font-display: 'Space Grotesk', sans-serif;

    /* Advanced Color System */
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-tertiary: #64748b;
    --text-inverse: #ffffff;
    --text-accent: #001219;

    /* Surface Colors */
    --surface: #ffffff;
    --surface-elevated: #f8fafc;
    --surface-overlay: rgba(15, 23, 42, 0.8);
    --surface-glass: rgba(255, 255, 255, 0.95);

    /* Professional Spacing */
    --space-xs: 0.5rem;
    --space-sm: 1rem;
    --space-md: 1.5rem;
    --space-lg: 2rem;
    --space-xl: 3rem;
    --space-2xl: 4rem;

    /* Advanced Borders */
    --border-radius: 0.5rem;
    --border-radius-lg: 1rem;
    --border-radius-xl: 1.5rem;
    --border-width: 1px;
    --border-color: rgba(255, 255, 255, 0.2);
    --border-focus: #001219;
}

/* Global Typography & App Base */
.stApp {
    font-family: var(--font-body);
    background:
        radial-gradient(circle at 20% 50%, rgba(0, 18, 25, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(118, 75, 162, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 40% 80%, rgba(79, 172, 254, 0.08) 0%, transparent 50%),
        linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    min-height: 100vh;
    font-feature-settings: 'liga' 1, 'kern' 1;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* Automotive-themed Professional Header */
.main-header {
    background:
        linear-gradient(135deg, rgba(0, 18, 25, 0.3) 0%, rgba(37, 99, 235, 0.3) 100%),
        url('https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80') center/cover;
    padding: 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    border: 1px solid rgba(0, 18, 25, 0.2);
    box-shadow: 0 4px 12px rgba(0, 18, 25, 0.1);
    position: relative;
}

.main-header:hover {
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.main-header h1 {
    color: #ffffff;
    text-align: center;
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
    font-size: clamp(1.8rem, 4vw, 2.5rem);
    font-weight: bold;
    letter-spacing: 0;
    line-height: 1.2;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.7);
}

.main-header p {
    color: #f1f5f9;
    text-align: center;
    margin: 0.5rem 0 0 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
    font-size: 1rem;
    font-weight: normal;
    line-height: 1.4;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
}

/* Executive Metric Cards */
.metric-card {
    background: var(--surface-glass);
    backdrop-filter: blur(20px) saturate(180%);
    padding: var(--space-lg) var(--space-md);
    border-radius: var(--border-radius-lg);
    border: var(--border-width) solid var(--border-color);
    box-shadow: var(--shadow-elevation-2);
    border-left: 4px solid transparent;
    border-image: var(--primary-gradient) 1;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    cursor: pointer;
}

.metric-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(0, 18, 25, 0.03) 0%, transparent 50%);
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
}

.metric-card:hover::after {
    opacity: 1;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: var(--primary-gradient);
    transform: scaleX(0);
    transform-origin: center;
    transition: all 0.4s ease;
    border-radius: var(--border-radius) var(--border-radius) 0 0;
}

.metric-card:hover::before {
    transform: scaleX(1);
}

.metric-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow:
        var(--shadow-elevation-3),
        var(--shadow-glow),
        inset 0 1px 0 rgba(255, 255, 255, 0.3);
    border-color: rgba(0, 18, 25, 0.3);
}

/* Executive Sidebar */
.css-1d391kg {
    background:
        linear-gradient(180deg, var(--surface-glass) 0%, var(--surface-elevated) 100%),
        linear-gradient(135deg, rgba(0, 18, 25, 0.02) 0%, rgba(118, 75, 162, 0.02) 100%);
    backdrop-filter: blur(20px) saturate(180%);
    border-right: var(--border-width) solid var(--border-color);
    box-shadow: inset -1px 0 0 rgba(255, 255, 255, 0.1);
}

/* Sidebar Navigation Enhancement */
.sidebar-nav-item {
    padding: var(--space-sm) var(--space-md);
    border-radius: var(--border-radius);
    margin-bottom: var(--space-xs);
    transition: all 0.3s ease;
    border: 1px solid transparent;
}

.sidebar-nav-item:hover {
    background: rgba(0, 18, 25, 0.08);
    border-color: rgba(0, 18, 25, 0.2);
    transform: translateX(4px);
}

.sidebar-nav-item.active {
    background: var(--primary-gradient);
    color: white;
    box-shadow: var(--shadow-elevation-1);
}

/* Premium Form Elements */
.stSelectbox > div > div {
    background: var(--surface-glass);
    backdrop-filter: blur(20px) saturate(180%);
    border: var(--border-width) solid var(--border-color);
    border-radius: var(--border-radius-lg);
    font-family: var(--font-body);
    font-weight: 500;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: var(--shadow-elevation-1);
}

.stSelectbox > div > div:hover {
    border-color: var(--border-focus);
    box-shadow: 0 8px 25px -8px rgba(0, 18, 25, 0.25);
    transform: translateY(-1px);
}

.stSelectbox > div > div:focus-within {
    border-color: var(--border-focus);
    box-shadow:
        0 0 0 3px rgba(0, 18, 25, 0.1),
        var(--shadow-elevation-2);
    transform: translateY(-2px);
}

.stSlider > div > div {
    background: var(--surface-glass);
    backdrop-filter: blur(20px) saturate(180%);
    border-radius: var(--border-radius-lg);
    padding: var(--space-md);
    border: var(--border-width) solid var(--border-color);
    box-shadow: var(--shadow-elevation-1);
    transition: all 0.3s ease;
}

.stSlider > div > div:hover {
    box-shadow: var(--shadow-elevation-2);
    border-color: rgba(0, 18, 25, 0.3);
}

/* Enhanced Labels */
.stSelectbox label, .stSlider label {
    font-family: var(--font-body);
    font-weight: 600;
    color: var(--text-primary);
    font-size: 0.9rem;
    letter-spacing: -0.01em;
    text-transform: uppercase;
    margin-bottom: var(--space-xs);
}

/* Executive Buttons */
.stButton > button {
    background: var(--primary-gradient);
    color: var(--text-inverse);
    border: none;
    border-radius: var(--border-radius-lg);
    font-family: var(--font-body);
    font-weight: 600;
    font-size: 0.9rem;
    padding: var(--space-sm) var(--space-lg);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: var(--shadow-elevation-1);
    position: relative;
    overflow: hidden;
    letter-spacing: 0.025em;
    text-transform: uppercase;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s ease;
}

.stButton > button:hover::before {
    left: 100%;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow:
        var(--shadow-elevation-3),
        0 0 20px rgba(0, 18, 25, 0.4);
}

.stButton > button:active {
    transform: translateY(-1px) scale(0.98);
    transition: all 0.1s ease;
}

/* Executive Data Tables */
.dataframe {
    background: var(--surface-glass);
    backdrop-filter: blur(20px) saturate(180%);
    border-radius: var(--border-radius-lg);
    border: var(--border-width) solid var(--border-color);
    font-family: var(--font-body);
    box-shadow: var(--shadow-elevation-2);
    overflow: hidden;
}

.dataframe th {
    background: var(--executive-navy);
    color: var(--text-inverse);
    font-family: var(--font-display);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.075em;
    font-size: 0.75rem;
    padding: var(--space-md) var(--space-sm);
    position: sticky;
    top: 0;
    z-index: 10;
}

.dataframe td {
    padding: var(--space-sm);
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    transition: background-color 0.2s ease;
}

.dataframe tr:hover td {
    background-color: rgba(0, 18, 25, 0.05);
}

.dataframe tr:nth-child(even) {
    background-color: rgba(248, 250, 252, 0.5);
}

/* Executive Metrics */
[data-testid="metric-container"] {
    background: var(--surface-glass);
    backdrop-filter: blur(20px) saturate(180%);
    border: var(--border-width) solid var(--border-color);
    border-radius: var(--border-radius-lg);
    padding: var(--space-md);
    box-shadow: var(--shadow-elevation-1);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    min-height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--primary-gradient);
    transform: scaleX(0);
    transition: transform 0.4s ease;
}

[data-testid="metric-container"]:hover::before {
    transform: scaleX(1);
}

[data-testid="metric-container"]:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow:
        var(--shadow-elevation-3),
        var(--shadow-glow);
    border-color: rgba(0, 18, 25, 0.3);
}

[data-testid="metric-container"] [data-testid="metric-label"] {
    font-family: var(--font-body);
    font-weight: 600;
    color: var(--text-secondary);
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
    line-height: 1.2;
}

[data-testid="metric-container"] [data-testid="metric-value"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: var(--text-primary);
    line-height: 1.1;
    margin-bottom: 0.25rem;
}

[data-testid="metric-container"] [data-testid="metric-delta"] {
    font-family: var(--font-body);
    font-weight: 600;
    font-size: 0.75rem;
    line-height: 1.2;
}

/* Executive Chart Containers */
.js-plotly-plot {
    border-radius: var(--border-radius-xl);
    background: var(--surface-glass);
    backdrop-filter: blur(20px) saturate(180%);
    border: var(--border-width) solid var(--border-color);
    box-shadow: var(--shadow-elevation-2);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
    position: relative;
}

.js-plotly-plot::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(0, 18, 25, 0.02) 0%, transparent 50%);
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
    z-index: 1;
}

.js-plotly-plot:hover::before {
    opacity: 1;
}

.js-plotly-plot:hover {
    transform: translateY(-4px);
    box-shadow:
        var(--shadow-elevation-3),
        0 0 40px rgba(0, 18, 25, 0.15);
    border-color: rgba(0, 18, 25, 0.2);
}

/* Utility Classes */
.fade-in {
    animation: fadeIn 0.6s ease forwards;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Responsive Design */
@media (max-width: 768px) {
    .main-header {
        padding: var(--space-lg) var(--space-md);
        margin-bottom: var(--space-lg);
    }

    .main-header h1 {
        font-size: clamp(1.75rem, 6vw, 2.5rem);
    }

    .main-header p {
        font-size: clamp(0.9rem, 4vw, 1.1rem);
    }
}
</style>
"""

# Professional Chart Configuration
CHART_CONFIG = {
    'default_height': 500,
    'header_height': 450,
    'detailed_height': 650,
    'mobile_height': 400,
    'plot_bgcolor': 'rgba(255, 255, 255, 0.95)',
    'paper_bgcolor': 'rgba(255, 255, 255, 0.95)',
    'font_family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif',
    'title_font_family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif',
    'title_font_size': 18,
    'title_color': '#2c3e50',
    'axis_color': '#475569',
    'grid_color': 'rgba(71, 85, 105, 0.1)',
    'hover_bgcolor': 'rgba(0, 18, 25, 0.1)',
    'hover_border_color': '#001219',
    'margin': {'l': 60, 'r': 60, 't': 80, 'b': 60},
    'showlegend': True,
    'legend_orientation': 'h',
    'legend_y': -0.1
}

# KPI Configuration for automotive market
KPI_THRESHOLDS = {
    'sales_performance': {
        'low': 1000,
        'medium': 10000,
        'high': 100000,
        'excellent': 500000
    },
    'price_range': {
        'budget': 15000,
        'mid_range': 35000,
        'premium': 70000,
        'luxury': 150000
    },
    'market_share': {
        'low': 1,
        'medium': 5,
        'high': 10,
        'dominant': 20
    }
}

# Correlation Analysis Configuration
CORRELATION_CONFIG = {
    'numeric_columns': [
        'price_mean', 'price_min', 'price_max', 'total_sales', 'avg_sales',
        'max_sales', 'years_with_data'
    ],
    'correlation_threshold': 0.3,
    'top_correlations': 10
}

# Outlier Detection Configuration
OUTLIER_CONFIG = {
    'methods': ['iqr', 'zscore'],
    'outlier_columns': ['price_mean', 'total_sales', 'avg_sales'],
    'zscore_threshold': 3,
    'iqr_multiplier': 1.5
}

# Clustering Configuration
CLUSTERING_CONFIG = {
    'n_clusters': 5,
    'clustering_features': [
        'price_mean', 'total_sales', 'avg_sales', 'max_sales'
    ],
    'random_state': 42
}
