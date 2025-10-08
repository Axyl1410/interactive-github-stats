import requests
import streamlit as st


@st.cache_data(ttl=3600)
def get_framework_data(framework_name, repo_path):
    """Fetch single repository data from GitHub API."""
    url = f"https://api.github.com/repos/{repo_path}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        repo_data = response.json()
        return {
            'Framework': framework_name,
            'Repo': repo_path,
            'Stars': repo_data.get('stargazers_count', 0),
            'Forks': repo_data.get('forks_count', 0),
            'Watchers': repo_data.get('subscribers_count', 0),
            'Open Issues': repo_data.get('open_issues_count', 0),
            'Description': repo_data.get('description', ''),
            'License': (repo_data.get('license') or {}).get('spdx_id', 'NOASSERTION'),
            'Created At': repo_data.get('created_at'),
            'Updated At': repo_data.get('updated_at'),
            'Pushed At': repo_data.get('pushed_at'),
            'Size (KB)': repo_data.get('size', 0)
        }
    except requests.exceptions.RequestException as e:
        st.error(f"Lỗi khi gọi API cho {framework_name}: {e}")
        return None


def get_frameworks_data(frameworks_dict, selected):
    data = []
    for name, path in frameworks_dict.items():
        if selected and name not in selected:
            continue
        item = get_framework_data(name, path)
        if item:
            data.append(item)
    return data


