import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import make_scorer, roc_auc_score, log_loss
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import warnings
warnings.filterwarnings('ignore')

# Define business-aligned scoring (example: prioritize AUC > 0.85, penalize log loss)
scoring = {
    'AUC': 'roc_auc',
    'LogLoss': make_scorer(log_loss, needs_proba=True, greater_is_better=False),
    'Accuracy': 'accuracy'
}

# Consistent preprocessing (critical for fair comparison!)
numeric_features = ['age', 'income', 'transaction_count']
categorical_features = ['country', 'device_type']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([('imputer', SimpleImputer(strategy='median')),
                          ('scaler', StandardScaler())]), numeric_features),
        ('cat', Pipeline([('imputer', SimpleImputer(strategy='most_frequent')),
                          ('ohe', OneHotEncoder(handle_unknown='ignore'))]), categorical_features)
    ],
    remainder='drop'
)

# Candidate models (all use same random_state for reproducibility)
candidates = {
    'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42),
    'RandomForest': RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1),
    'GradientBoosting': GradientBoostingClassifier(random_state=42),
    'XGBoost': XGBClassifier(n_estimators=300, random_state=42, eval_metric='logloss', n_jobs=-1),
    'LightGBM': LGBMClassifier(n_estimators=300, random_state=42, verbose=-1)
}

# Cross-validation strategy
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

results = []
print("Starting fair model benchmarking...\n")
for name, model in candidates.items():
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', model)
    ])
    
    scores = cross_validate(pipeline, X, y, cv=cv, scoring=scoring, n_jobs=-1, return_train_score=False)
    
    results.append({
        'Model': name,
        'AUC_mean': scores['test_AUC'].mean(),
        'AUC_std': scores['test_AUC'].std(),
        'LogLoss_mean': -scores['test_LogLoss'].mean(),  # negate for readability
        'Fit_time_mean': scores['fit_time'].mean()
    })

# Final leaderboard
leaderboard = pd.DataFrame(results).sort_values('AUC_mean', ascending=False)
print(leaderboard.round(4))
