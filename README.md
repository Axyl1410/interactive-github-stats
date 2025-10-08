# JavaScript Frameworks Popularity Dashboard

A Streamlit dashboard that compares the popularity of top JavaScript frameworks (React, Vue, Angular) using live data from the GitHub API. It includes data cleaning, descriptive statistics, multiple visualizations, and export options.

## Features

- Data processing: cleaning, typing, and computed metrics (repo age, stars/day, stars/fork, issues/stars), descriptive statistics, and grouping by license
- Visualizations: bar and line (toggle), pie, and scatter plots
- Sidebar controls: framework filter, chart type toggle, show/hide watchers and open issues
- Export: download CSV and HTML report (overview, stats, grouped tables)

## Project Structure

```
PythonProject/
  app.py                        # Orchestrates UI, data flow, charts, and exports
  components/
    charts.py                   # Plotly charts (bar/line, pie, scatter)
    sidebar.py                  # Sidebar controls
  services/
    github_api.py               # GitHub API fetching with caching
    processing.py               # Cleaning, metrics, stats, grouping
    exporting.py                # HTML report builder
  requirements.txt              # Minimal dependencies
  .gitignore                    # Standard Python/Streamlit/IDE ignores
```

## Requirements

- Python 3.10+
- See `requirements.txt` for Python packages

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501` by default.

## Notes

- GitHub API Rate Limits: Unauthenticated requests are rate-limited. If you hit limits, wait a bit or add authentication (e.g., a token) in `services/github_api.py`.
- Network/Firewall: The app fetches from the GitHub API; ensure outbound HTTPS is allowed.

## Troubleshooting

- Module not found (e.g., streamlit, pandas): run `pip install -r requirements.txt`.
- Blank charts or errors: check network connectivity and try again.
- High DPI text overlap in bar charts: resize the window or collapse the sidebar to increase space.

## License

This project is provided for educational/demo purposes. Use at your discretion.
