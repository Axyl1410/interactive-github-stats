import pandas as pd


def build_html_report(df: pd.DataFrame, stats: pd.DataFrame, grouped: pd.DataFrame) -> bytes:
    html = f"""
    <html>
    <head><meta charset='utf-8'><title>Báo cáo Frameworks</title></head>
    <body>
    <h1>Báo cáo Phân tích Frameworks</h1>
    <h2>Ngày tạo: {pd.Timestamp.utcnow()}</h2>
    <h3>Tổng quan</h3>
    {df.to_html(index=False)}
    <h3>Thống kê mô tả</h3>
    {stats.to_html()}
    <h3>Nhóm theo License</h3>
    {grouped.to_html()}
    </body></html>
    """
    return html.encode('utf-8')


