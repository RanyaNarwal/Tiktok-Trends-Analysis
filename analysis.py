import pandas as pd

# Load and filter TikTok only
df = pd.read_csv("youtube_shorts_tiktok_trends_2025.csv")
df = df[df["platform"] == "TikTok"]

# ── Define Viral Videos ──────────────────────────────
# Top 10% of views = viral
viral_threshold = df["views"].quantile(0.90)
df["is_viral"] = (df["views"] >= viral_threshold).astype(int)
 
print(f"Viral threshold: {viral_threshold:,.0f} views")
print(f"Viral videos: {df['is_viral'].sum()}")
print(f"Non-viral videos: {(df['is_viral'] == 0).sum()}")
 
# ── Video Length & Virality ──────────────
print("\n── Video Length Analysis ──")
bins = [0, 15, 30, 45, 60, 90]
labels = ["0-15s", "16-30s", "31-45s", "46-60s", "61-90s"]
df["length_bucket"] = pd.cut(df["duration_sec"], bins=bins, labels=labels)
 
length_stats = df.groupby("length_bucket", observed=True).agg(
    avg_views=("views", "mean"),
    viral_rate=("is_viral", "mean"),
    count=("views", "count"),
).round(3)
print(length_stats)
 
# ── Top Hashtags (100+ videos) ───────────
print("\n── Top 20 Hashtags by Avg Views (100+ videos) ──")
hashtag_stats = df.groupby("hashtag").agg(
    avg_views=("views", "mean"),
    count=("views", "count"),
)
hashtag_stats = hashtag_stats[hashtag_stats["count"] >= 100]
print(hashtag_stats.sort_values("avg_views", ascending=False).head(20).round(0))
 
# ── Viral vs Non-Viral Comparison ────────
print("\n── Viral vs Non-Viral Video Traits ──")
comparison = df.groupby("is_viral").agg(
    avg_views=("views", "mean"),
    avg_likes=("likes", "mean"),
    avg_duration=("duration_sec", "mean"),
    avg_engagement=("engagement_rate", "mean"),
    avg_completion=("completion_rate", "mean"),
    avg_title_length=("title_length", "mean"),
    has_emoji_pct=("has_emoji", "mean"),
).round(3)
print(comparison)
 
# ── Best Genre + Time Combo ──────────────
print("\n── Best Genre & Time of Day Combo ──")
combo = df.groupby(["genre", "publish_period"])["views"].mean().unstack()
print(combo.round(0))
 
# ── Creator Tier Performance ─────────────
print("\n── Views by Creator Tier ──")
tier = df.groupby("creator_tier").agg(
    avg_views=("views", "mean"),
    avg_engagement=("engagement_rate", "mean"),
    viral_rate=("is_viral", "mean"),
    count=("views", "count"),
).sort_values("avg_views", ascending=False).round(3)
print(tier)
 
# ── Best Hour to Post ────────────────────────────────
print("\n── Avg Views by Hour of Day ──")
hour_views = df.groupby("upload_hour").agg(
    avg_views=("views", "mean"),
    viral_rate=("is_viral", "mean"),
    count=("views", "count"),
).round(3)
print(hour_views)
 
# ── Best Hour per Genre (20+ videos) ─────────────────
print("\n── Best Posting Hour by Genre (20+ videos) ──")
genre_hour = df.groupby(["genre", "upload_hour"]).agg(
    avg_views=("views", "mean"),
    count=("views", "count"),
).reset_index()
genre_hour = genre_hour[genre_hour["count"] >= 20]
best_hour = genre_hour.loc[genre_hour.groupby("genre")["avg_views"].idxmax()]
print(best_hour.sort_values("avg_views", ascending=False).round(0))
 