# CLAUDE.md - AI Assistant Guide for Snippets-4-LLM-Testing

## Repository Overview

This repository contains **production-ready code snippets**, **educational Jupyter notebooks**, and **workflow automation templates** organized for testing and training Large Language Models (LLMs). The codebase provides real-world examples across three critical domains in modern data and ML infrastructure, plus interactive reinforcement learning tutorials and n8n workflow automation:

- **Data Engineering** (26 snippets)
- **Data Science** (24 snippets)
- **ML Ops** (24 snippets)
- **Reinforcement Learning** (10 Jupyter notebooks)
- **Workflows** (2 n8n automation templates)

**Total**: 74+ code snippets + 10 interactive RL notebooks + 2 workflow templates covering end-to-end workflows

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
├── ML-Ops/                  # 24 snippets for ML operations
│   ├── README.md           # Comprehensive catalog of MLOps snippets
│   ├── mlops-deploy-*      # Model serving and infrastructure
│   ├── mlops-monitor-*     # Observability and drift detection
│   ├── mlops-maintain-*    # Versioning and retraining
│   └── mlops-govern-*      # Compliance and explainability
│
├── Notebooks/               # 10 RL Jupyter notebooks
│   ├── README.md           # Comprehensive RL notebook guide
│   ├── requirements.txt    # RL-specific dependencies
│   ├── reinforcement__value_based__*.ipynb
│   ├── reinforcement__policy_based__*.ipynb
│   ├── reinforcement__actor_critic__*.ipynb
│   └── reinforcement__model_based__*.ipynb
│
└── Workflows/               # 2 n8n workflow automation templates
    ├── README.md           # Comprehensive workflow guide
    ├── prompt-generator.json
    └── semantic-cache-redis-vector-store.json
```

---

## File Naming Convention

### Code Snippets Naming Pattern

All code snippets follow a **strict hierarchical naming pattern**:

#### Pattern Structure
```
{domain}-{category}-{subcategory}-{number}-{description}.{extension}
```

#### Domain Prefixes
- `de-` = Data Engineering
- `ds-` = Data Science
- `mlops-` = ML Ops

#### Examples
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

### Jupyter Notebooks Naming Pattern

Reinforcement Learning notebooks follow a **double-underscore naming pattern**:

#### Pattern Structure
```
reinforcement__{category}__{algorithm}.ipynb
```

#### Categories
- `value_based` = Q-Learning, SARSA, DQN
- `policy_based` = REINFORCE, PPO, TRPO
- `actor_critic` = A2C, A3C
- `model_based` = Dyna-Q, MPC

#### Examples
```
reinforcement__value_based__q_learning.ipynb
│            │          │
│            │          └─ Algorithm name
│            └─────────── Category
└──────────────────────── Domain

reinforcement__policy_based__ppo.ipynb
reinforcement__actor_critic__a2c.ipynb
reinforcement__model_based__dyna_q.ipynb
```

### Workflow Templates Naming Pattern

Workflow automation templates follow a **descriptive, hyphen-separated naming pattern**:

#### Pattern Structure
```
{workflow-type}-{descriptive-name}.json
```

#### Examples
```
prompt-generator.json
│      │
│      └─ Descriptive name
└────────── Workflow type/purpose

semantic-cache-redis-vector-store.json
│         │     │     │
│         │     │     └─ Technology detail (vector-store)
│         │     └─────── Infrastructure (redis)
│         └───────────── Feature (cache)
└─────────────────────── Approach (semantic)
```

**Key Differences from Code Snippets**:
- No hierarchical domain-category-subcategory pattern
- More flexible, descriptive naming
- Technology stack often included in name (e.g., `redis-vector-store`)
- Focus on workflow purpose over categorization

### File Extensions
- `.py` - Python code snippets (majority)
- `.ipynb` - Jupyter notebooks (RL tutorials)
- `.json` - Workflow automation templates (n8n)
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

### Reinforcement Learning (`Notebooks/`)

**Focus**: Educational implementations of fundamental RL algorithms

**Categories**:
1. **Value-Based Methods** (`reinforcement__value_based__`)
   - `q_learning`: Classic tabular RL for discrete spaces
   - `sarsa`: On-policy temporal difference learning
   - `dqn`: Deep Q-Network with experience replay and target networks

2. **Policy-Based Methods** (`reinforcement__policy_based__`)
   - `reinforce`: Monte Carlo policy gradient algorithm
   - `ppo`: Proximal Policy Optimization with clipped objective
   - `trpo`: Trust Region Policy Optimization with KL constraints

3. **Actor-Critic Methods** (`reinforcement__actor_critic__`)
   - `a2c`: Advantage Actor-Critic (synchronous)
   - `a3c`: Asynchronous Advantage Actor-Critic variant

4. **Model-Based Methods** (`reinforcement__model_based__`)
   - `dyna_q`: Integrated planning and learning
   - `mpc`: Model Predictive Control with trajectory optimization

**Key Technologies**: Gymnasium, PyTorch, NumPy, Scipy, Matplotlib

**Notebook Structure**:
Each notebook follows a consistent educational format:
1. **Introduction** - Algorithm principle, definition, use cases, and assumptions
2. **Import Libraries** - Required dependencies with environment setup
3. **Algorithm Implementation** - Core agent class with detailed docstrings
4. **Training Loop** - Episode-based training with progress tracking
5. **Visualization** - Performance plots, learning curves, and policy visualization
6. **Evaluation** - Quantitative metrics and qualitative assessment

**Conventions**:
- Self-contained: Each notebook runs independently
- Reproducible: Fixed random seeds for consistent results
- Configurable: Hyperparameters clearly exposed at agent initialization
- Educational: Extensive markdown cells explaining concepts
- Visualizations: Matplotlib/Seaborn for learning curves and policy heatmaps

### Workflows (`Workflows/`)

**Focus**: Production-ready n8n workflow automation templates for AI-powered systems

**Templates**:
1. **Prompt Generator** (`prompt-generator.json`)
   - AI-guided prompt creation using Google Gemini
   - Multi-stage form collection with iterative refinement
   - Generates structured prompts with 6 sections (Role, Inputs, Tools, Instructions, Constraints, Conclusions)
   - 21 nodes including forms, AI chains, parsers, and merge operations

2. **Semantic Cache** (`semantic-cache-redis-vector-store.json`)
   - Cost-optimized LLM caching using Redis vector search
   - Semantic similarity matching for query variations
   - Dual-path processing: cache hit (instant) vs. cache miss (LLM call)
   - 18 nodes including vector search, embeddings, and conversation memory

**Key Technologies**: n8n, Google Gemini, OpenAI GPT, HuggingFace Inference, Redis, LangChain

**Workflow Structure**:
Unlike code snippets, these are JSON workflow definitions containing:
1. **Nodes** - Individual workflow steps (triggers, AI models, data processing, logic)
2. **Connections** - Data flow between nodes
3. **Credentials** - References to API keys and service credentials (not actual secrets)
4. **Configuration** - Parameters, settings, and customization options
5. **Documentation** - In-workflow Sticky Notes explaining sections

**Conventions**:
- Importable: Can be imported directly into any n8n instance
- Configurable: Credentials and parameters separated from workflow logic
- Documented: Sticky Notes provide in-workflow documentation
- Production-ready: Include error handling, validation, and robust patterns
- Modular: Nodes can be added, removed, or modified independently

**Key Patterns Demonstrated**:
- **Multi-Stage Data Collection**: Progressive disclosure with AI-guided questions
- **Semantic Caching**: Vector similarity search for cost optimization
- **Structured Output Parsing**: Reliable JSON extraction from LLM responses
- **Conversation Memory**: Redis-backed chat history preservation
- **Dual-Path Processing**: Conditional branching based on cache hits/misses

**Use Cases**:
- **Prompt Generator**: Creating consistent AI prompts, building system prompts for agents, standardizing prompt engineering workflows
- **Semantic Cache**: Reducing LLM costs for chat applications, improving response times, handling query variations

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

### When Adding New Notebooks

1. **Choose Category**
   - Determine algorithm category (value-based, policy-based, actor-critic, model-based)
   - Ensure it fits the educational purpose of the collection

2. **Follow Naming Convention**
   - Use pattern: `reinforcement__{category}__{algorithm}.ipynb`
   - Use lowercase with underscores
   - Use descriptive algorithm names

3. **Notebook Quality Checklist**
   - [ ] Introduction cell with principle, definition, use cases, and assumptions
   - [ ] Organized imports with version compatibility notes
   - [ ] Agent class with comprehensive docstrings
   - [ ] Training loop with progress indicators
   - [ ] Multiple visualizations (learning curves, policy plots, metrics)
   - [ ] Evaluation section with quantitative results
   - [ ] Markdown cells explaining key concepts
   - [ ] Configurable hyperparameters
   - [ ] Fixed random seeds for reproducibility

4. **Update Documentation**
   - Add entry to Notebooks/README.md
   - Include in appropriate category section
   - Update performance benchmarks table
   - Verify requirements.txt includes all dependencies

### When Adding New Workflows

1. **Determine Workflow Purpose**
   - Identify the automation use case (prompt engineering, caching, data enrichment, etc.)
   - Ensure it demonstrates a reusable pattern applicable to multiple scenarios
   - Consider if it fits the AI/automation focus of the Workflows folder

2. **Follow Naming Convention**
   - Use pattern: `{workflow-type}-{descriptive-name}.json`
   - Use hyphen-separated lowercase
   - Include technology stack in name when relevant (e.g., `redis-vector-store`)
   - Make names descriptive and self-explanatory

3. **Workflow Quality Checklist**
   - [ ] Uses credential references (never hardcoded API keys)
   - [ ] Includes Sticky Notes documenting workflow sections
   - [ ] Has clear node naming that explains each step's purpose
   - [ ] Implements error handling where appropriate
   - [ ] Uses structured output parsers for LLM responses
   - [ ] Configurable parameters exposed (thresholds, models, etc.)
   - [ ] Tested in n8n instance before committing
   - [ ] Compatible with current n8n LangChain integration

4. **Update Documentation**
   - Add comprehensive entry to Workflows/README.md
   - Include: Purpose, Key Features, Technology Stack, Workflow Flow, Use Cases
   - Document required infrastructure (APIs, databases, services)
   - Provide configuration guidance (similarity thresholds, model selection, etc.)
   - Update performance considerations if applicable

5. **Security & Best Practices**
   - Remove all actual API keys and credentials before exporting
   - Use credential references (e.g., `"id": "{{credentialId}}"`)
   - Document required credential types in README
   - Include setup instructions for required services

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

### When Refactoring Code

When asked to refactor code, follow this systematic approach using the comprehensive rules defined in `/refactoring_rules.json`:

#### 1. Load and Understand Refactoring Rules

Reference the 10 refactoring topics in `refactoring_rules.json`:
- **Critical Priority**: Data Validation, Resilience & Robustness, Correctness & Safety, Security, Testing & CI/CD
- **High Priority**: Design Patterns, Configuration Management, Observability & Metrics, Performance & Scalability
- **Medium Priority**: Real-World Connectivity

#### 2. Analysis Phase

**Before making any changes**:
- **Read the target file(s)** completely to understand current implementation
- **Identify anti-patterns** by comparing code against the `anti_patterns_to_find` in each rule
- **Assess scope**: Determine which refactoring topics apply to the current code
- **Check priority**: Focus on critical > high > medium issues first

**Example anti-patterns to look for**:
```python
# Security (Critical)
API_KEY = "secret123"  # Hardcoded secret

# Data Validation (Critical)
def process(df):  # Unchecked DataFrame
    if 'col' in df: ...  # Manual validation

# Design Patterns (High)
def fetch():
    s3 = boto3.client('s3')  # Hardcoded client instantiation

# Configuration (High)
if drift > 0.05:  # Hardcoded threshold
    raise Alert()
```

#### 3. Planning Phase

Use the TodoWrite tool to create a structured refactoring plan:

```markdown
1. **Critical Fixes** (Must address)
   - Fix SQL injection vulnerability (Correctness & Safety)
   - Add data validation with Pandera (Data Validation)
   - Implement retry logic for API calls (Resilience & Robustness)

2. **High-Priority Improvements** (Should address)
   - Refactor to dependency injection pattern (Design Patterns)
   - Extract hardcoded thresholds to config (Configuration Management)
   - Add structured logging with correlation IDs (Observability & Metrics)

3. **Medium-Priority Optimizations** (Nice to have)
   - Replace DataFrame iteration with vectorized ops (Performance & Scalability)
   - Abstract S3 access via repository pattern (Real-World Connectivity)
```

**Share the plan** with the user for approval before proceeding.

#### 4. Implementation Phase

Apply refactoring rules systematically:

**For each refactoring task**:
1. **Mark todo as in_progress** before starting
2. **Apply the transformation** following the `refactoring_guidance` in the rule
3. **Use the examples** in `refactoring_rules.json` as templates
4. **Cite the principle** when explaining changes
5. **Maintain backward compatibility** unless explicitly asked to break it
6. **Test incrementally** - verify syntax after each change

**Example transformations**:

```python
# Before: Security violation
API_KEY = "secret123"

# After: Following Security rule
API_KEY = os.getenv('API_KEY')
# Principle: "Load secrets from env/secret managers"
```

```python
# Before: No dependency injection
def process():
    s3 = boto3.client('s3')
    return s3.get_object(Bucket='data', Key='file.csv')

# After: Following Design Patterns rule
def process(s3_client):
    return s3_client.get_object(Bucket='data', Key='file.csv')
# Principle: "Pass clients into function args for testability"
```

```python
# Before: Manual data validation
def transform(df):
    if 'user_id' not in df:
        raise ValueError("Missing user_id")
    if df['age'].min() < 0:
        raise ValueError("Invalid age")

# After: Following Data Validation rule
import pandera as pa

class DataSchema(pa.SchemaModel):
    user_id: int = pa.Field()
    age: int = pa.Field(ge=0)

@pa.check_io(df=DataSchema)
def transform(df: pd.DataFrame) -> pd.DataFrame:
    return df
# Principle: "Automate data contracts to prevent silent corruption"
```

#### 5. Validation Phase

After each refactoring:
- **Verify syntax**: Ensure code is syntactically correct
- **Check imports**: Update imports for new dependencies (e.g., `import pandera as pa`)
- **Maintain type hints**: Keep or add type annotations
- **Update docstrings**: Reflect new parameters or behavior
- **No secrets**: Confirm no hardcoded credentials introduced
- **Mark todo completed**: Only after verification passes

#### 6. Documentation Phase

Update relevant documentation:
- **Code comments**: Explain why refactoring was necessary (reference the principle)
- **Docstrings**: Update if function signatures changed
- **README files**: Update if public interfaces changed

#### Refactoring Scope Guidelines

**Choose scope based on user request**:

| User Request | Refactoring Focus | Topics to Apply |
|--------------|-------------------|-----------------|
| "Full refactoring" | Comprehensive | All applicable rules by priority |
| "Make it production-ready" | Critical + High | Security, Validation, Resilience, Config |
| "Make it more testable" | Design + Testing | Design Patterns, Testing & CI/CD |
| "Improve error handling" | Robustness | Resilience & Robustness, Observability |
| "Add validation" | Data Quality | Data Validation, Correctness & Safety |
| "Security audit" | Security | Security, Correctness & Safety |
| "Performance issues" | Optimization | Performance & Scalability |
| "Fix code smells" | Design + Config | Design Patterns, Configuration Management |

#### Important Refactoring Principles

**DO**:
- ✅ Only refactor when explicitly requested or when fixing bugs
- ✅ Read the entire file before suggesting changes
- ✅ Apply rules relevant to the code's purpose
- ✅ Explain each change by citing the principle from `refactoring_rules.json`
- ✅ Make changes incrementally (one topic at a time)
- ✅ Preserve functionality - refactoring should not change behavior
- ✅ Use TodoWrite to track progress and give visibility

**DON'T**:
- ❌ Over-engineer - don't add abstractions for single-use cases
- ❌ Refactor unsolicited - only when user asks
- ❌ Apply all rules blindly - be selective based on context
- ❌ Change behavior - refactoring improves structure, not functionality
- ❌ Skip planning - always create a todo list for non-trivial refactoring
- ❌ Batch completions - mark todos done immediately after finishing each

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

**Reinforcement Learning**:
- `gymnasium` - RL environments (successor to OpenAI Gym)
- `torch` - Deep learning framework for neural network agents
- `scipy` - Optimization for model-based methods

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
   - Explain the four-domain organization (DE, DS, MLOps, RL Notebooks)
   - Clarify the naming conventions for both snippets and notebooks
   - Point to relevant README files

2. **Finding Relevant Code**
   - Use the naming pattern to locate snippets (hyphen-separated for .py files)
   - Use the double-underscore pattern for notebooks (.ipynb files)
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
   - Determine if it's DE, DS, MLOps, or RL Notebook
   - Select or create appropriate category/subcategory
   - Number it sequentially (for snippets) or use descriptive name (for notebooks)

2. **Follow Code Standards**
   - **For Python Snippets:**
     - Include all required imports
     - Add type hints
     - Write docstrings
     - Configure logging
     - Add error handling
     - Use production patterns
   - **For Jupyter Notebooks:**
     - Follow the 6-section structure (intro, imports, implementation, training, visualization, evaluation)
     - Include markdown cells explaining concepts
     - Use configurable hyperparameters
     - Add visualizations for learning curves and performance

3. **Update Documentation**
   - Add entry to appropriate domain README.md
   - Use consistent formatting
   - Provide clear description
   - For notebooks, update the learning path and benchmarks table

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
- Learn Q-Learning basics → `Notebooks/reinforcement__value_based__q_learning.ipynb`
- Implement deep RL → `Notebooks/reinforcement__value_based__dqn.ipynb`
- Understand policy gradients → `Notebooks/reinforcement__policy_based__ppo.ipynb`
- Explore actor-critic methods → `Notebooks/reinforcement__actor_critic__a2c.ipynb`
- Create AI prompts systematically → `Workflows/prompt-generator.json`
- Reduce LLM costs with caching → `Workflows/semantic-cache-redis-vector-store.json`
- **Refactor code to production standards** → See `refactoring_rules.json` and CLAUDE.md "When Refactoring Code"

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

# List all RL notebooks
ls Notebooks/reinforcement__*.ipynb

# List notebooks by category
ls Notebooks/reinforcement__value_based__*.ipynb
ls Notebooks/reinforcement__policy_based__*.ipynb
ls Notebooks/reinforcement__actor_critic__*.ipynb
ls Notebooks/reinforcement__model_based__*.ipynb

# List all Workflows
ls Workflows/*.json
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
- [Notebooks/README.md](Notebooks/README.md) - Complete RL notebooks guide with learning paths
- [Workflows/README.md](Workflows/README.md) - Complete workflow automation guide

### External Documentation

Referenced technologies maintain their own documentation:
- Python libraries: PyPI and official docs
- Cloud platforms: AWS, GCP, Azure documentation
- Orchestration: Airflow, Prefect, Dagster docs
- ML frameworks: scikit-learn, XGBoost, MLflow docs
- RL resources: Gymnasium docs, Sutton & Barto book, OpenAI Spinning Up
- n8n documentation: n8n.io/docs (workflow automation)
- LangChain integration: n8n LangChain nodes documentation

---

## Summary for AI Assistants

This repository is a **curated collection of production-ready code snippets, educational Jupyter notebooks, and workflow automation templates** designed to demonstrate best practices across Data Engineering, Data Science, ML Ops, Reinforcement Learning, and AI Automation domains.

**Key Points**:
1. **Code Snippets**: Strict naming convention `{domain}-{category}-{subcategory}-{number}-{description}`
2. **Notebooks**: Double-underscore pattern `reinforcement__{category}__{algorithm}.ipynb`
3. **Workflows**: Descriptive pattern `{workflow-type}-{descriptive-name}.json` for n8n templates
4. **Refactoring Rules**: Comprehensive refactoring guidelines in `refactoring_rules.json` with 10 topics (critical, high, medium priority)
5. Self-contained, independent code with full error handling and logging
6. Production-ready patterns (retries, validation, monitoring, semantic caching, etc.)
7. Comprehensive README files in each domain directory
8. Type hints, docstrings, and clear comments throughout (code snippets and notebooks)
9. In-workflow documentation with Sticky Notes (workflow templates)
10. No hardcoded secrets - all configuration via parameters or credential references
11. Educational notebooks with step-by-step implementations and visualizations
12. Workflow templates demonstrate AI automation patterns (prompt engineering, cost optimization)

**When working with this codebase**:
- Respect all three naming conventions (snippets vs. notebooks vs. workflows)
- Maintain code quality standards for snippets, educational clarity for notebooks, and security for workflows
- Update README files when adding snippets, notebooks, or workflows
- Keep snippets independent and self-contained
- Ensure notebooks follow the 6-section structure (intro, imports, implementation, training, visualization, evaluation)
- Ensure workflows use credential references (never hardcoded API keys)
- Follow the existing code style and patterns
- **When refactoring**: Use `refactoring_rules.json` as a guide, create a TodoWrite plan, apply rules by priority (critical > high > medium)

This repository serves as both a reference implementation and a testing ground for LLM understanding of production-grade data and ML code, educational RL implementations, and AI-powered workflow automation.
