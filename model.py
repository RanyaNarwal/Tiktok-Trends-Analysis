import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score, f1_score

# ── Load ML-ready dataset ────────────────────────────
print("Dataset")
df = pd.read_csv("youtube_shorts_tiktok_trends_2025.csv_ML.csv")
df = df[df["platform"] == "tiktok"]
print(f"Rows loaded: {len(df)}")

# ── Check target variable ────────────────────────────
print("\nTrend Label values:")
print(df["trend_label"].value_counts())

# ── Encode target ────────────────────────────────────
le = LabelEncoder()
df["target"] = le.fit_transform(df["trend_label"].astype(str))
print("\nEncoded labels:", dict(zip(le.classes_, le.transform(le.classes_))))

# ── Select Features ──────────────────────────────────
features = [
    "title_len",
    "text_richness",
    "like_rate",
    "comment_rate",
    "share_rate",
    "like_rate_log",
    "comment_rate_log",
    "share_rate_log",
    "views_per_day",
    "likes_per_day",
    "rel_like",
    "rel_share",
    "rel_combo",
    "like_hashtag_interaction",
    "share_hashtag_interaction",
    "weekend_hashtag_boost",
    "platform_cat",
    "region_cat",
    "traffic_source_cat",
    "device_brand_cat",
    "creator_tier_cat"
]

df_model = df[features + ["target"]].dropna()
print(f"\nClean rows for modeling: {len(df_model)}")

# ── Split Data ───────────────────────────────────────
X = df_model[features]
y = df_model["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")


# ── Model 1: Baseline Classification ─────────────────────
print("\n── Baseline Classification ──")
base = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
print(f"Baseline accuracy: {accuracy_score(y_test, base.predict(X_test)):.4f}")

# ── Model 2: Logistic Regression ─────────────────────
print("\n── Logistic Regression ──")
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train, y_train)
lr_preds = lr.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, lr_preds):.4f}")
print(classification_report(y_test, lr_preds, target_names=le.classes_))

# ── Model 3: Random Forest ───────────────────────────
print("\n── Random Forest ──")
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_preds = rf.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, rf_preds):.4f}")
print(classification_report(y_test, rf_preds, target_names=le.classes_))

# ── Feature Importance ───────────────────────────────
print("\n── Most Important Features (Random Forest) ──")
importance = pd.DataFrame({
    "feature": features,
    "importance": rf.feature_importances_
}).sort_values("importance", ascending=False)
print(importance.to_string())