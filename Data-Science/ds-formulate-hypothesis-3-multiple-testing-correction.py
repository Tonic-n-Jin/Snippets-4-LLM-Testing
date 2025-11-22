from statsmodels.stats.multitest import multipletests

class MultipleTestingCorrection:
    def __init__(self, p_values, alpha=0.05):
        self.p_values = p_values
        self.alpha = alpha
        
    def apply_corrections(self):
        """Apply various multiple testing corrections"""
        corrections = {}
        
        # Bonferroni correction
        bonf_results = multipletests(
            self.p_values, alpha=self.alpha, method='bonferroni'
        )
        corrections['bonferroni'] = {
            'reject': bonf_results[0],
            'adjusted_p': bonf_results[1]
        }
        
        # Benjamini-Hochberg (FDR control)
        fdr_results = multipletests(
            self.p_values, alpha=self.alpha, method='fdr_bh'
        )
        corrections['fdr_bh'] = {
            'reject': fdr_results[0],
            'adjusted_p': fdr_results[1]
        }
        
        # Holm-Bonferroni
        holm_results = multipletests(
            self.p_values, alpha=self.alpha, method='holm'
        )
        corrections['holm'] = {
            'reject': holm_results[0],
            'adjusted_p': holm_results[1]
        }
        
        return corrections
    
    def control_fdr(self, q=0.1):
        """Control False Discovery Rate"""
        m = len(self.p_values)
        sorted_p = np.sort(self.p_values)
        sorted_idx = np.argsort(self.p_values)
        
        # Find threshold
        threshold_idx = None
        for i in range(m-1, -1, -1):
            if sorted_p[i] <= (i+1) * q / m:
                threshold_idx = i
                break
        
        if threshold_idx is not None:
            discoveries = sorted_idx[:threshold_idx+1]
            return {
                'discoveries': discoveries,
                'threshold': sorted_p[threshold_idx],
                'expected_false_discoveries': len(discoveries) * q
            }
        
        return {'discoveries': [], 'threshold': 0}