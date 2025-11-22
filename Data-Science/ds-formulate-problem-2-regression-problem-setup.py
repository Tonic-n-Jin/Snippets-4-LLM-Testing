from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np

class RegressionProblem:
    def __init__(self, X, y, business_context):
        self.X = X
        self.y = y
        self.context = business_context
        
    def analyze_target_distribution(self):
        """Understand target variable characteristics"""
        analysis = {
            'mean': self.y.mean(),
            'median': self.y.median(),
            'std': self.y.std(),
            'skewness': self.y.skew(),
            'outliers': self.detect_outliers()
        }
        
        # Check if transformation needed
        if abs(analysis['skewness']) > 1:
            self.y_transformed = np.log1p(self.y)
            analysis['transformation'] = 'log'
        
        return analysis
    
    def define_business_metrics(self):
        """Convert ML metrics to business impact"""
        baseline_mae = mean_absolute_error(
            self.y, 
            [self.y.mean()] * len(self.y)
        )
        
        return {
            'baseline_error': baseline_mae,
            'dollar_impact': baseline_mae * self.context['unit_cost'],
            'acceptable_error': self.context['tolerance'],
            'required_r2': self.context.get('min_r2', 0.7)
        }
    
    def create_evaluation_framework(self):
        """Custom evaluation for business needs"""
        def business_scorer(y_true, y_pred):
            mae = mean_absolute_error(y_true, y_pred)
            # Penalize underestimation more than overestimation
            underestimation = (y_true - y_pred).clip(0).mean()
            return mae + 2 * underestimation
        
        return business_scorer