"""
🏢 Executive Dashboard Component for Car Market Analysis

Executive-grade dashboard providing high-level strategic insights and KPIs
for automotive market analysis with C-level decision support.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from typing import Dict, List, Optional, Any
import warnings
warnings.filterwarnings('ignore')

# Import components
try:
    from ..ui.layout import layout_component
    from ..ui.sidebar import sidebar_component
    from ..analytics.kpi_calculator import kpi_calculator
    from ..analytics.data_quality import data_quality
    from ..visualizations.chart_factory import chart_factory
    from ...business_logic import analyzer
except ImportError:
    # Fallback imports
    layout_component = None
    sidebar_component = None
    kpi_calculator = None
    data_quality = None
    chart_factory = None
    analyzer = None


class ExecutiveDashboard:
    """
    👔 Executive-Grade Strategic Dashboard
    
    Provides C-level executives with strategic insights, key performance indicators,
    and high-level market analysis for automotive industry decision making.
    """

    def __init__(self):
        """Initialize the ExecutiveDashboard with required components."""
        self.layout = layout_component
        self.sidebar = sidebar_component
        self.kpi_calc = kpi_calculator
        self.data_quality = data_quality
        self.chart_factory = chart_factory
        self.analyzer = analyzer

    def render_executive_dashboard(self) -> None:
        """Render the complete executive dashboard."""
        # Setup page layout
        if self.layout:
            self.layout.setup_executive_layout()
        
        # Create executive header
        st.markdown("""
        <div class="executive-header">
            <h1>📊 Executive Strategic Dashboard</h1>
            <p>Strategic Business Intelligence for Automotive Market Analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Executive summary section
        self._render_executive_summary()
        
        # Key performance indicators
        self._render_kpi_section()
        
        # Strategic insights
        self._render_strategic_insights()
        
        # Market overview
        self._render_market_overview()
        
        # Performance metrics
        self._render_performance_metrics()
        
        # Risk assessment
        self._render_risk_assessment()

    def _render_executive_summary(self) -> None:
        """Render executive summary section."""
        st.markdown("## 🎯 Executive Summary")
        
        if not self.analyzer:
            st.warning("Business logic analyzer not available")
            return
        
        try:
            # Get executive summary data
            executive_data = self.analyzer.get_executive_summary()
            
            # Display key insights
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### Market Position")
                market_insights = executive_data.get('market_insights', {})
                if market_insights:
                    st.success(f"**Market Leader:** {market_insights.get('market_leader', 'N/A')}")
                    st.info(f"**Market Concentration:** {market_insights.get('market_concentration', 0):.1f}%")
            
            with col2:
                st.markdown("### Financial Performance")
                if market_insights:
                    avg_price = market_insights.get('avg_market_price', 0)
                    st.success(f"**Average Market Price:** €{avg_price:,.0f}")
                    total_sales = market_insights.get('total_market_sales', 0)
                    st.info(f"**Total Market Sales:** {total_sales:,.0f} units")
            
            with col3:
                st.markdown("### Data Quality")
                quality_report = executive_data.get('quality_report', {})
                if quality_report:
                    avg_quality = np.mean([metrics.get('overall_quality_score', 0) 
                                         for metrics in quality_report.values() 
                                         if isinstance(metrics, dict)])
                    if avg_quality >= 90:
                        st.success(f"**Data Quality:** Excellent ({avg_quality:.1f}%)")
                    elif avg_quality >= 80:
                        st.info(f"**Data Quality:** Good ({avg_quality:.1f}%)")
                    else:
                        st.warning(f"**Data Quality:** Needs Improvement ({avg_quality:.1f}%)")
            
            # Recommendations
            recommendations = market_insights.get('recommendations', [])
            if recommendations:
                st.markdown("### 🎯 Strategic Recommendations")
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"{i}. {rec}")
            
        except Exception as e:
            st.error(f"Error loading executive summary: {str(e)}")

    def _render_kpi_section(self) -> None:
        """Render key performance indicators section."""
        st.markdown("## 📈 Key Performance Indicators")
        
        if not self.analyzer or not self.kpi_calc:
            st.warning("KPI calculator not available")
            return
        
        try:
            # Get KPI dashboard data
            kpi_data = self.analyzer.get_kpi_dashboard()
            
            if not kpi_data:
                st.info("No KPI data available")
                return
            
            # Create KPI columns
            col1, col2, col3, col4 = st.columns(4)
            
            kpi_metrics = [
                ('Total Models', 'total_models'),
                ('Total Sales', 'total_market_sales'),
                ('Avg Sales/Model', 'avg_sales_per_model'),
                ('Market Leader %', 'market_leader_share'),
                ('Avg Price', 'avg_market_price'),
                ('Price Range', 'price_range_span'),
                ('YoY Growth', 'yoy_growth_rate'),
                ('Top 3 Concentration', 'top_3_concentration')
            ]
            
            # Display KPIs in a grid
            for i, (label, key) in enumerate(kpi_metrics):
                col = [col1, col2, col3, col4][i % 4]
                with col:
                    value = kpi_data.get(key, 0)
                    
                    # Format value based on type
                    if key in ['total_market_sales', 'avg_sales_per_model', 'total_models']:
                        formatted_value = f"{value:,.0f}"
                    elif key in ['market_leader_share', 'top_3_concentration', 'yoy_growth_rate']:
                        formatted_value = f"{value:.1f}%"
                    elif key in ['avg_market_price', 'price_range_span']:
                        formatted_value = f"€{value:,.0f}"
                    else:
                        formatted_value = str(value)
                    
                    # Create metric card
                    if self.layout:
                        self.layout.create_metric_card(label, formatted_value)
                    else:
                        st.metric(label, formatted_value)
            
            # Performance ratings
            performance_ratings = kpi_data.get('performance_ratings', {})
            if performance_ratings:
                st.markdown("### 🏆 Performance Ratings")
                
                rating_cols = st.columns(len(performance_ratings))
                for i, (metric, rating) in enumerate(performance_ratings.items()):
                    with rating_cols[i]:
                        # Color coding for ratings
                        if 'Excellent' in rating or 'Strong' in rating:
                            st.success(f"**{metric.replace('_', ' ').title()}:** {rating}")
                        elif 'Good' in rating or 'Moderate' in rating:
                            st.info(f"**{metric.replace('_', ' ').title()}:** {rating}")
                        else:
                            st.warning(f"**{metric.replace('_', ' ').title()}:** {rating}")
            
        except Exception as e:
            st.error(f"Error loading KPIs: {str(e)}")

    def _render_strategic_insights(self) -> None:
        """Render strategic insights section."""
        st.markdown("## 🔍 Strategic Insights")
        
        if not self.analyzer:
            st.warning("Business logic analyzer not available")
            return
        
        try:
            # Get market insights
            market_insights = self.analyzer.generate_market_insights()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Market Analysis")
                
                # Market concentration analysis
                concentration = market_insights.get('market_concentration', 0)
                if concentration > 60:
                    st.warning(f"**High Market Concentration:** {concentration:.1f}% - Consider diversification")
                elif concentration > 40:
                    st.info(f"**Moderate Market Concentration:** {concentration:.1f}%")
                else:
                    st.success(f"**Fragmented Market:** {concentration:.1f}% - Opportunity for consolidation")
                
                # Market size analysis
                total_brands = market_insights.get('total_brands', 0)
                st.info(f"**Total Brands in Market:** {total_brands}")
                
                # Price positioning
                avg_price = market_insights.get('avg_market_price', 0)
                if avg_price > 60000:
                    st.info("**Premium Market Positioning** - Focus on luxury segment")
                elif avg_price > 35000:
                    st.info("**Mid-Range Market Positioning** - Balanced approach")
                else:
                    st.info("**Budget Market Positioning** - Volume-focused strategy")
            
            with col2:
                st.markdown("### Competitive Intelligence")
                
                # Market leader analysis
                market_leader = market_insights.get('market_leader', 'Unknown')
                st.success(f"**Market Leader:** {market_leader}")
                
                # Sales performance analysis
                avg_sales = market_insights.get('avg_model_sales', 0)
                if avg_sales > 100000:
                    st.success(f"**Strong Sales Performance:** {avg_sales:,.0f} avg units/model")
                elif avg_sales > 50000:
                    st.info(f"**Moderate Sales Performance:** {avg_sales:,.0f} avg units/model")
                else:
                    st.warning(f"**Weak Sales Performance:** {avg_sales:,.0f} avg units/model")
                
                # Outlier analysis
                outlier_count = market_insights.get('outlier_count', 0)
                if outlier_count > 20:
                    st.warning(f"**High Outlier Count:** {outlier_count} - Investigate exceptional performers")
                elif outlier_count > 10:
                    st.info(f"**Moderate Outlier Count:** {outlier_count}")
                else:
                    st.success(f"**Low Outlier Count:** {outlier_count} - Consistent performance")
            
        except Exception as e:
            st.error(f"Error loading strategic insights: {str(e)}")

    def _render_market_overview(self) -> None:
        """Render market overview section."""
        st.markdown("## 🌍 Market Overview")
        
        if not self.analyzer or not self.chart_factory:
            st.warning("Required components not available")
            return
        
        try:
            # Get market data
            market_share = self.analyzer.calculate_market_share()
            sales_summary = self.analyzer.get_sales_summary()
            
            if market_share.empty or sales_summary.empty:
                st.info("Insufficient data for market overview")
                return
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Market Share Distribution")
                # Create market share pie chart
                market_share_chart = self.chart_factory.create_market_share_pie_chart(
                    market_share, "Market Share by Automaker"
                )
                st.plotly_chart(market_share_chart, use_container_width=True)
            
            with col2:
                st.markdown("### Top Performing Models")
                # Create sales bar chart
                sales_chart = self.chart_factory.create_sales_bar_chart(
                    sales_summary, "Top 15 Models by Sales"
                )
                st.plotly_chart(sales_chart, use_container_width=True)
            
            # Market concentration metrics
            st.markdown("### Market Concentration Analysis")
            
            concentration_cols = st.columns(3)
            
            with concentration_cols[0]:
                top_3_share = market_share.head(3)['market_share_percent'].sum()
                st.metric("Top 3 Market Share", f"{top_3_share:.1f}%")
            
            with concentration_cols[1]:
                top_5_share = market_share.head(5)['market_share_percent'].sum()
                st.metric("Top 5 Market Share", f"{top_5_share:.1f}%")
            
            with concentration_cols[2]:
                hhi_index = (market_share['market_share_percent'] ** 2).sum()
                st.metric("HHI Index", f"{hhi_index:.0f}")
            
        except Exception as e:
            st.error(f"Error loading market overview: {str(e)}")

    def _render_performance_metrics(self) -> None:
        """Render performance metrics section."""
        st.markdown("## ⚡ Performance Metrics")
        
        if not self.analyzer or not self.chart_factory:
            st.warning("Required components not available")
            return
        
        try:
            # Get performance data
            price_data = self.analyzer.get_price_range_by_model()
            sales_data = self.analyzer.get_sales_summary()
            
            if price_data.empty or sales_data.empty:
                st.info("Insufficient data for performance metrics")
                return
            
            # Merge data for analysis
            merged_data = price_data.merge(sales_data, on='Genmodel_ID', how='inner')
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Price Performance")
                # Create price distribution chart
                price_chart = self.chart_factory.create_price_distribution_chart(
                    merged_data, "Price Distribution Analysis"
                )
                st.plotly_chart(price_chart, use_container_width=True)
            
            with col2:
                st.markdown("### Price vs Sales Correlation")
                # Create price vs sales scatter plot
                scatter_chart = self.chart_factory.create_price_vs_sales_scatter(
                    merged_data, "Price vs Sales Performance"
                )
                st.plotly_chart(scatter_chart, use_container_width=True)
            
            # Performance statistics
            st.markdown("### Performance Statistics")
            
            stats_cols = st.columns(4)
            
            with stats_cols[0]:
                avg_price = merged_data['price_mean'].mean()
                st.metric("Average Price", f"€{avg_price:,.0f}")
            
            with stats_cols[1]:
                avg_sales = merged_data['total_sales'].mean()
                st.metric("Average Sales", f"{avg_sales:,.0f}")
            
            with stats_cols[2]:
                price_volatility = merged_data['price_mean'].std() / merged_data['price_mean'].mean()
                st.metric("Price Volatility", f"{price_volatility:.2f}")
            
            with stats_cols[3]:
                sales_volatility = merged_data['total_sales'].std() / merged_data['total_sales'].mean()
                st.metric("Sales Volatility", f"{sales_volatility:.2f}")
            
        except Exception as e:
            st.error(f"Error loading performance metrics: {str(e)}")

    def _render_risk_assessment(self) -> None:
        """Render risk assessment section."""
        st.markdown("## ⚠️ Risk Assessment")
        
        if not self.analyzer:
            st.warning("Business logic analyzer not available")
            return
        
        try:
            # Get risk indicators
            market_insights = self.analyzer.generate_market_insights()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Market Risks")
                
                risks = []
                
                # Market concentration risk
                concentration = market_insights.get('market_concentration', 0)
                if concentration > 70:
                    risks.append(("High Market Concentration", "danger", 
                                f"Top 3 players control {concentration:.1f}% of market"))
                elif concentration > 50:
                    risks.append(("Moderate Market Concentration", "warning", 
                                f"Top 3 players control {concentration:.1f}% of market"))
                
                # Price volatility risk
                price_range = market_insights.get('price_range', {})
                if price_range and price_range.get('max', 0) - price_range.get('min', 0) > 200000:
                    risks.append(("High Price Volatility", "warning", 
                                "Large price range indicates market instability"))
                
                # Display risks
                for risk_name, risk_level, risk_desc in risks:
                    if risk_level == "danger":
                        st.error(f"**{risk_name}:** {risk_desc}")
                    elif risk_level == "warning":
                        st.warning(f"**{risk_name}:** {risk_desc}")
                    else:
                        st.info(f"**{risk_name}:** {risk_desc}")
                
                if not risks:
                    st.success("**No significant market risks identified**")
            
            with col2:
                st.markdown("### Opportunities")
                
                opportunities = []
                
                # Market fragmentation opportunity
                concentration = market_insights.get('market_concentration', 0)
                if concentration < 40:
                    opportunities.append("Market fragmentation presents consolidation opportunities")
                
                # Growth opportunity
                total_sales = market_insights.get('total_market_sales', 0)
                if total_sales > 10000000:
                    opportunities.append("Large market size supports growth strategies")
                
                # Price positioning opportunity
                avg_price = market_insights.get('avg_market_price', 0)
                if avg_price < 30000:
                    opportunities.append("Budget market positioning opportunity")
                elif avg_price > 50000:
                    opportunities.append("Premium market positioning opportunity")
                
                # Display opportunities
                for opportunity in opportunities:
                    st.success(f"• {opportunity}")
                
                if not opportunities:
                    st.info("**Limited opportunities identified**")
            
            # Risk mitigation recommendations
            st.markdown("### 🛡️ Risk Mitigation Recommendations")
            
            recommendations = [
                "Diversify product portfolio to reduce concentration risk",
                "Implement dynamic pricing strategies to manage volatility",
                "Develop strategic partnerships for market stability",
                "Invest in data analytics for better risk prediction",
                "Create contingency plans for market disruptions"
            ]
            
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"{i}. {rec}")
            
        except Exception as e:
            st.error(f"Error loading risk assessment: {str(e)}")

    def get_dashboard_config(self) -> Dict[str, Any]:
        """Get dashboard configuration."""
        return {
            'dashboard_type': 'executive',
            'components_available': {
                'layout': self.layout is not None,
                'sidebar': self.sidebar is not None,
                'kpi_calculator': self.kpi_calc is not None,
                'data_quality': self.data_quality is not None,
                'chart_factory': self.chart_factory is not None,
                'analyzer': self.analyzer is not None
            },
            'sections': [
                'executive_summary',
                'kpi_section',
                'strategic_insights',
                'market_overview',
                'performance_metrics',
                'risk_assessment'
            ]
        }


# Global instance for use throughout the application
executive_dashboard = ExecutiveDashboard()


def show_executive_dashboard(analyzer):
    """Render the Executive Summary dashboard using the provided analyzer.

    Note: relies on st.session_state['filter_automakers'] and ['filter_top_n'] set in the sidebar.
    """
    st.markdown("## 📊 Executive Summary")
    
    try:
        # Read filters from session state (populated in the main app sidebar)
        selected_automakers = st.session_state.get('filter_automakers', [])
        top_n = st.session_state.get('filter_top_n', 15)

        # Get data
        sales_summary = analyzer.get_sales_summary()
        price_summary = analyzer.get_price_range_by_model()
        
        # Apply filters
        if selected_automakers:
            sales_summary = sales_summary[sales_summary['Automaker'].isin(selected_automakers)]
            price_summary = price_summary[price_summary['Automaker'].isin(selected_automakers)]
        
        # Key metrics - Row 1
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            total_models = len(price_summary)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🚗</div>
                <div class="metric-value">{total_models}</div>
                <div class="metric-label">Total Models</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_sales = sales_summary['total_sales'].sum() if not sales_summary.empty else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">📈</div>
                <div class="metric-value">{int(total_sales):,}</div>
                <div class="metric-label">Total Sales</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_price = price_summary['price_mean'].mean() if not price_summary.empty else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">💰</div>
                <div class="metric-value">€{avg_price:,.0f}</div>
                <div class="metric-label">Avg Price</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            automakers_count = sales_summary['Automaker'].nunique() if not sales_summary.empty else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🏭</div>
                <div class="metric-value">{automakers_count}</div>
                <div class="metric-label">Automakers</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            # Market share of top automaker
            if not sales_summary.empty:
                top_automaker_sales = sales_summary.groupby('Automaker')['total_sales'].sum().max()
                total_sales_all = sales_summary['total_sales'].sum()
                market_share_top = (top_automaker_sales / total_sales_all * 100) if total_sales_all > 0 else 0
            else:
                market_share_top = 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">👑</div>
                <div class="metric-value">{market_share_top:.1f}%</div>
                <div class="metric-label">Top Market Share</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col6:
            # Price range
            if not price_summary.empty:
                price_range = price_summary['price_mean'].max() - price_summary['price_mean'].min()
            else:
                price_range = 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">📊</div>
                <div class="metric-value">€{price_range:,.0f}</div>
                <div class="metric-label">Price Range</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts
        st.markdown('<div class="section-header">📊 Sales Performance Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("🚗 Top Models by Sales")
            if not sales_summary.empty:
                # Remove NaN values for chart
                sales_clean = sales_summary.dropna(subset=['total_sales'])
                if not sales_clean.empty:
                    top_sales = sales_clean.nlargest(top_n, 'total_sales')
                    fig_sales = px.bar(
                        top_sales,
                        x='Genmodel',
                        y='total_sales',
                        color='Automaker',
                        title='',
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        template="plotly_dark"
                    )
                    fig_sales.update_layout(
                        xaxis_tickangle=-45,
                        height=450,
                        showlegend=True,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        title_font_size=16
                    )
                    st.plotly_chart(fig_sales, use_container_width=True)
                else:
                    st.info("No valid sales data available")
            else:
                st.info("No sales data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("💰 Average Price by Automaker")
            if not price_summary.empty:
                # Remove NaN values for chart
                price_clean = price_summary.dropna(subset=['price_mean'])
                if not price_clean.empty:
                    avg_price_by_maker = price_clean.groupby('Automaker')['price_mean'].mean().sort_values(ascending=False)
                    fig_price = px.bar(
                        x=avg_price_by_maker.index,
                        y=avg_price_by_maker.values,
                        title='',
                        color=avg_price_by_maker.values,
                        color_continuous_scale='Viridis',
                        template="plotly_dark"
                    )
                    fig_price.update_layout(
                        xaxis_tickangle=-45,
                        height=450,
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        title_font_size=16
                    )
                    st.plotly_chart(fig_price, use_container_width=True)
                else:
                    st.info("No valid price data available")
            else:
                st.info("No price data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")  # Separador visual
        
        # --- NUEVA SECCIÓN PARA EL TREEMAP ---
        st.subheader("📊 Sales Volume by Market Segment")
        try:
            sales_by_segment_data = analyzer.get_sales_by_segment()
            if not sales_by_segment_data.empty:
                # Crear el Treemap
                fig_treemap = px.treemap(
                    sales_by_segment_data,
                    path=[px.Constant("All Segments"), 'Price_Segment'],
                    values='total_sales',
                    color='Price_Segment',
                    title='Contribution of Each Price Segment to Total Sales',
                    color_discrete_map={
                        'Budget': '#2a9d8f',
                        'Mid-Range': '#e9c46a',
                        'Premium': '#f4a261',
                        'Luxury': '#e76f51',
                        '(?)': '#a9a9a9'  # Color para el total
                    },
                    template="plotly_dark"
                )
                fig_treemap.update_layout(
                    margin=dict(t=50, l=25, r=25, b=25),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=500
                )
                st.plotly_chart(fig_treemap, use_container_width=True)
                
                # Añadir información contextual sobre el Treemap
                st.markdown("""
                **📊 Market Segment Analysis:**
                - **Size of rectangles**: Represents total sales volume for each segment
                - **Color coding**: Consistent with market segmentation visualization
                - **Market dominance**: Larger segments drive the majority of sales volume
                """)
                
                # Mostrar estadísticas del Treemap
                total_sales_all_segments = sales_by_segment_data['total_sales'].sum()
                st.markdown("**🎯 Segment Contribution:**")
                for _, row in sales_by_segment_data.iterrows():
                    percentage = (row['total_sales'] / total_sales_all_segments) * 100
                    st.markdown(f"- **{row['Price_Segment']}**: {row['total_sales']:,.0f} units ({percentage:.1f}%)")
            else:
                st.info("Sales by segment data is not available.")
        except Exception as e:
            st.error(f"Error rendering sales by segment treemap: {str(e)}")
        # ------------------------------------
        
        # Additional Charts Section
        st.markdown('<div class="section-header">🔍 Advanced Analytics</div>', unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("💹 Price vs Sales Correlation")
            if not sales_summary.empty and not price_summary.empty:
                # Merge sales and price data for correlation analysis
                correlation_data = sales_summary.merge(
                    price_summary[['Genmodel', 'price_mean']], 
                    on='Genmodel', 
                    how='inner'
                ).dropna(subset=['total_sales', 'price_mean'])
                
                if not correlation_data.empty:
                    fig_scatter = px.scatter(
                        correlation_data,
                        x='price_mean',
                        y='total_sales',
                        color='Automaker',
                        size='total_sales',
                        title='',
                        template="plotly_dark",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_scatter.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=450,
                        xaxis_title="Average Price (€)",
                        yaxis_title="Total Sales"
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)
                else:
                    st.info("No correlation data available")
            else:
                st.info("No data available for correlation analysis")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📊 Price Distribution by Category")
            if not price_summary.empty:
                # Create price categories
                price_clean = price_summary.dropna(subset=['price_mean'])
                if not price_clean.empty:
                    # Define price categories
                    price_clean_copy = price_clean.copy()
                    price_clean_copy['Price Category'] = pd.cut(
                        price_clean_copy['price_mean'],
                        bins=[0, 20000, 40000, 60000, 100000, float('inf')],
                        labels=['Budget (<€20K)', 'Mid-range (€20K-€40K)', 'Premium (€40K-€60K)', 'Luxury (€60K-€100K)', 'Super Luxury (>€100K)']
                    )
                    
                    category_counts = price_clean_copy['Price Category'].value_counts()
                    
                    fig_pie = px.pie(
                        values=category_counts.values,
                        names=category_counts.index,
                        title='',
                        template="plotly_dark",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_pie.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=450
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("No price data available")
            else:
                st.info("No price data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Third Row - Box Plot and Heatmap
        col5, col6 = st.columns(2)
        
        with col5:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📦 Price Distribution by Automaker")
            if not price_summary.empty:
                price_clean = price_summary.dropna(subset=['price_mean'])
                if not price_clean.empty:
                    # Get top 10 automakers by model count
                    top_automakers = price_clean['Automaker'].value_counts().head(10).index
                    price_filtered = price_clean[price_clean['Automaker'].isin(top_automakers)]
                    
                    fig_box = px.box(
                        price_filtered,
                        x='Automaker',
                        y='price_mean',
                        title='',
                        template="plotly_dark",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_box.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=450,
                        xaxis_tickangle=-45,
                        xaxis_title="Automaker",
                        yaxis_title="Price (€)"
                    )
                    st.plotly_chart(fig_box, use_container_width=True)
                else:
                    st.info("No price data available")
            else:
                st.info("No price data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col6:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("🔥 Sales Heatmap by Year")
            if not sales_summary.empty:
                # Create a correlation matrix for sales data
                sales_numeric = sales_summary.select_dtypes(include=[np.number])
                if not sales_numeric.empty and len(sales_numeric.columns) > 1:
                    correlation_matrix = sales_numeric.corr()
                    
                    fig_heatmap = px.imshow(
                        correlation_matrix,
                        title='',
                        template="plotly_dark",
                        color_continuous_scale='RdBu',
                        aspect="auto"
                    )
                    fig_heatmap.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=450,
                        xaxis_title="Variables",
                        yaxis_title="Variables"
                    )
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                else:
                    st.info("Insufficient numeric data for heatmap")
            else:
                st.info("No sales data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Data table
        st.subheader("📋 Detailed Data")
        if not sales_summary.empty:
            st.dataframe(
                sales_summary.style.format(
                    {
                        'price_mean': "€{:,.0f}",
                        'price_min': "€{:,.0f}",
                        'price_max': "€{:,.0f}",
                        'total_sales': "{:,.0f}",
                        'avg_sales': "{:,.1f}"
                    },
                    na_rep="N/A"
                ),
                use_container_width=True
            )
        else:
            st.info("No data to display")
            
    except Exception as e:
        st.error(f"Error rendering executive summary: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
