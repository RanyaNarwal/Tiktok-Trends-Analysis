import pandas as pd
from sqlalchemy import create_engine

# ── Create SQLite Database ───────────────────────────
engine = create_engine("sqlite:///viralup.db")

# ── Load all CSV files ───────────────────────────────
print("Loading CSV files...")

main_df = pd.read_csv("youtube_shorts_tiktok_trends_2025.csv")
main_df = main_df[main_df["platform"] == "TikTok"]

hashtags_df = pd.read_csv("top_hashtags_2025.csv")
creators_df = pd.read_csv("top_creators_impact_2025.csv")
monthly_df = pd.read_csv("monthly_trends_2025.csv")
country_df = pd.read_csv("country_platform_summary_2025.csv")

# ── Load into SQL Tables ─────────────────────────────
print("Writing to database...")

main_df.to_sql("tiktok_videos", engine, if_exists="replace", index=False)
hashtags_df.to_sql("top_hashtags", engine, if_exists="replace", index=False)
creators_df.to_sql("top_creators", engine, if_exists="replace", index=False)
monthly_df.to_sql("monthly_trends", engine, if_exists="replace", index=False)
country_df.to_sql("country_summary", engine, if_exists="replace", index=False)

print("Database created successfully!")
print("\nTables created:")
print("  - tiktok_videos")
print("  - top_hashtags")
print("  - top_creators")
print("  - monthly_trends")
print("  - country_summary")

# ── Verify it worked ─────────────────────────────────
with engine.connect() as conn:
    from sqlalchemy import text
    result = conn.execute(text("SELECT COUNT(*) FROM tiktok_videos"))
    print(f"\nRows in tiktok_videos table: {result.fetchone()[0]}")