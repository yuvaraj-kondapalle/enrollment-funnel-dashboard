import streamlit as st
import plotly.express as px
import pandas as pd
from data.enrollment_data import generate_enrollment_data

# Page config
st.set_page_config(page_title="Enrollment Funnel Dashboard", layout="wide")

# Load data
df = generate_enrollment_data()

# Title
st.title("UMass Boston — Enrollment Funnel Dashboard")
st.markdown("Interactive dashboard tracking student progression from Inquiry to Enrollment.")

# Sidebar filters
st.sidebar.header("Filters")
year = st.sidebar.multiselect("Year", options=sorted(df['year'].unique()), default=sorted(df['year'].unique()))
program = st.sidebar.multiselect("Program", options=df['program'].unique(), default=df['program'].unique())
demographics = st.sidebar.multiselect("Demographics", options=df['demographics'].unique(), default=df['demographics'].unique())

# Filter data
filtered_df = df[
    (df['year'].isin(year)) &
    (df['program'].isin(program)) &
    (df['demographics'].isin(demographics))
]

# Row 1 - KPI metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Inquiries", len(filtered_df[filtered_df['stage'] == 'Inquiry']))
col2.metric("Applications", len(filtered_df[filtered_df['stage'] == 'Application']))
col3.metric("Admitted", len(filtered_df[filtered_df['stage'] == 'Admitted']))
col4.metric("Enrolled", len(filtered_df[filtered_df['stage'] == 'Enrolled']))

st.divider()

# Row 2 - Funnel chart and Program breakdown
col5, col6 = st.columns(2)

with col5:
    st.subheader("Enrollment Funnel")
    stage_order = ['Inquiry', 'Application', 'Admitted', 'Deposited', 'Enrolled']
    funnel_df = filtered_df['stage'].value_counts().reindex(stage_order).reset_index()
    funnel_df.columns = ['stage', 'count']
    fig1 = px.funnel(funnel_df, x='count', y='stage')
    st.plotly_chart(fig1, use_container_width=True)

with col6:
    st.subheader("Applications by Program")
    program_df = filtered_df.groupby('program').size().reset_index(name='count')
    fig2 = px.bar(program_df, x='program', y='count', color='program')
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Row 3 - Demographics and Financial Aid
col7, col8 = st.columns(2)

with col7:
    st.subheader("Domestic vs International")
    demo_df = filtered_df.groupby('demographics').size().reset_index(name='count')
    fig3 = px.pie(demo_df, names='demographics', values='count')
    st.plotly_chart(fig3, use_container_width=True)

with col8:
    st.subheader("Financial Aid Distribution")
    aid_df = filtered_df.groupby('financial_aid').size().reset_index(name='count')
    fig4 = px.pie(aid_df, names='financial_aid', values='count')
    st.plotly_chart(fig4, use_container_width=True)