import optuna
from optuna.integration import XGBoostPruningCallback
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score
import xgboost as xgb

def objective(trial):
    params = {
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-8, 10.0, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-8, 10.0, log=True),
    }
    
    model = xgb.XGBClassifier(**params, random_state=42, n_jobs=-1, eval_metric='auc')
    
    pipeline = Pipeline([
        ('preprocessor', preprocessor),  # same as benchmarking!
        ('model', model)
    ])
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = []
    for train_idx, val_idx in cv.split(X, y):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
        
        pipeline.fit(X_train, y_train)
        preds = pipeline.predict_proba(X_val)[:, 1]
        scores.append(roc_auc_score(y_val, preds))
        
        # Report intermediate score for pruning
        trial.report(scores[-1], step=len(scores))
        if trial.should_prune():
            raise optuna.TrialPruned()
    
    return np.mean(scores)

# Run optimization with timeout and pruning
study = optuna.create_study(direction='maximize', pruner=optuna.pruners.MedianPruner())
study.optimize(objective, n_trials=50, timeout=1800)  # 30 min max

print(f"Best AUC: {study.best_value:.4f}")
print("Best params:", study.best_params)
