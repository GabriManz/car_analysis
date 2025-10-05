"""
🌍 Market Dashboard Component for Car Market Analysis

Comprehensive market analysis dashboard providing detailed market insights,
competitive intelligence, and market segmentation analysis.
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
    from ..visualizations.chart_factory import chart_factory
    from ...business_logic import analyzer
except ImportError:
    # Fallback imports
    layout_component = None
    sidebar_component = None
    kpi_calculator = None
    chart_factory = None
    analyzer = None


class MarketDashboard:
    """
    🏪 Market Intelligence Dashboard
    
    Provides comprehensive market analysis including market share analysis,
    competitive positioning, market segmentation, and market trends.
    """

    def __init__(self):
        """Initialize the MarketDashboard with required components."""
        self.layout = layout_component
        self.sidebar = sidebar_component
        self.kpi_calc = kpi_calculator
        self.chart_factory = chart_factory
        self.analyzer = analyzer

    def render_market_dashboard(self) -> None:
        """Render the complete market dashboard."""
        # Setup page layout
        if self.layout:
            self.layout.setup_page_config()
            self.layout.inject_custom_css()
        
        # Create market header
        st.markdown("""
        <div class="main-header">
            <h1>🌍 Market Analysis Dashboard</h1>
            <p>Comprehensive Market Intelligence & Competitive Analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Market overview section
        self._render_market_overview()
        
        # Market share analysis
        self._render_market_share_analysis()
        
        # Competitive analysis
        self._render_competitive_analysis()
        
        # Market segmentation
        self._render_market_segmentation()
        
        # Price analysis
        self._render_price_analysis()
        
        # Market trends
        self._render_market_trends()

    def _render_market_overview(self) -> None:
        """Render market overview section."""
        st.markdown("## 📊 Market Overview")
        
        if not self.analyzer:
            st.warning("Business logic analyzer not available")
            return
        
        try:
            # Get basic market data
            basic_info = self.analyzer.get_basic_info()
            market_share = self.analyzer.calculate_market_share()
            
            # Market size metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_models = basic_info.get('basic', {}).get('shape', [0, 0])[0]
                st.metric("Total Models", f"{total_models:,}")
            
            with col2:
                total_automakers = len(self.analyzer.get_automaker_list())
                st.metric("Total Automakers", f"{total_automakers:,}")
            
            with col3:
                if not market_share.empty:
                    market_leader = market_share.iloc[0]['Automaker']
                    leader_share = market_share.iloc[0]['market_share_percent']
                    st.metric("Market Leader", f"{market_leader} ({leader_share:.1f}%)")
                else:
                    st.metric("Market Leader", "N/A")
            
            with col4:
                if not market_share.empty:
                    top_3_concentration = market_share.head(3)['market_share_percent'].sum()
                    st.metric("Top 3 Concentration", f"{top_3_concentration:.1f}%")
                else:
                    st.metric("Top 3 Concentration", "N/A")
            
            # Market concentration analysis
            st.markdown("### Market Concentration Analysis")
            
            if not market_share.empty:
                # Calculate concentration metrics
                hhi_index = (market_share['market_share_percent'] ** 2).sum()
                top_5_concentration = market_share.head(5)['market_share_percent'].sum()
                significant_players = (market_share['market_share_percent'] > 1).sum()
                
                conc_cols = st.columns(3)
                
                with conc_cols[0]:
                    st.metric("HHI Index", f"{hhi_index:.0f}")
                
                with conc_cols[1]:
                    st.metric("Top 5 Concentration", f"{top_5_concentration:.1f}%")
                
                with conc_cols[2]:
                    st.metric("Significant Players (>1%)", f"{significant_players}")
                
                # Market concentration interpretation
                if hhi_index > 2500:
                    st.warning("**Highly Concentrated Market** - Oligopoly structure")
                elif hhi_index > 1500:
                    st.info("**Moderately Concentrated Market** - Competitive structure")
                else:
                    st.success("**Fragmented Market** - High competition")
            
        except Exception as e:
            st.error(f"Error loading market overview: {str(e)}")

    def _render_market_share_analysis(self) -> None:
        """Render market share analysis section."""
        st.markdown("## 🥇 Market Share Analysis")
        
        if not self.analyzer or not self.chart_factory:
            st.warning("Required components not available")
            return
        
        try:
            # Get market share data
            market_share = self.analyzer.calculate_market_share()
            
            if market_share.empty:
                st.info("No market share data available")
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
                st.markdown("### Top 15 Automakers")
                # Create market share bar chart
                market_share_bar = self.chart_factory.create_market_share_bar_chart(
                    market_share, "Market Share by Automaker"
                )
                st.plotly_chart(market_share_bar, use_container_width=True)
            
            # Market share table
            st.markdown("### Detailed Market Share Data")
            
            # Add market share ranking
            market_share_ranked = market_share.copy()
            market_share_ranked['Rank'] = range(1, len(market_share_ranked) + 1)
            market_share_ranked['Cumulative_Share'] = market_share_ranked['market_share_percent'].cumsum()
            
            # Display top 20
            display_data = market_share_ranked.head(20)[['Rank', 'Automaker', 'market_share_percent', 'Cumulative_Share']]
            display_data.columns = ['Rank', 'Automaker', 'Market Share (%)', 'Cumulative Share (%)']
            
            st.dataframe(display_data, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading market share analysis: {str(e)}")

    def _render_competitive_analysis(self) -> None:
        """Render competitive analysis section."""
        st.markdown("## ⚔️ Competitive Analysis")
        
        if not self.analyzer:
            st.warning("Business logic analyzer not available")
            return
        
        try:
            # Get competitive data
            market_share = self.analyzer.calculate_market_share()
            sales_summary = self.analyzer.get_sales_summary()
            
            if market_share.empty or sales_summary.empty:
                st.info("Insufficient data for competitive analysis")
                return
            
            # Top competitors analysis
            st.markdown("### Top Competitors Analysis")
            
            top_competitors = market_share.head(10)
            
            comp_cols = st.columns(2)
            
            with comp_cols[0]:
                st.markdown("#### Market Share vs Sales Performance")
                
                # Merge market share with sales data
                comp_analysis = market_share.merge(
                    sales_summary.groupby('Automaker')['total_sales'].sum().reset_index(),
                    on='Automaker', how='left'
                )
                
                if not comp_analysis.empty:
                    # Create scatter plot of market share vs total sales
                    fig = self.chart_factory.chart_factory.create_price_vs_sales_scatter(
                        comp_analysis.rename(columns={'market_share_percent': 'price_mean', 'total_sales': 'total_sales'}),
                        "Market Share vs Sales Performance"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with comp_cols[1]:
                st.markdown("#### Competitive Positioning Matrix")
                
                # Create competitive positioning analysis
                comp_data = []
                for _, row in top_competitors.iterrows():
                    automaker = row['Automaker']
                    market_share_pct = row['market_share_percent']
                    
                    # Get average sales for this automaker
                    automaker_sales = sales_summary[sales_summary['Automaker'] == automaker]
                    avg_sales = automaker_sales['total_sales'].mean() if not automaker_sales.empty else 0
                    
                    comp_data.append({
                        'Automaker': automaker,
                        'Market_Share': market_share_pct,
                        'Avg_Sales': avg_sales,
                        'Position': self._determine_competitive_position(market_share_pct, avg_sales)
                    })
                
                comp_df = pd.DataFrame(comp_data)
                
                # Display competitive positioning
                for _, row in comp_df.iterrows():
                    position = row['Position']
                    if position == 'Leader':
                        st.success(f"**{row['Automaker']}**: Market Leader")
                    elif position == 'Challenger':
                        st.warning(f"**{row['Automaker']}**: Challenger")
                    elif position == 'Follower':
                        st.info(f"**{row['Automaker']}**: Market Follower")
                    else:
                        st.error(f"**{row['Automaker']}**: Niche Player")
            
            # Competitive insights
            st.markdown("### 🎯 Competitive Insights")
            
            # Market leader analysis
            market_leader = market_share.iloc[0]
            leader_share = market_leader['market_share_percent']
            
            insights = []
            
            if leader_share > 20:
                insights.append(f"**Dominant Market Leader:** {market_leader['Automaker']} controls {leader_share:.1f}% of the market")
            elif leader_share > 15:
                insights.append(f"**Strong Market Leader:** {market_leader['Automaker']} leads with {leader_share:.1f}% market share")
            else:
                insights.append(f"**Fragmented Leadership:** {market_leader['Automaker']} leads with only {leader_share:.1f}% market share")
            
            # Gap analysis
            if len(market_share) > 1:
                second_place = market_share.iloc[1]['market_share_percent']
                gap = leader_share - second_place
                if gap > 10:
                    insights.append(f"**Significant Gap:** {gap:.1f}% difference between #1 and #2")
                elif gap > 5:
                    insights.append(f"**Moderate Gap:** {gap:.1f}% difference between #1 and #2")
                else:
                    insights.append(f"**Close Competition:** Only {gap:.1f}% difference between #1 and #2")
            
            # Display insights
            for insight in insights:
                st.info(insight)
            
        except Exception as e:
            st.error(f"Error loading competitive analysis: {str(e)}")

    def _render_market_segmentation(self) -> None:
        """Render market segmentation section."""
        st.markdown("## 🎯 Market Segmentation")
        
        if not self.analyzer or not self.chart_factory:
            st.warning("Required components not available")
            return
        
        try:
            # Get segmentation data
            price_data = self.analyzer.get_price_range_by_model()
            
            if price_data.empty:
                st.info("No price data available for segmentation")
                return
            
            # Price segmentation
            st.markdown("### Price-Based Segmentation")
            
            # Define price segments
            price_segments = {
                'Budget': (0, 20000),
                'Mid-Range': (20000, 50000),
                'Premium': (50000, 100000),
                'Luxury': (100000, float('inf'))
            }
            
            # Segment analysis
            segment_data = []
            for segment_name, (min_price, max_price) in price_segments.items():
                segment_models = price_data[
                    (price_data['price_mean'] >= min_price) & 
                    (price_data['price_mean'] < max_price)
                ]
                
                segment_data.append({
                    'Segment': segment_name,
                    'Models': len(segment_models),
                    'Avg_Price': segment_models['price_mean'].mean() if not segment_models.empty else 0,
                    'Price_Range': f"€{min_price:,.0f} - €{max_price:,.0f}" if max_price != float('inf') else f"€{min_price:,.0f}+"
                })
            
            segment_df = pd.DataFrame(segment_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Segment Distribution")
                # Create segment distribution chart
                fig = go.Figure(data=[
                    go.Bar(
                        x=segment_df['Segment'],
                        y=segment_df['Models'],
                        text=segment_df['Models'],
                        textposition='auto',
                        marker_color=['#28a745', '#ffc107', '#fd7e14', '#dc3545']
                    )
                ])
                
                fig.update_layout(
                    title="Models by Price Segment",
                    xaxis_title="Price Segment",
                    yaxis_title="Number of Models",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### Segment Details")
                st.dataframe(segment_df, use_container_width=True)
            
            # Brand segmentation by price
            st.markdown("### Brand Positioning by Price Segment")
            
            # Analyze automaker positioning
            brand_segments = []
            for automaker in price_data['Automaker'].unique():
                automaker_data = price_data[price_data['Automaker'] == automaker]
                avg_price = automaker_data['price_mean'].mean()
                
                # Determine segment
                for segment_name, (min_price, max_price) in price_segments.items():
                    if min_price <= avg_price < max_price:
                        brand_segments.append({
                            'Automaker': automaker,
                            'Segment': segment_name,
                            'Avg_Price': avg_price,
                            'Models': len(automaker_data)
                        })
                        break
            
            brand_segment_df = pd.DataFrame(brand_segments)
            
            if not brand_segment_df.empty:
                # Create brand positioning chart
                fig = go.Figure()
                
                for segment in brand_segment_df['Segment'].unique():
                    segment_data = brand_segment_df[brand_segment_df['Segment'] == segment]
                    fig.add_trace(go.Bar(
                        name=segment,
                        x=segment_data['Automaker'],
                        y=segment_data['Avg_Price'],
                        text=[f"€{price:,.0f}" for price in segment_data['Avg_Price']],
                        textposition='auto'
                    ))
                
                fig.update_layout(
                    title="Brand Positioning by Price Segment",
                    xaxis_title="Automaker",
                    yaxis_title="Average Price (€)",
                    barmode='group',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading market segmentation: {str(e)}")

    def _render_price_analysis(self) -> None:
        """Render price analysis section."""
        st.markdown("## 💰 Price Analysis")
        
        if not self.analyzer or not self.chart_factory:
            st.warning("Required components not available")
            return
        
        try:
            # Get price data
            price_data = self.analyzer.get_price_range_by_model()
            
            if price_data.empty:
                st.info("No price data available")
                return
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Price Distribution")
                # Create price distribution chart
                price_dist_chart = self.chart_factory.create_price_distribution_chart(
                    price_data, "Price Distribution Analysis"
                )
                st.plotly_chart(price_dist_chart, use_container_width=True)
            
            with col2:
                st.markdown("### Price by Automaker")
                # Create price by automaker chart
                price_bar_chart = self.chart_factory.create_price_bar_chart(
                    price_data, "Average Price by Automaker"
                )
                st.plotly_chart(price_bar_chart, use_container_width=True)
            
            # Price statistics
            st.markdown("### Price Statistics")
            
            price_stats_cols = st.columns(4)
            
            with price_stats_cols[0]:
                avg_price = price_data['price_mean'].mean()
                st.metric("Average Price", f"€{avg_price:,.0f}")
            
            with price_stats_cols[1]:
                median_price = price_data['price_mean'].median()
                st.metric("Median Price", f"€{median_price:,.0f}")
            
            with price_stats_cols[2]:
                min_price = price_data['price_mean'].min()
                st.metric("Minimum Price", f"€{min_price:,.0f}")
            
            with price_stats_cols[3]:
                max_price = price_data['price_mean'].max()
                st.metric("Maximum Price", f"€{max_price:,.0f}")
            
            # Price volatility analysis
            st.markdown("### Price Volatility Analysis")
            
            # Calculate price volatility by automaker
            volatility_data = price_data.groupby('Automaker').agg({
                'price_mean': ['mean', 'std', 'count']
            }).round(2)
            
            volatility_data.columns = ['Avg_Price', 'Price_Std', 'Model_Count']
            volatility_data['Price_CV'] = volatility_data['Price_Std'] / volatility_data['Avg_Price']
            volatility_data = volatility_data.sort_values('Price_CV', ascending=False).head(10)
            
            st.dataframe(volatility_data, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading price analysis: {str(e)}")

    def _render_market_trends(self) -> None:
        """Render market trends section."""
        st.markdown("## 📈 Market Trends")
        
        if not self.analyzer or not self.chart_factory:
            st.warning("Required components not available")
            return
        
        try:
            # Get sales data for trend analysis
            sales_data = self.analyzer.get_sales_summary()
            
            if sales_data.empty:
                st.info("No sales data available for trend analysis")
                return
            
            # Sales trend analysis
            st.markdown("### Sales Trend Analysis")
            
            # Get yearly sales data
            year_columns = [col for col in sales_data.columns if col.isdigit()]
            if year_columns:
                yearly_sales = sales_data[year_columns].sum().sort_index()
                
                # Create sales trend chart
                trend_chart = self.chart_factory.create_sales_trend_chart(
                    sales_data, "Market Sales Trend (2001-2020)"
                )
                st.plotly_chart(trend_chart, use_container_width=True)
                
                # Trend analysis
                st.markdown("### Trend Analysis")
                
                trend_cols = st.columns(3)
                
                with trend_cols[0]:
                    # Calculate year-over-year growth
                    if len(yearly_sales) >= 2:
                        latest_year = yearly_sales.iloc[-1]
                        previous_year = yearly_sales.iloc[-2]
                        yoy_growth = (latest_year - previous_year) / previous_year * 100
                        st.metric("YoY Growth", f"{yoy_growth:+.1f}%")
                    else:
                        st.metric("YoY Growth", "N/A")
                
                with trend_cols[1]:
                    # Calculate 5-year CAGR
                    if len(yearly_sales) >= 5:
                        first_year = yearly_sales.iloc[-5]
                        last_year = yearly_sales.iloc[-1]
                        cagr = ((last_year / first_year) ** (1/5) - 1) * 100
                        st.metric("5-Year CAGR", f"{cagr:+.1f}%")
                    else:
                        st.metric("5-Year CAGR", "N/A")
                
                with trend_cols[2]:
                    # Peak year analysis
                    peak_year = yearly_sales.idxmax()
                    peak_sales = yearly_sales.max()
                    st.metric("Peak Year", f"{peak_year} ({peak_sales:,.0f})")
            
        except Exception as e:
            st.error(f"Error loading market trends: {str(e)}")

    def _determine_competitive_position(self, market_share: float, avg_sales: float) -> str:
        """Determine competitive position based on market share and sales."""
        if market_share > 15 and avg_sales > 100000:
            return 'Leader'
        elif market_share > 10 or avg_sales > 50000:
            return 'Challenger'
        elif market_share > 5 or avg_sales > 20000:
            return 'Follower'
        else:
            return 'Niche'

    def get_dashboard_config(self) -> Dict[str, Any]:
        """Get dashboard configuration."""
        return {
            'dashboard_type': 'market',
            'components_available': {
                'layout': self.layout is not None,
                'sidebar': self.sidebar is not None,
                'kpi_calculator': self.kpi_calc is not None,
                'chart_factory': self.chart_factory is not None,
                'analyzer': self.analyzer is not None
            },
            'sections': [
                'market_overview',
                'market_share_analysis',
                'competitive_analysis',
                'market_segmentation',
                'price_analysis',
                'market_trends'
            ]
        }


# Global instance for use throughout the application
market_dashboard = MarketDashboard()

