from scipy import stats
import numpy as np

class ABTestAnalyzer:
    def __init__(self, control, treatment, metric_type='continuous'):
        self.control = control
        self.treatment = treatment
        self.metric_type = metric_type
        
    def run_test(self, alpha=0.05):
        """Comprehensive A/B test analysis"""
        results = {
            'sample_size': {
                'control': len(self.control),
                'treatment': len(self.treatment)
            }
        }
        
        if self.metric_type == 'continuous':
            # T-test for continuous metrics
            t_stat, p_value = stats.ttest_ind(
                self.control, self.treatment
            )
            
            # Effect size (Cohen's d)
            pooled_std = np.sqrt(
                (self.control.std()**2 + self.treatment.std()**2) / 2
            )
            effect_size = (
                self.treatment.mean() - self.control.mean()
            ) / pooled_std
            
            # Confidence interval
            diff = self.treatment.mean() - self.control.mean()
            se = np.sqrt(
                self.control.var()/len(self.control) + 
                self.treatment.var()/len(self.treatment)
            )
            ci = stats.t.interval(1-alpha, len(self.control)+len(self.treatment)-2)
            
        elif self.metric_type == 'binary':
            # Chi-square test for proportions
            control_success = self.control.sum()
            treatment_success = self.treatment.sum()
            
            contingency = np.array([
                [control_success, len(self.control) - control_success],
                [treatment_success, len(self.treatment) - treatment_success]
            ])
            
            chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
            
            # Risk ratio and NNT
            control_rate = control_success / len(self.control)
            treatment_rate = treatment_success / len(self.treatment)
            risk_ratio = treatment_rate / control_rate
            nnt = 1 / (treatment_rate - control_rate) if treatment_rate != control_rate else np.inf
        
        results.update({
            'p_value': p_value,
            'significant': p_value < alpha,
            'effect_size': effect_size if self.metric_type == 'continuous' else risk_ratio
        })
        
        return results