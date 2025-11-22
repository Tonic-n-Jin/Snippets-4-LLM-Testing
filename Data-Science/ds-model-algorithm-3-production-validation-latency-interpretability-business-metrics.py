import time
import shap
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt

# Final candidate (from benchmarking or Optuna)
final_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', XGBClassifier(**study.best_params, random_state=42, n_jobs=-1))
])
final_pipeline.fit(X_train, y_train)

# 1. Inference Latency Check (p99 < 50ms target)
latencies = []
for _ in range(1000):
    sample = X_test.sample(1)
    start = time.perf_counter()
    _ = final_pipeline.predict_proba(sample)
    latencies.append((time.perf_counter() - start) * 1000)

p99_latency = np.percentile(latencies, 99)
print(f"P99 Inference Latency: {p99_latency:.2f} ms")
assert p99_latency < 50, "Model too slow for real-time serving!"

# 2. SHAP Explainability (Global + Local)
explainer = shap.TreeExplainer(final_pipeline.named_steps['model'])
shap_values = explainer.shap_values(final_pipeline.named_steps['preprocessor'].transform(X_test.sample(1000)))

shap.summary_plot(shap_values, X_test.sample(1000), max_display=10)

# 3. Business Metric Simulation (Expected Uplift)
# Example: fraud detection → value saved = TP * avg_fraud_amount
avg_fraud_amount = 2400
y_prob = final_pipeline.predict_proba(X_test)[:, 1]
threshold = 0.65  # tuned via profit curve
y_pred = (y_prob >= threshold).astype(int)

tp = ((y_pred == 1) & (y_test == 1)).sum()
expected_value_saved = tp * avg_fraud_amount
print(f"Expected annual value saved: ${expected_value_saved * 365:,.0f}")

# Final production decision checklist
validation_report = {
    "AUC": roc_auc_score(y_test, y_prob),
    "P99_Latency_ms": p99_latency,
    "Interpretability": "SHAP values computed",
    "Business_Value_Annual": expected_value_saved * 365,
    "Deploy_Ready": p99_latency < 50 and roc_auc_score(y_test, y_prob) > 0.82
}
print("\nProduction Validation Report:")
print(validation_report)
