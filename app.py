import pandas as pd
import streamlit as st

from components.sidebar import render_sidebar
from components.charts import (plot_stars, plot_forks, plot_issues_pie, plot_scatter, 
                              plot_correlation_heatmap, plot_trend_analysis, 
                              plot_statistical_insights, plot_framework_ranking, 
                              plot_outliers_analysis)
from services.github_api import get_frameworks_data
from services.processing import (clean_and_cast, add_metrics, describe_stats, group_by_license,
                               correlation_analysis, trend_analysis, statistical_insights, 
                               framework_comparison_analysis)
from services.exporting import build_html_report


# --- Ứng dụng ---

# --- Giao diện ứng dụng Streamlit ---
st.set_page_config(page_title="So sánh Framework JS", layout="wide")

# Global CSS for a cleaner, modern look with dark theme support
st.markdown(
    """
    <style>
    /* Base styles */
    .main > div {padding-top: 1rem; padding-bottom: 2rem;}
    .block-container {padding-top: 2rem;}
    
    /* Dark theme variables */
    :root {
        --bg-primary: #0f0f23;
        --bg-secondary: #1a1a2e;
        --bg-tertiary: #16213e;
        --text-primary: #ffffff;
        --text-secondary: #b0b0b0;
        --text-muted: #888888;
        --border-color: #2d3748;
        --border-light: #4a5568;
        --accent-color: #0ea5e9;
        --accent-gradient: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        --shadow-color: rgba(0, 0, 0, 0.3);
        --card-bg: #1a1a2e;
        --metric-bg: #16213e;
    }
    
    /* Light theme variables */
    @media (prefers-color-scheme: light) {
        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f8fafc;
            --bg-tertiary: #f1f5f9;
            --text-primary: #1a202c;
            --text-secondary: #4a5568;
            --text-muted: #718096;
            --border-color: #e2e8f0;
            --border-light: #cbd5e0;
            --accent-color: #0ea5e9;
            --accent-gradient: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
            --shadow-color: rgba(0, 0, 0, 0.1);
            --card-bg: #ffffff;
            --metric-bg: #ffffff;
        }
    }
    
    /* Force dark theme */
    .stApp {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    
    /* Metrics styling */
    .stMetric {
        background: var(--metric-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 16px !important;
        color: var(--text-primary) !important;
        box-shadow: 0 2px 8px var(--shadow-color) !important;
    }
    
    .stMetric > div {
        color: var(--text-primary) !important;
    }
    
    .stMetric [data-testid="metric-value"] {
        color: var(--text-primary) !important;
    }
    
    .stMetric [data-testid="metric-label"] {
        color: var(--text-secondary) !important;
    }
    
    /* Hero section */
    .hero {
        padding: 18px 22px;
        border-radius: 14px;
        background: linear-gradient(135deg, #111827 0%, #1f2937 60%, #0ea5e9 120%);
        color: #f9fafb;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 24px rgba(2,6,23,0.35);
        margin-bottom: 2rem;
    }
    
    .hero h1 {
        margin: 0 0 8px 0;
        font-size: 1.6rem;
        color: #f9fafb;
    }
    
    .hero p {
        margin: 0;
        opacity: 0.9;
        color: #f9fafb;
    }
    
    /* Section cards */
    .section-card {
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 16px !important;
        color: var(--text-primary) !important;
        box-shadow: 0 2px 8px var(--shadow-color) !important;
    }
    
    /* Tabs styling */
    .stTabs {
        margin: 8px 0 16px 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 14px;
        background-color: var(--bg-secondary) !important;
        border-radius: 8px !important;
        padding: 4px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--bg-tertiary) !important;
        border-top-left-radius: 8px !important;
        border-top-right-radius: 12px !important;
        padding: 10px 16px !important;
        color: var(--text-secondary) !important;
        border: 1px solid transparent !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        border-color: var(--border-light) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--accent-gradient) !important;
        color: white !important;
        border-color: var(--accent-color) !important;
        box-shadow: 0 2px 8px rgba(14, 165, 233, 0.3) !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
    }
    
    .stDataFrame table {
        background-color: var(--card-bg) !important;
        color: var(--text-primary) !important;
    }
    
    .stDataFrame th {
        background-color: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        border-color: var(--border-color) !important;
    }
    
    .stDataFrame td {
        background-color: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border-color: var(--border-color) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--bg-secondary) !important;
    }
    
    .css-1d391kg .stMarkdown {
        color: var(--text-primary) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: var(--accent-color) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #0284c7 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3) !important;
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background-color: var(--accent-color) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
    }
    
    /* Warning and info boxes */
    .stAlert {
        background-color: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }
    
    /* Divider styling */
    .stDivider {
        border-color: var(--border-color) !important;
    }
    
    /* Caption styling */
    .stCaption {
        color: var(--text-muted) !important;
    }
    
    /* Header styling */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: var(--text-primary) !important;
    }
    
    /* Subheader styling */
    .stSubheader {
        color: var(--text-primary) !important;
    }
    
    /* Form controls styling */
    .stSelectbox > div > div {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    .stSelectbox label {
        color: var(--text-primary) !important;
    }
    
    .stMultiselect > div > div {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    .stMultiselect label {
        color: var(--text-primary) !important;
    }
    
    .stRadio > div {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }
    
    .stRadio label {
        color: var(--text-primary) !important;
    }
    
    .stCheckbox > div {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }
    
    .stCheckbox label {
        color: var(--text-primary) !important;
    }
    
    /* Enhanced dataframe styling */
    .stDataFrame .dataframe {
        background-color: var(--card-bg) !important;
        color: var(--text-primary) !important;
    }
    
    .stDataFrame .dataframe thead th {
        background-color: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        font-weight: 600 !important;
    }
    
    .stDataFrame .dataframe tbody td {
        background-color: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    .stDataFrame .dataframe tbody tr:nth-child(even) {
        background-color: var(--bg-secondary) !important;
    }
    
    .stDataFrame .dataframe tbody tr:hover {
        background-color: var(--bg-tertiary) !important;
    }
    
    /* Enhanced metric cards */
    .stMetric > div[data-testid="metric-container"] {
        background: var(--metric-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 16px !important;
        box-shadow: 0 2px 8px var(--shadow-color) !important;
        transition: all 0.3s ease !important;
    }
    
    .stMetric > div[data-testid="metric-container"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 16px var(--shadow-color) !important;
        border-color: var(--accent-color) !important;
    }
    
    /* Enhanced section cards */
    .section-card {
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        color: var(--text-primary) !important;
        box-shadow: 0 2px 8px var(--shadow-color) !important;
        transition: all 0.3s ease !important;
        margin-bottom: 16px !important;
    }
    
    .section-card:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px var(--shadow-color) !important;
        border-color: var(--accent-color) !important;
    }
    
    /* Plotly chart container styling */
    .js-plotly-plot {
        background-color: transparent !important;
    }
    
    /* Streamlit elements dark theme overrides */
    .element-container {
        background-color: transparent !important;
    }
    
    /* Better spacing and layout */
    .main .block-container {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Custom scrollbar for dark theme */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-color);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Tiêu đề
st.markdown(
    """
    <div class="hero">
      <h1>📊 Phân tích độ phổ biến Framework JavaScript</h1>
      <p>Sử dụng dữ liệu trực tiếp từ GitHub để so sánh React, Vue và Angular.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Danh sách các framework và repository chính thức của chúng
frameworks = {
    'React': 'facebook/react',
    'Vue': 'vuejs/core',
    'Angular': 'angular/angular'
}

# --- Bộ lọc/thiết lập giao diện ---
selected_frameworks, chart_type, show_watchers, show_issues = render_sidebar(frameworks)

# Lấy dữ liệu
data = get_frameworks_data(frameworks, selected_frameworks)

if not data:
    st.warning("Không thể lấy dữ liệu từ GitHub. Vui lòng thử lại sau.")
else:
    # DataFrame + xử lý
    df = pd.DataFrame(data)
    df = clean_and_cast(df)
    df = add_metrics(df)

    # Tabs layout
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        'Tổng quan', 'Chỉ số nhanh', 'Nhóm & Thống kê', 'Biểu đồ', 'Phân tích nâng cao', 'Xuất & Mô tả'
    ])

    with tab1:
        st.subheader('Tổng quan dữ liệu')
        highlight_cols = ['Stars', 'Forks'] + (['Open Issues'] if show_issues else [])
        st.dataframe(
            df[
                ['Framework', 'Repo', 'License', 'Size (KB)', 'Created At', 'Updated At', 'Pushed At', 'Stars', 'Forks']
                + (['Watchers'] if show_watchers else [])
                + (['Open Issues'] if show_issues else [])
                + ['Stars/Day (ước tính)', 'Stars/Fork', 'Tỉ lệ Issues/Stars', 'Tuổi repo (năm)']
            ].style.highlight_max(axis=0, subset=highlight_cols, color='lightgreen')
        )

    with tab2:
        st.subheader('Chỉ số nhanh')
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            st.metric('Tổng Stars', int(df['Stars'].sum()))
        with kpi2:
            st.metric('Tổng Forks', int(df['Forks'].sum()))
        with kpi3:
            st.metric('Tuổi repo trung bình (năm)', float(df['Tuổi repo (năm)'].mean().round(2)))

    with tab3:
        st.subheader('Nhóm theo License (nếu có)')
        grouped = group_by_license(df, include_watchers=show_watchers, include_issues=show_issues)
        st.dataframe(grouped)
        st.subheader('Thống kê mô tả')
        stats = describe_stats(df, include_watchers=show_watchers, include_issues=show_issues)
        st.dataframe(stats)

    with tab4:
        st.subheader('Biểu đồ so sánh')
        col1, col2 = st.columns(2)
        with col1:
            plot_stars(df, chart_type)
        with col2:
            plot_forks(df, chart_type)
        if show_issues:
            st.subheader('Tỷ lệ các vấn đề đang mở (Open Issues)')
            plot_issues_pie(df)
        st.subheader('Quan hệ Stars và Forks')
        plot_scatter(df, show_issues)

    with tab5:
        st.subheader('Phân tích nâng cao')
        
        # Correlation Analysis
        st.subheader('🔗 Phân tích tương quan')
        corr_matrix = correlation_analysis(df)
        plot_correlation_heatmap(corr_matrix)
        
        # Trend Analysis
        st.subheader('📈 Phân tích xu hướng')
        trend_data = trend_analysis(df)
        plot_trend_analysis(trend_data, df)
        
        # Display trend results
        if trend_data:
            st.subheader('Kết quả phân tích xu hướng')
            for analysis, result in trend_data.items():
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(f"Tương quan ({analysis})", f"{result['correlation']}")
                with col2:
                    st.metric("P-value", f"{result['p_value']}")
                with col3:
                    st.metric("Ý nghĩa thống kê", result['significance'])
        
        # Statistical Insights
        st.subheader('📊 Insights thống kê')
        insights = statistical_insights(df)
        plot_statistical_insights(insights, df)
        
        # Framework Comparison
        st.subheader('🏆 So sánh Framework')
        comparison_df = framework_comparison_analysis(df)
        st.dataframe(comparison_df, use_container_width=True)
        plot_framework_ranking(comparison_df)
        
        # Outliers Analysis
        plot_outliers_analysis(insights, df)

    with tab6:
        st.subheader('Xuất kết quả')
        export_col1, export_col2 = st.columns(2)
        with export_col1:
            csv_bytes = df.to_csv(index=False).encode('utf-8')
            st.download_button('Tải CSV dữ liệu', data=csv_bytes, file_name='frameworks_summary.csv', mime='text/csv')
        with export_col2:
            report_bytes = build_html_report(df, stats, grouped)
            st.download_button('Tải báo cáo HTML', data=report_bytes, file_name='report.html', mime='text/html')
        st.subheader('Mô tả từ GitHub')
        for _, row in df.iterrows():
            st.markdown(f"**{row['Framework']}**: *{row['Description']}*")