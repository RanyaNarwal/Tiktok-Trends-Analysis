# ViralUp 🚀
### TikTok Trends Analysis Dashboard

A data science project analyzing 48,000+ TikTok videos to identify what content performs best and drives views for people who want to grow as creators. It covers data cleaning, SQL analysis, a machine learning model, and an interactive dashboard.

## Tech Stack
- **Python** — Data cleaning, analysis, ML model
- **SQL (SQLite), ScikitLearn** — Database storage and querying
- **Tableau** — Interactive dashboard

## Dashboard
[View Live Dashboard]: https://public.tableau.com/views/ViralUp-TikTokTrends/Dashboard1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link

## Questions this project answers
Which genres, video lengths and posting times get the most views?
What separates the top 10% of videos from the rest?
How do the top genres move month to month?
Can a model classify a video's trend type (rising, stable, seasonal, declining)?

## 🔍 Key Insights
- DIY and Lifestyle content drives highest views
- Posting at 7–8am maximizes reach
- ML model predicts trend labels with 80% accuracy

## 📁 Project Structure
- `explore.py` — Initial data exploration
- `analysis.py` — Deep EDA and insights
- `database.py` — SQL database setup
- `queries.sql` — Analytical SQL queries
- `model.py` — Trend-type classification model
- `export_for_tableau.py` — Data export for dashboard