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

# Handle NaN values in total_sales
total_sales_value = sales_filtered['total_sales'].sum()
if pd.isna(total_sales_value):
    total_sales_display = "0"
else:
    total_sales_display = f"{int(total_sales_value):,}"
kpi2.metric(label="Ventas Totales (Unidades)", value=total_sales_display)

# Handle NaN values in price_mean
avg_price_value = price_filtered['price_mean'].mean()
if pd.isna(avg_price_value):
    avg_price_display = "€0.00"
else:
    avg_price_display = f"€{avg_price_value:,.2f}"
kpi3.metric(label="Precio Promedio", value=avg_price_display)

st.markdown("---")

# Visualizaciones
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Top {top_n} Modelos por Ventas")
    # Filter out NaN values for sales chart
    sales_for_chart = sales_filtered.dropna(subset=['total_sales'])
    if not sales_for_chart.empty:
        top_sales = sales_for_chart.nlargest(top_n, 'total_sales')
        fig_sales = px.bar(top_sales,
                           x='Genmodel',
                           y='total_sales',
                           color='Automaker',
                           title=f'Top {top_n} Modelos por Ventas Totales',
                           labels={'Genmodel': 'Modelo', 'total_sales': 'Ventas Totales'})
        st.plotly_chart(fig_sales, use_container_width=True)
    else:
        st.info("No hay datos de ventas disponibles para los filtros seleccionados.")

with col2:
    st.subheader(f"Top {top_n} Fabricantes por Precio Promedio")
    # Filter out NaN values for price chart
    price_for_chart = price_filtered.dropna(subset=['price_mean'])
    if not price_for_chart.empty:
        avg_price_by_maker = price_for_chart.groupby('Automaker')['price_mean'].mean().sort_values(ascending=False).nlargest(top_n)
        fig_price = px.bar(avg_price_by_maker,
                           x=avg_price_by_maker.index,
                           y=avg_price_by_maker.values,
                           title=f'Top {top_n} Fabricantes por Precio Promedio',
                           labels={'x': 'Fabricante', 'y': 'Precio Promedio (€)'})
        st.plotly_chart(fig_price, use_container_width=True)
    else:
        st.info("No hay datos de precios disponibles para los filtros seleccionados.")

# Tabla de datos
st.markdown("---")
st.subheader("Datos Detallados")
st.dataframe(sales_filtered)
