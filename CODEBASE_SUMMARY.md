# Codebase Summary

## Repository Overview
- **Purpose**: Car Market Analysis Executive Dashboard for automotive market intelligence using Streamlit, pandas, and Plotly.
- **Key Data Sources**: CSV files in `data/` (`Basic_table.csv`, `Price_table.csv`, `Sales_table.csv`).
- **Primary App Entrypoint**: `app.py` (Streamlit app launcher; dashboards rendered via `src/router.py`).
- **Core Logic Location**: `src/` (data processing, business logic, visualization layer, dashboards, and configs).

## Project Structure (high-level)
- `app.py`: Initializes Streamlit, wires UI and routing.
- `data/`: CSV data files used by the app.
- `notebooks/`: EDA, cleaning, and exploratory notebooks.
- `src/`: Main application source code (detailed below).
- `README.md`: Project documentation and deployment link.
- `requirements.txt`, `runtime.txt`: Dependencies and runtime configuration.

## src/ Overview
- `src/data_cleaner.py`: Reusable cleaning utilities for `Automaker` and `Genmodel`, plus validation and reporting.
- `src/data_layer.py`: `DataProcessor` class for loading, validating, optimizing, feature engineering, and exporting datasets.
- `src/business_logic.py`: `CarDataAnalyzer` class providing analytics over the datasets (KPIs, market share, clustering, correlations, insights).
- `src/presentation_layer.py`: `PresentationLayer` to generate Plotly figures, dashboards composites, and responsive utilities.
- `src/router.py`: Page router that maps menu items to `executive`, `market`, and `sales` dashboards.
- `src/components/`: UI, dashboards, analytics utilities, charts, and configs.
- `src/config/`: Additional app/deployment configuration.

### src/data_cleaner.py
- **Key functions**:
  - `clean_automaker_data(df)`: Normalizes `Automaker`, fixes known mislabels (e.g., 'VW'→'Volkswagen', 'Mercedes'→'Mercedes-Benz'), removes problematic placeholders (`undefined`, `unknown`, empty strings), trims/condenses spaces, and logs a cleaning report.
  - `validate_automaker_consistency(df)`: Validates `Automaker` column (nulls, empties, duplicates, suspicious tokens) and returns a scored quality report with status and recommendations.
  - `clean_genmodel_data(df)`: Trims and de-spaces `Genmodel`, removes problematic values.
  - `clean_all_data(df)`: Orchestrates cleaning of `Automaker` and `Genmodel`, collects validation summary and final shape.
  - `print_cleaning_report(report)`: Pretty prints a human-readable cleaning summary.
- **Notable behaviors**:
  - Defensive checks for empty dataframes and missing columns.
  - Spanish log messages; normalization preserves English naming in data values.

### src/data_layer.py (DataProcessor)
- **Purpose**: Centralized data ingestion and quality management.
- **Initialization**: Loads configuration from `src/components/config/{data_config, app_config}` with fallbacks.
- **Core responsibilities**:
  - Loading files from `data/` with chunking for large files; dtype optimization by downcasting numerics and categoricals.
  - Column name standardization via `COLUMN_MAPPING`.
  - Validation against `VALIDATION_RULES` (required columns, types, ranges, uniqueness).
  - Quality assessment: completeness, uniqueness, consistency, memory usage, and aggregate overall score.
  - Feature engineering:
    - Price features: `price_tier`, `price_volatility`, `high_price_volatility` (per `Genmodel_ID`).
    - Sales features: `total_sales`, `avg_sales`, linear `sales_trend`, performance tiers.
    - Market features: per-model `automaker_market_share`, `market_segment` mapping.
  - Export functions: CSV/XLSX/JSON with optional metadata/quality sheets and timestamps; bulk export.
- **Public API**:
  - `get_data_summary()`, `get_quality_report()`, `get_validation_results()`
  - `get_dataset(name)`, `list_datasets()`, `get_dataset_info(name)`, `reload_dataset(name)`
  - `export_dataset(name, format)`, `export_all_datasets(format)`
- **Globals**: `data_processor = DataProcessor()` initialized for app-wide access.

### src/business_logic.py (CarDataAnalyzer)
- **Purpose**: Executive-grade analytics over basic/price/sales datasets.
- **Initialization**:
  - Loads `Basic_table.csv`, `Price_table.csv`, `Sales_table.csv` under `data/` with encoding fallback and partial read (up to 6000 rows).
  - Removes rows where `Genmodel == 'undefined'`.
  - Applies memory dtype optimization; standardizes `Maker`→`Automaker`.
  - For `basic`, applies `clean_automaker_data` and validates with `validate_automaker_consistency`.
  - Builds a `quality_report` per dataset (missing/duplicate ratios, memory usage) with thresholds from `DATA_QUALITY_THRESHOLDS`.
- **Key methods**:
  - Data overview: `get_basic_info()`, `_calculate_quality_score(df)`, `get_automaker_list()`, `get_model_count_by_automaker()`.
  - Price and sales transforms:
    - `get_price_range_by_model()`: Aggregates `Entry_price` by `Genmodel_ID` to `price_min/max/mean/median/std/count`, volatility, joined to `basic` by `Genmodel_ID`.
    - `get_sales_summary()`: Melts wide `sales` to long, aggregates per `Genmodel_ID` (sum/mean/max/min/std/count) plus slope `sales_trend`, then joins with `basic`.
  - Analytics:
    - `calculate_market_share()`: Aggregates total sales per `Automaker`, computes `%` of total.
    - `calculate_price_elasticity()`: Joins price and sales and computes a simplified elasticity with categorical bins.
    - `detect_outliers(method)`: IQR/Z-score outliers over configured numeric fields.
    - `perform_clustering_analysis()`: KMeans on selected features, adds `cluster` and friendly `cluster_type` mapping.
    - `calculate_correlation_matrix()`: Correlations across configured numeric columns.
    - `generate_market_insights()`: Collects market leader, concentration, price range, totals, outlier counts and recommendations.
    - Executive outputs: `get_executive_summary()`, `get_kpi_dashboard()`, `get_data_quality_report()`, `get_price_segments()`, `get_sales_by_segment()`.
  - Filtering: `query_models_by_automaker(automaker)`, `get_filtered_data(automakers, models)`.

### src/presentation_layer.py (PresentationLayer)
- **Purpose**: Encapsulates chart creation and responsive behavior using Plotly.
- **Config**: Pulls `CHART_CONFIG`, `COLOR_PALETTE`, `COOLORS_PALETTE`, `RISK_COLORS`, `MANUFACTURER_COLORS`, `CUSTOM_CSS` from app config (with fallbacks if imports fail).
- **Charts provided**:
  - Bars: sales by model, average price by automaker.
  - Pie: market share (top 10 + Others grouping).
  - Line/Area: `create_sales_trend_line` from yearly totals.
  - Histogram: price distribution.
  - Heatmap: correlation matrix.
  - Scatter: clustering analysis, price elasticity categories.
  - Executive KPI indicators: `create_executive_summary_chart`.
  - Composite dashboards: `create_market_analysis_dashboard`, `create_analytics_dashboard`.
- **Utilities**: empty-state chart helper, manufacturer color utilities, hex→rgb, responsive config and applier.
- **Global**: `presentation_layer = PresentationLayer()`.

### src/router.py
- **Function**: `navigate(page, analyzer)` routes to the desired dashboard based on a Spanish label:
  - "Resumen Ejecutivo" → `show_executive_dashboard`
  - "Análisis de Mercado" → `show_market_dashboard`
  - "Rendimiento de Ventas" → `show_sales_dashboard`

### src/components/ (panorama)
- `config/app_config.py`:
  - App metadata, color palettes, extended `CUSTOM_CSS` for Streamlit theming.
  - KPI thresholds, correlation, outlier, and clustering configurations.
  - Data file naming and ranges in `DATA_CONFIG`.
- `config/data_config.py`:
  - `DATA_FILES` describing each dataset, `COLUMN_MAPPING` to standardize (`Maker`→`Automaker`, `Model`→`Genmodel`, `Model_ID`→`Genmodel_ID`).
  - `VALIDATION_RULES`, `SALES_YEARS`, `DATA_QUALITY_THRESHOLDS`, `MEMORY_CONFIG`, `EXPORT_CONFIG`.
- `dashboards/executive_dashboard.py`:
  - Renders executive summary with KPIs, insights, market overview, performance metrics, risk assessment, and additional advanced sections (treemap of sales by price segment, correlation scatter, price distribution box/heatmap, detailed table).
- `dashboards/market_dashboard.py`:
  - Market overview, market share analysis (pie/bar), competitive analysis (scatter and positioning), segmentation (segments and brand positioning), price analysis, market trends with YoY/CAGR/peak.
- `dashboards/sales_dashboard.py`:
  - Sales overview, top performers, trends (overall and top automakers), performance analysis (distribution and thresholds), simple linear forecasting, and optimization insights.
- `ui/`, `visualizations/`, `analytics/`, `utils/`: Not fully expanded here; referenced in dashboards for layout, sidebar, KPI calculations, chart factories, and helpers.

## End-to-End Data Flow
1. `data/` CSVs are read by `CarDataAnalyzer` (and/or `DataProcessor` when used) → columns standardized.
2. Cleaning functions in `src/data_cleaner.py` normalize `Automaker`/`Genmodel` for consistency and quality.
3. `CarDataAnalyzer` computes aggregates and analytics (price stats, sales summaries, KPIs, insights).
4. `PresentationLayer` builds Plotly figures; dashboards in `src/components/dashboards/` orchestrate UI/sections in Streamlit.
5. `src/router.py` maps sidebar/page selection to the appropriate dashboard rendering.

## Conventions and Key Decisions
- **Join Keys**: Robust joins by `Genmodel_ID` for price/sales/basic merges; also merges on `Automaker`/`Genmodel` where appropriate.
- **Standardization**: `Maker` renamed to `Automaker` across datasets.
- **Quality Thresholds**: Controlled via `DATA_QUALITY_THRESHOLDS` with warnings for missing and duplicate ratios.
- **Memory Optimization**: Downcasting integers/floats and categoricals to fit interactive cloud environments.
- **Partial Loads**: Up to 6000 rows in `CarDataAnalyzer` default loader; encoding fallbacks (`utf-8`, `latin-1`, `cp1252`).

## Extensibility
- **Add a dataset**: Update `DATA_FILES`, `COLUMN_MAPPING`, and optionally `VALIDATION_RULES`; extend `DataProcessor` or `CarDataAnalyzer` accessors.
- **Add features**: Implement new feature engineering steps in `DataProcessor` and surface via `CarDataAnalyzer`.
- **Add charts/dashboards**: Extend `PresentationLayer` and integrate via `src/components/dashboards/*` and `src/router.py`.
- **Export**: Use `DataProcessor.export_dataset`/`export_all_datasets` to generate CSV/XLSX/JSON with metadata.

## Dependencies (key)
- pandas, numpy, plotly, streamlit, scipy, scikit-learn (KMeans, StandardScaler, PCA), openpyxl (for XLSX), and standard Python libs.

## Appendix: Function Index (selected)
- `src/data_cleaner.py`: `clean_automaker_data`, `validate_automaker_consistency`, `clean_genmodel_data`, `clean_all_data`, `print_cleaning_report`.
- `src/data_layer.py`: `DataProcessor` and its public API; globals `data_processor`.
- `src/business_logic.py`: `CarDataAnalyzer` and analytics methods; joins on `Genmodel_ID`.
- `src/presentation_layer.py`: Chart creation methods and composites; global `presentation_layer`.
- `src/router.py`: `navigate(page, analyzer)`.
