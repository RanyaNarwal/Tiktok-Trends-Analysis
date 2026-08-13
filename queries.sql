-- ── 1. Top 5 Genres by Avg Views ─────────────────────
SELECT 
    genre,
    ROUND(AVG(views), 0) AS avg_views,
    ROUND(AVG(engagement_rate), 4) AS avg_engagement,
    COUNT(*) AS total_videos
FROM tiktok_videos
GROUP BY genre
ORDER BY avg_views DESC
LIMIT 5;


-- ── 2. Viral Videos (Top 10%) ────────────────────────
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

-- ── 3. Best Posting Hour ─────────────────────────────
SELECT 
    upload_hour,
    ROUND(AVG(views), 0) AS avg_views,
    ROUND(AVG(engagement_rate), 4) AS avg_engagement,
    COUNT(*) AS total_videos
FROM tiktok_videos
GROUP BY upload_hour
ORDER BY avg_views DESC
LIMIT 5;

-- ── 4. Best Hashtags ─────────────────────────────────
SELECT 
    hashtag,
    ROUND(AVG(views), 0) AS avg_views,
    ROUND(AVG(engagement_rate), 4) AS avg_engagement,
    COUNT(*) AS total_videos
FROM tiktok_videos
GROUP BY hashtag
ORDER BY avg_views DESC
LIMIT 10;

-- ── 5. Creator Tier Performance ──────────────────────
SELECT 
    creator_tier,
    ROUND(AVG(views), 0) AS avg_views,
    ROUND(AVG(engagement_rate), 4) AS avg_engagement,
    ROUND(AVG(completion_rate), 4) AS avg_completion,
    COUNT(*) AS total_videos
FROM tiktok_videos
GROUP BY creator_tier
ORDER BY avg_views DESC;

-- ── 6. Best Genre + Hour Combo ───────────────────────
SELECT 
    genre,
    upload_hour,
    ROUND(AVG(views), 0) AS avg_views,
    COUNT(*) AS total_videos
FROM tiktok_videos
GROUP BY genre, upload_hour
ORDER BY avg_views DESC
LIMIT 10;

-- ── 7. Monthly Trend Overview ────────────────────────
SELECT 
    year_month,
    ROUND(AVG(views), 0) AS avg_views,
    ROUND(AVG(engagement_rate), 4) AS avg_engagement,
    COUNT(*) AS total_videos
FROM tiktok_videos
GROUP BY year_month
ORDER BY year_month;