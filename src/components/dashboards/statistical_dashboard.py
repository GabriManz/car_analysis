"""
📊 Statistical Analysis Dashboard for Car Market Analysis

Advanced statistical analysis including correlation, hypothesis testing, and regression.
Provides executive-grade statistical insights with interactive visualizations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from scipy.stats import pearsonr, spearmanr, ttest_ind, f_oneway, shapiro
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')


class StatisticalDashboard:
    """📈 Advanced Statistical Analysis Dashboard"""
    
    def __init__(self, analyzer):
        """Initialize the Statistical Dashboard with data analyzer."""
        self.analyzer = analyzer
        self.merged_data = self._prepare_merged_data()
    
    def _prepare_merged_data(self):
        """Prepare merged dataset for statistical analysis."""
        try:
            # Get price and sales data
            price_data = self.analyzer.get_price_range_by_model()
            sales_data = self.analyzer.get_sales_summary()
            
            if price_data.empty or sales_data.empty:
                return pd.DataFrame()
            
            # Merge on Genmodel_ID
            merged = price_data.merge(
                sales_data, 
                on=['Automaker', 'Genmodel', 'Genmodel_ID'], 
                how='inner'
            )
            
            # Clean data: remove nulls and infinite values
            numeric_cols = merged.select_dtypes(include=[np.number]).columns
            merged = merged.replace([np.inf, -np.inf], np.nan)
            merged = merged.dropna(subset=numeric_cols)
            
            return merged
            
        except Exception as e:
            st.error(f"Error preparing data: {e}")
            return pd.DataFrame()


def show_statistical_dashboard(analyzer):
    """Main function to display the Statistical Analysis Dashboard."""
    
    st.title("📊 Statistical Analysis Dashboard")
    st.markdown("Advanced statistical analysis with correlation, hypothesis testing, and regression models")
    st.markdown("---")
    
    # Initialize dashboard
    dashboard = StatisticalDashboard(analyzer)
    
    if dashboard.merged_data.empty:
        st.error("⚠️ No data available for statistical analysis")
        return
    
    df = dashboard.merged_data
    
    # =============================================================================
    # SECTION 1: CORRELATION ANALYSIS
    # =============================================================================
    
    st.header("1️⃣ Correlation Analysis")
    st.markdown("Analysis of relationships between key variables using Pearson and Spearman correlation")
    
    # Select numeric columns for correlation
    numeric_cols = ['price_mean', 'price_std', 'price_volatility', 
                   'total_sales', 'avg_sales', 'max_sales', 'sales_std', 'sales_trend']
    available_cols = [col for col in numeric_cols if col in df.columns]
    
    if len(available_cols) >= 2:
        # Calculate Pearson correlation matrix
        corr_pearson = df[available_cols].corr(method='pearson')
        
        # Calculate Spearman correlation matrix
        corr_spearman = df[available_cols].corr(method='spearman')
        
        # Display correlation matrices side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Pearson Correlation")
            st.caption("Measures linear relationships")
            
            # Create heatmap
            fig_pearson = go.Figure(data=go.Heatmap(
                z=corr_pearson.values,
                x=corr_pearson.columns,
                y=corr_pearson.columns,
                colorscale='RdBu_r',
                zmid=0,
                zmin=-1,
                zmax=1,
                text=np.round(corr_pearson.values, 2),
                texttemplate='%{text}',
                textfont={"size": 10},
                colorbar=dict(title="Correlation")
            ))
            
            fig_pearson.update_layout(
                height=500,
                xaxis_title="",
                yaxis_title="",
                template="plotly_dark"
            )
            
            st.plotly_chart(fig_pearson, use_container_width=True)
        
        with col2:
            st.subheader("📊 Spearman Correlation")
            st.caption("Measures monotonic relationships (rank-based)")
            
            # Create heatmap
            fig_spearman = go.Figure(data=go.Heatmap(
                z=corr_spearman.values,
                x=corr_spearman.columns,
                y=corr_spearman.columns,
                colorscale='RdBu_r',
                zmid=0,
                zmin=-1,
                zmax=1,
                text=np.round(corr_spearman.values, 2),
                texttemplate='%{text}',
                textfont={"size": 10},
                colorbar=dict(title="Correlation")
            ))
            
            fig_spearman.update_layout(
                height=500,
                xaxis_title="",
                yaxis_title="",
                template="plotly_dark"
            )
            
            st.plotly_chart(fig_spearman, use_container_width=True)
        
        # Top correlations table
        st.subheader("🔝 Top Correlations")
        
        # Get upper triangle of correlation matrix (avoid duplicates)
        mask = np.triu(np.ones_like(corr_pearson, dtype=bool), k=1)
        corr_pairs = corr_pearson.where(mask).stack().reset_index()
        corr_pairs.columns = ['Variable 1', 'Variable 2', 'Pearson r']
        
        # Add Spearman correlation
        corr_pairs_spearman = corr_spearman.where(mask).stack().reset_index()
        corr_pairs['Spearman ρ'] = corr_pairs_spearman[0].values
        
        # Sort by absolute Pearson correlation
        corr_pairs['abs_corr'] = corr_pairs['Pearson r'].abs()
        corr_pairs = corr_pairs.sort_values('abs_corr', ascending=False)
        
        # Display top 10
        top_corr = corr_pairs.head(10)[['Variable 1', 'Variable 2', 'Pearson r', 'Spearman ρ']].copy()
        top_corr['Pearson r'] = top_corr['Pearson r'].round(3)
        top_corr['Spearman ρ'] = top_corr['Spearman ρ'].round(3)
        
        # Interpretation column
        def interpret_correlation(r):
            abs_r = abs(r)
            if abs_r > 0.7:
                strength = "Strong"
            elif abs_r > 0.4:
                strength = "Moderate"
            elif abs_r > 0.2:
                strength = "Weak"
            else:
                strength = "Very Weak"
            
            direction = "Positive" if r > 0 else "Negative"
            return f"{strength} {direction}"
        
        top_corr['Interpretation'] = top_corr['Pearson r'].apply(interpret_correlation)
        
        st.dataframe(top_corr, use_container_width=True, hide_index=True)
        
        # Key insights
        strongest = corr_pairs.iloc[0]
        st.info(f"""
        **🔍 Key Insight:** The strongest correlation found is between **{strongest['Variable 1']}** and **{strongest['Variable 2']}** 
        with Pearson r = **{strongest['Pearson r']:.3f}** ({interpret_correlation(strongest['Pearson r'])})
        """)
    
    else:
        st.warning("Not enough numeric columns for correlation analysis")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 2: HYPOTHESIS TESTING
    # =============================================================================
    
    st.header("2️⃣ Hypothesis Testing")
    st.markdown("Statistical tests to validate business hypotheses about market segments and pricing")
    
    # Add price tiers if not present
    if 'price_tier' not in df.columns and 'price_mean' in df.columns:
        # Create price tiers based on quantiles
        df['price_tier'] = pd.qcut(
            df['price_mean'], 
            q=4, 
            labels=['Budget', 'Mid-Range', 'Premium', 'Luxury'],
            duplicates='drop'
        )
    
    # Test 1: T-Test (Premium vs Budget)
    st.subheader("📊 Test 1: Independent T-Test")
    st.markdown("**Hypothesis:** Do Premium cars have significantly different sales than Budget cars?")
    
    if 'price_tier' in df.columns and 'total_sales' in df.columns:
        # Get samples
        premium_sales = df[df['price_tier'] == 'Premium']['total_sales'].dropna()
        budget_sales = df[df['price_tier'] == 'Budget']['total_sales'].dropna()
        
        if len(premium_sales) > 0 and len(budget_sales) > 0:
            # Perform t-test
            t_stat, p_value = ttest_ind(premium_sales, budget_sales)
            
            # Calculate effect size (Cohen's d)
            pooled_std = np.sqrt((premium_sales.std()**2 + budget_sales.std()**2) / 2)
            cohens_d = (premium_sales.mean() - budget_sales.mean()) / pooled_std
            
            # Display results in columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Premium Mean Sales", f"{premium_sales.mean():,.0f}")
            with col2:
                st.metric("Budget Mean Sales", f"{budget_sales.mean():,.0f}")
            with col3:
                st.metric("t-statistic", f"{t_stat:.3f}")
            with col4:
                st.metric("p-value", f"{p_value:.4f}")
            
            # Interpretation
            alpha = 0.05
            if p_value < alpha:
                conclusion = f"✅ **Reject H₀** (p < {alpha}): There IS a statistically significant difference in sales between Premium and Budget cars."
                if cohens_d > 0:
                    conclusion += f" Premium cars sell **more** on average (Cohen's d = {cohens_d:.2f})."
                else:
                    conclusion += f" Budget cars sell **more** on average (Cohen's d = {cohens_d:.2f})."
            else:
                conclusion = f"❌ **Fail to reject H₀** (p ≥ {alpha}): No statistically significant difference in sales between Premium and Budget cars."
            
            # Effect size interpretation
            if abs(cohens_d) < 0.2:
                effect = "negligible"
            elif abs(cohens_d) < 0.5:
                effect = "small"
            elif abs(cohens_d) < 0.8:
                effect = "medium"
            else:
                effect = "large"
            
            st.success(conclusion)
            st.caption(f"**Effect Size:** Cohen's d = {cohens_d:.3f} ({effect} effect)")
        else:
            st.warning("Insufficient data for t-test")
    else:
        st.warning("Price tier or sales data not available")
    
    st.markdown("---")
    
    # Test 2: ANOVA (All price tiers)
    st.subheader("📊 Test 2: One-Way ANOVA")
    st.markdown("**Hypothesis:** Do sales differ significantly across ALL price tiers?")
    
    if 'price_tier' in df.columns and 'total_sales' in df.columns:
        # Get samples for each tier
        tier_groups = []
        tier_names = []
        
        for tier in df['price_tier'].unique():
            tier_data = df[df['price_tier'] == tier]['total_sales'].dropna()
            if len(tier_data) > 0:
                tier_groups.append(tier_data)
                tier_names.append(tier)
        
        if len(tier_groups) >= 2:
            # Perform ANOVA
            f_stat, p_value_anova = f_oneway(*tier_groups)
            
            # Display results
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("F-statistic", f"{f_stat:.3f}")
            with col2:
                st.metric("p-value", f"{p_value_anova:.4f}")
            with col3:
                st.metric("Groups Compared", len(tier_groups))
            
            # Interpretation
            if p_value_anova < alpha:
                conclusion = f"✅ **Reject H₀** (p < {alpha}): At least one price tier has significantly different sales from the others."
            else:
                conclusion = f"❌ **Fail to reject H₀** (p ≥ {alpha}): No statistically significant difference in sales across price tiers."
            
            st.success(conclusion)
            
            # Show means by tier
            tier_means = df.groupby('price_tier')['total_sales'].mean().sort_values(ascending=False)
            st.caption("**Mean Sales by Price Tier:**")
            
            cols = st.columns(len(tier_means))
            for idx, (tier, mean_val) in enumerate(tier_means.items()):
                with cols[idx]:
                    st.metric(tier, f"{mean_val:,.0f}")
        else:
            st.warning("Insufficient groups for ANOVA")
    else:
        st.warning("Price tier or sales data not available")
    
    st.markdown("---")
    
    # Test 3: Normality Tests
    st.subheader("📊 Test 3: Normality Tests (Shapiro-Wilk)")
    st.markdown("**Purpose:** Test if variables follow a normal distribution (determines if parametric tests are appropriate)")
    
    normality_results = []
    
    test_vars = ['price_mean', 'total_sales']
    available_test_vars = [v for v in test_vars if v in df.columns]
    
    if available_test_vars:
        for var in available_test_vars:
            data = df[var].dropna()
            
            if len(data) > 3:  # Shapiro needs at least 3 samples
                # Limit to 5000 samples for computational efficiency
                if len(data) > 5000:
                    data = data.sample(5000, random_state=42)
                
                stat, p_val = shapiro(data)
                
                is_normal = "✅ Yes" if p_val >= 0.05 else "❌ No"
                
                normality_results.append({
                    'Variable': var,
                    'W-statistic': f"{stat:.4f}",
                    'p-value': f"{p_val:.4f}",
                    'Normal Distribution?': is_normal,
                    'Sample Size': len(data)
                })
        
        if normality_results:
            st.dataframe(pd.DataFrame(normality_results), use_container_width=True, hide_index=True)
            
            st.info("""
            **📌 Interpretation Guide:**
            - **p-value < 0.05**: Reject normality → Use non-parametric tests (Mann-Whitney, Kruskal-Wallis)
            - **p-value ≥ 0.05**: Assume normality → Use parametric tests (t-test, ANOVA)
            """)
        else:
            st.warning("Could not perform normality tests")
    else:
        st.warning("Required variables not available for normality testing")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 3: REGRESSION ANALYSIS
    # =============================================================================
    
    st.header("3️⃣ Regression Analysis")
    st.markdown("Linear regression models to understand and predict relationships between price and sales")
    
    if 'price_mean' in df.columns and 'total_sales' in df.columns:
        # Prepare data for regression
        reg_data = df[['price_mean', 'total_sales']].dropna()
        
        if len(reg_data) > 10:
            X = reg_data['price_mean'].values.reshape(-1, 1)
            y = reg_data['total_sales'].values
            
            # Fit linear regression
            model = LinearRegression()
            model.fit(X, y)
            
            # Predictions
            y_pred = model.predict(X)
            
            # Calculate metrics
            r2 = r2_score(y, y_pred)
            
            # Calculate p-value for slope
            n = len(X)
            residuals = y - y_pred
            residual_std_error = np.sqrt(np.sum(residuals**2) / (n - 2))
            x_mean = X.mean()
            x_std = np.sqrt(np.sum((X - x_mean)**2))
            se_slope = residual_std_error / x_std
            t_stat_slope = model.coef_[0] / se_slope
            p_value_slope = 2 * (1 - stats.t.cdf(abs(t_stat_slope), n - 2))
            
            # Display regression equation and metrics
            st.subheader("📐 Linear Regression Model")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("R² Score", f"{r2:.4f}")
            with col2:
                st.metric("Slope (β₁)", f"{model.coef_[0]:,.2f}")
            with col3:
                st.metric("Intercept (β₀)", f"{model.intercept_:,.0f}")
            with col4:
                st.metric("p-value (slope)", f"{p_value_slope:.4f}")
            
            # Regression equation
            st.code(f"""
Regression Equation:
Sales = {model.intercept_:,.0f} + ({model.coef_[0]:,.2f}) × Price

Interpretation:
- For every €1,000 increase in price, sales {"increase" if model.coef_[0] > 0 else "decrease"} by {abs(model.coef_[0] * 1000):,.0f} units on average
- The model explains {r2*100:.1f}% of the variance in sales
            """)
            
            # Interpretation
            if p_value_slope < 0.05:
                st.success(f"✅ **Significant relationship** (p < 0.05): Price is a statistically significant predictor of sales.")
            else:
                st.warning(f"⚠️ **No significant relationship** (p ≥ 0.05): Price is NOT a statistically significant predictor of sales.")
            
            # Scatter plot with regression line
            st.subheader("📊 Regression Visualization")
            
            fig_reg = go.Figure()
            
            # Scatter plot
            fig_reg.add_trace(go.Scatter(
                x=reg_data['price_mean'],
                y=reg_data['total_sales'],
                mode='markers',
                name='Actual Data',
                marker=dict(
                    size=6,
                    color=reg_data['total_sales'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Sales")
                ),
                text=[f"Price: €{p:,.0f}<br>Sales: {s:,.0f}" for p, s in zip(reg_data['price_mean'], reg_data['total_sales'])],
                hovertemplate='%{text}<extra></extra>'
            ))
            
            # Regression line
            fig_reg.add_trace(go.Scatter(
                x=reg_data['price_mean'],
                y=y_pred,
                mode='lines',
                name=f'Regression Line (R²={r2:.3f})',
                line=dict(color='red', width=3)
            ))
            
            # Confidence interval (95%)
            from scipy import stats as sp_stats
            predict_se = residual_std_error * np.sqrt(1/n + (X - x_mean)**2 / np.sum((X - x_mean)**2))
            margin = 1.96 * predict_se  # 95% CI
            
            # Sort for proper polygon drawing
            sorted_indices = np.argsort(X.flatten())
            X_sorted = X.flatten()[sorted_indices]
            y_pred_sorted = y_pred[sorted_indices]
            margin_sorted = margin.flatten()[sorted_indices]
            
            fig_reg.add_trace(go.Scatter(
                x=np.concatenate([X_sorted, X_sorted[::-1]]),
                y=np.concatenate([y_pred_sorted + margin_sorted, (y_pred_sorted - margin_sorted)[::-1]]),
                fill='toself',
                fillcolor='rgba(255, 0, 0, 0.2)',
                line=dict(color='rgba(255, 0, 0, 0)'),
                showlegend=True,
                name='95% Confidence Interval'
            ))
            
            fig_reg.update_layout(
                title="Price vs Sales with Linear Regression",
                xaxis_title="Average Price (€)",
                yaxis_title="Total Sales (units)",
                template="plotly_dark",
                height=500,
                hovermode='closest'
            )
            
            st.plotly_chart(fig_reg, use_container_width=True)
            
            # Model quality assessment
            st.subheader("📋 Model Quality Assessment")
            
            quality_metrics = []
            
            # R² interpretation
            if r2 > 0.7:
                r2_quality = "Excellent - Strong predictive power"
            elif r2 > 0.5:
                r2_quality = "Good - Moderate predictive power"
            elif r2 > 0.3:
                r2_quality = "Fair - Weak predictive power"
            else:
                r2_quality = "Poor - Very weak predictive power"
            
            quality_metrics.append({
                'Metric': 'R² Score',
                'Value': f"{r2:.4f}",
                'Interpretation': r2_quality
            })
            
            # Slope significance
            if p_value_slope < 0.001:
                slope_sig = "Highly significant (p < 0.001)"
            elif p_value_slope < 0.01:
                slope_sig = "Very significant (p < 0.01)"
            elif p_value_slope < 0.05:
                slope_sig = "Significant (p < 0.05)"
            else:
                slope_sig = "Not significant (p ≥ 0.05)"
            
            quality_metrics.append({
                'Metric': 'Slope Significance',
                'Value': f"{p_value_slope:.4f}",
                'Interpretation': slope_sig
            })
            
            # Sample size adequacy
            if n > 100:
                sample_adequacy = "Excellent - Large sample"
            elif n > 50:
                sample_adequacy = "Good - Adequate sample"
            elif n > 30:
                sample_adequacy = "Fair - Minimum acceptable"
            else:
                sample_adequacy = "Poor - Small sample"
            
            quality_metrics.append({
                'Metric': 'Sample Size',
                'Value': f"{n}",
                'Interpretation': sample_adequacy
            })
            
            st.dataframe(pd.DataFrame(quality_metrics), use_container_width=True, hide_index=True)
            
        else:
            st.warning("Insufficient data points for regression analysis (minimum 10 required)")
    else:
        st.warning("Required variables (price_mean, total_sales) not available for regression")
    
    st.markdown("---")
    
    # Final Summary
    st.success("""
    ### 🎯 Statistical Analysis Summary
    
    This dashboard provides three levels of statistical analysis:
    
    1. **Correlation Analysis**: Identifies relationships between variables using Pearson (linear) and Spearman (monotonic) correlations
    2. **Hypothesis Testing**: Validates business hypotheses using t-tests, ANOVA, and normality tests with proper statistical rigor
    3. **Regression Analysis**: Models the relationship between price and sales, with confidence intervals and model quality metrics
    
    All tests use standard significance level α = 0.05 (95% confidence)
    """)

