import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

class ModelRegistry:
    def __init__(self, tracking_uri='http://localhost:5000'):
        mlflow.set_tracking_uri(tracking_uri)

    def register_model(self, model, model_name, metadata):
        """Register model with version control"""
        with mlflow.start_run():
            # Log parameters
            mlflow.log_params(metadata['hyperparameters'])

            # Log metrics
            mlflow.log_metrics(metadata['metrics'])

            # Log model
            mlflow.sklearn.log_model(
                model,
                artifact_path="model",
                registered_model_name=model_name
            )

            # Log additional artifacts
            mlflow.log_artifact(metadata['confusion_matrix_path'])

            # Add tags
            mlflow.set_tags({
                'model_type': metadata.get('model_type', 'classifier'),
                'environment': metadata.get('environment', 'production'),
                'author': metadata.get('author', 'data-science-team')
            })

            run_id = mlflow.active_run().info.run_id

        return run_id

    def promote_model_stage(self, model_name, version, stage):
        """Promote model to different stage"""
        client = mlflow.tracking.MlflowClient()

        client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage  # 'Staging', 'Production', 'Archived'
        )

    def load_production_model(self, model_name):
        """Load the production version of a model"""
        model_uri = f"models:/{model_name}/Production"
        model = mlflow.sklearn.load_model(model_uri)
        return model

    def compare_models(self, model_name, versions):
        """Compare multiple model versions"""
        client = mlflow.tracking.MlflowClient()

        comparison = []
        for version in versions:
            model_version = client.get_model_version(model_name, version)
            run = client.get_run(model_version.run_id)

            comparison.append({
                'version': version,
                'stage': model_version.current_stage,
                'metrics': run.data.metrics,
                'params': run.data.params,
                'created_at': model_version.creation_timestamp
            })

        return comparison