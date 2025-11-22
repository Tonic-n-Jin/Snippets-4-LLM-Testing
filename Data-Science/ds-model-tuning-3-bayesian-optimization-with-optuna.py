import optuna
from sklearn.model_selection import cross_val_score
from lightgbm import LGBMClassifier

def objective(trial):
    """Objective function for Bayesian optimization"""
    # Suggest hyperparameters
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'max_depth': trial.suggest_int('max_depth', 3, 15),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'num_leaves': trial.suggest_int('num_leaves', 20, 100),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 100),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-8, 10.0, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-8, 10.0, log=True)
    }

    # Create model with suggested parameters
    model = LGBMClassifier(**params, random_state=42, n_jobs=-1, verbose=-1)

    # Cross-validation score
    scores = cross_val_score(
        model, X_train, y_train,
        cv=5,
        scoring='roc_auc',
        n_jobs=-1
    )

    return scores.mean()

# Create study
study = optuna.create_study(
    direction='maximize',
    pruner=optuna.pruners.MedianPruner()
)

# Optimize
study.optimize(objective, n_trials=100, timeout=3600)

print(f"Best parameters: {study.best_params}")
print(f"Best CV score: {study.best_value:.4f}")

# Plot optimization history
optuna.visualization.plot_optimization_history(study)
optuna.visualization.plot_param_importances(study)