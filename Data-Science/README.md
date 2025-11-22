# Data Science Code Snippets

This directory contains code examples for Data Science.

## Table of Contents

- [Problem Definition](#problem-definition)
- [Hypothesis Testing](#hypothesis-testing)
- [EDA Techniques](#eda-techniques)
- [Feature Engineering](#feature-engineering)
- [Algorithm Selection](#algorithm-selection)
- [Hyperparameter Tuning](#hyperparameter-tuning)
- [Evaluation Metrics](#evaluation-metrics)
- [Data Storytelling](#data-storytelling)

---

## Problem Definition

*Translating business questions into analytical frameworks*

### Classification Problem Framework

Predict categories: fraud detection, customer churn, diagnosis

**File:** [`ds-formulate-problem-1-classification-problem-framework.py`](./ds-formulate-problem-1-classification-problem-framework.py)

### Regression Problem Setup

Predict values: price forecasting, demand estimation, risk scoring

**File:** [`ds-formulate-problem-2-regression-problem-setup.py`](./ds-formulate-problem-2-regression-problem-setup.py)

### Clustering Problem Approach

Find groups: customer segmentation, anomaly detection, patterns

**File:** [`ds-formulate-problem-3-clustering-problem-approach.py`](./ds-formulate-problem-3-clustering-problem-approach.py)


---

## Hypothesis Testing

*Making data-driven decisions with statistical rigor*

### A/B Test Implementation

Compare variants to measure impact of changes

**File:** [`ds-formulate-hypothesis-1-ab-test-implementation.py`](./ds-formulate-hypothesis-1-ab-test-implementation.py)

### Statistical Power Analysis

Determine sample size for reliable conclusions

**File:** [`ds-formulate-hypothesis-2-statistical-power-analysis.py`](./ds-formulate-hypothesis-2-statistical-power-analysis.py)

### Multiple Testing Correction

Correct for multiple comparisons to avoid false positives

**File:** [`ds-formulate-hypothesis-3-multiple-testing-correction.py`](./ds-formulate-hypothesis-3-multiple-testing-correction.py)


---

## EDA Techniques

*Systematic exploration to understand data characteristics*

### Comprehensive Distribution Analysis

Understand univariate patterns and outliers

**File:** [`ds-explore-eda-1-comprehensive-distribution-analysis.py`](./ds-explore-eda-1-comprehensive-distribution-analysis.py)

### Advanced Correlation Analysis

Discover relationships between variables

**File:** [`ds-explore-eda-2-advanced-correlation-analysis.py`](./ds-explore-eda-2-advanced-correlation-analysis.py)

### Time Series Analysis

Identify trends and seasonality in time series

**File:** [`ds-explore-eda-3-time-series-analysis.py`](./ds-explore-eda-3-time-series-analysis.py)


---

## Feature Engineering

*Designing, transforming, and validating model inputs*

### Feature Extraction (Time & Aggregates)

Aggregations, time windows, embeddings, domain signals

**File:** [`ds-explore-features-1-feature-extraction-time-aggregates.py`](./ds-explore-features-1-feature-extraction-time-aggregates.py)

### Feature Transformation (ColumnTransformer)

Scaling, normalization, encoding, imputation, binning

**File:** [`ds-explore-features-2-feature-transformation-columntransformer.py`](./ds-explore-features-2-feature-transformation-columntransformer.py)

### Selection & Validation (RFECV)

Importance scoring, correlation, leakage checks,
                        cross-validation

**File:** [`ds-explore-features-3-selection-validation-rfecv.py`](./ds-explore-features-3-selection-validation-rfecv.py)


---

## Algorithm Selection

*Systematically choosing the best model family and hyperparameters*

### Model Benchmarking (Fair Comparison Framework)

Comparing multiple algorithms with consistent preprocessing &
                        CV

**File:** [`ds-model-algorithm-1-model-benchmarking-fair-comparison-framework.py`](./ds-model-algorithm-1-model-benchmarking-fair-comparison-framework.py)

### Automated Selection (Optuna with Early Stopping)

Hyperparameter optimization with early stopping and resource control

**File:** [`ds-model-algorithm-2-automated-selection-optuna-with-early-stopping.py`](./ds-model-algorithm-2-automated-selection-optuna-with-early-stopping.py)

### Production Validation (Latency, Interpretability & Business Metrics)

Business metric alignment, latency constraints, interpretability checks

**File:** [`ds-model-algorithm-3-production-validation-latency-interpretability-business-metrics.py`](./ds-model-algorithm-3-production-validation-latency-interpretability-business-metrics.py)


---

## Hyperparameter Tuning

*Optimizing model configuration for peak performance*

### Grid Search with Cross-Validation

Exhaustive search over parameter grid

**File:** [`ds-model-tuning-1-grid-search-with-cross-validation.py`](./ds-model-tuning-1-grid-search-with-cross-validation.py)

### Randomized Search for Efficiency

Sampling random combinations efficiently

**File:** [`ds-model-tuning-2-randomized-search-for-efficiency.py`](./ds-model-tuning-2-randomized-search-for-efficiency.py)

### Bayesian Optimization with Optuna

Smart search using prior results

**File:** [`ds-model-tuning-3-bayesian-optimization-with-optuna.py`](./ds-model-tuning-3-bayesian-optimization-with-optuna.py)


---

## Evaluation Metrics

*Measuring model performance with appropriate metrics*

### Comprehensive Classification Evaluation

Accuracy, precision, recall, F1, AUC-ROC

**File:** [`ds-validate-metrics-1-comprehensive-classification-evaluation.py`](./ds-validate-metrics-1-comprehensive-classification-evaluation.py)

### Regression Metrics Evaluation

MAE, RMSE, R², MAPE

**File:** [`ds-validate-metrics-2-regression-metrics-evaluation.py`](./ds-validate-metrics-2-regression-metrics-evaluation.py)

### Business Metrics Calculator

Revenue impact, cost savings, user satisfaction

**File:** [`ds-validate-metrics-3-business-metrics-calculator.py`](./ds-validate-metrics-3-business-metrics-calculator.py)


---

## Data Storytelling

*Communicating insights effectively to stakeholders*

### Effective Visualization Framework

Creating clear, actionable charts

**File:** [`ds-validate-storytelling-1-effective-visualization-framework.py`](./ds-validate-storytelling-1-effective-visualization-framework.py)

### Interactive Dashboard with Plotly

Building interactive executive dashboards

**File:** [`ds-validate-storytelling-2-interactive-dashboard-with-plotly.py`](./ds-validate-storytelling-2-interactive-dashboard-with-plotly.py)

### Automated Report Generation

Automated reporting with insights

**File:** [`ds-validate-storytelling-3-automated-report-generation.py`](./ds-validate-storytelling-3-automated-report-generation.py)


---
