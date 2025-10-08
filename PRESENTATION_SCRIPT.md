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

> "Ahora voy a recorrer la app en el mismo orden que verán en Streamlit: primero Executive Summary, luego Market Analysis y por último Sales Performance."

### 🧭 Executive Summary

#### 1) Executive Summary (KPI Cards)
- **619 Total Models** · **31.5M Total Sales** · **€32,407 Avg Price** · **73 Automakers** · **12.9% Top Market Share** · **€287,136 Price Range**
- Mensaje: Mercado grande, muy fragmentado y con amplio rango de precios.

#### 2) Sales Performance Analysis
- **Top Models by Sales (bar)**
  - Cómo leer: barras ordenadas por volumen; hover para ver cifras exactas.
  - **Lo que muestra**: Fiesta lidera con ~1.4M unidades, seguido de Focus (~1.1M), Corsa (~0.9M), Golf (~1.0M), Astra (~0.8M). Modelos de segmento B/C dominan.
  - **Conclusiones clave**:
    - **Dominio de segmento B/C**: Los 5 modelos top son todos de segmento B/C → "El mercado masivo se concentra en coches compactos y medianos"
    - **Gap significativo**: Fiesta (1.4M) vs Focus (1.1M) = 300k diferencia → "Fiesta tiene ventaja competitiva clara"
    - **Concentración de ventas**: Top 5 modelos representan ~5.2M de 31.5M total → "16.5% de modelos generan 16.5% de ventas (regla 80/20)"
    - **Estrategia de portfolio**: Ford tiene 2 modelos en top 5 → "Diversificación exitosa vs dependencia de un solo hit"
  - Responde: ¿qué modelos empujan el volumen total? ¿cuál es el gap entre #1 y #5?
  - Decisiones: foco comercial, mix de producción, campañas por modelo.
- **Average Price by Automaker (bar)**
  - Cómo leer: fabricantes ordenados por precio medio; compara clusters low/mid/premium.
  - **Lo que muestra**: Maybach (~220k), Rolls-Royce (~200k), Bentley (~180k) en la cima. Tesla, Porsche, BMW, Mercedes en rango premium. Toyota, Hyundai en zona media-baja (~20-30k).
  - **Conclusiones clave**:
    - **Segmentación clara**: 3 clusters bien definidos: Ultra-lujo (200k+), Premium (50-100k), Masivo (20-40k) → "Mercado bien segmentado por precio"
    - **Tesla disruptor**: Tesla en rango premium (80-100k) vs marcas tradicionales → "Nuevos entrantes pueden competir en premium"
    - **Gap de precio**: Salto de 40k (Toyota) a 80k (Tesla) → "Oportunidad en segmento 40-80k"
    - **Estrategia de grupos**: BMW/Mercedes vs Toyota/Hyundai → "Dos estrategias: premium vs masivo"
  - Responde: ¿quién compite en entry vs premium? ¿hay canibalización entre marcas del mismo grupo?
  - Decisiones: reajuste de pricing/posicionamiento, bundles por marca.
- **Sales Volume by Market Segment (treemap)**
  - Cómo leer: rectángulos ∝ ventas; colores por segmento.
  - **Lo que muestra**: Mid-Range (amarillo, 49.0%) y Budget (verde, 44.1%) dominan con 93% del volumen. Premium (naranja, 6.9%) y Luxury (0.0%) son nichos pequeños.
  - **Diferencia clave vs Price Distribution by Category**: Este gráfico mide **VOLUMEN DE VENTAS** (unidades vendidas), mientras que Price Distribution mide **NÚMERO DE MODELOS** disponibles. Budget tiene 58% de modelos pero solo 44% de ventas → sobresaturación de oferta.
  - **Conclusiones clave**:
    - **Mercado masivo**: 93% de ventas en Budget + Mid-Range → "El mercado se concentra en precios accesibles"
    - **Premium nicho**: Solo 6.9% de ventas en Premium → "Segmento premium es pequeño pero rentable"
    - **Luxury inexistente**: 0.0% de ventas en Luxury → "Ultra-lujo no tiene volumen significativo"
    - **Estrategia dual**: Volumen en masivo, margen en premium → "Necesario balance entre volumen y rentabilidad"
  - Responde: ¿qué segmento domina el mercado? ¿cuál es el tamaño real de premium/luxury?
  - Decisiones: estrategia de portfolio (volumen en Mid-Range, margen en Premium/Luxury).

#### 3) Advanced Analytics
- **Price vs Sales Correlation (scatter)**
  - Cómo leer: eje X precio medio; eje Y ventas; tamaño = volumen; color = marca.
  - **Lo que muestra**: Mayoría de burbujas en esquina inferior izquierda (precios <100k, ventas <0.5M). Burbuja grande en superior izquierda (altas ventas, bajo precio). A medida que precio sube, ventas bajan (trade-off esperado).
  - **Conclusiones clave**:
    - **Trade-off confirmado**: Precio alto = ventas bajas → "Ley fundamental del mercado automovilístico"
    - **Sweet spot identificado**: Burbuja grande en superior izquierda → "Existe un punto óptimo de precio-volumen"
    - **Excepciones valiosas**: Burbujas en esquina superior derecha → "Algunos modelos premium venden bien (diferenciación)"
    - **Estrategia de pricing**: Evitar esquina inferior derecha → "Precios altos sin diferenciación = fracaso"
  - Responde: ¿existe un trade-off precio-volumen? ¿quién rompe la regla (caros que venden mucho)?
  - Decisiones: identificar "sweet spot" de precio y excepciones por diferenciación.
- **Price Distribution by Category (pie)**
  - Cómo leer: porcentaje de modelos por tier de precio.
  - **Lo que muestra**: Budget (<€20K) domina con 58%, Mid-range (€20K-€40K) 24.9%, Premium (€40K-€60K) 6.62%, Super Luxury (>€100K) 6.62%, Luxury (€60K-€100K) 3.88%. Budget + Mid-range = 82.9% del mercado.
  - **Diferencia clave vs Sales Volume by Market Segment**: Este gráfico mide **DIVERSIDAD DE OFERTA** (número de modelos), mientras que Sales Volume mide **VOLUMEN DE VENTAS** (unidades vendidas). Mid-Range tiene solo 25% de modelos pero 49% de ventas → alta eficiencia de mercado.
  - **Conclusiones clave**:
    - **Sobresaturación Budget**: 58% de modelos vs 44% de ventas → "Mercado Budget saturado, competencia feroz"
    - **Eficiencia Mid-Range**: 25% de modelos vs 49% de ventas → "Segmento Mid-Range muy eficiente"
    - **Oportunidad Premium**: Solo 6.62% de modelos en Premium → "Espacio para más modelos premium"
    - **Luxury nicho**: 3.88% de modelos en Luxury → "Segmento ultra-exclusivo"
  - Responde: ¿estamos sesgados a Mid-Range? ¿espacio para ampliar Premium?
  - Decisiones: reequilibrar roadmap por tier.
- **Price Distribution by Automaker (box)**
  - Cómo leer: caja (Q1–Q3), línea (mediana), whiskers y outliers.
  - **Lo que muestra**: BMW y Mercedes-Benz con medianas 40-50k, bigotes hasta 70-80k, outliers >100k (premium). Citroen, Fiat, Ford, Hyundai, Nissan, Peugeot, Toyota, Vauxhall con medianas 10-25k (budget/mid-range). Toyota y Nissan con outliers premium.
  - **Conclusiones clave**:
    - **Estrategias claras**: BMW/Mercedes (premium puro) vs Ford/Toyota (masivo) → "Dos estrategias de portfolio bien definidas"
    - **Outliers valiosos**: Toyota/Nissan con modelos premium → "Marcas masivas pueden competir en premium"
    - **Amplitud de gama**: BMW/Mercedes con bigotes largos → "Portfolio amplio en premium"
    - **Consistencia de precio**: Marcas masivas con cajas estrechas → "Enfoque en segmento específico"
  - Responde: ¿qué marcas tienen portfolio amplio vs enfocado? ¿outliers que requieren narrativa?
  - Decisiones: simplificar gama o ampliar según estrategia.
- **Sales Heatmap by Year (heatmap)**
  - Cómo leer: intensidad de color por métrica/año; patrones verticales/horizontales.
  - **Lo que muestra**: Correlaciones fuertes (azul oscuro) entre total_sales, avg_sales, max_sales, min_sales, sales_std. years_with_data correlaciona positivamente con ventas (modelos longevos = más ventas acumuladas). sales_trend con correlaciones más débiles. Automaker_ID sin correlación (identificador).
  - **Conclusiones clave**:
    - **Correlaciones fuertes (azul oscuro)**: total_sales, avg_sales, max_sales, min_sales, sales_std están altamente correlacionadas → "Los modelos que venden mucho también tienen alta variabilidad de ventas y promedios altos"
    - **years_with_data correlaciona con ventas**: Modelos con más años en el mercado tienen mayores ventas acumuladas → "La longevidad del modelo es predictor de éxito"
    - **sales_trend correlaciones débiles**: La tendencia de crecimiento no está fuertemente ligada a las ventas totales → "El crecimiento no garantiza volumen total"
    - **Automaker_ID sin correlación**: El identificador numérico no influye en el rendimiento → "El éxito no depende del orden de entrada al mercado"
  - Responde: ¿años pico/valle? ¿métricas que co-varían?
  - Decisiones: planificación de lanzamientos y capacidades.

> Clasificación de precios utilizada (cuantiles sobre `price_mean`):
- **Budget**: Bottom 25% (≤ Q1)
- **Mid-Range**: Q1–Q3 (25–75%)
- **Premium**: Q3–Q95 (75–95%)
- **Luxury**: Top 5% (> Q95)

---

### 🌍 Market Analysis

#### 1) Market Share & Distribution Analysis
- **📊 Market Concentration Metrics**
  - Cómo leer: HHI (∑ share²), Top3/Top5, nº de jugadores >1%.
  - **Lo que muestra**: HHI = 583, Top 3 = 31.6%, Top 5 = 43.2%, 23 jugadores significativos (>1%). Sistema clasifica como "Fragmented Market - High competition".
  - **Conclusiones clave**:
    - **Mercado fragmentado**: HHI = 583 (<1500) → "Alta competencia, ningún monopolio"
    - **Liderazgo débil**: Top 3 solo 31.6% → "Ningún fabricante domina el mercado"
    - **Oportunidad de entrada**: 23 jugadores significativos → "Mercado accesible para nuevos entrantes"
    - **Competencia saludable**: Fragmentación alta → "Innovación y eficiencia premiadas"
  - Responde: ¿nivel de competencia? ¿riesgo de concentración?
  - Decisiones: estrategia de entrada/defensa según fragmentación.
- **Market Share by Automaker (pie/bar)**
  - Cómo leer: top 10 + "Others"; atención al tamaño de "Others".
  - **Lo que muestra**: Ford lidera con 19.7%, seguido de Vauxhall (15.1%), Volkswagen (13.5%), BMW (9.19%), Audi (8.58%), Mercedes-Benz (7.66%), Nissan (7.42%), Toyota (7.32%), Peugeot (6.61%), Honda (4.86%). Fragmentación evidente - ningún fabricante domina.
  - **Conclusiones clave**:
    - **Liderazgo relativo**: Ford 19.7% vs Vauxhall 15.1% → "Ford lidera pero sin dominancia absoluta"
    - **Grupo alemán fuerte**: VW (13.5%) + BMW (9.19%) + Audi (8.58%) = 31.27% → "Grupo alemán domina premium"
    - **Fragmentación extrema**: Top 10 suman ~100% → "Mercado muy fragmentado, sin 'Others' significativos"
    - **Oportunidad de crecimiento**: Gap entre #1 (19.7%) y #2 (15.1%) → "Espacio para que Vauxhall crezca"
  - Responde: ¿quién lidera realmente? ¿cuán parejo es el top?
  - Decisiones: alianzas, pricing, distribución.
- **Price Distribution Analysis (histogram)**
  - Cómo leer: sesgo a la izquierda (muchos modelos económicos) y cola larga.
  - **Lo que muestra**: Pico masivo en 0-50k (~340-350 modelos), segundo pico en 50-100k (~150 modelos). Distribución fuertemente sesgada hacia precios bajos. Muy pocos modelos >100k, casi ninguno >200k.
  - **Conclusiones clave**:
    - **Mercado masivo**: 70% de modelos en 0-50k → "El mercado se concentra en precios accesibles"
    - **Oportunidad premium**: Solo 30% de modelos en 50k+ → "Espacio para más modelos premium"
    - **Ultra-lujo nicho**: Muy pocos modelos >100k → "Segmento ultra-exclusivo"
    - **Estrategia de pricing**: Evitar saturación en 0-50k → "Diferenciación en premium"
  - Responde: ¿elasticidad potencial del mercado? ¿oportunidad en rangos poco poblados?
  - Decisiones: lanzamiento de modelos en huecos de precio.

#### 2) Market Trends & Analytics
- **Market Share vs Average Price (bubble)**
  - Cómo leer: X precio, Y cuota, tamaño volumen, color marca.
  - **Lo que muestra**: Mayoría de puntos pequeños púrpuras (baja cuota, precios bajos). Dos burbujas grandes amarillo-verdes destacan: una en 20-25k con ~5% cuota, otra en 25-30k con ~6% cuota. Sweet spot en precios bajos (20-30k).
  - **Conclusiones clave**:
    - **Sweet spot identificado**: 20-30k con 5-6% cuota → "Precios bajos generan alta cuota de mercado"
    - **Estrategia de volumen**: Precios bajos = alta cuota → "Competir por precio para ganar share"
    - **Premium limitado**: Pocas burbujas grandes en precios altos → "Premium no genera alta cuota"
    - **Oportunidad de diferenciación**: Espacio en 30-50k → "Posición intermedia poco explotada"
  - Responde: ¿quién captura share cobrando más? ¿punto dulce €35–45k?
  - Decisiones: subir/bajar precio para movernos hacia el cuadrante objetivo.
- **Price Range Distribution (hist/box)**
  - Cómo leer: dispersión global; identifica multimodalidad.
  - **Lo que muestra**: Histograma azul con pico masivo en 0-10k (~260 modelos). Distribución fuertemente sesgada a la izquierda. Box plot estrecho hacia la izquierda, bigote largo hacia la derecha, múltiples outliers azules (modelos premium/luxury).
  - **Conclusiones clave**:
    - **Sesgo extremo**: Pico masivo en 0-10k → "Mercado dominado por modelos económicos"
    - **Outliers valiosos**: Múltiples outliers en precios altos → "Modelos premium/luxury son excepciones"
    - **Box plot estrecho**: Mediana cerca del mínimo → "La mayoría de modelos son económicos"
    - **Bigote largo**: Cola larga hacia precios altos → "Amplio rango de precios pero pocos modelos"
  - Responde: ¿segmentación natural? ¿necesidad de sub-marcas?
  - Decisiones: arquitectura de marcas.
- **Market Positioning by Price Segment (stacked bar)**
  - Cómo leer: nº de modelos por segmento y fabricante.
  - **Lo que muestra**: Citroen, Fiat, Ford, Peugeot, Renault con 18-27 modelos (predominantemente Budget/Mid-Range). Audi, BMW, Mercedes exclusivamente Premium/Luxury (BMW/Mercedes ~24 modelos, Audi ~12). Ferrari puramente Luxury (~13 modelos). Toyota, Honda, Hyundai con mix balanceado.
  - **Conclusiones clave**:
    - **Estrategias claras**: Masivos (Ford, Renault) vs Premium (BMW, Mercedes) → "Dos estrategias de portfolio bien definidas"
    - **Diversificación exitosa**: Toyota, Honda con mix balanceado → "Estrategia de diversificación funciona"
    - **Nicho premium**: BMW/Mercedes exclusivamente premium → "Enfoque en segmento premium rentable"
    - **Ultra-lujo puro**: Ferrari solo luxury → "Estrategia de ultra-exclusividad"
  - Responde: ¿diversificados (Ford/Toyota) vs nicho (Ferrari/Lambo)?
  - Decisiones: expansión o foco por fabricante.

---

### 📈 Sales Performance

#### 1) Advanced Sales Performance Analytics
- **Sales Trend by Automaker (multi-line)**
  - Cómo leer: líneas por marca 2001–2020; anotar 2008 y pico 2016.
  - **Lo que muestra**: 73 líneas de colores diferentes (ABARTH, ACURA, AIXAM, ALFA ROMEO, AUDI, BMW, BENTLEY, etc.). Anotación "Peak Year (2016)" marca el máximo histórico. Líneas top alcanzan 200-250k unidades en 2016. Líneas suben desde 2001, pico en 2016, luego declive hacia 2020.
  - **Conclusiones clave**:
    - **Ciclo del mercado**: Pico en 2016, declive post-2016 → "Mercado maduro, posible saturación"
    - **Crecimiento sostenido**: 2001-2016 crecimiento general → "Período de expansión del mercado"
    - **Diferenciación de marcas**: Líneas top vs líneas bajas → "Algunas marcas dominan consistentemente"
    - **Crisis 2008**: Impacto visible en algunas líneas → "Resiliencia diferenciada por marca"
  - Responde: ¿quién crece sostenidamente? ¿quién es cíclico?
  - Decisiones: inversiones y asignación comercial.
- **Top Performing Models (bar)**
  - Cómo leer: ranking acumulado; evaluar concentración en pocos hits.
  - **Lo que muestra**: Fiesta lidera con ~1.5M, seguido de Focus (~1.2M), Corsa (~1M), Astra (~0.9M), Golf (~0.8M), Polo (~0.7M), Hatch (~0.6M), Qashqai (~0.55M), 3 Series (~0.5M), 1 Series/Yaris (~0.4M). Modelos de segmento B/C dominan.
  - **Conclusiones clave**:
    - **Dominio de segmento B/C**: Top 10 modelos son B/C → "El mercado masivo se concentra en compactos"
    - **Ford lidera**: Fiesta + Focus = 2.7M → "Ford domina con dos superventas"
    - **Concentración moderada**: Gap gradual entre posiciones → "No hay monopolio de un solo modelo"
    - **Diversificación exitosa**: Múltiples marcas en top 10 → "Competencia saludable"
  - Responde: ¿dependencia de superventas? ¿riesgo si cae el #1?
  - Decisiones: diversificar o duplicar apuesta.
- **Sales Performance by Automaker (bubble)**
  - Cómo leer: X nº modelos, Y ventas promedio, tamaño = ventas totales.
  - **Lo que muestra**: Ford domina con 4.065M (bubble azul oscuro), Vauxhall 3.121M (verde claro), Volkswagen 2.787M (gris/púrpura), BMW 1.895M (naranja oscuro), Audi 1.769M (púrpura claro), Mercedes-Benz 1.580M (rosa), Nissan 1.529M (rojo), Toyota 1.510M (verde). Bubbles más grandes = mayor volumen total.
  - **Conclusiones clave**:
    - **Ford dominante**: 4.065M vs #2 Vauxhall 3.121M → "Ford lidera con ventaja significativa"
    - **Grupo alemán fuerte**: VW + BMW + Audi = 6.45M → "Grupo alemán domina premium"
    - **Estrategias diferenciadas**: Ford (volumen) vs BMW (premium) → "Dos estrategias exitosas"
    - **Competencia equilibrada**: Top 8 con 1.5-4M → "Mercado fragmentado pero con líderes claros"
  - Responde: ¿portfolio eficiente (muchos modelos que venden bien) vs ineficiente?
  - Decisiones: poda de gama o refuerzo.

#### 2) Advanced Sales Analytics
- **Sales Distribution Analysis (histogram)**
  - Cómo leer: conteo por tier (Low→Exceptional).
  - **Lo que muestra**: "Low (<1K)" domina con ~210 modelos (barra amarilla), seguido de "Very High (10K-50K)" ~165 modelos (naranja), "Medium (1K-5K)" ~150 modelos (rojo), "Exceptional (>50K)" ~130 modelos (púrpura), "High (5K-10K)" ~65 modelos (azul oscuro). Distribución típica 80/20.
  - **Conclusiones clave**:
    - **Long tail dominante**: 210 modelos "Low" vs 130 "Exceptional" → "Mayoría de modelos venden poco"
    - **Distribución 80/20**: Pocos modelos excepcionales, muchos low performers → "Regla de Pareto confirmada"
    - **Oportunidad de optimización**: 210 modelos low performers → "Espacio para mejorar o eliminar"
    - **Estrategia dual**: Foco en excepcionales + optimización long tail → "Balance entre hits y eficiencia"
  - Responde: ¿regla 80/20? ¿cuánto representa el long tail?
  - Decisiones: long-tail optimization vs foco en top sellers.
- **Sales Performance Matrix (scatter)**
  - Cómo leer: cuadrantes (focalizados, eficientes, ineficientes, exploradores).
  - **Lo que muestra**: Ford (bubble azul oscuro, 4.065M total sales), Vauxhall (verde claro, 3.121M), Volkswagen (gris/púrpura, 2.787M), BMW (naranja oscuro, 1.895M), Audi (púrpura claro, 1.769M), Mercedes-Benz (rosa, 1.580M), Nissan (rojo, 1.529M), Toyota (verde, 1.510M). Estrategias de portfolio claramente diferenciadas por tamaño de bubble.
  - **Conclusiones clave**:
    - **Ford líder absoluto**: 4.065M vs competencia → "Ford domina con estrategia de volumen"
    - **Grupo alemán consolidado**: VW + BMW + Audi = 6.45M → "Estrategia premium exitosa"
    - **Competencia equilibrada**: Top 8 con 1.5-4M → "Mercado fragmentado pero estable"
    - **Estrategias diferenciadas**: Volumen (Ford) vs Premium (BMW) → "Dos modelos de negocio exitosos"
  - Responde: ¿qué estrategia de portfolio sigue cada marca?
  - Decisiones: priorización de inversiones por cuadrante.

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

