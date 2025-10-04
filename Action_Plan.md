# Project Plan: Global Video Game Sales Analysis

This document details the phases and tasks for the data analysis project, from initial setup to creating a business intelligence dashboard.

## Phase 0: Environment Setup and Project Structure (Setup)

* **Objective:** Create a solid and organized foundation for our work.
* **Tasks:**
    1.  Create folder structure (`data/`, `notebooks/`, `src/`).
    2.  Configure a virtual environment to isolate dependencies.
    3.  Create a `requirements.txt` file to manage libraries.
    4.  Create an initial script for data loading.

## Phase 1: Data Preprocessing and Cleaning (Data Cleaning)

* **Objective:** Ensure the dataset is reliable, consistent and ready for analysis.
* **Tasks:**
    1.  **Quality Analysis:** Review data types, nulls and duplicates.
    2.  **Cleaning:** Apply strategies to handle null values and ensure consistency.
    3.  **Feature Engineering:** Create new columns (e.g. `Total_Regional_Sales`, `Decade`) to enrich the analysis.

## Phase 2: Exploratory Data Analysis (EDA)

* **Objective:** Extract key insights and answer business questions through visualization and statistical analysis.
* **Tasks:**
    1.  **Univariate Analysis:** Study the distribution of key variables (sales, releases by year).
    2.  **Bivariate and Multivariate Analysis:** Investigate relationships between variables such as sales over time, performance by genre, platform and publisher.

## Phase 3: Business Intelligence Dashboard Construction

* **Objective:** Create an interactive dashboard that summarizes EDA findings for executive presentation.
* **Tasks:**
    1.  **Design and Layout:** Define dashboard structure (sidebar, charts area).
    2.  **Interactive Filters:** Implement widgets to filter by year, genre, platform, etc.
    3.  **Key Visualizations:** Develop KPIs, time series charts, bars and interactive tables.
    4.  **Modularization:** Structure dashboard code in a clean and maintainable way.
---
