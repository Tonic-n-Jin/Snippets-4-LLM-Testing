# CLAUDE.md - AI Assistant Guide for Snippets-4-LLM-Testing

## Repository Overview

This repository contains **production-ready code snippets** organized for testing and training Large Language Models (LLMs). The codebase provides real-world examples across three critical domains in modern data and ML infrastructure:

- **Data Engineering** (26 snippets)
- **Data Science** (24 snippets)
- **ML Ops** (24 snippets)

**Total**: 74+ code snippets covering end-to-end workflows

### Repository Purpose

This is a **reference collection** of high-quality, production-grade code patterns that demonstrate:
- Industry best practices
- Common architectural patterns
- Real-world implementation strategies
- Comprehensive coverage of each domain's lifecycle

The code is designed to be:
- **Self-contained**: Each snippet works independently
- **Educational**: Clear comments and docstrings explain concepts
- **Production-ready**: Includes error handling, logging, retries, and robust patterns
- **Modular**: Easy to extract and adapt for specific use cases

---

## Repository Structure

```
Snippets-4-LLM-Testing/
├── Data-Engineering/          # 26 snippets for data pipelines
│   ├── README.md             # Comprehensive catalog of DE snippets
│   ├── de-arch-*             # Architecture patterns (Lambda, Kappa, Data Mesh)
│   ├── de-collect-*          # Data ingestion and sources
│   ├── de-transform-*        # Data processing and quality
│   └── de-deliver-*          # Data serving and observability
│
├── Data-Science/             # 24 snippets for ML/analytics workflows
│   ├── README.md            # Comprehensive catalog of DS snippets
│   ├── ds-formulate-*       # Problem definition and hypothesis testing
│   ├── ds-explore-*         # EDA and feature engineering
│   ├── ds-model-*           # Algorithm selection and tuning
│   └── ds-validate-*        # Evaluation and storytelling
│
└── ML-Ops/                  # 24 snippets for ML operations
    ├── README.md           # Comprehensive catalog of MLOps snippets
    ├── mlops-deploy-*      # Model serving and infrastructure
    ├── mlops-monitor-*     # Observability and drift detection
    ├── mlops-maintain-*    # Versioning and retraining
    └── mlops-govern-*      # Compliance and explainability
```

---

## File Naming Convention

All code snippets follow a **strict hierarchical naming pattern**:

### Pattern Structure
```
{domain}-{category}-{subcategory}-{number}-{description}.{extension}
```

### Domain Prefixes
- `de-` = Data Engineering
- `ds-` = Data Science
- `mlops-` = ML Ops

### Examples
```
de-collect-sources-2-robust-api-client-pagination.py
│  │       │       │ │
│  │       │       │ └─ Description
│  │       │       └─── Sequential number (1, 2, 3)
│  │       └─────────── Subcategory
│  └─────────────────── Category
└────────────────────── Domain

ds-model-algorithm-1-model-benchmarking-fair-comparison-framework.py
mlops-deploy-serving-2-real-time-api-with-fastapi.py
```

### File Extensions
- `.py` - Python code snippets (majority)
- `.yml` / `.yaml` - Configuration files (Kubernetes, alerts)
- `.dockerfile` - Docker configurations
- `.md` - Documentation

---

## Code Conventions & Style

### Python Code Standards

1. **Imports**
   - Standard library imports first
   - Third-party imports second
   - Organized logically (e.g., logging, typing, specific libraries)
   ```python
   import logging
   import time
   from typing import Generator, Dict, Any

   import requests
   import pandas as pd
   from sklearn.model_selection import cross_validate
   ```

2. **Type Hints**
   - Used consistently for function parameters and return types
   - Helps with code clarity and IDE support
   ```python
   def get_paginated_data(self, endpoint: str, params: Dict[str, Any] = None) -> Generator[Dict[str, Any], None, None]:
   ```

3. **Docstrings**
   - Classes and key methods have docstrings
   - Explain the "what" and "why"
   ```python
   class ApiClient:
       """
       Handles robust, paginated data ingestion from a third-party REST API.
       Includes retries, backoff, and auth.
       """
   ```

4. **Logging**
   - Configured at module level
   - INFO level by default
   - Structured log messages
   ```python
   logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
   logging.info(f"API Client initialized for {base_url}")
   ```

5. **Error Handling**
   - Comprehensive try-except blocks
   - Specific exception handling
   - Graceful degradation
   ```python
   try:
       response = self.session.get(url)
       response.raise_for_status()
   except requests.exceptions.HTTPError as e:
       logging.error(f"HTTP error fetching {url}: {e}")
   ```

6. **Production Patterns**
   - Retry logic with exponential backoff
   - Rate limit handling
   - Session management
   - Configuration via parameters (not hardcoded)

### Configuration Files

YAML files use standard indentation (2 spaces) and include comments explaining configuration choices.

---

## Domain-Specific Guidelines

### Data Engineering (`Data-Engineering/`)

**Focus**: Building reliable, scalable data pipelines

**Categories**:
1. **Architecture** (`de-arch-`)
   - `patterns-*`: Lambda, Kappa, Data Mesh architectures
   - `infra-*`: Spark, storage, orchestration (Airflow)

2. **Collection** (`de-collect-`)
   - `ingest-*`: CDC, Kafka producers, batch ETL
   - `sources-*`: Database connectors, API clients, S3 access

3. **Transformation** (`de-transform-`)
   - `quality-*`: Data validation, completeness, consistency checks
   - `process-*`: Cleansing, enrichment, aggregation

4. **Delivery** (`de-deliver-`)
   - `serving-*`: Semantic layers, feature stores, API gateways
   - `observe-*`: Metrics, drift detection, SLA monitoring

**Key Technologies**: Spark, Kafka, Airflow, Pandera, FastAPI, S3

### Data Science (`Data-Science/`)

**Focus**: End-to-end analytical and ML workflows

**Categories**:
1. **Formulation** (`ds-formulate-`)
   - `problem-*`: Classification, regression, clustering frameworks
   - `hypothesis-*`: A/B testing, power analysis, multiple testing

2. **Exploration** (`ds-explore-`)
   - `eda-*`: Distribution analysis, correlations, time series
   - `features-*`: Extraction, transformation, selection (RFECV)

3. **Modeling** (`ds-model-`)
   - `algorithm-*`: Benchmarking, automated selection, production validation
   - `tuning-*`: Grid search, random search, Bayesian optimization

4. **Validation** (`ds-validate-`)
   - `metrics-*`: Classification, regression, business metrics
   - `storytelling-*`: Visualization, dashboards, automated reports

**Key Technologies**: pandas, scikit-learn, XGBoost, LightGBM, Optuna, Plotly

### ML Ops (`ML-Ops/`)

**Focus**: Production ML systems and governance

**Categories**:
1. **Deployment** (`mlops-deploy-`)
   - `serving-*`: Batch predictions, FastAPI endpoints, stream processing
   - `infra-*`: Docker, Kubernetes, serverless functions

2. **Monitoring** (`mlops-monitor-`)
   - `observe-*`: Comprehensive monitoring, tracing, alerting
   - `drift-*`: Data drift, concept drift, performance degradation

3. **Maintenance** (`mlops-maintain-`)
   - `retrain-*`: Scheduled, trigger-based, online learning
   - `version-*`: Model registry (MLflow), experiment tracking, lineage

4. **Governance** (`mlops-govern-*)
   - `comply-*`: Audit trails, data privacy (GDPR), bias detection
   - `explain-*`: SHAP, LIME, counterfactual explanations

**Key Technologies**: FastAPI, MLflow, Docker, Kubernetes, Faust, SHAP, LIME

---

## Development Workflows

### When Adding New Snippets

1. **Choose Appropriate Domain**
   - Determine if it's DE, DS, or MLOps
   - If unclear, consider the primary use case

2. **Follow Naming Convention**
   - Use existing category/subcategory if applicable
   - Create new category only if necessary
   - Number sequentially within subcategory
   - Use descriptive, hyphenated names

3. **Code Quality Checklist**
   - [ ] Imports organized properly
   - [ ] Type hints on functions
   - [ ] Docstrings for classes and key methods
   - [ ] Logging configured and used
   - [ ] Error handling included
   - [ ] Production-ready patterns (retries, validation, etc.)
   - [ ] Comments explain non-obvious logic
   - [ ] No hardcoded credentials or secrets

4. **Update README**
   - Add entry to appropriate domain README.md
   - Include descriptive title
   - Link to the file
   - Place in correct category section

### When Modifying Existing Snippets

1. **Maintain Backward Compatibility**
   - Don't change file names (breaks references)
   - Preserve existing function signatures
   - Add new features as optional parameters

2. **Update Documentation**
   - Update docstrings if behavior changes
   - Update comments if logic changes
   - Update README if description changes

3. **Test Changes**
   - Ensure snippet still runs independently
   - Verify imports are available
   - Check error handling still works

### When Reviewing Code

**Look for**:
- Proper error handling
- Logging at appropriate levels
- Type hints on public interfaces
- Clear variable names
- Comments explaining "why" not "what"
- No hardcoded secrets
- Production-ready patterns (retries, timeouts, etc.)

---

## Key Architectural Patterns

### Data Engineering Patterns

1. **Lambda Architecture** (`de-arch-patterns-1-lambda-architecture-implementation.py`)
   - Batch layer: complete, accurate historical processing
   - Speed layer: real-time approximate results
   - Serving layer: merged views

2. **Kappa Architecture** (`de-arch-patterns-2-kappa-architecture-stream-processing.py`)
   - Stream-first processing
   - Replay capabilities for corrections
   - Simplified infrastructure

3. **Data Mesh** (`de-arch-patterns-3-data-mesh-domain-implementation.py`)
   - Domain-oriented ownership
   - Data as a product
   - Self-serve infrastructure

### Data Science Patterns

1. **Fair Model Comparison** (`ds-model-algorithm-1-model-benchmarking-fair-comparison-framework.py`)
   - Consistent preprocessing for all models
   - Same cross-validation strategy
   - Standardized metrics
   - Reproducible results (fixed random_state)

2. **Feature Engineering Pipeline** (`ds-explore-features-2-feature-transformation-columntransformer.py`)
   - ColumnTransformer for different feature types
   - Proper train/test separation
   - Avoid data leakage

### ML Ops Patterns

1. **Model Serving** (FastAPI pattern in `mlops-deploy-serving-2-real-time-api-with-fastapi.py`)
   - Pydantic for validation
   - Health check endpoints
   - Error handling at API level
   - Model loaded at startup

2. **Drift Detection** (`mlops-monitor-drift-*`)
   - Data drift: input distribution changes
   - Concept drift: relationship changes
   - Performance drift: accuracy degradation

---

## Common Technologies & Dependencies

### Core Python Libraries

**Data Processing**:
- `pandas` - DataFrames and data manipulation
- `numpy` - Numerical computing

**Machine Learning**:
- `scikit-learn` - Classical ML algorithms and utilities
- `xgboost` - Gradient boosting
- `lightgbm` - Fast gradient boosting
- `optuna` - Hyperparameter optimization

**Data Engineering**:
- `pyspark` - Distributed data processing
- `kafka-python` / `confluent-kafka` - Event streaming
- `sqlalchemy` - Database abstraction
- `boto3` - AWS SDK (S3, etc.)
- `pandera` - Data validation

**ML Ops**:
- `fastapi` - Web APIs
- `mlflow` - Experiment tracking and model registry
- `shap` - Model explanations
- `lime` - Local explanations
- `prometheus_client` - Metrics

**Orchestration**:
- `apache-airflow` - Workflow management
- `prefect` / `dagster` - Modern workflow engines

**Visualization**:
- `matplotlib` - Static plots
- `seaborn` - Statistical visualizations
- `plotly` - Interactive dashboards

### Infrastructure Technologies

- **Docker** - Containerization
- **Kubernetes** - Container orchestration
- **AWS Lambda** - Serverless functions
- **Prometheus** - Metrics collection
- **Grafana** - Metrics visualization

---

## AI Assistant Guidelines

### When Asked About This Repository

1. **Understanding Structure**
   - Explain the three-domain organization
   - Clarify the naming convention
   - Point to relevant README files

2. **Finding Relevant Code**
   - Use the naming pattern to locate snippets
   - Check the domain README for descriptions
   - Consider the category and subcategory

3. **Explaining Code**
   - Reference the specific file name
   - Explain the production patterns used
   - Highlight key concepts and best practices
   - Point out error handling and logging

4. **Suggesting Modifications**
   - Maintain the existing code style
   - Preserve error handling patterns
   - Keep type hints and docstrings
   - Update comments if logic changes
   - Follow the naming convention

### When Creating New Snippets

1. **Choose Domain and Category**
   - Determine if it's DE, DS, or MLOps
   - Select or create appropriate category/subcategory
   - Number it sequentially

2. **Follow Code Standards**
   - Include all required imports
   - Add type hints
   - Write docstrings
   - Configure logging
   - Add error handling
   - Use production patterns

3. **Update Documentation**
   - Add entry to domain README.md
   - Use consistent formatting
   - Provide clear description

### When Debugging or Reviewing

**Check for**:
- Missing imports
- Hardcoded credentials (should be parameterized)
- Missing error handling
- Lack of logging
- No type hints
- Missing docstrings
- Unclear variable names

**Common Patterns to Look For**:
- Retry logic with exponential backoff
- Session/connection pooling
- Rate limit handling
- Data validation before processing
- Graceful degradation on errors

---

## Testing Considerations

### Snippet Independence

Each snippet should be:
- **Self-contained**: Runnable with minimal setup
- **Well-documented**: Clear what it does and why
- **Example-driven**: Uses example data/parameters

### Dependencies

Snippets assume common libraries are installed but don't include:
- `requirements.txt` files (since they're snippets, not projects)
- Database setup scripts
- Infrastructure provisioning

When using snippets:
1. Install required libraries (visible in imports)
2. Replace placeholders (API keys, URLs, etc.)
3. Provide necessary data/connections

---

## Git Workflow

### Branch Naming

- Feature branches: `claude/claude-md-*` (AI assistant generated)
- Use descriptive names for manual branches

### Commit Messages

- Clear, concise descriptions
- Reference specific files when applicable
- Example: "Add SHAP explanations snippet for MLOps governance"

### Pull Requests

- Update relevant README files
- Ensure new snippets follow conventions
- Test that code is syntactically correct
- Verify no secrets are committed

---

## Quick Reference

### Find a Snippet By Topic

**I need to...**
- Build an API for data access → `de-deliver-serving-3-data-api-gateway-fastapi.py`
- Detect data drift → `mlops-monitor-drift-1-data-drift-detection.py`
- Compare multiple ML models → `ds-model-algorithm-1-model-benchmarking-fair-comparison-framework.py`
- Set up Kafka producer → `de-collect-ingest-2-application-event-producer-kafka.py`
- Explain model predictions → `mlops-govern-explain-1-shap-explanations.py`
- Validate data quality → `de-transform-quality-2-accuracy-value-validation-with-pandera.py`
- Create an A/B test → `ds-formulate-hypothesis-1-ab-test-implementation.py`
- Deploy on Kubernetes → `mlops-deploy-infra-2-kubernetes-deployment.yml`

### Common File Patterns

```bash
# List all Data Engineering snippets
ls Data-Engineering/de-*.py

# Find all serving-related code
find . -name "*serving*.py"

# Find all Kubernetes configs
find . -name "*.yml"

# List snippets by category
ls Data-Engineering/de-collect-*
ls Data-Science/ds-model-*
ls ML-Ops/mlops-govern-*
```

---

## Maintenance Notes

### Repository Health

**Current State**: Active, well-organized snippet collection

**To Maintain Quality**:
1. Regularly review for deprecated library usage
2. Update to latest best practices
3. Ensure all snippets remain independent
4. Keep README files synchronized with code

### Evolution Strategy

**Add new snippets for**:
- Emerging technologies (e.g., new ML frameworks)
- Common production patterns not yet covered
- Updated best practices

**Don't add**:
- Highly specific use cases
- Experimental or unstable patterns
- Duplicate functionality without clear improvement

---

## Additional Resources

### Domain README Files

- [Data-Engineering/README.md](Data-Engineering/README.md) - Complete DE catalog
- [Data-Science/README.md](Data-Science/README.md) - Complete DS catalog
- [ML-Ops/README.md](ML-Ops/README.md) - Complete MLOps catalog

### External Documentation

Referenced technologies maintain their own documentation:
- Python libraries: PyPI and official docs
- Cloud platforms: AWS, GCP, Azure documentation
- Orchestration: Airflow, Prefect, Dagster docs
- ML frameworks: scikit-learn, XGBoost, MLflow docs

---

## Summary for AI Assistants

This repository is a **curated collection of production-ready code snippets** designed to demonstrate best practices across Data Engineering, Data Science, and ML Ops domains.

**Key Points**:
1. Strict naming convention: `{domain}-{category}-{subcategory}-{number}-{description}`
2. Self-contained, independent snippets with full error handling and logging
3. Production-ready patterns (retries, validation, monitoring, etc.)
4. Comprehensive README files in each domain directory
5. Type hints, docstrings, and clear comments throughout
6. No hardcoded secrets - all configuration via parameters

**When working with this codebase**:
- Respect the naming convention
- Maintain code quality standards
- Update README files when adding snippets
- Keep snippets independent and self-contained
- Follow the existing code style and patterns

This repository serves as both a reference implementation and a testing ground for LLM understanding of production-grade data and ML code.
