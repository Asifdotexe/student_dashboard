import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e3a8a;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f1f5f9;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1e3a8a;
    }
    .metric-label {
        font-size: 1rem;
        color: #4b5563;
    }
    .trend-up {
        color: #10b981;
    }
    .trend-down {
        color: #ef4444;
    }
    .trend-neutral {
        color: #f59e0b;
    }
</style>
""", unsafe_allow_html=True)

# Load the data
@st.cache_data
def load_data():
    df = pd.read_excel(r"02062025-delhi-aiims-bsc-nursing-prepatory-data-set.xlsx")
    df = df[['date', 'subject', 'no_of_questions', 'correct', 
            'incorrect', 'unattempted', 'marks', 'total', 
            'percentage', '30_mark_scale', 'accuracy_rate',
            'attempt_rate', 'penalty_rate']]
    df = df.dropna()
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    
    return df

df = load_data()

# Header
st.markdown("<h1 class='main-header'>Student Performance Dashboard</h1>", unsafe_allow_html=True)

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['date'].min().date(), df['date'].max().date()),
    min_value=df['date'].min().date(),
    max_value=df['date'].max().date()
)

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]
else:
    filtered_df = df

# Subject filter
subjects = ["All"] + list(df['subject'].unique())
selected_subject = st.sidebar.selectbox("Select Subject", subjects)

if selected_subject != "All":
    filtered_df = filtered_df[filtered_df['subject'] == selected_subject]

# Dashboard metrics section
st.markdown("<h2 class='sub-header'>Overall Performance</h2>", unsafe_allow_html=True)

# Calculate overall metrics
avg_percentage = filtered_df['percentage'].mean()
avg_accuracy = filtered_df['accuracy_rate'].mean() * 100
avg_attempt_rate = filtered_df['attempt_rate'].mean() * 100
avg_penalty_rate = filtered_df['penalty_rate'].mean() * 100

# Define performance tiers
def get_performance_tier(percentage):
    if percentage >= 90:
        return "Excellent", "#10b981"  # Green
    elif percentage >= 75:
        return "Good", "#059669"  # Green-blue
    elif percentage >= 60:
        return "Satisfactory", "#f59e0b"  # Yellow
    else:
        return "Needs Improvement", "#ef4444"  # Red

performance_tier, tier_color = get_performance_tier(avg_percentage)

# Calculate trends (comparing with the first half of the date range)
mid_date = filtered_df['date'].min() + (filtered_df['date'].max() - filtered_df['date'].min()) / 2
first_half = filtered_df[filtered_df['date'] < mid_date]
second_half = filtered_df[filtered_df['date'] >= mid_date]

if not first_half.empty and not second_half.empty:
    percentage_trend = second_half['percentage'].mean() - first_half['percentage'].mean()
    accuracy_trend = second_half['accuracy_rate'].mean() - first_half['accuracy_rate'].mean()
    attempt_trend = second_half['attempt_rate'].mean() - first_half['attempt_rate'].mean()
else:
    percentage_trend = accuracy_trend = attempt_trend = 0

# Define the metric columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-value'>{avg_percentage:.2f}%</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-label'>Average Percentage</div>", unsafe_allow_html=True)
    if percentage_trend > 2:
        st.markdown(f"<div class='trend-up'>↑ {percentage_trend:.2f}%</div>", unsafe_allow_html=True)
    elif percentage_trend < -2:
        st.markdown(f"<div class='trend-down'>↓ {abs(percentage_trend):.2f}%</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='trend-neutral'>→ Stable</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-value'>{avg_accuracy:.2f}%</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-label'>Accuracy Rate</div>", unsafe_allow_html=True)
    if accuracy_trend > 0.05:
        st.markdown(f"<div class='trend-up'>↑ {accuracy_trend*100:.2f}%</div>", unsafe_allow_html=True)
    elif accuracy_trend < -0.05:
        st.markdown(f"<div class='trend-down'>↓ {abs(accuracy_trend*100):.2f}%</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='trend-neutral'>→ Stable</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-value'>{avg_attempt_rate:.2f}%</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-label'>Attempt Rate</div>", unsafe_allow_html=True)
    if attempt_trend > 0.05:
        st.markdown(f"<div class='trend-up'>↑ {attempt_trend*100:.2f}%</div>", unsafe_allow_html=True)
    elif attempt_trend < -0.05:
        st.markdown(f"<div class='trend-down'>↓ {abs(attempt_trend*100):.2f}%</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='trend-neutral'>→ Stable</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-value' style='color:{tier_color}'>{performance_tier}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-label'>Performance Tier</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Visualization section
st.markdown("<h2 class='sub-header'>Performance Trends</h2>", unsafe_allow_html=True)

# Prepare data for subject-wise comparison
subject_comparison = filtered_df.groupby(['subject', 'date']).agg({
    'percentage': 'mean',
    '30_mark_scale': 'mean'
}).reset_index()

# Line chart for percentage trends over time
fig1 = px.line(
    subject_comparison, 
    x='date', 
    y='percentage', 
    color='subject',
    markers=True,
    labels={'percentage': 'Percentage (%)', 'date': 'Date', 'subject': 'Subject'},
    title='Performance Trend Over Time',
    color_discrete_map={'Physics': '#3b82f6', 'Chemistry': '#10b981', 'Biology': '#f59e0b'}
)
fig1.update_layout(
    height=400,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis_title="Date",
    yaxis_title="Percentage (%)",
    hovermode="x unified"
)
st.plotly_chart(fig1, use_container_width=True)

# Create two columns for the next charts
col1, col2 = st.columns(2)

# Subject-wise comparison barplot
with col1:
    subject_avg = filtered_df.groupby('subject').agg({
        'percentage': 'mean',
        'accuracy_rate': 'mean',
        'attempt_rate': 'mean',
        'penalty_rate': 'mean'
    }).reset_index()
    
    fig2 = px.bar(
        subject_avg, 
        x='subject', 
        y='percentage',
        color='subject',
        labels={'percentage': 'Average Percentage (%)', 'subject': 'Subject'},
        title='Subject-wise Performance Comparison',
        color_discrete_map={'Physics': '#3b82f6', 'Chemistry': '#10b981', 'Biology': '#f59e0b'}
    )
    fig2.update_layout(
        height=400,
        xaxis_title="Subject",
        yaxis_title="Average Percentage (%)"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Heatmap for metrics by subject
with col2:
    metrics_heatmap = pd.pivot_table(
        subject_avg,
        values=['accuracy_rate', 'attempt_rate', 'penalty_rate'],
        index='subject'
    ).reset_index()
    
    metrics_heatmap = metrics_heatmap.rename(columns={
        'accuracy_rate': 'Accuracy',
        'attempt_rate': 'Attempt Rate',
        'penalty_rate': 'Penalty Rate'
    })
    
    metrics_heatmap_long = pd.melt(
        metrics_heatmap,
        id_vars=['subject'],
        value_vars=['Accuracy', 'Attempt Rate', 'Penalty Rate'],
        var_name='Metric',
        value_name='Rate'
    )
    
    fig3 = px.density_heatmap(
        metrics_heatmap_long,
        x='Metric',
        y='subject',
        z='Rate',
        color_continuous_scale='RdYlGn_r' if 'Penalty Rate' in metrics_heatmap_long['Metric'].unique() else 'RdYlGn',
        labels={'Rate': 'Value (0-1)', 'subject': 'Subject', 'Metric': 'Metric'},
        title='Key Performance Metrics by Subject'
    )
    fig3.update_layout(
        height=400,
        xaxis_title="Metric",
        yaxis_title="Subject"
    )
    st.plotly_chart(fig3, use_container_width=True)

# Question analysis section
st.markdown("<h2 class='sub-header'>Question Analysis</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# Question attempt distribution
with col1:
    question_dist = filtered_df.groupby('subject').agg({
        'correct': 'sum',
        'incorrect': 'sum',
        'unattempted': 'sum'
    }).reset_index()
    
    question_dist_long = pd.melt(
        question_dist,
        id_vars=['subject'],
        value_vars=['correct', 'incorrect', 'unattempted'],
        var_name='Status',
        value_name='Count'
    )
    
    fig4 = px.bar(
        question_dist_long,
        x='subject',
        y='Count',
        color='Status',
        barmode='stack',
        labels={'Count': 'Number of Questions', 'subject': 'Subject', 'Status': 'Question Status'},
        title='Question Attempt Distribution by Subject',
        color_discrete_map={'correct': '#10b981', 'incorrect': '#ef4444', 'unattempted': '#d1d5db'}
    )
    fig4.update_layout(
        height=400,
        xaxis_title="Subject",
        yaxis_title="Number of Questions"
    )
    st.plotly_chart(fig4, use_container_width=True)

# Performance gauge chart
with col2:
    overall_perf = filtered_df['percentage'].mean()
    
    fig5 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=overall_perf,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Performance", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': tier_color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#fee2e2'},
                {'range': [40, 60], 'color': '#fef3c7'},
                {'range': [60, 75], 'color': '#d1fae5'},
                {'range': [75, 90], 'color': '#a7f3d0'},
                {'range': [90, 100], 'color': '#6ee7b7'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 60
            }
        }
    ))
    fig5.update_layout(
        height=400,
        font={'color': "#1e3a8a", 'family': "Arial"}
    )
    st.plotly_chart(fig5, use_container_width=True)

# Study focus recommendations
st.markdown("<h2 class='sub-header'>Study Focus Recommendations</h2>", unsafe_allow_html=True)

# Calculate weakest metrics
subject_metrics = filtered_df.groupby('subject').agg({
    'percentage': 'mean',
    'accuracy_rate': 'mean',
    'attempt_rate': 'mean',
    'penalty_rate': 'mean'
}).reset_index()

weakest_subject = subject_metrics.loc[subject_metrics['percentage'].idxmin()]['subject']
lowest_percentage = subject_metrics.loc[subject_metrics['percentage'].idxmin()]['percentage']
lowest_accuracy_subject = subject_metrics.loc[subject_metrics['accuracy_rate'].idxmin()]['subject']
lowest_accuracy = subject_metrics.loc[subject_metrics['accuracy_rate'].idxmin()]['accuracy_rate']
lowest_attempt_subject = subject_metrics.loc[subject_metrics['attempt_rate'].idxmin()]['subject']
lowest_attempt = subject_metrics.loc[subject_metrics['attempt_rate'].idxmin()]['attempt_rate']
highest_penalty_subject = subject_metrics.loc[subject_metrics['penalty_rate'].idxmax()]['subject']
highest_penalty = subject_metrics.loc[subject_metrics['penalty_rate'].idxmax()]['penalty_rate']

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='metric-card' style='height: 300px;'>
        <h3 style='font-size: 1.3rem; color: #1e3a8a;'>Areas Needing Focus</h3>
        <ul style='list-style-type: none; padding-left: 0;'>
    """, unsafe_allow_html=True)
    
    if lowest_percentage < 75:
        st.markdown(f"""
            <li style='margin-bottom: 10px;'>
                <span style='font-weight: bold; color: #ef4444;'>Overall Performance in {weakest_subject}:</span> 
                {lowest_percentage:.2f}% - Focused study recommended
            </li>
        """, unsafe_allow_html=True)
        
    if lowest_accuracy < 0.75:
        st.markdown(f"""
            <li style='margin-bottom: 10px;'>
                <span style='font-weight: bold; color: #ef4444;'>Accuracy in {lowest_accuracy_subject}:</span> 
                {lowest_accuracy*100:.2f}% - Review core concepts
            </li>
        """, unsafe_allow_html=True)
        
    if lowest_attempt < 0.85:
        st.markdown(f"""
            <li style='margin-bottom: 10px;'>
                <span style='font-weight: bold; color: #ef4444;'>Attempt Rate in {lowest_attempt_subject}:</span> 
                {lowest_attempt*100:.2f}% - Practice more questions
            </li>
        """, unsafe_allow_html=True)
        
    if highest_penalty > 0.1:
        st.markdown(f"""
            <li style='margin-bottom: 10px;'>
                <span style='font-weight: bold; color: #ef4444;'>High Penalty Rate in {highest_penalty_subject}:</span> 
                {highest_penalty*100:.2f}% - Be more careful with answers
            </li>
        """, unsafe_allow_html=True)
    
    st.markdown("</ul></div>", unsafe_allow_html=True)

with col2:
    # Create recommendation based on data
    st.markdown("""
    <div class='metric-card' style='height: 300px;'>
        <h3 style='font-size: 1.3rem; color: #1e3a8a;'>Study Recommendations</h3>
        <ul style='list-style-type: none; padding-left: 0;'>
    """, unsafe_allow_html=True)
    
    # General recommendations based on data
    if weakest_subject == "Physics":
        st.markdown("""
            <li style='margin-bottom: 10px;'>
                <span style='font-weight: bold; color: #3b82f6;'>Physics:</span> 
                Focus on practicing numerical problems and conceptual understanding
            </li>
        """, unsafe_allow_html=True)
    
    if lowest_accuracy_subject == "Chemistry":
        st.markdown("""
            <li style='margin-bottom: 10px;'>
                <span style='font-weight: bold; color: #10b981;'>Chemistry:</span> 
                Review fundamental concepts and practice more problems
            </li>
        """, unsafe_allow_html=True)
    
    # Time management recommendation
    if lowest_attempt < 0.9:
        st.markdown("""
            <li style='margin-bottom: 10px;'>
                <span style='font-weight: bold; color: #f59e0b;'>Time Management:</span> 
                Practice timed mock tests to improve question attempt rate
            </li>
        """, unsafe_allow_html=True)
    
    # Accuracy recommendation
    if highest_penalty > 0.1:
        st.markdown("""
            <li style='margin-bottom: 10px;'>
                <span style='font-weight: bold; color: #ef4444;'>Accuracy:</span> 
                Take a more measured approach to answering questions - don't rush!
            </li>
        """, unsafe_allow_html=True)

    st.markdown("</ul></div>", unsafe_allow_html=True)

# Recent test analysis
st.markdown("<h2 class='sub-header'>Recent Test Analysis</h2>", unsafe_allow_html=True)

# Get the most recent test date
recent_date = filtered_df['date'].max()
recent_tests = filtered_df[filtered_df['date'] == recent_date]

# Check if there are recent tests
if not recent_tests.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        # Recent test metrics table
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='font-size: 1.3rem; color: #1e3a8a;'>Tests on {recent_date.strftime('%d-%m-%Y')}</h3>", unsafe_allow_html=True)
        
        # Create a styled table
        recent_table = recent_tests[['subject', 'percentage', 'accuracy_rate', 'attempt_rate']].copy()
        recent_table['percentage'] = recent_table['percentage'].round(2)
        recent_table['accuracy_rate'] = (recent_table['accuracy_rate'] * 100).round(2)
        recent_table['attempt_rate'] = (recent_table['attempt_rate'] * 100).round(2)
        
        recent_table.columns = ['Subject', 'Percentage (%)', 'Accuracy (%)', 'Attempt (%)']
        st.table(recent_table)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Recent test radar chart
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        
        # Prepare data for radar chart
        radar_data = recent_tests[['subject', 'accuracy_rate', 'attempt_rate', 'percentage']].copy()
        
        # Normalize percentage to 0-1 scale for radar chart
        radar_data['percentage_norm'] = radar_data['percentage'] / 100
        
        # Convert to long format for radar chart
        radar_data_long = pd.melt(
            radar_data,
            id_vars=['subject'],
            value_vars=['accuracy_rate', 'attempt_rate', 'percentage_norm'],
            var_name='Metric',
            value_name='Value'
        )
        
        # Rename metrics for display
        radar_data_long['Metric'] = radar_data_long['Metric'].replace({
            'accuracy_rate': 'Accuracy',
            'attempt_rate': 'Attempt Rate',
            'percentage_norm': 'Performance'
        })
        
        # Create radar chart
        fig6 = px.line_polar(
            radar_data_long, 
            r='Value', 
            theta='Metric', 
            color='subject', 
            line_close=True,
            range_r=[0, 1],
            labels={'Value': 'Score (0-1)', 'Metric': 'Metric'},
            title='Recent Test Performance Radar',
            color_discrete_map={'Physics': '#3b82f6', 'Chemistry': '#10b981', 'Biology': '#f59e0b'}
        )
        fig6.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=True
        )
        st.plotly_chart(fig6, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Footer with performance insights
st.markdown("<h2 class='sub-header'>Quick Performance Insights</h2>", unsafe_allow_html=True)

# Calculate improvement metrics
if len(filtered_df['date'].unique()) > 1:
    first_date = filtered_df['date'].min()
    last_date = filtered_df['date'].max()
    
    first_day = filtered_df[filtered_df['date'] == first_date]
    last_day = filtered_df[filtered_df['date'] == last_date]
    
    first_day_avg = first_day['percentage'].mean()
    last_day_avg = last_day['percentage'].mean()
    
    improvement = last_day_avg - first_day_avg
    
    if improvement > 5:
        insight = f"🚀 Great improvement! Your average score increased by {improvement:.2f}% from {first_date.strftime('%d-%m-%Y')} to {last_date.strftime('%d-%m-%Y')}."
    elif improvement < -5:
        insight = f"📉 Note: Your average score decreased by {abs(improvement):.2f}% from {first_date.strftime('%d-%m-%Y')} to {last_date.strftime('%d-%m-%Y')}. Review your study approach."
    else:
        insight = f"📊 Your performance has been relatively stable (change of {improvement:.2f}%) from {first_date.strftime('%d-%m-%Y')} to {last_date.strftime('%d-%m-%Y')}."
    
    # Best and worst subjects
    best_subject = subject_metrics.loc[subject_metrics['percentage'].idxmax()]
    worst_subject = subject_metrics.loc[subject_metrics['percentage'].idxmin()]
    
    st.info(insight)
    st.success(f"💪 Strongest Subject: {best_subject['subject']} with average score of {best_subject['percentage']:.2f}%")
    
    if worst_subject['percentage'] < 70:
        st.warning(f"🔍 Focus Area: {worst_subject['subject']} with average score of {worst_subject['percentage']:.2f}%")
    else:
        st.info(f"👍 Your weakest subject is {worst_subject['subject']} with a still good average of {worst_subject['percentage']:.2f}%")

# Help section in the sidebar
st.sidebar.markdown("## Dashboard Help")
st.sidebar.markdown("""
**How to Use This Dashboard:**
- Use the date range selector to view performance for specific periods
- Select a subject to filter all charts and metrics for that subject only
- Hover over charts for detailed information
- Look for recommendations in the "Study Focus" section
""")

# Add a data download option
st.sidebar.markdown("## Download Your Data")
csv_export = filtered_df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="Download as CSV",
    data=csv_export,
    file_name="student_performance_data.csv",
    mime="text/csv",
)

# Add an expandable data table
with st.expander("View Raw Data Table"):
    st.dataframe(filtered_df.sort_values(by=['date', 'subject']), use_container_width=True)

st.text("Made for Armaan Chautala 🎀")