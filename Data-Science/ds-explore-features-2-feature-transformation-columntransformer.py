import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, KBinsDiscretizer
from sklearn.compose import ColumnTransformer

# This is the standard, production-grade way to handle preprocessing.
# It prevents data leakage and bundles all transformations.

# 1. Define feature lists
numeric_features = ['age', 'last_purchase_value']
categorical_features = ['country', 'account_status']
binned_features = ['time_on_site_seconds']

# 2. Create preprocessing pipelines for each feature type

# --- Numeric Transformer ---
# (Impute missing values, then scale)
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# --- Categorical Transformer ---
# (Impute missing, then one-hot encode)
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# --- Binned (Discretized) Transformer ---
# (Group continuous values into bins)
binned_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('binner', KBinsDiscretizer(n_bins=5, encode='ordinal', strategy='quantile'))
])

# 3. Combine pipelines into a single ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features),
        ('bin', binned_transformer, binned_features)
    ],
    remainder='passthrough' # Keep other columns not listed
)

# --- Example Usage ---
# This 'preprocessor' object is now a complete transformation step.
# It can be put at the start of a final model pipeline.

# Example: model_pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', RandomForestClassifier())])
