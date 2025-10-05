"""
🏢 Executive Dashboard Component for Car Market Analysis

Executive-grade dashboard providing high-level strategic insights and KPIs
for automotive market analysis with C-level decision support.
"""

import streamlit as st
import pandas as pd
import numpy as np
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

