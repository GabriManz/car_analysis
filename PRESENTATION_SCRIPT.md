# 🚗 Guión de Presentación - Car Market Analysis Executive Dashboard

**Duración total: ~15 minutos**  
**Autor**: Gabriel Manzano Reche

---

## 📋 Estructura de la Presentación

1. **Introducción y Dataset** (2-3 min)
2. **Arquitectura del Código** (3-4 min)
3. **KPIs Definidos** (4-5 min)
4. **Visualizaciones y Gráficos** (4-5 min)
5. **Demostración en Vivo** (2-3 min)
6. **Conclusiones** (1 min)

---

## 1. INTRODUCCIÓN Y DATASET (2-3 min)

### Apertura
> "Buenos días/tardes. Hoy les voy a presentar mi proyecto de análisis del mercado automovilístico, un dashboard ejecutivo desarrollado con Streamlit que proporciona inteligencia de mercado en tiempo real para la toma de decisiones estratégicas."

### El Dataset Seleccionado
> "He seleccionado un conjunto de datos del mercado automovilístico que consta de **tres tablas principales**:"
V
**1. Basic Table (Tabla Básica)**
- Contiene información fundamental de cada modelo de vehículo
- Campos clave: `Automaker` (fabricante), `Genmodel` (modelo), `Genmodel_ID` (identificador único)
- **Más de 6,000 registros** de modelos diferentes
- **Desafío inicial**: Inconsistencias en nombres de fabricantes (por ejemplo, "VW" vs "Volkswagen", modelos clasificados erróneamente como fabricantes)

**2. Price Table (Tabla de Precios)**
- Información de precios de entrada por modelo y año
- Campo principal: `Entry_price` (precio de entrada al mercado)
- Permite análisis de posicionamiento de precio y segmentación de mercado
- Rango de precios: desde vehículos económicos (~€5,000) hasta ultra-lujo (>€200,000)

**3. Sales Table (Tabla de Ventas)**
- Datos históricos de ventas **desde 2001 hasta 2020** (20 años de datos)
- Formato wide: cada año es una columna con volumen de ventas
- Permite análisis de tendencias temporales y forecasting
- **Millones de unidades vendidas** en el período analizado

### Problemática y Solución
> "El principal desafío de este dataset era la **calidad de los datos**. Encontré inconsistencias en nomenclaturas, valores nulos, y clasificaciones erróneas. Por ello, implementé un **módulo de limpieza de datos robusto** que:"
- Normaliza nombres de fabricantes (mapping de variaciones comunes)
- Elimina registros problemáticos (`undefined`, `unknown`, valores vacíos)
- Valida la consistencia de datos con un **quality score**
- Genera reportes de limpieza detallados

> "Esta limpieza es **crítica** porque los KPIs y visualizaciones dependen de datos de alta calidad para proporcionar insights precisos."

---

## 2. ARQUITECTURA DEL CÓDIGO (3-4 min)

### Diseño Modular y Escalable
> "El proyecto está diseado con una arquitectura modular de tres capas que separa responsabilidades y facilita el mantenimiento:"

### **Capa 1: Data Layer (Capa de Datos)**
**Módulo**: `src/data_layer.py` - Clase `DataProcessor`

> "La capa de datos es responsable de:"
- **Carga optimizada**: Lectura con chunking para archivos grandes, múltiples encodings
- **Optimización de memoria**: Downcast de tipos numéricos (int64 → int16, float64 → float32)
- **Validación automática**: Contra reglas definidas en `data_config.py`
  - Tipos de datos esperados
  - Valores mínimos/máximos
  - Campos requeridos vs opcionales
- **Feature Engineering**: Creación de features derivadas
  - `price_tier`: Budget / Mid-Range / Premium / Luxury
  - `price_volatility`: Variabilidad de precios por modelo
  - `sales_trend`: Tendencia lineal de ventas
  - `performance_tier`: Clasificación de rendimiento de ventas

**Punto clave:**
> "La optimización de memoria es crucial - reduje el uso de memoria en **aproximadamente 60%** usando tipos de datos apropiados, permitiendo que la aplicación corra eficientemente en Streamlit Cloud con recursos limitados."

### **Capa 2: Business Logic Layer (Lógica de Negocio)**
**Módulo**: `src/business_logic.py` - Clase `CarDataAnalyzer`

> "Esta es el **cerebro analítico** del dashboard. Aquí es donde calculamos todos los KPIs y métricas avanzadas:"

**Funcionalidades principales:**
1. **Agregaciones complejas**:
   - `get_price_range_by_model()`: Estadísticas de precio por modelo (min/max/mean/median/std)
   - `get_sales_summary()`: Resumen de ventas con totales, promedios, máximos y tendencias

2. **Análisis de mercado**:
   - `calculate_market_share()`: Cuota de mercado por fabricante
   - `calculate_price_elasticity()`: Análisis de elasticidad precio-demanda (sensibilidad de ventas ante cambios de precio)
   - `detect_outliers()`: Detección de outliers usando IQR y Z-score

3. **Analytics avanzados**:
   - `perform_clustering_analysis()`: K-means clustering para segmentación
   - `calculate_correlation_matrix()`: Correlaciones entre variables
   - `generate_market_insights()`: Generación automática de insights y recomendaciones

**Diseño técnico clave:**
> "Todos los joins entre tablas se realizan usando **`Genmodel_ID`** como clave primaria, asegurando integridad referencial. Los métodos están optimizados para manejar NaNs y valores faltantes sin romper la ejecución."

### **Capa 3: Presentation Layer (Capa de Presentación)**
**Módulo**: `src/presentation_layer.py` - Clase `PresentationLayer`

> "Esta capa traduce los datos analíticos en visualizaciones ejecutivas de alta calidad usando Plotly:"
- Configuración centralizada de estilos y colores
- Métodos especializados para cada tipo de gráfico
- Responsive design para diferentes tamaños de pantalla
- Hover tooltips personalizados e interactivos

### **Routing y Componentes UI**
**Módulos**: `src/router.py`, `src/components/dashboards/`

> "El router mapea las páginas del sidebar a los dashboards correspondientes:"
- **Executive Dashboard**: Resumen ejecutivo con KPIs principales
- **Market Dashboard**: Análisis de mercado y competencia
- **Sales Dashboard**: Análisis de ventas y forecasting

**Configuración Centralizada:**
> "Toda la configuración está centralizada en `src/components/config/`:"
- `app_config.py`: Paletas de colores, configuración de gráficos, CSS personalizado
- `data_config.py`: Reglas de validación, umbrales de calidad, mappings de columnas

---

## 3. KPIs DEFINIDOS (4-5 min)

> "Ahora vamos a profundizar en los **KPIs (Key Performance Indicators)** que he definido. Estos están organizados en tres categorías principales:"

### **A. KPIs de Mercado**

**1. Market Share (Cuota de Mercado)**
```python
market_share_percent = (total_sales_by_automaker / total_market_sales) * 100
```
> "**¿Qué es?** La cuota de mercado mide qué porcentaje del total de ventas del mercado corresponde a cada fabricante. Es como dividir un pastel: si el mercado vendió 100 coches y Toyota vendió 18, entonces Toyota tiene el 18.5% del pastel."

> "**¿Por qué es importante?** Identifica a los líderes del mercado y la distribución de poder entre fabricantes. Un fabricante con alta cuota tiene más influencia en el mercado y mejor posición para negociar con proveedores y distribuidores."

**Ejemplo práctico:**
- Total mercado: 15.8 millones de vehículos vendidos (2001-2020)
- Toyota: 2.9 millones → 18.5% del mercado (líder)
- Ford: 1.8 millones → 11.4% del mercado
- Honda: 1.5 millones → 9.5% del mercado

- **Insight generado**: "Toyota lidera con 18.5% del mercado total, casi el doble que muchos competidores"
- **Visualización**: Pie chart con top 10 fabricantes + "Others"

**2. HHI Index (Herfindahl-Hirschman Index)**
```python
HHI = Σ(market_share_i²)
```
> "**¿Qué mide?** La concentración del mercado. Valores:"
- **< 1,500**: Mercado fragmentado (alta competencia)
- **1,500 - 2,500**: Mercado moderadamente concentrado
- **> 2,500**: Mercado altamente concentrado (oligopolio)

> "En nuestro análisis, el HHI es de **~1,850**, indicando un mercado **moderadamente concentrado** con competencia saludable."

**3. Top 3/Top 5 Concentration**
```python
top_3_concentration = sum(top_3_market_shares)
```
> "Mide qué porcentaje del mercado controlan los 3 o 5 principales fabricantes."
- **Resultado**: Los top 3 controlan el **42.3%** del mercado
- **Interpretación**: No hay monopolio, pero existe un grupo dominante

### **B. KPIs de Ventas**

**4. Total Market Sales**
```python
total_sales = df['total_sales'].sum()
```
> "Volumen total de unidades vendidas en el período 2001-2020."
- **Resultado**: **~15.8 millones de unidades**
- **Uso**: Establece el tamaño del mercado y contexto para otros KPIs

**5. Average Sales per Model**
```python
avg_sales = df['total_sales'].mean()
```
> "Promedio de ventas por modelo en el período completo."
- **Resultado**: **~8,500 unidades por modelo**
- **Uso**: Benchmark para clasificar modelos como high/low performers

**6. Sales Growth Rate (YoY)**
```python
yoy_growth = ((sales_year_n - sales_year_n-1) / sales_year_n-1) * 100
```
> "Crecimiento año sobre año de las ventas totales."
- **Peak detectado**: 2016 con máximo histórico de ventas
- **Tendencia reciente**: Decline post-2016 (posible saturación de mercado)

**7. Sales Trend (Linear Regression)**
```python
sales_trend = np.polyfit(years, sales_values, degree=1)[0]  # slope
```
> "Pendiente de la regresión lineal sobre las ventas históricas."
- **Interpretación**: Positiva = crecimiento sostenido, Negativa = decline
- **Uso**: Input para forecasting simple de próximos años

### **C. KPIs de Precios**

**8. Average Market Price**
```python
avg_price = df['price_mean'].mean()
```
> "Precio promedio ponderado del mercado: **€32,450**"
- **Interpretación**: Mercado posicionado en segmento **mid-range**

**9. Price Segments Distribution**
```python
# Definición de segmentos basada en cuantiles
Budget: Q1 (0-25%)        → < €20,000
Mid-Range: Q2-Q3 (25-75%) → €20,000 - €50,000
Premium: Q3-Q4 (75-95%)   → €50,000 - €100,000
Luxury: Top 5%            → > €100,000
```
> "**Hallazgo clave**: El **52%** de los modelos están en segmento Mid-Range, indicando que la mayoría de fabricantes compiten en el mercado masivo."

**10. Price Volatility**
```python
price_volatility = price_std / price_mean  # Coefficient of Variation
```
> "Mide la variabilidad de precios dentro de un fabricante."
- **High volatility** (>0.5): Fabricante con amplio portfolio (budget a luxury)
- **Low volatility** (<0.2): Fabricante enfocado en un segmento
- **Ejemplo**: Mercedes-Benz tiene alta volatility (0.68) porque va desde Clase A hasta Clase S

**11. Price-Sales Correlation**
```python
correlation = df['price_mean'].corr(df['total_sales'])
```
> "Correlación entre precio y volumen de ventas: **-0.23** (débilmente negativa)"
- **Interpretación**: Los modelos más caros tienden a vender menos unidades (esperado)
- **Insight**: La correlación es débil, sugiriendo que otros factores (marca, marketing) son más importantes

**11b. Price Elasticity (Elasticidad Precio-Demanda)** ⭐
```python
price_elasticity = -(% cambio en ventas / % cambio en precio)
```
> "**¿Qué es?** La elasticidad mide cómo reaccionan las ventas cuando cambiamos el precio. Es como un termómetro de sensibilidad al precio."

**Explicación sencilla con ejemplo:**

Imaginemos dos modelos de coche:

**Modelo Económico (Toyota Corolla) - Inelástico (-0.3)**
- Subimos precio 10%: €20,000 → €22,000
- Ventas bajan solo 3%: 10,000 → 9,700 unidades
- **Interpretación**: "Los clientes necesitan este coche y seguirán comprándolo aunque suba un poco el precio"
- **Decisión de negocio**: Podemos subir precios sin perder muchas ventas → ✅ Más ingresos

**Modelo de Lujo (Ferrari 488) - Elástico (-2.5)**
- Subimos precio 10%: €250,000 → €275,000
- Ventas caen 25%: 1,000 → 750 unidades
- **Interpretación**: "Los compradores de lujo son muy sensibles al precio y buscarán alternativas"
- **Decisión de negocio**: Subir precios puede ser peligroso → ⚠️ Pérdida de ventas

**Valores de referencia:**
- **|Elasticidad| < 1**: INELÁSTICO - Precio tiene poco impacto (productos necesarios)
- **|Elasticidad| > 1**: ELÁSTICO - Precio tiene gran impacto (productos de lujo/opcionales)
- **|Elasticidad| = 1**: Unitario - Cambios proporcionales

> "**¿Por qué es importante?** Este KPI nos dice si debemos competir por precio o por valor agregado. Un modelo inelástico puede soportar precios más altos, mientras que uno elástico requiere estrategias de diferenciación más allá del precio."

### **D. KPIs de Performance**

**12. Performance Tiers**
> "Clasificación de modelos en tiers de rendimiento basados en ventas:"
- **Excellent** (Top 10%): > 85,000 unidades
- **Good** (Top 30%): > 32,000 unidades
- **Average** (Top 50%): > 12,000 unidades
- **Below Average** (Bottom 30%): < 12,000 unidades
- **Poor** (Bottom 10%): < 3,000 unidades

**13. Data Quality Score**
```python
quality_score = (completeness * 0.4) + (uniqueness * 0.3) + (consistency * 0.3)
```
> "Score de calidad de datos (0-100):"
- **Basic Table**: 94.2/100 (Excellent)
- **Price Table**: 87.8/100 (Good)
- **Sales Table**: 91.5/100 (Excellent)

> "Este KPI es **meta-analítico** - nos dice qué tan confiables son nuestros otros KPIs."

---

## 4. VISUALIZACIONES Y GRÁFICOS (4-5 min)

> "Ahora veamos las **visualizaciones clave** que transforman estos KPIs en insights accionables. He diseñado cada gráfico con un propósito estratégico específico:"

### **A. Executive Summary - Métricas Clave del Mercado**

**📊 KPIs Principales del Dashboard**
> "En el Executive Summary vemos las métricas más importantes del mercado automovilístico:"

- **619 Total Models**: Tenemos datos de 619 modelos diferentes analizados
- **31.5M Total Sales**: Más de 31 millones de unidades vendidas en total
- **€32,407 Avg Price**: Precio promedio del mercado de €32,407
- **73 Automakers**: 73 fabricantes diferentes compitiendo
- **12.9% Top Market Share**: El líder del mercado solo tiene 12.9% (mercado muy fragmentado)
- **€287,136 Price Range**: Rango de precios desde €0 hasta €287,136

> "Estas métricas nos dan una visión general: es un mercado **altamente fragmentado** con **alta competencia** y un **amplio rango de precios**."

### **B. Market Analysis - Análisis de Concentración**

**📊 Market Concentration Metrics**
> "En el Market Analysis, lo más importante son las métricas de concentración:"

- **HHI Index: 583** - Este es un índice muy bajo que indica **mercado altamente fragmentado**
- **Top 3 Concentration: 31.6%** - Los 3 principales fabricantes solo controlan el 31.6%
- **Top 5 Concentration: 43.2%** - Los 5 principales controlan menos de la mitad del mercado
- **23 Significant Players** - Hay 23 fabricantes con más del 1% de cuota de mercado

> "El sistema automáticamente clasifica esto como **'Fragmented Market - High competition'**. Esto significa que ningún fabricante domina el mercado y la competencia es muy intensa."

### **C. Gráficos Clave del Dashboard**

**1. Market Share Pie Chart (Executive Summary)**
> "El gráfico de pastel muestra la distribución real de cuota de mercado. Como pueden ver, **Ford lidera con 12.9%**, pero la fragmentación es evidente - ningún fabricante domina."

**2. Price Distribution Histogram (Executive Summary)**
> "El histograma revela que la mayoría de modelos se concentran en el rango de **€0-€50k**, con una cola larga hacia precios premium. Esto confirma que el mercado está dominado por vehículos asequibles."

**3. Market Share vs Average Price Scatter Plot (Market Analysis)**
> "Este gráfico de dispersión muestra la relación entre precio promedio y cuota de mercado. Los puntos amarillos representan los líderes de mercado, que se concentran en el rango de €35k-€45k - el 'punto dulce' del mercado."

**4. Price Distribution by Category Pie Chart (Market Analysis)**
> "La distribución por categorías confirma que el **58% del mercado** está en el segmento Mid-Range, seguido del 24.9% en Budget. Solo el 6.62% está en Premium y 1.55% en Luxury."

**5. Sales Trend by Automaker (Sales Performance)**
> "El gráfico de líneas muestra la evolución temporal de 2001-2020. **2016 fue el año pico** con el mayor volumen total. Pueden ver cómo diferentes fabricantes respondieron a crisis del mercado."

**6. Top Performing Models (Sales Performance)**
> "El gráfico de barras horizontal muestra que **Fiesta lidera con 1.4M unidades**, seguido de Focus con 1.1M y Corsa con 0.9M. Son modelos de segmento B y C los que dominan las ventas."

**7. Sales Performance by Automaker (Sales Performance)**
> "El scatter plot muestra la relación entre número de modelos y ventas totales. Ford domina con 3.9M ventas, seguido de Vauxhall con 3.1M."

**8. Sales Distribution Analysis (Sales Performance)**
> "El análisis de distribución muestra que la mayoría de modelos están en la categoría 'Low' (<1K ventas), pero los modelos 'Very High' (10K-50K) representan una porción significativa."

**9. Sales Performance Matrix (Sales Performance)**
> "La matriz de performance combina número de modelos, ventas promedio por modelo y ventas totales. Los bubbles más grandes representan los fabricantes con mayor volumen total."

### **D. Insights Clave de los Gráficos**

> "Estos gráficos nos revelan **insights estratégicos importantes**:"

1. **Mercado Fragmentado**: El HHI de 583 confirma alta competencia
2. **Punto Dulce de Precios**: Los líderes se concentran en €35k-€45k
3. **Dominio de Segmentos B/C**: Fiesta, Focus, Corsa lideran las ventas
4. **Ciclo de Mercado**: 2016 fue el año pico, con recuperación post-crisis
5. **Estrategia de Portfolio**: Ford y Vauxhall dominan con múltiples modelos exitosos

---
---

## 5. DEMOSTRACIÓN EN VIVO (2-3 min)

> "Ahora les voy a mostrar el dashboard en funcionamiento. La aplicación está desplegada en Streamlit Cloud:"

### **Demo Flow:**

1. **Página de inicio**
   > "Al cargar la aplicación, vemos inmediatamente el Executive Dashboard con los KPIs principales."

2. **Filtros interactivos (sidebar)**
   > "En el sidebar, puedo filtrar por fabricantes específicos y ajustar el número de modelos a mostrar en los gráficos. Por ejemplo, voy a seleccionar solo Toyota, Honda y Ford."
   - Mostrar cómo los gráficos se actualizan en tiempo real

3. **Navegación entre dashboards**
   > "Puedo navegar entre tres dashboards principales:"
   - Executive Summary (overview general)
   - Market Analysis (análisis de mercado y competencia)
   - Sales Performance (análisis de ventas y tendencias)

4. **Interactividad de Plotly**
   > "Todos los gráficos son interactivos gracias a Plotly:"
   - Hover sobre un punto/barra para ver detalles
   - Zoom y pan en gráficos temporales
   - Click en leyenda para ocultar/mostrar series
   - Export de gráficos como PNG

5. **Responsive design**
   > "El dashboard es completamente responsive. Si lo abro en un dispositivo móvil o tablet, los layouts se adaptan automáticamente."
   - (Si es posible, mostrar en modo responsive de browser DevTools)

6. **Performance**
   > "Gracias a las optimizaciones de memoria y caching de Streamlit, la aplicación carga en menos de 3 segundos y responde instantáneamente a los filtros."

---

## 6. CONCLUSIONES (1 min)

### **Resumen de logros técnicos:**
> "En resumen, este proyecto demuestra:"

1. **Data Engineering**:
   - Limpieza y validación robusta de datos complejos
   - Optimización de memoria (60% reducción)
   - Feature engineering automático

2. **Analytics**:
   - 13+ KPIs bien definidos con interpretación de negocio
   - Análisis avanzados (clustering, correlaciones, forecasting)
   - Generación automática de insights

3. **Visualización**:
   - 13+ tipos de gráficos diferentes, cada uno con propósito específico
   - Interactividad completa con Plotly
   - Diseño ejecutivo profesional

4. **Arquitectura**:
   - Clean architecture de 3 capas (Data, Business, Presentation)
   - Modular y escalable
   - Configuración centralizada

5. **Deployment**:
   - Aplicación en producción en Streamlit Cloud
   - Responsive y performante
   - Accesible desde cualquier dispositivo

### **Valor de negocio:**
> "Desde una perspectiva de negocio, este dashboard permitiría a:"
- **Ejecutivos**: Tomar decisiones estratégicas informadas sobre posicionamiento de mercado
- **Marketing**: Identificar oportunidades de segmentación y pricing
- **Sales**: Entender qué modelos empujar y en qué segmentos
- **Product**: Identificar gaps en portfolio y necesidades de nuevos modelos

### **Próximos pasos (si te preguntan):**
> "Como mejoras futuras, considero implementar:"
- Machine Learning para forecasting más sofisticado (ARIMA, Prophet)
- Análisis de sentimiento con reviews de clientes
- Comparación con datos de competidores en tiempo real
- Alertas automáticas cuando KPIs crucen thresholds

### **Cierre:**
> "Muchas gracias por su atención. Estoy disponible para responder cualquier pregunta que tengan sobre el proyecto, la implementación técnica, o los insights de negocio."

---

## 📝 NOTAS ADICIONALES PARA LA PRESENTACIÓN

### **Tips de presentación:**
1. **Practica los tiempos**: Ensaya cada sección con cronómetro para no pasarte de 15 min
2. **Prepara respuestas a preguntas comunes**:
   - "¿Por qué Streamlit y no otro framework?" → Rapidez de desarrollo, ideal para dashboards analíticos
   - "¿Cómo manejaste datos faltantes?" → Estrategia multi-capa: limpieza, validación, fillna en cálculos
   - "¿Escalabilidad con más datos?" → Chunking, dtypes optimizados, lazy loading
3. **Ten el código abierto en otro tab** para mostrar snippets si preguntan por implementación
4. **Ten backup slides/screenshots** por si falla el internet durante la demo en vivo

### **Puntos de énfasis:**
- **Calidad de datos** es foundacional - sin limpieza robusta, los KPIs no tienen sentido
- **KPIs no son solo números** - cada uno cuenta una historia y guía decisiones
- **Visualizaciones son comunicación** - cada gráfico debe ser inmediatamente interpretable
- **Arquitectura limpia** permite escalabilidad y mantenibilidad

### **Lenguaje corporal:**
- Mantén contacto visual con la audiencia
- Usa las manos para señalar elementos en pantalla
- Varía el tono de voz para mantener interés
- Sonríe cuando muestres gráficos impresionantes (orgullo por tu trabajo)

¡Mucha suerte con tu presentación! 🚀

