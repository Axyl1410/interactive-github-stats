import streamlit as st


def render_sidebar(frameworks):
    with st.sidebar:
        # Add custom CSS for sidebar dark theme
        st.markdown("""
        <style>
        .sidebar .stMarkdown h3 {
            color: #ffffff !important;
            background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 16px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(14, 165, 233, 0.3);
        }
        .sidebar .stMarkdown p {
            color: #b0b0b0 !important;
            text-align: center;
            margin-bottom: 20px;
        }
        .sidebar .stMarkdown h4 {
            color: #ffffff !important;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .sidebar .stDivider {
            border-color: #4a5568 !important;
            margin: 20px 0;
        }
        .sidebar .stCaption {
            color: #888888 !important;
            text-align: center;
            font-style: italic;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('### 🚀 JS Framework Insights')
        st.caption('So sánh nhanh React · Vue · Angular')
        st.divider()
        st.header('⚙️ Tùy chọn hiển thị')
        selected_frameworks = st.multiselect(
            'Chọn framework', options=list(frameworks.keys()), default=list(frameworks.keys())
        )
        chart_type = st.radio('Loại biểu đồ', options=['Cột', 'Đường'], index=0, horizontal=True)
        show_watchers = st.checkbox('Hiển thị Watchers', value=True)
        show_issues = st.checkbox('Hiển thị Open Issues', value=True)
        st.divider()
        st.caption('Dữ liệu nhận trực tiếp từ GitHub API trong thời gian thực')
    return selected_frameworks, chart_type, show_watchers, show_issues


