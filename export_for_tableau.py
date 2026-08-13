import pandas as pd

# Load and filter TikTok only
df = pd.read_csv("youtube_shorts_tiktok_trends_2025.csv")
df = df[df["platform"] == "TikTok"]

# Add viral flag
viral_threshold = df["views"].quantile(0.90)
df["is_viral"] = (df["views"] >= viral_threshold).astype(int)

# Add length bucket
bins = [0, 15, 30, 45, 60, 90]
labels = ["0-15s", "16-30s", "31-45s", "46-60s", "61-90s"]
df["length_bucket"] = pd.cut(
    df["duration_sec"], 
    bins=bins, 
    labels=labels
)

# Save final CSV
df.to_csv("viralup_tableau.csv", index=False)
print(f"✅ Exported {len(df)} rows to viralup_tableau.csv")