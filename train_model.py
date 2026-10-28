"""Reproducible demo training script. Replace the synthetic data with approved data for real use."""
import json
from pathlib import Path

import joblib
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

FEATURE_NAMES = [f"feature_{i}" for i in range(1, 7)]
X, y = make_classification(
    n_samples=2500,
    n_features=6,
    n_informative=4,
    n_redundant=1,
    n_repeated=0,
    n_classes=2,
    weights=[0.55, 0.45],
    class_sep=1.0,
    random_state=42,
)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
])
pipeline.fit(X, y)

joblib.dump(pipeline, MODEL_DIR / "champion_model.joblib")
with (MODEL_DIR / "feature_names.json").open("w", encoding="utf-8") as f:
    json.dump(FEATURE_NAMES, f, indent=2)

print(f"Saved model to {MODEL_DIR / 'champion_model.joblib'}")
print(f"Saved feature names to {MODEL_DIR / 'feature_names.json'}")
