from lime import lime_tabular
import numpy as np

class LIMEExplainer:
    def __init__(self, model, X_train, feature_names, class_names):
        """Initialize LIME explainer"""
        self.model = model
        self.feature_names = feature_names
        self.class_names = class_names

        # Create LIME explainer
        self.explainer = lime_tabular.LimeTabularExplainer(
            training_data=X_train.values,
            feature_names=feature_names,
            class_names=class_names,
            mode='classification'
        )

    def explain_instance(self, instance, num_features=10):
        """Explain a single prediction"""
        explanation = self.explainer.explain_instance(
            data_row=instance.values[0],
            predict_fn=self.model.predict_proba,
            num_features=num_features
        )

        return explanation

    def visualize_explanation(self, instance, num_features=10):
        """Create visual explanation"""
        explanation = self.explain_instance(instance, num_features)

        # Show in notebook
        explanation.show_in_notebook(show_table=True)

        # Get as list
        return explanation.as_list()

    def get_explanation_html(self, instance, num_features=10):
        """Get explanation as HTML for dashboard"""
        explanation = self.explain_instance(instance, num_features)
        return explanation.as_html()

    def batch_explain(self, X_test, num_samples=10, num_features=10):
        """Explain multiple predictions"""
        explanations = []

        indices = np.random.choice(len(X_test), num_samples, replace=False)

        for idx in indices:
            instance = X_test.iloc[[idx]]
            exp = self.explain_instance(instance, num_features)
            explanations.append({
                'instance_id': idx,
                'prediction': self.model.predict(instance)[0],
                'probability': self.model.predict_proba(instance)[0],
                'explanation': exp.as_list()
            })

        return explanations