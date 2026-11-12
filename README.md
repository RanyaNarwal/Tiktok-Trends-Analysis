# ViralUp 🚀
### TikTok Trends Analysis Dashboard

A data science project analyzing 48,000+ TikTok videos to identify what content performs best and drives views for people who want to grow as creators. It covers data cleaning, SQL analysis, a machine learning model, and an interactive dashboard.

## Dashboard
[View Live Dashboard]: https://public.tableau.com/views/ViralUp-TikTokTrends/Dashboard1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link

## Data
Public Kaggle dataset, "YouTube Shorts & TikTok Trends 2025" (48,079 rows, 58 columns).
Filtered to TikTok only: 28,844 videos, 14 genres, Jan to Aug 2025.
"Viral" is defined as the top 10% of videos by views.

## Key Questions this project answers
**1. Which genres get the most views?**
DIY (108,175 average views), Fashion (107,350) and Lifestyle (105,017) lead, and Food (95,408) is lowest.

**2. When is the best time to post?**
The best hours to post are 8am (105,205 average views), 7am (104,590) and 2pm (103,342), about 6% above the overall average of 99,292. 
Weekends are only about 2% higher than weekdays.

**3. Does video length matter?**
Videos of length 0–15s (103,099) and 46–60s (102,587) average the most views, and 61–90s (92,335) the least. That is about a 12% gap with no steady decline as video length increases.

**4. How do the top genres move month to month?**
Among the five highest-viewed genres with 2,000+ videos (Fashion, Lifestyle, Gaming, Tech and Comedy), monthly averages stay between roughly 85,000 and 127,000 views with no clear rise or fall, so I don't claim any genre is rising or fading. DIY is excluded from this chart because its 142 videos make its monthly numbers swing widely.

## Tech Stack and Tools
- **Python (Pandas, Scikit-learn)** — Data cleaning, analysis, ML model, loading data into SQLite
- **SQL (SQLite, DBeaver)** — Database storage and querying
- **Tableau Public** — Interactive dashboard
- **Git and GitHub** — Version control
- **VS Code** — Code and query editing

## 📁 Project Structure
- `explore.py` — Initial data exploration
- `analysis.py` — Deep EDA and insights
- `database.py` — SQL database setup
- `queries.sql` — Analytical SQL queries
- `model.py` — Trend-type classification model
- `export_for_tableau.py` — Data export for dashboard

## SQL analysis
Techniques used: CTEs, `NTILE`, `ROW_NUMBER`, `RANK`, window functions and conditional aggregation.

## Machine learning
- Target: `trend_label` (rising, stable, seasonal, declining) on 25,911 TikTok videos using 20 features.
- Compared Logistic Regression and Random Forest. Random Forest performed best at 80% accuracy (macro F1 0.74) against a 53% baseline. Logistic Regression reached    72%. Five-fold cross-validation gave a macro F1 of 0.75 (±0.01).
- "Declining" videos are only 5% of the data. Random Forest gets 51% recall and 68% precision for it compared to the 80% overall accuracy.
- The model classifies trend type. It does NOT predict video virality.