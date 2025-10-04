# src/app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from business_logic import analyzer # Importamos nuestro motor de análisis

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Análisis de Mercado de Coches",
    page_icon="🚗",
    layout="wide"
)

# --- Título Principal ---
st.title("🚗 Dashboard de Análisis del Mercado de Coches")
st.markdown("Utiliza los filtros en el panel de la izquierda para explorar los datos.")

# --- Sidebar (Panel de Filtros) ---
st.sidebar.header("Filtros")

# Obtenemos los datos para los filtros desde nuestro analizador
automaker_list = sorted(analyzer.get_automaker_list())
selected_automakers = st.sidebar.multiselect(
    'Selecciona Fabricantes',
    options=automaker_list,
    default=automaker_list[:5] if len(automaker_list) >= 5 else automaker_list # Top 5 or all available
)

top_n = st.sidebar.slider('Top N a mostrar', min_value=5, max_value=30, value=15, step=5)

# --- Lógica de Filtrado de Datos ---
# Obtenemos los datos una sola vez y los filtramos
sales_summary = analyzer.get_sales_summary()
price_summary = analyzer.get_price_range_by_model()

if selected_automakers:
    sales_filtered = sales_summary[sales_summary['Automaker'].isin(selected_automakers)]
    price_filtered = price_summary[price_summary['Automaker'].isin(selected_automakers)]
else:
    sales_filtered = sales_summary
    price_filtered = price_summary

# --- Layout del Dashboard (Cuerpo Principal) ---

# Métricas Clave (KPIs)
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(label="Modelos Analizados", value=len(price_filtered))
kpi2.metric(label="Ventas Totales (Unidades)", value=f"{int(sales_filtered['total_sales'].sum()):,}")
kpi3.metric(label="Precio Promedio", value=f"€{price_filtered['price_mean'].mean():,.2f}")

st.markdown("---")

# Visualizaciones
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Top {top_n} Modelos por Ventas")
    top_sales = sales_filtered.nlargest(top_n, 'total_sales')
    fig_sales = px.bar(top_sales,
                       x='Genmodel',
                       y='total_sales',
                       color='Automaker',
                       title=f'Top {top_n} Modelos por Ventas Totales',
                       labels={'Genmodel': 'Modelo', 'total_sales': 'Ventas Totales'})
    st.plotly_chart(fig_sales, use_container_width=True)

with col2:
    st.subheader(f"Top {top_n} Fabricantes por Precio Promedio")
    avg_price_by_maker = price_filtered.groupby('Automaker')['price_mean'].mean().sort_values(ascending=False).nlargest(top_n)
    fig_price = px.bar(avg_price_by_maker,
                       x=avg_price_by_maker.index,
                       y=avg_price_by_maker.values,
                       title=f'Top {top_n} Fabricantes por Precio Promedio',
                       labels={'x': 'Fabricante', 'y': 'Precio Promedio (€)'})
    st.plotly_chart(fig_price, use_container_width=True)

# Tabla de datos
st.markdown("---")
st.subheader("Datos Detallados")
st.dataframe(sales_filtered)
