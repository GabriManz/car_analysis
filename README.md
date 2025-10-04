# Car Dataset Entity Relationship Analysis

This document contains an automatically generated diagram that describes the inferred relationships between CSV tables in the car analysis project.

## Dataset Overview

The dataset consists of 4 CSV files containing car-related information:

- **Basic_table.csv**: Central reference table with 1,011 unique car models
- **Price_table.csv**: Entry prices by model and year (6,333 records)
- **Sales_table.csv**: Sales data by model and year 2001-2020 (773 records)
- **Trim_table.csv**: Detailed trim specifications (335,562 records)

## Schema Analysis

### Key Columns Identified:
- **Primary Keys**: `Genmodel_ID` (unique identifier for car models)
- **Foreign Keys**: `Maker`/`Automaker` (car manufacturer), `Genmodel` (model name)
- **Naming Inconsistencies**: `Maker` vs `Automaker`, whitespace in column names

### Data Quality Issues:
- Column name inconsistencies between tables
- Leading whitespace in Ad_table column names (e.g., `' Genmodel_ID'`)
- Different naming conventions for the same entity

## Entity Relationship Diagram

```mermaid
graph TD
    %% Central Reference Table
    Basic[Basic_table<br/>1,011 records<br/>Automaker, Automaker_ID,<br/>Genmodel, Genmodel_ID]
    
    %% Related Tables
    Price[Price_table<br/>6,333 records<br/>Maker, Genmodel, Genmodel_ID,<br/>Year, Entry_price]
    
    Sales[Sales_table<br/>773 records<br/>Maker, Genmodel, Genmodel_ID,<br/>2020, 2019, ..., 2001]
    
    Trim[Trim_table<br/>335,562 records<br/>Genmodel_ID, Maker, Genmodel,<br/>Trim, Year, Price, Gas_emission,<br/>Fuel_type, Engine_size]
    
    %% Relationships
    Basic -->|Genmodel_ID<br/>Genmodel<br/>Maker→Automaker| Price
    Basic -->|Genmodel_ID<br/>Genmodel<br/>Maker→Automaker| Sales
    Basic -->|Genmodel_ID| Trim
    
    %% Cardinality Labels
    Basic -.->|1:Many| Price
    Basic -.->|1:Many| Trim
    Basic -.->|1:1| Sales
    
    %% Styling
    style Basic fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    style Price fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    style Sales fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    style Trim fill:#fff3e0,stroke:#e65100,stroke-width:2px
```

## Relationship Details

### Primary Relationships:
1. **Basic_table** → **All other tables** (Central hub)
   - **Join Key**: `Genmodel_ID` (primary identifier)
   - **Additional Keys**: `Genmodel`, `Maker`/`Automaker` (with name mapping)

### Cardinality Analysis:
- **Basic → Price**: 1:Many (one model, multiple price entries by year)
- **Basic → Trim**: 1:Many (one model, multiple trim variants)
- **Basic → Sales**: 1:1 (one model, one sales record with yearly breakdown)

### Data Volume:
- **Central Table**: 1,011 unique car models
- **Largest Table**: Trim_table (335K records)
- **Most Complex**: Trim_table (9 columns with detailed specifications)

## Merge Strategy Recommendations

1. **Start with Basic_table** as the central reference
2. **Aggregate large tables** (Trim) before merging to prevent cartesian explosion
3. **Handle naming inconsistencies** by standardizing `Maker` → `Automaker`
4. **Clean column names** (remove leading whitespace)
5. **Use appropriate join types** (LEFT JOIN to preserve all models)

## Data Quality Considerations

- **Coverage**: Not all models have data in all tables
- **Consistency**: Different naming conventions require standardization
- **Completeness**: Sales data available for only 773/1,011 models
- **Memory Management**: Trim table requires aggregation strategies
