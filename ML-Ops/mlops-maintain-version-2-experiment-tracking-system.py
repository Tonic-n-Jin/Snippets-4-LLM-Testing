import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature

class ExperimentTracker:
    def __init__(self, experiment_name):
        mlflow.set_experiment(experiment_name)
        self.experiment_name = experiment_name

    def track_training(self, model, X_train, y_train, X_val, y_val,
                      params, run_name=None):
        """Comprehensive experiment tracking"""
        with mlflow.start_run(run_name=run_name):
            # 1. Log hyperparameters
            mlflow.log_params(params)

            # 2. Train model
            model.fit(X_train, y_train)

            # 3. Evaluate and log metrics
            train_score = model.score(X_train, y_train)
            val_score = model.score(X_val, y_val)

            mlflow.log_metric("train_accuracy", train_score)
            mlflow.log_metric("val_accuracy", val_score)

            # 4. Log predictions for analysis
            y_pred = model.predict(X_val)
            y_proba = model.predict_proba(X_val)

            # Calculate additional metrics
            from sklearn.metrics import (
                classification_report, roc_auc_score,
                precision_score, recall_score, f1_score
            )

            mlflow.log_metric("precision", precision_score(y_val, y_pred))
            mlflow.log_metric("recall", recall_score(y_val, y_pred))
            mlflow.log_metric("f1", f1_score(y_val, y_pred))
            mlflow.log_metric("auc_roc", roc_auc_score(y_val, y_proba[:, 1]))

            # 5. Log model with signature
            signature = infer_signature(X_train, model.predict(X_train))
            mlflow.sklearn.log_model(
                model,
                "model",
                signature=signature,
                input_example=X_train[:5]
            )

            # 6. Log artifacts
            # Save and log confusion matrix
            import matplotlib.pyplot as plt
            from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

            cm = confusion_matrix(y_val, y_pred)
            disp = ConfusionMatrixDisplay(cm)
            disp.plot()
            plt.savefig("confusion_matrix.png")
            mlflow.log_artifact("confusion_matrix.png")

            # 7. Log feature importance
            if hasattr(model, 'feature_importances_'):
                feature_importance = dict(
                    zip(X_train.columns, model.feature_importances_)
                )
                mlflow.log_dict(feature_importance, "feature_importance.json")

            # 8. Log system info
            import platform
            mlflow.set_tags({
                'python_version': platform.python_version(),
                'platform': platform.platform()
            })

            return mlflow.active_run().info.run_id

    def search_best_run(self, metric='val_accuracy'):
        """Find the best run based on a metric"""
        experiment = mlflow.get_experiment_by_name(self.experiment_name)

        runs = mlflow.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=[f"metrics.{metric} DESC"],
            max_results=1
        )

        return runs.iloc[0] if not runs.empty else None