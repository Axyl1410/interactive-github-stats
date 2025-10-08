import plotly.express as px
import streamlit as st


def plot_stars(df, chart_type: str):
    if chart_type == 'Cột':
        fig = px.bar(
            df,
            x='Framework', y='Stars', color='Framework', text='Stars',
            title='So sánh số lượng Sao (Stars)', labels={'Stars': 'Số lượng Sao', 'Framework': 'Framework'}
        )
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    else:
        fig = px.line(
            df.sort_values('Stars', ascending=False),
            x='Framework', y='Stars', color='Framework', markers=True,
            title='So sánh số lượng Sao (Stars) - Line', labels={'Stars': 'Số lượng Sao', 'Framework': 'Framework'}
        )
    st.plotly_chart(fig, use_container_width=True)


def plot_forks(df, chart_type: str):
    if chart_type == 'Cột':
        fig = px.bar(
            df,
            x='Framework', y='Forks', color='Framework', text='Forks',
            title='So sánh số lượng Forks', labels={'Forks': 'Số lượng Forks', 'Framework': 'Framework'}
        )
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    else:
        fig = px.line(
            df.sort_values('Forks', ascending=False),
            x='Framework', y='Forks', color='Framework', markers=True,
            title='So sánh số lượng Forks - Line', labels={'Forks': 'Số lượng Forks', 'Framework': 'Framework'}
        )
    st.plotly_chart(fig, use_container_width=True)


def plot_issues_pie(df):
    fig = px.pie(
        df, values='Open Issues', names='Framework', title='Phân bổ Open Issues', hole=.3
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_scatter(df, show_issues: bool):
    fig = px.scatter(
        df,
        x='Stars', y='Forks', color='Framework',
        size=(df['Open Issues'] if show_issues else df['Forks']).astype(float),
        hover_data=['Repo', 'License', 'Watchers', 'Open Issues', 'Stars/Day (ước tính)'],
        labels={'Stars': 'Sao', 'Forks': 'Forks'},
        title='Stars vs Forks (kích thước ~ Open Issues)'
    )
    st.plotly_chart(fig, use_container_width=True)


