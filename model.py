import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score, f1_score
 
# ── Load Data ────────────────────────────────────────
df = pd.read_csv("youtube_shorts_tiktok_trends_2025.csv_ML.csv")
df = df[df["platform"] == "tiktok"]
 
# ── Features ────────────────────────────────────────
numeric = [
    "title_len", "text_richness", "like_rate", "comment_rate", "share_rate",
    "like_rate_log", "comment_rate_log", "share_rate_log",
    "views_per_day", "likes_per_day", "rel_like", "rel_share", "rel_combo",
    "like_hashtag_interaction", "share_hashtag_interaction", "weekend_hashtag_boost",
]
categorical = ["region_cat", "traffic_source_cat", "device_brand_cat", "creator_tier_cat"]
 
data = df[numeric + categorical + ["trend_label"]].dropna()
print(f"Rows used: {len(data)}")
print(data["trend_label"].value_counts())
 
# ── Encode Target and Features ───────────────────────
le = LabelEncoder()
y = le.fit_transform(data["trend_label"])
X = pd.get_dummies(data[numeric + categorical], columns=categorical, dtype=int)
 
# ── Train and Test Split ───────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Baseline Model
baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
print(f"\nBaseline accuracy: {accuracy_score(y_test, baseline.predict(X_test)):.4f}")
 
# Logistc Regression and Random Forest Models
models = {
    "Logistic Regression": make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42),
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=100, class_weight="balanced", random_state=42, n_jobs=-1
    ),
}
 
# ── Train and Evaluate ───────────────────────────────
for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    print(f"\n{name}: accuracy {accuracy_score(y_test, preds):.4f}, "
          f"macro F1 {f1_score(y_test, preds, average='macro'):.4f}")
    print(classification_report(y_test, preds, target_names=le.classes_))
 
# ── Cross Validation ───────────────────────────────
cv = cross_val_score(models["Random Forest"], X, y, cv=5, scoring="f1_macro", n_jobs=-1)
print(f"Random Forest 5-fold macro F1: {cv.mean():.4f} (+/- {cv.std():.4f})")

# ── Feature Importance ───────────────────────────────
importance = pd.Series(models["Random Forest"].feature_importances_, index=X.columns)
print("\nTop 10 features (Random Forest):")
print(importance.sort_values(ascending=False).head(10).round(4).to_string())