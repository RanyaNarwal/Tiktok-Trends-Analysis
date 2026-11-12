import pandas as pd

# Load the main dataset
df = pd.read_csv("youtube_shorts_tiktok_trends_2025.csv")

# ── Filter TikTok only ───────────────────────────────
df = df[df["platform"] == "TikTok"]
print("TikTok videos:", len(df))

# ── Check missing values ─────────────────────────────── 
print("Missing values:", int(df.isna().sum().sum()))

# ── What genres get the most views? ──────
genre_views = df.groupby("genre").agg(
    avg_views=("views", "mean"),
    videos=("views", "count"),
).sort_values("avg_views", ascending=False).round(0)
print("\nAvg Views by Genre:")
print(genre_views)
 
# ── What genres get the most engagement? ─
genre_eng = df.groupby("genre")["engagement_rate"].mean().sort_values(ascending=False)
print("\nAvg Engagement Rate by Genre:")
print(genre_eng)
 
# ── Best time to post ────────────────────
time_views = df.groupby("publish_period")["views"].mean().sort_values(ascending=False)
print("\nAvg Views by Time of Day:")
print(time_views)
 
# ── Weekend vs Weekday ───────────────────
weekend = df.groupby("is_weekend")["views"].mean()
print("\nWeekday(0) vs Weekend(1) Avg Views:")
print(weekend)
 
# ── What trend types perform best? ───────
trend = df.groupby("trend_type")["views"].mean().sort_values(ascending=False)
print("\nAvg Views by Trend Type:")
print(trend)