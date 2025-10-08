import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import pearsonr, spearmanr


def clean_and_cast(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['Description'] = df['Description'].fillna('')
    numeric_cols = ['Stars', 'Forks', 'Watchers', 'Open Issues', 'Size (KB)']
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)
    for col in ['Created At', 'Updated At', 'Pushed At']:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df


def add_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    today = pd.Timestamp.utcnow()
    age_days = (today - df['Created At']).dt.days.clip(lower=1)
    df['Tuổi repo (năm)'] = (age_days / 365.25).round(2)
    df['Stars/Day (ước tính)'] = (df['Stars'] / age_days).round(2)
    df['Tỉ lệ Issues/Stars'] = (df['Open Issues'] / df['Stars'].replace(0, pd.NA)).astype(float).round(3)
    df['Stars/Fork'] = (df['Stars'] / df['Forks'].replace(0, pd.NA)).astype(float).round(2)
    return df


def describe_stats(df: pd.DataFrame, include_watchers: bool, include_issues: bool) -> pd.DataFrame:
    cols = ['Stars', 'Forks'] + (['Watchers'] if include_watchers else []) + (['Open Issues'] if include_issues else [])
    return df[cols].describe().round(2)


def group_by_license(df: pd.DataFrame, include_watchers: bool, include_issues: bool) -> pd.DataFrame:
    cols = ['Stars', 'Forks'] + (['Watchers'] if include_watchers else []) + (['Open Issues'] if include_issues else [])
    grouped = df.groupby('License', dropna=False)[cols].agg(['sum', 'mean', 'max']).round(2)
    return grouped


def correlation_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Tính toán ma trận tương quan giữa các metrics quan trọng."""
    numeric_cols = ['Stars', 'Forks', 'Watchers', 'Open Issues', 'Size (KB)', 
                   'Stars/Day (ước tính)', 'Stars/Fork', 'Tỉ lệ Issues/Stars', 'Tuổi repo (năm)']
    available_cols = [col for col in numeric_cols if col in df.columns]
    corr_matrix = df[available_cols].corr().round(3)
    return corr_matrix


def trend_analysis(df: pd.DataFrame) -> dict:
    """Phân tích xu hướng dựa trên tuổi repo và các metrics."""
    results = {}
    
    # Phân tích xu hướng Stars theo thời gian
    if 'Tuổi repo (năm)' in df.columns and 'Stars' in df.columns:
        age_stars_corr, age_stars_p = pearsonr(df['Tuổi repo (năm)'], df['Stars'])
        results['age_stars_correlation'] = {
            'correlation': round(age_stars_corr, 3),
            'p_value': round(age_stars_p, 3),
            'significance': 'Có ý nghĩa' if age_stars_p < 0.05 else 'Không có ý nghĩa'
        }
    
    # Phân tích xu hướng Forks theo Stars
    if 'Stars' in df.columns and 'Forks' in df.columns:
        stars_forks_corr, stars_forks_p = pearsonr(df['Stars'], df['Forks'])
        results['stars_forks_correlation'] = {
            'correlation': round(stars_forks_corr, 3),
            'p_value': round(stars_forks_p, 3),
            'significance': 'Có ý nghĩa' if stars_forks_p < 0.05 else 'Không có ý nghĩa'
        }
    
    # Phân tích xu hướng Issues theo Stars
    if 'Stars' in df.columns and 'Open Issues' in df.columns:
        stars_issues_corr, stars_issues_p = pearsonr(df['Stars'], df['Open Issues'])
        results['stars_issues_correlation'] = {
            'correlation': round(stars_issues_corr, 3),
            'p_value': round(stars_issues_p, 3),
            'significance': 'Có ý nghĩa' if stars_issues_p < 0.05 else 'Không có ý nghĩa'
        }
    
    return results


def statistical_insights(df: pd.DataFrame) -> dict:
    """Cung cấp các insights thống kê nâng cao."""
    insights = {}
    
    # Coefficient of Variation (CV) - độ biến thiên
    numeric_cols = ['Stars', 'Forks', 'Watchers', 'Open Issues']
    available_cols = [col for col in numeric_cols if col in df.columns]
    
    for col in available_cols:
        if df[col].std() > 0:
            cv = (df[col].std() / df[col].mean()) * 100
            insights[f'{col}_cv'] = round(cv, 2)
    
    # Z-scores để phát hiện outliers
    for col in available_cols:
        if df[col].std() > 0:
            z_scores = np.abs(stats.zscore(df[col]))
            outliers = df[z_scores > 2][['Framework', col]]
            if not outliers.empty:
                insights[f'{col}_outliers'] = outliers.to_dict('records')
    
    # Phân tích phân phối
    for col in available_cols:
        if len(df[col].dropna()) > 3:
            skewness = stats.skew(df[col].dropna())
            kurtosis = stats.kurtosis(df[col].dropna())
            insights[f'{col}_distribution'] = {
                'skewness': round(skewness, 3),
                'kurtosis': round(kurtosis, 3),
                'skew_interpretation': 'Lệch phải' if skewness > 0.5 else 'Lệch trái' if skewness < -0.5 else 'Gần đối xứng',
                'kurtosis_interpretation': 'Nhọn' if kurtosis > 0.5 else 'Phẳng' if kurtosis < -0.5 else 'Bình thường'
            }
    
    return insights


def framework_comparison_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """So sánh chi tiết giữa các framework."""
    comparison_data = []
    
    for framework in df['Framework'].unique():
        framework_data = df[df['Framework'] == framework].iloc[0]
        
        # Tính ranking trong từng metric
        rankings = {}
        metrics = ['Stars', 'Forks', 'Watchers', 'Open Issues', 'Stars/Day (ước tính)']
        available_metrics = [m for m in metrics if m in df.columns]
        
        for metric in available_metrics:
            sorted_df = df.sort_values(metric, ascending=False)
            rank = sorted_df[sorted_df['Framework'] == framework].index[0] + 1
            rankings[f'{metric}_rank'] = rank
        
        # Tổng điểm ranking (thấp hơn = tốt hơn)
        total_rank = sum(rankings.values())
        
        comparison_data.append({
            'Framework': framework,
            'Total_Rank_Score': total_rank,
            **rankings,
            'Stars': framework_data.get('Stars', 0),
            'Forks': framework_data.get('Forks', 0),
            'Watchers': framework_data.get('Watchers', 0),
            'Open_Issues': framework_data.get('Open Issues', 0),
            'Stars_Per_Day': framework_data.get('Stars/Day (ước tính)', 0)
        })
    
    return pd.DataFrame(comparison_data).sort_values('Total_Rank_Score')


