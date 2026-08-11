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

# ── Question 1: Video Length & Virality ─────────────
print("\n── Video Length Analysis ──")
bins = [0, 15, 30, 45, 60, 90]
labels = ["0-15s", "16-30s", "31-45s", "46-60s", "61-90s"]
df["length_bucket"] = pd.cut(df["duration_sec"], bins=bins, labels=labels)

length_stats = df.groupby("length_bucket", observed=True).agg(
    avg_views=("views", "mean"),
    viral_rate=("is_viral", "mean"),
    count=("views", "count")
).round(3)
print(length_stats)

# ── Question 2: Top Hashtags ─────────────────────────
print("\n── Top 20 Hashtags by Avg Views ──")
hashtag_views = df.groupby("hashtag")["views"].mean().sort_values(ascending=False).head(20)
print(hashtag_views)

# ── Question 3: Viral vs Non-Viral Comparison ───────
print("\n── Viral vs Non-Viral Video Traits ──")
comparison = df.groupby("is_viral").agg(
    avg_views=("views", "mean"),
    avg_likes=("likes", "mean"),
    avg_duration=("duration_sec", "mean"),
    avg_engagement=("engagement_rate", "mean"),
    avg_completion=("completion_rate", "mean"),
    avg_title_length=("title_length", "mean"),
    has_emoji_pct=("has_emoji", "mean")
).round(3)
print(comparison)

# ── Question 4: Best Genre + Time Combo ─────────────
print("\n── Best Genre & Time of Day Combo ──")
combo = df.groupby(["genre", "publish_period"])["views"].mean().unstack()
print(combo.round(0))

# ── Question 5: Creator Tier Performance ─────────────
print("\n── Views by Creator Tier ──")
tier = df.groupby("creator_tier").agg(
    avg_views=("views", "mean"),
    avg_engagement=("engagement_rate", "mean"),
    viral_rate=("is_viral", "mean")
).sort_values("avg_views", ascending=False).round(3)
print(tier)

# ── Question 6: Traffic Source ───────────────────────
print("\n── Traffic Source & Views ──")
traffic = df.groupby("traffic_source")["views"].mean().sort_values(ascending=False)
print(traffic)

# ── Best Hour to Post ────────────────────────────────
print("\n── Avg Views by Hour of Day ──")
hour_views = df.groupby("upload_hour").agg(
    avg_views=("views", "mean"),
    viral_rate=("is_viral", "mean"),
    count=("views", "count")
).round(3)
print(hour_views)

# ── Best Hour per Genre ──────────────────────────────
print("\n── Best Posting Hour by Genre ──")
best_hour = df.groupby(["genre", "upload_hour"])["views"].mean()
best_hour = best_hour.reset_index()
best_hour = best_hour.loc[best_hour.groupby("genre")["views"].idxmax()]
best_hour = best_hour.sort_values("views", ascending=False)
print(best_hour)