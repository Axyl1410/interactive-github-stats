import pandas as pd
import streamlit as st

from components.sidebar import render_sidebar
from components.charts import plot_stars, plot_forks, plot_issues_pie, plot_scatter
from services.github_api import get_frameworks_data
from services.processing import clean_and_cast, add_metrics, describe_stats, group_by_license
from services.exporting import build_html_report


# --- Ứng dụng ---

# --- Giao diện ứng dụng Streamlit ---
st.set_page_config(page_title="So sánh Framework JS", layout="wide")

# Tiêu đề
st.title('📊 Phân tích độ phổ biến Framework JavaScript trên GitHub')
st.markdown("""
Ứng dụng này sử dụng dữ liệu trực tiếp từ GitHub API để so sánh độ phổ biến
của ba framework JavaScript hàng đầu: **React, Vue, và Angular**.
""")

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

    # --- Hiển thị dữ liệu ---
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

    # Statistics / Grouping
    st.subheader('Thống kê mô tả')
    stats = describe_stats(df, include_watchers=show_watchers, include_issues=show_issues)
    st.dataframe(stats)

    # KPIs nhanh
    st.subheader('Chỉ số nhanh')
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric('Tổng Stars', int(df['Stars'].sum()))
    with kpi2:
        st.metric('Tổng Forks', int(df['Forks'].sum()))
    with kpi3:
        st.metric('Tuổi repo trung bình (năm)', float(df['Tuổi repo (năm)'].mean().round(2)))

    # Nhóm và tổng hợp
    st.subheader('Nhóm theo License (nếu có)')
    grouped = group_by_license(df, include_watchers=show_watchers, include_issues=show_issues)
    st.dataframe(grouped)

    # --- Trực quan hóa dữ liệu ---
    st.subheader('Biểu đồ so sánh')

    col1, col2 = st.columns(2)

    with col1:
        plot_stars(df, chart_type)

    with col2:
        plot_forks(df, chart_type)

    # Biểu đồ tròn thể hiện tỷ lệ Open Issues
    if show_issues:
        st.subheader('Tỷ lệ các vấn đề đang mở (Open Issues)')
        plot_issues_pie(df)

    # Biểu đồ scatter: Stars vs Forks
    st.subheader('Quan hệ Stars và Forks')
    plot_scatter(df, show_issues)

    # Xuất kết quả
    st.subheader('Xuất kết quả')
    export_col1, export_col2 = st.columns(2)
    with export_col1:
        csv_bytes = df.to_csv(index=False).encode('utf-8')
        st.download_button('Tải CSV dữ liệu', data=csv_bytes, file_name='frameworks_summary.csv', mime='text/csv')
    with export_col2:
        report_bytes = build_html_report(df, stats, grouped)
        st.download_button('Tải báo cáo HTML', data=report_bytes, file_name='report.html', mime='text/html')

    # Hiển thị mô tả của từng framework
    st.subheader('Mô tả từ GitHub')
    for _, row in df.iterrows():
        st.markdown(f"**{row['Framework']}**: *{row['Description']}*")