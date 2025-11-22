from sklearn.model_selection import cross_validate
from sklearn.metrics import classification_report

class ClassificationProblem:
    def __init__(self, X, y, business_context):
        self.X = X
        self.y = y
        self.context = business_context
        self.class_balance = y.value_counts(normalize=True)
        
    def define_metrics(self):
        """Choose metrics based on business impact"""
        if self.context['false_positives_costly']:
            # High precision needed (e.g., fraud detection)
            self.primary_metric = 'precision'
            self.threshold = 0.7  # Conservative threshold
        elif self.context['false_negatives_costly']:
            # High recall needed (e.g., disease detection)
            self.primary_metric = 'recall'
            self.threshold = 0.3  # Aggressive threshold
        else:
            # Balanced approach
            self.primary_metric = 'f1'
            self.threshold = 0.5
    
    def baseline_model(self):
        """Establish baseline performance"""
        from sklearn.dummy import DummyClassifier
        
        # Try different strategies
        strategies = ['most_frequent', 'stratified', 'prior']
        baselines = {}
        
        for strategy in strategies:
            dummy = DummyClassifier(strategy=strategy)
            scores = cross_validate(
                dummy, self.X, self.y,
                cv=5,
                scoring=[self.primary_metric]
            )
            baselines[strategy] = scores[f'test_{self.primary_metric}'].mean()
        
        return baselines