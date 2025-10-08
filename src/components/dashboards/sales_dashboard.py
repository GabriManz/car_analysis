"""
📈 Sales Dashboard Component for Car Market Analysis

Comprehensive sales analysis dashboard providing detailed sales performance insights,
trend analysis, and sales forecasting for automotive market analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional, Any
import warnings
warnings.filterwarnings('ignore')

# Import components (absolute)
try:
    from src.components.ui.layout import layout_component
    from src.components.ui.sidebar import sidebar_component
    from src.components.analytics.kpi_calculator import kpi_calculator
    from src.components.visualizations.chart_factory import chart_factory
    from src.business_logic import CarDataAnalyzer as analyzer
except ImportError:
    layout_component = None
    sidebar_component = None
    kpi_calculator = None
    chart_factory = None
    analyzer = None


class SalesDashboard:
    """
    📊 Sales Performance Dashboard
    
    Provides comprehensive sales analysis including sales performance metrics,
    trend analysis, forecasting, and sales optimization insights.
    """

    def __init__(self):
        """Initialize the SalesDashboard with required components."""
        self.layout = layout_component
        self.sidebar = sidebar_component
        self.kpi_calc = kpi_calculator
        self.chart_factory = chart_factory
        self.analyzer = analyzer

    def render_sales_dashboard(self) -> None:
        """Render the complete sales dashboard."""
        # Setup page layout
        if self.layout:
            self.layout.setup_page_config()
            self.layout.inject_custom_css()
        
        # Create sales header
        st.markdown("""
        <div class="main-header">
            <h1>📈 Sales Analysis Dashboard</h1>
            <p>Comprehensive Sales Performance & Trend Analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sales overview section
        self._render_sales_overview()
        
        # Top performers
        self._render_top_performers()
        
        # Sales trends
        self._render_sales_trends()
        
        # Performance analysis
        self._render_performance_analysis()
        
        # Sales forecasting
        self._render_sales_forecasting()
        
        # Sales optimization
        self._render_sales_optimization()

    def _render_sales_overview(self) -> None:
        """Render sales overview section."""
        st.markdown("## 📊 Sales Overview")
        
        if not self.analyzer:
            st.warning("Business logic analyzer not available")
            return
        
        try:
            # Get sales data
            sales_summary = self.analyzer.get_sales_summary()
            
            if sales_summary.empty:
                st.info("No sales data available")
                return
            
            # Sales metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_sales = sales_summary['total_sales'].sum()
                st.metric("Total Market Sales", f"{total_sales:,.0f}")
            
            with col2:
                avg_sales_per_model = sales_summary['total_sales'].mean()
                st.metric("Avg Sales/Model", f"{avg_sales_per_model:,.0f}")
            
            with col3:
                top_performer_sales = sales_summary['total_sales'].max()
                st.metric("Top Performer Sales", f"{top_performer_sales:,.0f}")
            
            with col4:
                models_with_sales = (sales_summary['total_sales'] > 0).sum()
                total_models = len(sales_summary)
                sales_coverage = (models_with_sales / total_models) * 100
                st.metric("Sales Coverage", f"{sales_coverage:.1f}%")
            
            # Sales distribution analysis
            st.markdown("### Sales Distribution Analysis")
            
            # Calculate sales distribution
            sales_data = sales_summary['total_sales'].dropna()
            
            dist_cols = st.columns(3)
            
            with dist_cols[0]:
                # Sales quartiles
                q1 = sales_data.quantile(0.25)
                q2 = sales_data.quantile(0.50)
                q3 = sales_data.quantile(0.75)
                
                st.markdown("#### Sales Quartiles")
                st.metric("Q1 (25th percentile)", f"{q1:,.0f}")
                st.metric("Q2 (Median)", f"{q2:,.0f}")
                st.metric("Q3 (75th percentile)", f"{q3:,.0f}")
            
            with dist_cols[1]:
                # Sales performance tiers
                high_performers = (sales_data > q3).sum()
                medium_performers = ((sales_data >= q2) & (sales_data <= q3)).sum()
                low_performers = (sales_data < q2).sum()
                
                st.markdown("#### Performance Distribution")
                st.metric("High Performers (>Q3)", f"{high_performers}")
                st.metric("Medium Performers (Q2-Q3)", f"{medium_performers}")
                st.metric("Low Performers (<Q2)", f"{low_performers}")
            
            with dist_cols[2]:
                # Sales volatility
                sales_std = sales_data.std()
                sales_cv = sales_std / sales_data.mean()
                
                st.markdown("#### Sales Volatility")
                st.metric("Standard Deviation", f"{sales_std:,.0f}")
                st.metric("Coefficient of Variation", f"{sales_cv:.2f}")
                
                if sales_cv > 2:
                    st.warning("High sales volatility")
                elif sales_cv > 1:
                    st.info("Moderate sales volatility")
                else:
                    st.success("Low sales volatility")
            
        except Exception as e:
            st.error(f"Error loading sales overview: {str(e)}")

    def _render_top_performers(self) -> None:
        """Render top performers section."""
        st.markdown("## 🏆 Top Performers")
        
        if not self.analyzer or not self.chart_factory:
            st.warning("Required components not available")
            return
        
        try:
            # Get sales data
            sales_summary = self.analyzer.get_sales_summary()
            
            if sales_summary.empty:
                st.info("No sales data available")
                return
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Top 20 Models by Sales")
                # Create sales bar chart
                sales_chart = self.chart_factory.create_sales_bar_chart(
                    sales_summary, "Top 20 Models by Sales Volume"
                )
                st.plotly_chart(sales_chart, use_container_width=True)
            
            with col2:
                st.markdown("### Top 15 Automakers by Total Sales")
                # Group by automaker
                automaker_sales = sales_summary.groupby('Automaker')['total_sales'].sum().sort_values(ascending=False).head(15)
                
                # Create automaker sales chart
                fig = self.chart_factory.create_sales_bar_chart(
                    pd.DataFrame({
                        'Genmodel': automaker_sales.index,
                        'total_sales': automaker_sales.values,
                        'Automaker': automaker_sales.index
                    }), "Top 15 Automakers by Total Sales"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Top performers table
            st.markdown("### Top Performers Detailed View")
            
            # Top 10 models
            top_models = sales_summary.nlargest(10, 'total_sales')[
                ['Genmodel', 'Automaker', 'total_sales', 'avg_sales', 'max_sales', 'years_with_data']
            ]
            top_models.columns = ['Model', 'Automaker', 'Total Sales', 'Avg Sales/Year', 'Peak Sales', 'Years Active']
            
            st.markdown("#### Top 10 Models")
            st.dataframe(top_models, use_container_width=True)
            
            # Top automakers
            top_automakers = sales_summary.groupby('Automaker').agg({
                'total_sales': ['sum', 'mean', 'count'],
                'avg_sales': 'mean',
                'max_sales': 'max'
            }).round(0)
            
            top_automakers.columns = ['Total Sales', 'Avg Sales/Model', 'Model Count', 'Avg Sales/Year', 'Peak Sales']
            top_automakers = top_automakers.sort_values('Total Sales', ascending=False).head(10)
            
            st.markdown("#### Top 10 Automakers")
            st.dataframe(top_automakers, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading top performers: {str(e)}")

    def _render_sales_trends(self) -> None:
        """Render sales trends section."""
        st.markdown("## 📈 Sales Trends")
        
        if not self.analyzer or not self.chart_factory:
            st.warning("Required components not available")
            return
        
        try:
            # Get sales data
            sales_data = self.analyzer.get_sales_summary()
            
            if sales_data.empty:
                st.info("No sales data available")
                return
            
            # Reshape sales data for trend analysis
            year_columns = [col for col in sales_data.columns if col.isdigit()]
            if not year_columns:
                st.info("No yearly sales data available")
                return
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Overall Market Sales Trend")
                # Create sales trend chart
                trend_chart = self.chart_factory.create_sales_trend_chart(
                    sales_data, "Market Sales Trend (2001-2020)"
                )
                st.plotly_chart(trend_chart, use_container_width=True)
            
            with col2:
                st.markdown("### Top 5 Automakers Sales Trend")
                # Get top 5 automakers by total sales
                top_automakers = sales_data.groupby('Automaker')['total_sales'].sum().nlargest(5).index
                
                # Create trend chart for top automakers
                fig = go.Figure()
                
                for automaker in top_automakers:
                    automaker_data = sales_data[sales_data['Automaker'] == automaker]
                    yearly_sales = automaker_data[year_columns].sum().sort_index()
                    
                    fig.add_trace(go.Scatter(
                        x=yearly_sales.index,
                        y=yearly_sales.values,
                        mode='lines+markers',
                        name=automaker,
                        line=dict(width=3)
                    ))
                
                fig.update_layout(
                    title="Top 5 Automakers Sales Trend",
                    xaxis_title="Year",
                    yaxis_title="Total Sales (Units)",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Trend analysis metrics
            st.markdown("### Trend Analysis Metrics")
            
            # Calculate yearly totals
            yearly_totals = sales_data[year_columns].sum().sort_index()
            
            trend_cols = st.columns(4)
            
            with trend_cols[0]:
                # Year-over-year growth
                if len(yearly_totals) >= 2:
                    latest_year = yearly_totals.iloc[-1]
                    previous_year = yearly_totals.iloc[-2]
                    yoy_growth = (latest_year - previous_year) / previous_year * 100
                    st.metric("YoY Growth", f"{yoy_growth:+.1f}%")
                else:
                    st.metric("YoY Growth", "N/A")
            
            with trend_cols[1]:
                # 5-year CAGR
                if len(yearly_totals) >= 5:
                    first_year = yearly_totals.iloc[-5]
                    last_year = yearly_totals.iloc[-1]
                    cagr = ((last_year / first_year) ** (1/5) - 1) * 100
                    st.metric("5-Year CAGR", f"{cagr:+.1f}%")
                else:
                    st.metric("5-Year CAGR", "N/A")
            
            with trend_cols[2]:
                # Peak year
                peak_year = yearly_totals.idxmax()
                peak_sales = yearly_totals.max()
                st.metric("Peak Year", f"{peak_year} ({peak_sales:,.0f})")
            
            with trend_cols[3]:
                # Trend direction
                if len(yearly_totals) >= 3:
                    recent_avg = yearly_totals.tail(3).mean()
                    earlier_avg = yearly_totals.head(3).mean()
                    trend_direction = "Growing" if recent_avg > earlier_avg else "Declining"
                    st.metric("Trend Direction", trend_direction)
                else:
                    st.metric("Trend Direction", "N/A")
            
            # Seasonal analysis
            st.markdown("### Seasonal Sales Analysis")
            
            # Analyze sales patterns by year
            seasonal_data = []
            for year in year_columns:
                year_sales = sales_data[year].sum()
                seasonal_data.append({'Year': int(year), 'Sales': year_sales})
            
            seasonal_df = pd.DataFrame(seasonal_data)
            
            if len(seasonal_df) > 0:
                # Calculate growth rates
                seasonal_df['YoY_Growth'] = seasonal_df['Sales'].pct_change() * 100
                seasonal_df['Growth_Status'] = seasonal_df['YoY_Growth'].apply(
                    lambda x: 'Growth' if x > 0 else 'Decline' if x < 0 else 'Stable'
                )
                
                # Display seasonal analysis
                st.dataframe(seasonal_df, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading sales trends: {str(e)}")

    def _render_performance_analysis(self) -> None:
        """Render performance analysis section."""
        st.markdown("## ⚡ Performance Analysis")
        
        if not self.analyzer:
            st.warning("Business logic analyzer not available")
            return
        
        try:
            # Get performance data
            sales_summary = self.analyzer.get_sales_summary()
            
            if sales_summary.empty:
                st.info("No sales data available")
                return
            
            # Performance benchmarking
            st.markdown("### Performance Benchmarking")
            
            # Calculate performance benchmarks
            sales_data = sales_summary['total_sales'].dropna()
            
            # Define performance tiers
            excellent_threshold = sales_data.quantile(0.9)
            good_threshold = sales_data.quantile(0.7)
            average_threshold = sales_data.quantile(0.5)
            poor_threshold = sales_data.quantile(0.3)
            
            # Categorize performance
            def categorize_performance(sales):
                if sales >= excellent_threshold:
                    return 'Excellent'
                elif sales >= good_threshold:
                    return 'Good'
                elif sales >= average_threshold:
                    return 'Average'
                elif sales >= poor_threshold:
                    return 'Below Average'
                else:
                    return 'Poor'
            
            sales_summary['Performance_Tier'] = sales_summary['total_sales'].apply(categorize_performance)
            
            # Performance distribution
            perf_dist = sales_summary['Performance_Tier'].value_counts()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Performance Distribution")
                # Create performance distribution chart
                fig = go.Figure(data=[
                    go.Bar(
                        x=perf_dist.index,
                        y=perf_dist.values,
                        text=perf_dist.values,
                        textposition='auto',
                        marker_color=['#28a745', '#20c997', '#ffc107', '#fd7e14', '#dc3545']
                    )
                ])
                
                fig.update_layout(
                    title="Sales Performance Distribution",
                    xaxis_title="Performance Tier",
                    yaxis_title="Number of Models",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### Performance Thresholds")
                st.metric("Excellent (Top 10%)", f"{excellent_threshold:,.0f}+")
                st.metric("Good (Top 30%)", f"{good_threshold:,.0f}+")
                st.metric("Average (Top 50%)", f"{average_threshold:,.0f}+")
                st.metric("Below Average (Bottom 30%)", f"{poor_threshold:,.0f}-")
            
            # Performance by automaker
            st.markdown("### Performance by Automaker")
            
            automaker_performance = sales_summary.groupby('Automaker').agg({
                'total_sales': ['sum', 'mean', 'count'],
                'Performance_Tier': lambda x: x.value_counts().to_dict()
            })
            
            automaker_performance.columns = ['Total_Sales', 'Avg_Sales_per_Model', 'Model_Count', 'Performance_Breakdown']
            
            # Add performance score
            automaker_performance['Performance_Score'] = (
                automaker_performance['Avg_Sales_per_Model'] / 
                automaker_performance['Avg_Sales_per_Model'].mean() * 100
            ).round(1)
            
            automaker_performance = automaker_performance.sort_values('Performance_Score', ascending=False)
            
            # Display top and bottom performers
            st.markdown("#### Top 10 Automakers by Performance Score")
            top_performers = automaker_performance.head(10)[['Total_Sales', 'Avg_Sales_per_Model', 'Model_Count', 'Performance_Score']]
            st.dataframe(top_performers, use_container_width=True)
            
            st.markdown("#### Bottom 10 Automakers by Performance Score")
            bottom_performers = automaker_performance.tail(10)[['Total_Sales', 'Avg_Sales_per_Model', 'Model_Count', 'Performance_Score']]
            st.dataframe(bottom_performers, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading performance analysis: {str(e)}")

    def _render_sales_forecasting(self) -> None:
        """Render sales forecasting section."""
        st.markdown("## 🔮 Sales Forecasting")
        
        if not self.analyzer:
            st.warning("Business logic analyzer not available")
            return
        
        try:
            # Get sales data for forecasting
            sales_data = self.analyzer.get_sales_summary()
            
            if sales_data.empty:
                st.info("No sales data available for forecasting")
                return
            
            # Simple trend-based forecasting
            year_columns = [col for col in sales_data.columns if col.isdigit()]
            if len(year_columns) < 3:
                st.info("Insufficient historical data for forecasting")
                return
            
            # Calculate yearly totals
            yearly_totals = sales_data[year_columns].sum().sort_index()
            
            # Simple linear trend forecast
            years = np.array([int(year) for year in yearly_totals.index])
            sales_values = yearly_totals.values
            
            # Fit linear trend
            coeffs = np.polyfit(years, sales_values, 1)
            trend_line = np.poly1d(coeffs)
            
            # Forecast next 3 years
            future_years = np.arange(max(years) + 1, max(years) + 4)
            forecast_values = trend_line(future_years)
            
            # Create forecast chart
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=years,
                y=sales_values,
                mode='lines+markers',
                name='Historical Sales',
                line=dict(color='blue', width=3)
            ))
            
            # Forecast data
            fig.add_trace(go.Scatter(
                x=future_years,
                y=forecast_values,
                mode='lines+markers',
                name='Forecast',
                line=dict(color='red', width=3, dash='dash')
            ))
            
            fig.update_layout(
                title="Sales Forecast (Next 3 Years)",
                xaxis_title="Year",
                yaxis_title="Total Sales (Units)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Forecast summary
            st.markdown("### Forecast Summary")
            
            forecast_cols = st.columns(3)
            
            with forecast_cols[0]:
                next_year = forecast_values[0]
                current_year = sales_values[-1]
                growth_rate = (next_year - current_year) / current_year * 100
                st.metric("Next Year Forecast", f"{next_year:,.0f}")
                st.metric("Expected Growth", f"{growth_rate:+.1f}%")
            
            with forecast_cols[1]:
                year_2 = forecast_values[1]
                year_3 = forecast_values[2]
                st.metric("Year 2 Forecast", f"{year_2:,.0f}")
                st.metric("Year 3 Forecast", f"{year_3:,.0f}")
            
            with forecast_cols[2]:
                # Trend analysis
                slope = coeffs[0]
                if slope > 0:
                    trend = "Growing"
                    trend_color = "success"
                elif slope < 0:
                    trend = "Declining"
                    trend_color = "warning"
                else:
                    trend = "Stable"
                    trend_color = "info"
                
                st.metric("Trend Direction", trend)
                st.metric("Annual Change", f"{slope:,.0f}")
            
            # Forecasting assumptions and limitations
            st.markdown("### Forecasting Assumptions & Limitations")
            
            assumptions = [
                "Linear trend assumption based on historical data",
                "No external factors (economic, regulatory, competitive) considered",
                "Based on historical sales patterns only",
                "Does not account for market saturation or disruption",
                "Simple extrapolation method - not suitable for long-term planning"
            ]
            
            for assumption in assumptions:
                st.markdown(f"• {assumption}")
            
        except Exception as e:
            st.error(f"Error loading sales forecasting: {str(e)}")

    def _render_sales_optimization(self) -> None:
        """Render sales optimization section."""
        st.markdown("## 🚀 Sales Optimization")
        
        if not self.analyzer:
            st.warning("Business logic analyzer not available")
            return
        
        try:
            # Get optimization data
            sales_summary = self.analyzer.get_sales_summary()
            price_data = self.analyzer.get_price_range_by_model()
            
            if sales_summary.empty:
                st.info("No sales data available for optimization")
                return
            
            # Merge sales and price data
            optimization_data = sales_summary.merge(price_data, on='Genmodel_ID', how='left')
            
            # Sales optimization insights
            st.markdown("### Sales Optimization Opportunities")
            
            # Underperforming models analysis
            avg_sales = sales_summary['total_sales'].mean()
            underperformers = sales_summary[sales_summary['total_sales'] < avg_sales * 0.5]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Underperforming Models")
                st.info(f"**{len(underperformers)} models** performing below 50% of average sales")
                
                if not underperformers.empty:
                    # Top underperformers by automaker
                    underperformer_breakdown = underperformers.groupby('Automaker').size().sort_values(ascending=False).head(10)
                    
                    st.markdown("**Top Automakers with Underperforming Models:**")
                    for automaker, count in underperformer_breakdown.items():
                        st.markdown(f"• {automaker}: {count} models")
            
            with col2:
                st.markdown("#### High-Performing Models")
                high_performers = sales_summary[sales_summary['total_sales'] > avg_sales * 2]
                
                st.success(f"**{len(high_performers)} models** performing above 200% of average sales")
                
                if not high_performers.empty:
                    # Top performers by automaker
                    performer_breakdown = high_performers.groupby('Automaker').size().sort_values(ascending=False).head(10)
                    
                    st.markdown("**Top Automakers with High-Performing Models:**")
                    for automaker, count in performer_breakdown.items():
                        st.markdown(f"• {automaker}: {count} models")
            
            # Price-sales correlation analysis
            if not optimization_data.empty and 'price_mean' in optimization_data.columns:
                st.markdown("### Price-Sales Correlation Analysis")
                
                # Calculate correlation
                price_sales_corr = optimization_data['price_mean'].corr(optimization_data['total_sales'])
                
                corr_cols = st.columns(3)
                
                with corr_cols[0]:
                    st.metric("Price-Sales Correlation", f"{price_sales_corr:.3f}")
                
                with corr_cols[1]:
                    if abs(price_sales_corr) > 0.5:
                        correlation_strength = "Strong"
                    elif abs(price_sales_corr) > 0.3:
                        correlation_strength = "Moderate"
                    else:
                        correlation_strength = "Weak"
                    st.metric("Correlation Strength", correlation_strength)
                
                with corr_cols[2]:
                    correlation_direction = "Positive" if price_sales_corr > 0 else "Negative"
                    st.metric("Correlation Direction", correlation_direction)
                
                # Price optimization recommendations
                st.markdown("### Price Optimization Recommendations")
                
                recommendations = []
                
                if price_sales_corr < -0.3:
                    recommendations.append("**Price Sensitivity Detected:** Consider price reduction strategies for underperforming models")
                elif price_sales_corr > 0.3:
                    recommendations.append("**Premium Positioning Opportunity:** Higher prices correlate with better sales performance")
                else:
                    recommendations.append("**Price Neutral Market:** Sales performance not strongly correlated with pricing")
                
                # Market positioning recommendations
                if not optimization_data.empty:
                    # Analyze price segments
                    budget_models = optimization_data[optimization_data['price_mean'] < 25000]
                    premium_models = optimization_data[optimization_data['price_mean'] > 75000]
                    
                    budget_avg_sales = budget_models['total_sales'].mean() if not budget_models.empty else 0
                    premium_avg_sales = premium_models['total_sales'].mean() if not premium_models.empty else 0
                    
                    if budget_avg_sales > premium_avg_sales:
                        recommendations.append("**Volume Strategy:** Budget segment shows higher sales volumes - focus on volume-based growth")
                    elif premium_avg_sales > budget_avg_sales:
                        recommendations.append("**Premium Strategy:** Premium segment shows better sales performance - consider upmarket positioning")
                
                for recommendation in recommendations:
                    st.info(recommendation)
            
            # Sales improvement strategies
            st.markdown("### Sales Improvement Strategies")
            
            strategies = [
                "**Focus on High-Performing Models:** Invest in marketing and distribution for top-performing models",
                "**Address Underperformers:** Conduct detailed analysis of underperforming models to identify improvement opportunities",
                "**Market Penetration:** Target underserved market segments with existing successful models",
                "**Product Portfolio Optimization:** Consider discontinuing consistently underperforming models",
                "**Competitive Analysis:** Study successful competitors' strategies in high-performing segments",
                "**Price Optimization:** Implement dynamic pricing strategies based on price-sales correlation analysis",
                "**Geographic Expansion:** Identify markets where successful models could be introduced",
                "**Customer Segmentation:** Develop targeted marketing strategies for different customer segments"
            ]
            
            for strategy in strategies:
                st.markdown(f"• {strategy}")
            
        except Exception as e:
            st.error(f"Error loading sales optimization: {str(e)}")

    def get_dashboard_config(self) -> Dict[str, Any]:
        """Get dashboard configuration."""
        return {
            'dashboard_type': 'sales',
            'components_available': {
                'layout': self.layout is not None,
                'sidebar': self.sidebar is not None,
                'kpi_calculator': self.kpi_calc is not None,
                'chart_factory': self.chart_factory is not None,
                'analyzer': self.analyzer is not None
            },
            'sections': [
                'sales_overview',
                'top_performers',
                'sales_trends',
                'performance_analysis',
                'sales_forecasting',
                'sales_optimization'
            ]
        }


# Global instance for use throughout the application
sales_dashboard = SalesDashboard()


def show_sales_dashboard(analyzer):
    """Render the Sales Performance dashboard using the provided analyzer.

    Reads filters from st.session_state: 'filter_automakers', 'filter_top_n'.
    """
    st.markdown("## 📈 Sales Performance")
    
    try:
        selected_automakers = st.session_state.get('filter_automakers', [])
        top_n = st.session_state.get('filter_top_n', 15)

        # Get data
        sales_summary = analyzer.get_sales_summary()
        
        # Apply filters
        if selected_automakers:
            sales_summary = sales_summary[sales_summary['Automaker'].isin(selected_automakers)]
        
        # Sales trends
        st.markdown('<div class="section-header">📈 Advanced Sales Performance Analytics</div>', unsafe_allow_html=True)
        
        # Sales Trend by Automaker
        st.subheader("📈 Sales Trend by Automaker")
        
        # Preparamos los datos para el gráfico de tendencias competitivas
        if not sales_summary.empty:
            # Necesitamos obtener los datos originales de ventas para el análisis temporal
            sales_data = analyzer.sales  # Acceso directo a los datos de ventas
            
            if not sales_data.empty:
                # Transformamos los datos de ventas de formato ancho a largo
                year_columns = [col for col in sales_data.columns if col.isdigit()]
                
                if year_columns:
                    sales_long = pd.melt(
                        sales_data,
                        id_vars=['Automaker', 'Genmodel', 'Genmodel_ID'],
                        value_vars=year_columns,
                        var_name='Year',
                        value_name='Sales_Volume'
                    )
                    
                    # Aplicamos filtros si están seleccionados
                    if selected_automakers:
                        sales_long = sales_long[sales_long['Automaker'].isin(selected_automakers)]
                    
                    # Agrupamos por año y fabricante para obtener las ventas por fabricante
                    yearly_sales_by_automaker = sales_long.groupby(['Year', 'Automaker'])['Sales_Volume'].sum().reset_index()
                    yearly_sales_by_automaker['Year'] = pd.to_numeric(yearly_sales_by_automaker['Year'])  # Aseguramos que el año sea numérico

                    # Creamos el gráfico de líneas competitivo con Plotly Express
                    fig_trend = px.line(
                        yearly_sales_by_automaker,
                        x='Year',
                        y='Sales_Volume',
                        color='Automaker',  # ¡Esta es la línea clave para múltiples líneas!
                        title='Sales Volume Trend by Automaker (2001-2020)',
                        markers=True,  # Añade puntos en cada dato anual
                        labels={'Sales_Volume': 'Total Sales', 'Year': 'Year'},
                        template="plotly_dark",
                        color_discrete_sequence=px.colors.qualitative.Set3  # Paleta de colores distintiva
                    )
                    
                    fig_trend.update_layout(
                        xaxis_title='Year',
                        yaxis_title='Total Sales Volume',
                        showlegend=True,  # Mostramos la leyenda para identificar fabricantes
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1,
                            font=dict(color="white", size=10)
                        ),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=500  # Aumentamos altura para acomodar la leyenda
                    )
                    
                    # Añadimos anotaciones para eventos importantes (solo si hay datos)
                    if 2016 in yearly_sales_by_automaker['Year'].values:
                        # Calculamos el promedio de ventas en 2016 para posicionar la anotación
                        sales_2016 = yearly_sales_by_automaker[yearly_sales_by_automaker['Year'] == 2016]['Sales_Volume'].mean()
                        fig_trend.add_annotation(
                            x=2016,
                            y=sales_2016,
                            text="Peak Year (2016)",
                            showarrow=True,
                            arrowhead=2,
                            arrowcolor="red",
                            bgcolor="rgba(255,255,255,0.8)",
                            bordercolor="red",
                            font=dict(color="black", size=12)
                        )
                    
                    # Mostramos el gráfico
                    st.plotly_chart(fig_trend, use_container_width=True)
                    
                    # Añadimos información adicional sobre las tendencias competitivas
                    st.markdown("""
                    **📊 Competitive Analysis Insights:**
                    - **Market Leaders**: Compare performance of different automakers over time
                    - **Growth Patterns**: Identify which brands show consistent growth vs volatility
                    - **Market Share Evolution**: See how brand positions changed from 2001-2020
                    - **Crisis Impact**: Observe how different brands responded to market challenges
                    - **Peak Performance**: 2016 marked the highest overall market volume
                    """)
                    
                    # Añadimos estadísticas rápidas si hay datos filtrados
                    if selected_automakers:
                        st.markdown("**🎯 Selected Automakers Analysis:**")
                        for automaker in selected_automakers:
                            automaker_data = yearly_sales_by_automaker[yearly_sales_by_automaker['Automaker'] == automaker]
                            if not automaker_data.empty:
                                peak_year = automaker_data.loc[automaker_data['Sales_Volume'].idxmax(), 'Year']
                                peak_sales = automaker_data['Sales_Volume'].max()
                                total_sales = automaker_data['Sales_Volume'].sum()
                                st.markdown(f"- **{automaker}**: Peak in {peak_year} ({peak_sales:,.0f} units), Total: {total_sales:,.0f} units")
                    
                    st.markdown("---")  # Añadimos un separador visual
                else:
                    st.info("No yearly sales data available to display trend.")
            else:
                st.info("No sales data available for trend analysis.")
        else:
            st.info("No filtered sales data available to display trend.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("🏆 Top Performing Models")
            if not sales_summary.empty:
                sales_clean = sales_summary.dropna(subset=['total_sales'])
                if not sales_clean.empty:
                    top_models = sales_clean.nlargest(top_n, 'total_sales')
                    fig_bar = px.bar(
                        top_models,
                        x='total_sales',
                        y='Genmodel',
                        orientation='h',
                        color='Automaker',
                        title='',
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        template="plotly_dark"
                    )
                    fig_bar.update_layout(
                        height=450,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        xaxis_title="Total Sales",
                        yaxis_title="Model"
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No valid sales data available")
            else:
                st.info("No sales data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("🎯 Sales Performance by Automaker")
            if not sales_summary.empty:
                sales_clean = sales_summary.dropna(subset=['total_sales'])
                if not sales_clean.empty:
                    sales_by_maker = sales_clean.groupby('Automaker')['total_sales'].sum().sort_values(ascending=False).head(15)
                    fig_scatter = px.scatter(
                        x=sales_by_maker.index,
                        y=sales_by_maker.values,
                        title='',
                        color=sales_by_maker.values,
                        color_continuous_scale='plasma',
                        size=sales_by_maker.values,
                        template="plotly_dark"
                    )
                    fig_scatter.update_layout(
                        xaxis_tickangle=-45,
                        height=450,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        xaxis_title="Automaker",
                        yaxis_title="Total Sales"
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)
                else:
                    st.info("No valid sales data available")
            else:
                st.info("No sales data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional Sales Analytics
        st.markdown('<div class="section-header">🎯 Advanced Sales Analytics</div>', unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📊 Sales Distribution Analysis")
            if not sales_summary.empty:
                sales_clean = sales_summary.dropna(subset=['total_sales'])
                if not sales_clean.empty:
                    # Create sales categories
                    sales_clean_copy = sales_clean.copy()
                    sales_clean_copy['Sales Category'] = pd.cut(
                        sales_clean_copy['total_sales'],
                        bins=[0, 1000, 5000, 10000, 50000, float('inf')],
                        labels=['Low (<1K)', 'Medium (1K-5K)', 'High (5K-10K)', 'Very High (10K-50K)', 'Exceptional (>50K)']
                    )
                    
                    category_counts = sales_clean_copy['Sales Category'].value_counts()
                    
                    fig_bar = px.bar(
                        x=category_counts.index,
                        y=category_counts.values,
                        title='',
                        template="plotly_dark",
                        color=category_counts.values,
                        color_continuous_scale='plasma'
                    )
                    fig_bar.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=450,
                        xaxis_title="Sales Category",
                        yaxis_title="Number of Models",
                        xaxis_tickangle=-45
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No sales data available")
            else:
                st.info("No sales data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📈 Sales Performance Matrix")
            if not sales_summary.empty:
                sales_clean = sales_summary.dropna(subset=['total_sales'])
                if not sales_clean.empty:
                    # Create performance matrix by automaker
                    performance_matrix = sales_clean.groupby('Automaker').agg({
                        'total_sales': ['sum', 'mean', 'count']
                    }).round(0)
                    
                    performance_matrix.columns = ['Total Sales', 'Avg Sales per Model', 'Model Count']
                    performance_matrix = performance_matrix.sort_values('Total Sales', ascending=False).head(15)
                    
                    # Calculate market share for bubble size
                    total_market_sales = performance_matrix['Total Sales'].sum()
                    performance_matrix['Market Share (%)'] = (performance_matrix['Total Sales'] / total_market_sales * 100).round(1)
                    
                    # Create scatter plot for performance matrix
                    fig_scatter = px.scatter(
                        performance_matrix,
                        x='Model Count',
                        y='Avg Sales per Model',
                        size='Market Share (%)',
                        color=performance_matrix.index,  # Use automaker names for color
                        title='',
                        template="plotly_dark",
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        hover_data={
                            'Total Sales': ':,.0f', 
                            'Model Count': ':.0f', 
                            'Avg Sales per Model': ':,.0f',
                            'Market Share (%)': ':.1f'
                        }
                    )
                    # Update hover template for better information
                    fig_scatter.update_traces(
                        hovertemplate='<b>%{legendgroup}</b><br>' +
                                     'Modelos: %{x}<br>' +
                                     'Ventas promedio: %{y:,.0f}<br>' +
                                     'Ventas totales: %{customdata[0]:,.0f}<br>' +
                                     'Market share: %{marker.size:.1f}%<br>' +
                                     '<extra></extra>'
                    )
                    
                    fig_scatter.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=450,
                        xaxis_title="Number of Models",
                        yaxis_title="Average Sales per Model",
                        legend_title="Automaker",
                        showlegend=True
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)
                else:
                    st.info("No sales data available")
            else:
                st.info("No sales data available")
            st.markdown('</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error rendering sales performance: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

