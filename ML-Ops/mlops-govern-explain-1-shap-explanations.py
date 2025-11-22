import shap
import matplotlib.pyplot as plt
import numpy as np

class SHAPExplainer:
    def __init__(self, model, X_background):
        """Initialize SHAP explainer with background data"""
        self.model = model
        self.X_background = X_background

        # Choose appropriate explainer based on model type
        if hasattr(model, 'predict_proba'):
            self.explainer = shap.TreeExplainer(model)
        else:
            self.explainer = shap.KernelExplainer(
                model.predict,
                shap.sample(X_background, 100)
            )

    def explain_prediction(self, X_instance):
        """Explain a single prediction"""
        shap_values = self.explainer.shap_values(X_instance)

        # For binary classification, get values for positive class
        if isinstance(shap_values, list):
            shap_values = shap_values[1]

        return shap_values

    def plot_force_plot(self, X_instance, feature_names=None):
        """Create force plot for single prediction"""
        shap_values = self.explain_prediction(X_instance)

        return shap.force_plot(
            self.explainer.expected_value[1],
            shap_values[0],
            X_instance.iloc[0],
            feature_names=feature_names
        )

    def plot_waterfall(self, X_instance, feature_names=None):
        """Create waterfall plot showing contribution of each feature"""
        shap_values = self.explain_prediction(X_instance)

        shap.waterfall_plot(
            shap.Explanation(
                values=shap_values[0],
                base_values=self.explainer.expected_value[1],
                data=X_instance.iloc[0],
                feature_names=feature_names
            )
        )

    def global_feature_importance(self, X_test, feature_names=None):
        """Calculate global feature importance"""
        shap_values = self.explainer.shap_values(X_test)

        if isinstance(shap_values, list):
            shap_values = shap_values[1]

        # Summary plot
        shap.summary_plot(
            shap_values,
            X_test,
            feature_names=feature_names,
            plot_type="bar"
        )

        # Calculate mean absolute SHAP values
        mean_shap = np.abs(shap_values).mean(axis=0)

        if feature_names:
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': mean_shap
            }).sort_values('importance', ascending=False)

            return importance_df

        return mean_shap

    def dependence_plot(self, feature_name, X_test):
        """Show how a feature affects predictions"""
        shap_values = self.explainer.shap_values(X_test)

        if isinstance(shap_values, list):
            shap_values = shap_values[1]

        shap.dependence_plot(
            feature_name,
            shap_values,
            X_test
        )