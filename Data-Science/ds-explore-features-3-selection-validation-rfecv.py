import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.feature_selection import RFECV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
import matplotlib.pyplot as plt

# RFECV = Recursive Feature Elimination with Cross-Validation
# This technique combines selection (RFE) with validation (CV)
# to find the *optimal* number of features.

# 1. Create a sample dataset
# (20 features, 10 are informative, 10 are noise)
X, y = make_classification(
    n_samples=1000,
    n_features=20,
    n_informative=10,
    n_redundant=5,
    n_repeated=0,
    n_classes=2,
    random_state=42
)
# Create DataFrame with feature names
feature_names = [f'feature_{i}' for i in range(X.shape[1])]
X = pd.DataFrame(X, columns=feature_names)

# 2. Create the estimator and the RFECV object
# The estimator is used to get feature importance
estimator = RandomForestClassifier(n_estimators=100, random_state=42)

# The cross-validation strategy
cv = StratifiedKFold(5)

# Create the RFECV selector
selector = RFECV(
    estimator=estimator,
    step=1,          # Remove 1 feature at a time
    cv=cv,
    scoring='accuracy', # Use accuracy to evaluate feature subsets
    min_features_to_select=1,
    n_jobs=-1
)

# 3. Run the selection
print("Starting feature selection...")
selector.fit(X, y)
print("Feature selection finished.")

# 4. Review results
optimal_n_features = selector.n_features_
selected_features = X.columns[selector.support_]

print(f"Optimal number of features: {optimal_n_features}")
print("Selected features:")
print(list(selected_features))

# Plot the cross-validation score vs. number of features
plt.figure()
plt.title('Recursive Feature Elimination (RFECV)')
plt.xlabel('Number of features selected')
plt.ylabel('CV score (Accuracy)')
plt.plot(range(1, len(selector.cv_results_['mean_test_score']) + 1), selector.cv_results_['mean_test_score'])
plt.axvline(optimal_n_features, color='r', linestyle='--', label='Optimal features')
plt.legend()
plt.show()

# 5. Get the transformed dataset
X_transformed = selector.transform(X)
print(f"Original shape: {X.shape}")
print(f"Transformed shape: {X_transformed.shape}")
