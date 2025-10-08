import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
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
    fig.update_layout(template='plotly_white', legend_title_text='Framework')
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
    fig.update_layout(template='plotly_white', legend_title_text='Framework')
    st.plotly_chart(fig, use_container_width=True)


def plot_issues_pie(df):
    fig = px.pie(
        df, values='Open Issues', names='Framework', title='Phân bổ Open Issues', hole=.3
    )
    fig.update_layout(template='plotly_white')
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
    fig.update_layout(template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)


def plot_correlation_heatmap(corr_matrix):
    """Vẽ biểu đồ heatmap cho ma trận tương quan."""
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values,
        texttemplate="%{text:.2f}",
        textfont={"size": 10},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='Ma trận tương quan giữa các metrics',
        template='plotly_white',
        width=600,
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_trend_analysis(trend_data, df):
    """Vẽ biểu đồ phân tích xu hướng."""
    if not trend_data:
        st.warning("Không có dữ liệu xu hướng để hiển thị")
        return
    
    # Tạo subplot cho các correlation
    fig = go.Figure()
    
    # Thêm các scatter plots cho correlations
    if 'age_stars_correlation' in trend_data:
        fig.add_trace(go.Scatter(
            x=df['Tuổi repo (năm)'],
            y=df['Stars'],
            mode='markers+text',
            text=df['Framework'],
            textposition='top center',
            name='Tuổi vs Stars',
            marker=dict(size=10, opacity=0.7)
        ))
    
    fig.update_layout(
        title='Phân tích xu hướng: Tuổi repo vs Stars',
        xaxis_title='Tuổi repo (năm)',
        yaxis_title='Số lượng Stars',
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_statistical_insights(insights, df):
    """Vẽ biểu đồ cho các insights thống kê."""
    # Coefficient of Variation chart
    cv_data = {k: v for k, v in insights.items() if k.endswith('_cv')}
    if cv_data:
        fig = px.bar(
            x=list(cv_data.keys()),
            y=list(cv_data.values()),
            title='Hệ số biến thiên (CV) của các metrics',
            labels={'x': 'Metrics', 'y': 'Coefficient of Variation (%)'}
        )
        fig.update_layout(template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    
    # Distribution analysis
    dist_data = {k: v for k, v in insights.items() if k.endswith('_distribution')}
    if dist_data:
        st.subheader('Phân tích phân phối dữ liệu')
        for metric, dist_info in dist_data.items():
            col1, col2 = st.columns(2)
            with col1:
                st.metric(f"Skewness ({metric.replace('_distribution', '')})", 
                         f"{dist_info['skewness']} ({dist_info['skew_interpretation']})")
            with col2:
                st.metric(f"Kurtosis ({metric.replace('_distribution', '')})", 
                         f"{dist_info['kurtosis']} ({dist_info['kurtosis_interpretation']})")


def plot_framework_ranking(comparison_df):
    """Vẽ biểu đồ ranking của các framework."""
    if comparison_df.empty:
        return
    
    # Tạo radar chart cho ranking
    categories = [col for col in comparison_df.columns if col.endswith('_rank') and col != 'Total_Rank_Score']
    
    fig = go.Figure()
    
    for _, row in comparison_df.iterrows():
        values = [row[cat] for cat in categories]
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=[cat.replace('_rank', '') for cat in categories],
            fill='toself',
            name=row['Framework']
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, len(comparison_df)]
            )),
        showlegend=True,
        title="Radar Chart: Ranking các Framework",
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_outliers_analysis(insights, df):
    """Vẽ biểu đồ phát hiện outliers."""
    outlier_data = {k: v for k, v in insights.items() if k.endswith('_outliers')}
    
    if not outlier_data:
        st.info("Không phát hiện outliers trong dữ liệu")
        return
    
    st.subheader('Phân tích Outliers')
    
    for metric, outliers in outlier_data.items():
        if outliers:
            st.write(f"**Outliers trong {metric.replace('_outliers', '')}:**")
            outlier_df = pd.DataFrame(outliers)
            st.dataframe(outlier_df, use_container_width=True)


