import pandas as pd
import streamlit as st

from components.sidebar import render_sidebar
from utils import apply_css
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

# Apply CSS styling
apply_css()

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