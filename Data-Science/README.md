# Data Science Code Snippets

This directory contains **production-ready code examples** for Data Science, covering the complete analytical lifecycle from problem formulation to storytelling.

![Data Science](https://img.shields.io/badge/Data-Science-FF6F00?style=for-the-badge&logo=jupyter&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Snippets](https://img.shields.io/badge/Snippets-24-green?style=for-the-badge)

> **Data Science Lifecycle**: Formulate → Explore → Model → Validate → Communicate

---

## 📑 Table of Contents

| **Problem Formulation** | **Data Exploration** | **Model Development** | **Validation & Communication** |
| :--- | :--- | :--- | :--- |
| [🎯 Problem Definition](#-problem-definition) | [🔍 EDA Techniques](#-eda-techniques) | [🤖 Algorithm Selection](#-algorithm-selection) | [📊 Evaluation Metrics](#-evaluation-metrics) |
| [🧪 Hypothesis Testing](#-hypothesis-testing) | [🔧 Feature Engineering](#-feature-engineering) | [⚙️ Hyperparameter Tuning](#️-hyperparameter-tuning) | [📖 Data Storytelling](#-data-storytelling) |

---

## 🎯 Problem Definition

*Translating business questions into analytical frameworks*

### Classification Problem Framework
> Predict categories: fraud detection, customer churn, diagnosis
>
> ![Classification](https://img.shields.io/badge/Type-Classification-blueviolet) ![Binary](https://img.shields.io/badge/Mode-Binary%20%7C%20Multi-blue) ![Supervised](https://img.shields.io/badge/Learning-Supervised-orange)

**File:** [`ds-formulate-problem-1-classification-problem-framework.py`](./ds-formulate-problem-1-classification-problem-framework.py)

### Regression Problem Setup
> Predict values: price forecasting, demand estimation, risk scoring
>
> ![Regression](https://img.shields.io/badge/Type-Regression-blueviolet) ![Continuous](https://img.shields.io/badge/Output-Continuous-blue) ![Supervised](https://img.shields.io/badge/Learning-Supervised-orange)

**File:** [`ds-formulate-problem-2-regression-problem-setup.py`](./ds-formulate-problem-2-regression-problem-setup.py)

### Clustering Problem Approach
> Find groups: customer segmentation, anomaly detection, patterns
>
> ![Clustering](https://img.shields.io/badge/Type-Clustering-blueviolet) ![Groups](https://img.shields.io/badge/Output-Groups-blue) ![Unsupervised](https://img.shields.io/badge/Learning-Unsupervised-orange)

**File:** [`ds-formulate-problem-3-clustering-problem-approach.py`](./ds-formulate-problem-3-clustering-problem-approach.py)


---

## 🧪 Hypothesis Testing

*Making data-driven decisions with statistical rigor*

### A/B Test Implementation
> Compare variants to measure impact of changes
>
> ![Testing](https://img.shields.io/badge/Type-A%2FB%20Test-success) ![Stats](https://img.shields.io/badge/Method-T--Test-blue) ![Scipy](https://img.shields.io/badge/Scipy-8CAAE6?logo=scipy&logoColor=white)

**File:** [`ds-formulate-hypothesis-1-ab-test-implementation.py`](./ds-formulate-hypothesis-1-ab-test-implementation.py)

### Statistical Power Analysis
> Determine sample size for reliable conclusions
>
> ![Power](https://img.shields.io/badge/Type-Power%20Analysis-success) ![Sample](https://img.shields.io/badge/Calc-Sample%20Size-blue) ![StatsModels](https://img.shields.io/badge/StatsModels-4051B5?logoColor=white)

**File:** [`ds-formulate-hypothesis-2-statistical-power-analysis.py`](./ds-formulate-hypothesis-2-statistical-power-analysis.py)

### Multiple Testing Correction
> Correct for multiple comparisons to avoid false positives
>
> ![Correction](https://img.shields.io/badge/Type-Multiple%20Testing-success) ![Bonferroni](https://img.shields.io/badge/Method-Bonferroni%20%7C%20FDR-blue)

**File:** [`ds-formulate-hypothesis-3-multiple-testing-correction.py`](./ds-formulate-hypothesis-3-multiple-testing-correction.py)


---

## 🔍 EDA Techniques

*Systematic exploration to understand data characteristics*

### Comprehensive Distribution Analysis
> Understand univariate patterns and outliers
>
> ![EDA](https://img.shields.io/badge/Type-Distribution-9cf) ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?logo=python&logoColor=white) ![Seaborn](https://img.shields.io/badge/Seaborn-444876?logoColor=white)

**File:** [`ds-explore-eda-1-comprehensive-distribution-analysis.py`](./ds-explore-eda-1-comprehensive-distribution-analysis.py)

### Advanced Correlation Analysis
> Discover relationships between variables
>
> ![EDA](https://img.shields.io/badge/Type-Correlation-9cf) ![Pearson](https://img.shields.io/badge/Method-Pearson%20%7C%20Spearman-blue) ![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)

**File:** [`ds-explore-eda-2-advanced-correlation-analysis.py`](./ds-explore-eda-2-advanced-correlation-analysis.py)

### Time Series Analysis
> Identify trends and seasonality in time series
>
> ![EDA](https://img.shields.io/badge/Type-Time%20Series-9cf) ![Trend](https://img.shields.io/badge/Detect-Trend%20%7C%20Seasonality-blue) ![StatsModels](https://img.shields.io/badge/StatsModels-4051B5?logoColor=white)

**File:** [`ds-explore-eda-3-time-series-analysis.py`](./ds-explore-eda-3-time-series-analysis.py)


---

## 🔧 Feature Engineering

*Designing, transforming, and validating model inputs*

### Feature Extraction (Time & Aggregates)
> Aggregations, time windows, embeddings, domain signals
>
> ![Feature](https://img.shields.io/badge/Type-Extraction-yellowgreen) ![Time](https://img.shields.io/badge/Domain-Time%20%7C%20Aggregates-blue) ![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)

**File:** [`ds-explore-features-1-feature-extraction-time-aggregates.py`](./ds-explore-features-1-feature-extraction-time-aggregates.py)

### Feature Transformation (ColumnTransformer)
> Scaling, normalization, encoding, imputation, binning
>
> ![Feature](https://img.shields.io/badge/Type-Transformation-yellowgreen) ![Pipeline](https://img.shields.io/badge/Tool-ColumnTransformer-blue) ![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?logo=scikitlearn&logoColor=white)

**File:** [`ds-explore-features-2-feature-transformation-columntransformer.py`](./ds-explore-features-2-feature-transformation-columntransformer.py)

### Selection & Validation (RFECV)
> Importance scoring, correlation, leakage checks, cross-validation
>
> ![Feature](https://img.shields.io/badge/Type-Selection-yellowgreen) ![RFECV](https://img.shields.io/badge/Method-RFECV-blue) ![CV](https://img.shields.io/badge/Validation-Cross--Val-orange)

**File:** [`ds-explore-features-3-selection-validation-rfecv.py`](./ds-explore-features-3-selection-validation-rfecv.py)


---

## 🤖 Algorithm Selection

*Systematically choosing the best model family and hyperparameters*

### Model Benchmarking (Fair Comparison Framework)
> Comparing multiple algorithms with consistent preprocessing & CV
>
> ![Benchmark](https://img.shields.io/badge/Type-Benchmarking-critical) ![XGBoost](https://img.shields.io/badge/XGBoost-337AB7?logoColor=white) ![LightGBM](https://img.shields.io/badge/LightGBM-02569B?logoColor=white) ![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?logo=scikitlearn&logoColor=white)

**File:** [`ds-model-algorithm-1-model-benchmarking-fair-comparison-framework.py`](./ds-model-algorithm-1-model-benchmarking-fair-comparison-framework.py)

### Automated Selection (Optuna with Early Stopping)
> Hyperparameter optimization with early stopping and resource control
>
> ![AutoML](https://img.shields.io/badge/Type-AutoML-critical) ![Optuna](https://img.shields.io/badge/Optuna-0081C6?logoColor=white) ![Bayesian](https://img.shields.io/badge/Method-Bayesian-blue)

**File:** [`ds-model-algorithm-2-automated-selection-optuna-with-early-stopping.py`](./ds-model-algorithm-2-automated-selection-optuna-with-early-stopping.py)

### Production Validation (Latency, Interpretability & Business Metrics)
> Business metric alignment, latency constraints, interpretability checks
>
> ![Production](https://img.shields.io/badge/Type-Production-critical) ![Latency](https://img.shields.io/badge/Check-Latency-blue) ![Business](https://img.shields.io/badge/Metrics-Business-orange)

**File:** [`ds-model-algorithm-3-production-validation-latency-interpretability-business-metrics.py`](./ds-model-algorithm-3-production-validation-latency-interpretability-business-metrics.py)


---

## ⚙️ Hyperparameter Tuning

*Optimizing model configuration for peak performance*

### Grid Search with Cross-Validation
> Exhaustive search over parameter grid
>
> ![Tuning](https://img.shields.io/badge/Method-Grid%20Search-informational) ![Exhaustive](https://img.shields.io/badge/Strategy-Exhaustive-blue) ![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?logo=scikitlearn&logoColor=white)

**File:** [`ds-model-tuning-1-grid-search-with-cross-validation.py`](./ds-model-tuning-1-grid-search-with-cross-validation.py)

### Randomized Search for Efficiency
> Sampling random combinations efficiently
>
> ![Tuning](https://img.shields.io/badge/Method-Random%20Search-informational) ![Efficient](https://img.shields.io/badge/Strategy-Random%20Sample-blue) ![Fast](https://img.shields.io/badge/Speed-Fast-green)

**File:** [`ds-model-tuning-2-randomized-search-for-efficiency.py`](./ds-model-tuning-2-randomized-search-for-efficiency.py)

### Bayesian Optimization with Optuna
> Smart search using prior results
>
> ![Tuning](https://img.shields.io/badge/Method-Bayesian-informational) ![Optuna](https://img.shields.io/badge/Optuna-0081C6?logoColor=white) ![Smart](https://img.shields.io/badge/Strategy-Intelligent-blue)

**File:** [`ds-model-tuning-3-bayesian-optimization-with-optuna.py`](./ds-model-tuning-3-bayesian-optimization-with-optuna.py)


---

## 📊 Evaluation Metrics

*Measuring model performance with appropriate metrics*

### Comprehensive Classification Evaluation
> Accuracy, precision, recall, F1, AUC-ROC
>
> ![Metrics](https://img.shields.io/badge/Type-Classification-ff69b4) ![ROC](https://img.shields.io/badge/Metrics-ROC%20%7C%20F1%20%7C%20Precision-blue) ![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?logo=scikitlearn&logoColor=white)

**File:** [`ds-validate-metrics-1-comprehensive-classification-evaluation.py`](./ds-validate-metrics-1-comprehensive-classification-evaluation.py)

### Regression Metrics Evaluation
> MAE, RMSE, R², MAPE
>
> ![Metrics](https://img.shields.io/badge/Type-Regression-ff69b4) ![RMSE](https://img.shields.io/badge/Metrics-RMSE%20%7C%20MAE%20%7C%20R²-blue) ![Error](https://img.shields.io/badge/Focus-Error%20Measures-orange)

**File:** [`ds-validate-metrics-2-regression-metrics-evaluation.py`](./ds-validate-metrics-2-regression-metrics-evaluation.py)

### Business Metrics Calculator
> Revenue impact, cost savings, user satisfaction
>
> ![Metrics](https://img.shields.io/badge/Type-Business-ff69b4) ![Revenue](https://img.shields.io/badge/Impact-Revenue%20%7C%20Cost-blue) ![ROI](https://img.shields.io/badge/Calculate-ROI-green)

**File:** [`ds-validate-metrics-3-business-metrics-calculator.py`](./ds-validate-metrics-3-business-metrics-calculator.py)


---

## 📖 Data Storytelling

*Communicating insights effectively to stakeholders*

### Effective Visualization Framework
> Creating clear, actionable charts
>
> ![Viz](https://img.shields.io/badge/Type-Visualization-purple) ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?logo=python&logoColor=white) ![Seaborn](https://img.shields.io/badge/Seaborn-444876?logoColor=white)

**File:** [`ds-validate-storytelling-1-effective-visualization-framework.py`](./ds-validate-storytelling-1-effective-visualization-framework.py)

### Interactive Dashboard with Plotly
> Building interactive executive dashboards
>
> ![Dashboard](https://img.shields.io/badge/Type-Dashboard-purple) ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white) ![Interactive](https://img.shields.io/badge/Mode-Interactive-blue)

**File:** [`ds-validate-storytelling-2-interactive-dashboard-with-plotly.py`](./ds-validate-storytelling-2-interactive-dashboard-with-plotly.py)

### Automated Report Generation
> Automated reporting with insights
>
> ![Report](https://img.shields.io/badge/Type-Report-purple) ![Automated](https://img.shields.io/badge/Mode-Automated-blue) ![PDF](https://img.shields.io/badge/Format-PDF%20%7C%20HTML-orange)

**File:** [`ds-validate-storytelling-3-automated-report-generation.py`](./ds-validate-storytelling-3-automated-report-generation.py)


---
