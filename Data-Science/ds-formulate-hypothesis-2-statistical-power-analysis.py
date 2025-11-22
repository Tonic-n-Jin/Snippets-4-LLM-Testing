from statsmodels.stats.power import TTestPower, NormalIndPower
import numpy as np

class PowerAnalysis:
    def __init__(self, test_type='t-test'):
        self.test_type = test_type
        
    def calculate_sample_size(self, effect_size, alpha=0.05, power=0.8):
        """Calculate required sample size"""
        if self.test_type == 't-test':
            analysis = TTestPower()
            n = analysis.solve_power(
                effect_size=effect_size,
                alpha=alpha,
                power=power,
                nobs1=None,
                ratio=1.0
            )
        else:
            analysis = NormalIndPower()
            n = analysis.solve_power(
                effect_size=effect_size,
                alpha=alpha,
                power=power,
                nobs1=None,
                ratio=1.0
            )
        
        return int(np.ceil(n))
    
    def calculate_mde(self, sample_size, alpha=0.05, power=0.8):
        """Calculate minimum detectable effect"""
        analysis = TTestPower()
        mde = analysis.solve_power(
            effect_size=None,
            alpha=alpha,
            power=power,
            nobs1=sample_size
        )
        
        return mde
    
    def sequential_analysis(self, data_stream, alpha=0.05):
        """Early stopping with sequential analysis"""
        cumsum = 0
        n = 0
        
        # Wald's Sequential Probability Ratio Test
        log_likelihood_ratio = 0
        upper_bound = np.log((1-beta)/alpha)
        lower_bound = np.log(beta/(1-alpha))
        
        for observation in data_stream:
            n += 1
            log_likelihood_ratio += self.calculate_llr(observation)
            
            if log_likelihood_ratio >= upper_bound:
                return {'decision': 'reject_null', 'n': n}
            elif log_likelihood_ratio <= lower_bound:
                return {'decision': 'accept_null', 'n': n}
        
        return {'decision': 'continue', 'n': n}