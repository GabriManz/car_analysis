# Centralized application configuration and styles

APP_CONFIG = {
    'title': 'Car Market Analysis Executive Dashboard',
    'icon': '🚗',
    'version': '2.0.0'
}

CUSTOM_CSS = """
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2.5rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.main-header::before {
    content: "🚗";
    position: absolute;
    top: 20px;
    right: 30px;
    font-size: 4rem;
    opacity: 0.3;
    z-index: 1;
}
.main-header h1 {
    font-size: 3rem;
    margin: 0;
    text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
    font-weight: 700;
    position: relative;
    z-index: 2;
}
.main-header p {
    font-size: 1.3rem;
    margin: 0.5rem 0 0 0;
    opacity: 0.95;
    position: relative;
    z-index: 2;
    font-weight: 300;
}
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    border: 1px solid rgba(255,255,255,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    position: relative;
    overflow: hidden;
}
.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);
}
.metric-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
    pointer-events: none;
}
.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 1rem 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    position: relative;
    z-index: 1;
}
.metric-label {
    font-size: 1.1rem;
    opacity: 0.9;
    font-weight: 500;
    position: relative;
    z-index: 1;
}
.metric-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 1;
}
.section-header {
    background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 10px;
    margin: 2rem 0 1rem 0;
    font-size: 1.5rem;
    font-weight: 600;
    text-align: center;
    box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
}
.chart-container {
    background: rgba(255,255,255,0.05);
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
}
</style>
"""


