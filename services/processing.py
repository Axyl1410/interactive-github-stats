import pandas as pd


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


