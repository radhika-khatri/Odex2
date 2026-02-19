import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="ODeX Data Analytics Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple, clean CSS
st.markdown("""
    <style>
    .main {
        background-color: #1a1a1a;
    }
    h1 {
        color: #ffffff;
        font-weight: 600;
    }
    h2 {
        color: #e0e0e0;
        font-weight: 500;
        margin-top: 30px;
    }
    h3 {
        color: #cccccc;
    }
    p {
        color: #b0b0b0;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff;
    }
    [data-testid="stMetricLabel"] {
        color: #b0b0b0;
    }
    div[data-testid="metric-container"] {
        background-color: #2d2d2d;
        border: 1px solid #404040;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# DATA LOADING
@st.cache_data
def load_data():
    file_path = "ODeX_Data_Analytics_Case_Dummy_Dataset.xlsx"
    cust_master = pd.read_excel(file_path, sheet_name='Customer Master')
    trans_data = pd.read_excel(file_path, sheet_name='Transaction Data')
    support_data = pd.read_excel(file_path, sheet_name='Support Data')
    pricing_plans = pd.read_excel(file_path, sheet_name='Pricing Plans')
    
    trans_data['Month'] = pd.to_datetime(trans_data['Month'])
    return cust_master, trans_data, support_data, pricing_plans

try:
    cust_master, trans_data, support_data, pricing_plans = load_data()
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# Sidebar Navigation
st.sidebar.title("ODeX Analytics")
st.sidebar.markdown("---")

section = st.sidebar.radio(
    "Navigation",
    ["Overview", "Revenue Analysis", "Pricing & Discounts", "Product Adoption", "Behavioral Insights"]
)

st.sidebar.markdown("---")

# Quick Stats
total_rev = trans_data['Total Revenue'].sum()
total_cust = cust_master['Customer ID'].nunique()
st.sidebar.subheader("Quick Stats")
st.sidebar.write(f"**Revenue:** ${total_rev:,.0f}")
st.sidebar.write(f"**Customers:** {total_cust}")

# Global Calculations
cust_stats = trans_data.groupby('Customer ID').agg({
    'No. of Transactions': 'sum', 
    'Total Revenue': 'sum'
}).reset_index()
cust_stats['Yield'] = cust_stats['Total Revenue'] / cust_stats['No. of Transactions']

# ============================================================
# SECTION 1: OVERVIEW
# ============================================================
if section == "Overview":
    st.title("Dashboard Overview")
    st.write("Welcome to the ODeX Data Analytics Dashboard")
    
    st.markdown("---")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Customers", f"{total_cust:,}")
    
    # Active/Dormant calculation
    last_date = trans_data['Month'].max()
    active_cutoff = last_date - pd.DateOffset(months=2)
    active_count = len(trans_data[trans_data['Month'] >= active_cutoff]['Customer ID'].unique())
    
    with col2:
        st.metric("Active Customers", f"{active_count:,}")
    
    with col3:
        st.metric("Dormant Customers", f"{total_cust - active_count:,}")
    
    with col4:
        total_transactions = trans_data['No. of Transactions'].sum()
        st.metric("Total Transactions", f"{total_transactions:,}")
    
    st.markdown("---")
    
    # Customer Distribution
    st.subheader("Customer Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        country_data = cust_master['Country'].value_counts().reset_index()
        country_data.columns = ['Country', 'Count']
        fig_country = px.bar(
            country_data, 
            x='Count', 
            y='Country', 
            orientation='h',
            title="Customer Base by Country"
        )
        fig_country.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_country, use_container_width=True)
    
    with col2:
        fig_type = px.pie(
            cust_master, 
            names='Customer Type',
            title="Customer Mix by Type"
        )
        fig_type.update_layout(height=400)
        st.plotly_chart(fig_type, use_container_width=True)
    
    # Monthly Trend
    st.subheader("Transaction Trends")
    monthly_trend = trans_data.groupby('Month')['No. of Transactions'].sum().reset_index()
    fig_trend = px.line(
        monthly_trend, 
        x='Month', 
        y='No. of Transactions',
        title="Monthly Transaction Volume",
        markers=True
    )
    fig_trend.update_layout(height=400)
    st.plotly_chart(fig_trend, use_container_width=True)

# ============================================================
# SECTION 2: REVENUE ANALYSIS
# ============================================================
elif section == "Revenue Analysis":
    st.title("Revenue Analysis")
    
    st.markdown("---")
    
    # Revenue Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Revenue", f"${total_rev:,.2f}")
    
    with col2:
        avg_revenue = total_rev / total_cust
        st.metric("Average Revenue per Customer", f"${avg_revenue:,.2f}")
    
    with col3:
        avg_transaction = total_rev / trans_data['No. of Transactions'].sum()
        st.metric("Average Transaction Value", f"${avg_transaction:,.2f}")
    
    st.markdown("---")
    
    # Top Customers
    st.subheader("Top 10 Customers by Revenue")
    
    top_10 = cust_stats.sort_values('Total Revenue', ascending=False).head(10)
    top_10_share = (top_10['Total Revenue'].sum() / total_rev) * 100
    
    st.info(f"Top 10 customers contribute **{top_10_share:.1f}%** of total revenue")
    
    fig_top = px.bar(
        top_10, 
        x='Total Revenue', 
        y='Customer ID',
        orientation='h',
        title="Top 10 Revenue Contributors"
    )
    fig_top.update_layout(showlegend=False, height=500)
    st.plotly_chart(fig_top, use_container_width=True)
    
    # Revenue by Module
    st.subheader("Revenue by Module")
    
    module_rev = trans_data.groupby('Module Used')['Total Revenue'].sum().sort_values(ascending=False).reset_index()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_mod = px.bar(
            module_rev, 
            x='Module Used', 
            y='Total Revenue',
            title="Module Revenue Distribution"
        )
        fig_mod.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_mod, use_container_width=True)
    
    with col2:
        st.write("**Top Modules:**")
        for idx, row in module_rev.head(5).iterrows():
            percentage = (row['Total Revenue'] / total_rev) * 100
            st.write(f"{row['Module Used']}: ${row['Total Revenue']:,.0f} ({percentage:.1f}%)")
    
    # Yield Analysis
    st.subheader("Customer Yield Analysis")
    
    fig_yield = px.scatter(
        cust_stats, 
        x='No. of Transactions', 
        y='Yield',
        size='Total Revenue',
        hover_name='Customer ID',
        title="Transaction Volume vs Yield per Transaction"
    )
    fig_yield.update_layout(height=500)
    st.plotly_chart(fig_yield, use_container_width=True)

# ============================================================
# SECTION 3: PRICING & DISCOUNTS
# ============================================================
elif section == "Pricing & Discounts":
    st.title("Pricing & Discount Analysis")
    
    st.markdown("---")
    
    # Pricing Metrics
    avg_standard = pricing_plans['Standard Price'].mean()
    avg_contracted = pricing_plans['Contracted Price'].mean()
    avg_gap = avg_standard - avg_contracted
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average Standard Price", f"${avg_standard:.2f}")
    
    with col2:
        st.metric("Average Contracted Price", f"${avg_contracted:.2f}")
    
    with col3:
        st.metric("Average Price Gap", f"${avg_gap:.2f}")
    
    st.markdown("---")
    
    # Revenue Leakage
    pricing_merged = pricing_plans.merge(cust_stats, on='Customer ID')
    rev_lost = ((pricing_merged['Standard Price'] - pricing_merged['Contracted Price']) * 
                pricing_merged['No. of Transactions']).sum()
    
    st.error(f"**Estimated Annual Revenue Leakage: ${rev_lost:,.2f}**")
    
    st.markdown("---")
    
    # Discount Distribution
    st.subheader("Discount Distribution")
    
    # Create discount ranges
    pricing_plans['Discount Range'] = pd.cut(
        pricing_plans['Discount %'],
        bins=[0, 10, 20, 30, 40, 100],
        labels=['0-10%', '10-20%', '20-30%', '30-40%', '40%+']
    )
    discount_counts = pricing_plans['Discount Range'].value_counts().sort_index().reset_index()
    discount_counts.columns = ['Range', 'Count']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_disc_bar = px.bar(
            discount_counts,
            x='Range',
            y='Count',
            title="Customers by Discount Range"
        )
        fig_disc_bar.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_disc_bar, use_container_width=True)
    
    with col2:
        fig_disc_pie = px.pie(
            discount_counts,
            values='Count',
            names='Range',
            title="Discount Range Distribution"
        )
        fig_disc_pie.update_layout(height=400)
        st.plotly_chart(fig_disc_pie, use_container_width=True)
    
    # Correlation Analysis
    st.subheader("Discount vs Transaction Volume")
    
    correlation = pricing_merged['Discount %'].corr(pricing_merged['No. of Transactions'])
    
    fig_corr = px.scatter(
        pricing_merged,
        x='Discount %',
        y='No. of Transactions',
        trendline="ols",
        title=f"Discount Impact (Correlation: {correlation:.3f})"
    )
    fig_corr.update_layout(height=500)
    st.plotly_chart(fig_corr, use_container_width=True)
    
    if abs(correlation) > 0.3:
        st.info(f"Correlation coefficient: {correlation:.3f}")

# ============================================================
# SECTION 4: PRODUCT ADOPTION
# ============================================================
elif section == "Product Adoption":
    st.title("Product Adoption Analysis")
    
    st.markdown("---")
    
    # Adoption Metrics
    adoption = (trans_data.groupby('Module Used')['Customer ID'].nunique() / total_cust * 100).reset_index()
    adoption.columns = ['Module', 'Adoption %']
    adoption = adoption.sort_values('Adoption %', ascending=False)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        top_module = adoption.iloc[0]
        st.metric("Top Module", top_module['Module'])
        st.write(f"Adoption: {top_module['Adoption %']:.1f}%")
    
    with col2:
        total_modules = len(adoption)
        st.metric("Total Modules", total_modules)
    
    with col3:
        avg_adoption = adoption['Adoption %'].mean()
        st.metric("Average Adoption Rate", f"{avg_adoption:.1f}%")
    
    st.markdown("---")
    
    # Adoption Chart
    st.subheader("Module Adoption Rates")
    
    fig_adopt = px.bar(
        adoption,
        x='Module',
        y='Adoption %',
        title="Customer Adoption by Module"
    )
    fig_adopt.update_layout(showlegend=False, height=450)
    st.plotly_chart(fig_adopt, use_container_width=True)
    
    # Usage vs Revenue
    st.subheader("Usage vs Revenue Comparison")
    
    usage_rev = trans_data.groupby('Module Used').agg({
        'No. of Transactions': 'sum',
        'Total Revenue': 'sum'
    }).reset_index()
    
    fig_comp = go.Figure()
    
    fig_comp.add_trace(go.Bar(
        x=usage_rev['Module Used'],
        y=usage_rev['No. of Transactions'],
        name='Transactions'
    ))
    
    fig_comp.add_trace(go.Bar(
        x=usage_rev['Module Used'],
        y=usage_rev['Total Revenue'],
        name='Revenue',
        yaxis='y2'
    ))
    
    fig_comp.update_layout(
        title="Transaction Volume vs Revenue by Module",
        yaxis=dict(title='Transactions'),
        yaxis2=dict(title='Revenue', overlaying='y', side='right'),
        barmode='group',
        height=500
    )
    
    st.plotly_chart(fig_comp, use_container_width=True)

# ============================================================
# SECTION 5: BEHAVIORAL INSIGHTS
# ============================================================
elif section == "Behavioral Insights":
    st.title("Customer Behavior Insights")
    
    st.markdown("---")
    
    behavior = support_data.merge(cust_stats, on='Customer ID')
    
    # Support Metrics
    total_tickets = support_data['No. of Support Tickets'].sum()
    total_failures = support_data['Failed Transactions'].sum()
    avg_resolution = support_data['Avg Resolution Time (hrs)'].mean()
    payment_failures = support_data['Payment Failures'].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Support Tickets", f"{total_tickets:,}")
    
    with col2:
        st.metric("Failed Transactions", f"{total_failures:,}")
    
    with col3:
        st.metric("Avg Resolution Time", f"{avg_resolution:.1f} hrs")
    
    with col4:
        st.metric("Payment Failures", f"{payment_failures:,}")
    
    st.markdown("---")
    
    # Top Support Customers
    st.subheader("Q1: Customers with Highest Support Tickets")
    
    top_support = support_data.sort_values('No. of Support Tickets', ascending=False).head(10)
    
    fig_q1 = px.bar(
        top_support,
        x='Customer ID',
        y='No. of Support Tickets',
        title="Top 10 Customers by Support Tickets"
    )
    fig_q1.update_layout(showlegend=False, height=450)
    st.plotly_chart(fig_q1, use_container_width=True)
    
    # Correlations
    st.subheader("Q2 & Q3: Support Tickets and Failed Transactions Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        corr_support = behavior['No. of Support Tickets'].corr(behavior['No. of Transactions'])
        
        fig_q2 = px.scatter(
            behavior,
            x='No. of Support Tickets',
            y='No. of Transactions',
            trendline="ols",
            title=f"Support Tickets vs Transactions (Corr: {corr_support:.3f})"
        )
        fig_q2.update_layout(height=450)
        st.plotly_chart(fig_q2, use_container_width=True)
    
    with col2:
        corr_failed = behavior['Failed Transactions'].corr(behavior['No. of Transactions'])
        
        fig_q3 = px.scatter(
            behavior,
            x='Failed Transactions',
            y='No. of Transactions',
            trendline="ols",
            title=f"Failed Transactions vs Total Usage (Corr: {corr_failed:.3f})"
        )
        fig_q3.update_layout(height=450)
        st.plotly_chart(fig_q3, use_container_width=True)
    
    # Payment Failure Impact
    st.subheader("Q4: Payment Failure Revenue Impact")
    
    behavior['Payment Loss'] = behavior['Yield'] * behavior['Payment Failures']
    total_loss = behavior['Payment Loss'].sum()
    
    st.error(f"**Total Estimated Revenue Loss: ${total_loss:,.2f}**")
    
    # Top customers by payment loss - simple bar graph
    top_losers = behavior.nlargest(15, 'Payment Loss')[['Customer ID', 'Payment Loss', 'Payment Failures']]
    
    fig_q4 = px.bar(
        top_losers,
        x='Customer ID',
        y='Payment Loss',
        title="Top 15 Customers by Payment Loss",
        hover_data=['Payment Failures']
    )
    fig_q4.update_layout(showlegend=False, height=500)
    st.plotly_chart(fig_q4, use_container_width=True)
    
    # Show detailed table
    st.write("**Detailed Breakdown:**")
    st.dataframe(top_losers, hide_index=True, use_container_width=True)
    
    # Resolution Time Impact
    st.subheader("Q5: Resolution Time vs Customer Usage")
    
    corr_resolution = behavior['Avg Resolution Time (hrs)'].corr(behavior['No. of Transactions'])
    
    fig_q5 = px.scatter(
        behavior,
        x='Avg Resolution Time (hrs)',
        y='No. of Transactions',
        trendline="ols",
        title=f"Resolution Time Impact (Correlation: {corr_resolution:.3f})"
    )
    fig_q5.update_layout(height=500)
    st.plotly_chart(fig_q5, use_container_width=True)

# Footer
st.markdown("---")
st.caption("ODeX Data Analytics Dashboard © 2024")