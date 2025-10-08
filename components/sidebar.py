import streamlit as st


def render_sidebar(frameworks):
    with st.sidebar:
        st.header('⚙️ Tùy chọn hiển thị')
        selected_frameworks = st.multiselect(
            'Chọn framework', options=list(frameworks.keys()), default=list(frameworks.keys())
        )
        chart_type = st.radio('Loại biểu đồ', options=['Cột', 'Đường'], index=0, horizontal=True)
        show_watchers = st.checkbox('Hiển thị Watchers', value=True)
        show_issues = st.checkbox('Hiển thị Open Issues', value=True)
    return selected_frameworks, chart_type, show_watchers, show_issues


