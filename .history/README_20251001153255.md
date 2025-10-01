# Project: Car Sales & Pricing Analysis

## 1. Project Objective

*(The researcher will define the main goal of the analysis here. For example: To analyze the factors influencing the selling price of used cars and to create an interactive dashboard to explore these insights.)*

## 2. Dataset Description

The dataset is a relational data model composed of several tables in CSV format, located in the `/data` folder. Key tables include information on car models, technical specifications (trims), pricing, sales figures, advertisements, and the quality of ad images. A crucial first step in preprocessing will be to join these tables to create a consolidated dataframe for analysis.

### Available Data Files:
- `Basic_table.csv` - Basic car information
- `Trim_table.csv` - Technical specifications and trim details
- `Price_table.csv` - Pricing information
- `Sales_table.csv` - Sales figures and performance data
- `Ad_table_(extra).csv` - Advertisement details
- `Image_table.csv` - Image quality and metadata

## 3. Detailed Action Plan

This plan follows a 5-phase structured methodology to ensure a complete and reproducible analysis.

### Phase 1: Setup and Initial Exploration
- [ ] Set up the working environment (e.g., `conda` or `venv`).
- [ ] Load all CSV datasets into pandas dataframes in an initial notebook.
- [ ] Perform a basic inspection of each table (`.info()`, `.head()`, `.describe()`).
- [ ] Plan the table joining strategy (`merge`).
- [ ] Document data quality issues and missing values.

### Phase 2: Data Preprocessing and Cleaning
- [ ] Create the `01_Data_Cleaning.ipynb` notebook.
- [ ] Join the tables to create a master dataframe.
- [ ] Handle null values (identify, decide on a strategy - drop/impute - and apply).
- [ ] Identify and remove duplicate rows.
- [ ] Correct incorrect data types (e.g., dates as objects).
- [ ] Perform feature engineering (create new columns, e.g., 'car_age' from the year).
- [ ] Validate data integrity after cleaning.
- [ ] Save the cleaned dataframe to the `/data` folder as a new file (e.g., `car_analysis_data.csv`).

### Phase 3: Exploratory Data Analysis (EDA)
- [ ] Create the `02_EDA.ipynb` notebook.
- [ ] **Univariate Analysis:** Study the distribution of key variables (price, year, quality score, etc.) using histograms and boxplots. Identify outliers.
- [ ] **Bivariate Analysis:** Investigate relationships between pairs of variables.
    - [ ] Correlation matrix and heatmap for numerical variables.
    - [ ] Scatter plots for key relationships (e.g., `quality_score` vs. `selling_price`).
    - [ ] Grouped boxplots (e.g., `selling_price` by `brand_name`).
    - [ ] Categorical analysis (brands, models, trim levels).
- [ ] **Multivariate Analysis:** Explore complex relationships and interactions.
- [ ] Statistical testing for significant differences and correlations.
- [ ] Save the most relevant plots to the `/img` folder.
- [ ] Document the key findings in the notebook.

### Phase 4: Intelligence Dashboard Development
- [ ] Create the `app.py` script in the `/panel` folder.
- [ ] Choose the dashboarding tool (e.g., Streamlit, Panel, Dash).
- [ ] Design a visual narrative that tells the data's story in 3-4 key points.
- [ ] Implement the dashboard by loading the cleaned dataset.
- [ ] Add interactivity (filters, sliders, dropdowns) to allow users to explore the data.
- [ ] Implement key performance indicators (KPIs) and summary statistics.
- [ ] Add data export functionality.
- [ ] Test dashboard functionality and user experience.

### Phase 5: Presentation Preparation
- [ ] Structure a script for a 15-minute presentation based on the dashboard.
- [ ] Prepare key insights and actionable recommendations.
- [ ] Create presentation slides highlighting main findings.
- [ ] Rehearse the presentation, ensuring the flow is logical and the conclusions are clear.
- [ ] Prepare backup materials and alternative explanations.

## 4. Repository Structure

```
Project Root/
├── data/                    # Contains original (.csv) datasets and cleaned datasets
├── example/                 # Contains a reference project
├── img/                     # Stores the generated visualizations and charts
├── notebooks/               # Contains Jupyter Notebooks for each phase of the analysis
│   ├── 01_Data_Cleaning.ipynb
│   └── 02_EDA.ipynb
├── panel/                   # Contains the source code for the interactive intelligence dashboard
│   └── app.py
├── .gitignore              # Specifies files and folders to be ignored by Git
├── .cursorrules            # Project coding standards and conventions
└── README.md               # This file, containing the project plan and documentation
```

## 5. Technical Requirements

### Python Environment
- Python 3.8+
- Key libraries: pandas, numpy, matplotlib, seaborn, plotly, streamlit/panel/dash
- Jupyter notebooks for interactive analysis

### Data Analysis Tools
- Pandas for data manipulation
- Matplotlib/Seaborn for static visualizations
- Plotly for interactive plots
- Scikit-learn for statistical analysis (if needed)

### Dashboard Framework
- Streamlit (recommended for simplicity)
- Panel (for more advanced features)
- Dash (for complex applications)

## 6. Success Criteria

- [ ] Clean, well-documented dataset ready for analysis
- [ ] Comprehensive EDA with clear insights
- [ ] Interactive dashboard that effectively communicates findings
- [ ] 15-minute presentation that tells a compelling data story
- [ ] Reproducible analysis with clear documentation

## 7. Next Steps

1. Begin with Phase 1: Set up environment and perform initial data exploration
2. Document findings and plan data cleaning strategy
3. Proceed systematically through each phase
4. Regularly commit progress to version control
5. Maintain clear documentation throughout the process

---

*This project follows a structured approach to ensure comprehensive analysis and clear communication of insights. All work will be conducted in English with proper documentation and version control.*
