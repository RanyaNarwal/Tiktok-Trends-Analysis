-- ── Data Check ─────────────────────
SELECT 'total_rows' AS check_name, COUNT(*) AS value FROM tiktok_videos
UNION ALL SELECT 'duplicate_row_ids', COUNT(*) - COUNT(DISTINCT row_id) FROM tiktok_videos
UNION ALL SELECT 'views_zero_or_negative', COUNT(*) FROM tiktok_videos WHERE views <= 0
UNION ALL SELECT 'likes_exceed_views', COUNT(*) FROM tiktok_videos WHERE likes > views
UNION ALL SELECT 'bad_engagement_rate', COUNT(*) FROM tiktok_videos WHERE engagement_rate < 0 OR engagement_rate > 1
UNION ALL SELECT 'bad_upload_hour', COUNT(*) FROM tiktok_videos WHERE upload_hour NOT BETWEEN 0 AND 23
UNION ALL SELECT 'null_genre_or_hashtag', COUNT(*) FROM tiktok_videos WHERE genre IS NULL OR hashtag IS NULL;

-- ── Dataset Overview ─────────────────────
SELECT 
    COUNT(*) AS total_videos,
    COUNT(DISTINCT genre) AS total_genres,
    COUNT(DISTINCT year_month) AS total_months
FROM tiktok_videos;

-- ──  Viral Videos (Top 10%) ────────────────────────
SELECT 
    genre,
    title,
    views,
    likes,
    shares,
    engagement_rate,
    upload_hour,
    duration_sec
FROM tiktok_videos
WHERE views >= 216819
ORDER BY views DESC
LIMIT 20;

-- ── Group Videos by Views (Viral) ────────────────────────
WITH scored AS (
    SELECT *, NTILE(10) OVER (ORDER BY views) AS views_decile
    FROM tiktok_videos
    )
SELECT
    CASE WHEN views_decile = 10 THEN 'Top 10%'  ELSE 'rest' END AS
segment,
    COUNT(*)                          AS videos,
    MIN(views)                        AS min_views,
    ROUND(AVG(views))                 AS avg_views,
    ROUND(AVG(engagement_rate), 4)    AS avg_engagement,
    ROUND(AVG(duration_sec), 1)       AS avg_duration_sec,
    ROUND(AVG(completion_rate), 3)    AS avg_completion,
    ROUND(AVG(has_emoji), 3)          AS emoji_share
FROM scored
GROUP BY CASE WHEN views_decile = 10 THEN 'Top 10%' ELSE 'rest' END
ORDER BY min_views DESC;

-- ── Genres by Avg Views ─────────────────────
SELECT
    genre,
    ROUND(AVG(views), 0) AS avg_views,
    ROUND(AVG(engagement_rate), 4) AS avg_engagement,
    ROUND(AVG(completion_rate), 3) AS avg_completion,
    COUNT(*) AS total_videos
FROM tiktok_videos
GROUP BY genre
ORDER BY avg_views DESC;

-- ── Creator Tier Performance ──────────────────────
SELECT 
    creator_tier,
    ROUND(AVG(views), 0) AS avg_views,
    ROUND(AVG(engagement_rate), 4) AS avg_engagement,
    ROUND(AVG(completion_rate), 4) AS avg_completion,
    COUNT(*) AS total_videos
FROM tiktok_videos
GROUP BY creator_tier
ORDER BY avg_views DESC;


-- ── Video Length ─────────────────────────────
WITH scored AS (
    SELECT 
        views, duration_sec, NTILE(10) OVER (ORDER BY views) AS views_decile,
        CASE
            WHEN duration_sec <= 15 THEN '0-15s'
            WHEN duration_sec <= 30 THEN '16-30s'
            WHEN duration_sec <= 45 THEN '31-45s'
            WHEN duration_sec <= 60 THEN '46-60s'
            ELSE '61-90s'
        END AS length_bucket
    FROM tiktok_videos
)
SELECT 
    length_bucket,
    COUNT(*) AS videos,
    ROUND(AVG(views)) AS avg_views,
    ROUND(100.0 * SUM(CASE WHEN views_decile = 10 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_in_top10
FROM scored
GROUP BY length_bucket
ORDER BY MIN(duration_sec);

-- ── Best Posting Hour Overall─────────────────────────────
SELECT 
    upload_hour,
    ROUND(AVG(views), 0) AS avg_views,
    ROUND(AVG(engagement_rate), 4) AS avg_engagement,
    COUNT(*) AS total_videos
FROM tiktok_videos
GROUP BY upload_hour
ORDER BY avg_views DESC;

-- ── Weekend vs Weekday─────────────────────────────────
WITH wk AS (
    SELECT is_weekend, AVG(views) AS avg_views, COUNT(*) AS total_videos
    FROM tiktok_videos
    GROUP BY is_weekend
)
SELECT
    CASE WHEN is_weekend = 1 THEN 'Weekend' ELSE 'Weekday' END AS day_type,
    ROUND(avg_views, 0) AS avg_views,
    total_videos,
    ROUND(100.0 * (avg_views / (SELECT avg_views FROM wk WHERE is_weekend = 0) - 1), 1) AS pct_vs_weekday
FROM wk
ORDER BY is_weekend;

-- ── Best Genre + Hour Combo (20+ videos) ───────────────────────
SELECT
    genre,
    upload_hour,
    ROUND(AVG(views), 0) AS avg_views,
    COUNT(*) AS total_videos
FROM tiktok_videos
GROUP BY genre, upload_hour
HAVING COUNT(*) >= 20
ORDER BY avg_views DESC;

-- ── Best Hashtags (100+ videos) ─────────────────────────────────
SELECT
    hashtag,
    ROUND(AVG(views), 0) AS avg_views,
    ROUND(AVG(engagement_rate), 4) AS avg_engagement,
    COUNT(*) AS total_videos
FROM tiktok_videos
GROUP BY hashtag
HAVING COUNT(*) >= 100
ORDER BY avg_views DESC;

-- ── Monthly Trend by Genre ───────────────────────
SELECT
    genre,
    year_month,
    ROUND(AVG(views), 0) AS avg_views,
    COUNT(*) AS total_videos
FROM tiktok_videos
GROUP BY genre, year_month
ORDER BY genre, year_month;

-- ── Rising vs Fading Genres ──────────────────────
SELECT
    genre,
    ROUND(AVG(CASE WHEN year_month <= '2025-04' THEN views END), 0) AS jan_apr_avg_views,
    ROUND(AVG(CASE WHEN year_month >= '2025-05' THEN views END), 0) AS may_aug_avg_views,
    ROUND(100.0 * (AVG(CASE WHEN year_month >= '2025-05' THEN views END) /
                   AVG(CASE WHEN year_month <= '2025-04' THEN views END) - 1), 1) AS pct_change
FROM tiktok_videos
GROUP BY genre
ORDER BY pct_change DESC;