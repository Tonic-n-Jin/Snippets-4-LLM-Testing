from scipy.stats import spearmanr, kendalltau
from sklearn.feature_selection import mutual_info_regression

class CorrelationAnalyzer:
    def __init__(self, data):
        self.data = data
        
    def comprehensive_correlation(self):
        """Multiple correlation methods"""
        numerical_data = self.data.select_dtypes(include=[np.number])
        
        correlations = {
            # Linear correlation
            'pearson': numerical_data.corr(method='pearson'),
            
            # Monotonic correlation
            'spearman': numerical_data.corr(method='spearman'),
            
            # Ordinal correlation
            'kendall': numerical_data.corr(method='kendall')
        }
        
        # Mutual information for non-linear relationships
        mi_matrix = self.mutual_information_matrix(numerical_data)
        correlations['mutual_info'] = mi_matrix
        
        return correlations
    
    def find_multicollinearity(self, threshold=0.9):
        """Identify highly correlated feature pairs"""
        corr_matrix = self.data.corr().abs()
        upper_tri = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        )
        
        high_corr_pairs = [
            (col, row, corr_matrix.loc[row, col])
            for col in corr_matrix.columns
            for row in corr_matrix.index
            if upper_tri.loc[row, col] > threshold
        ]
        
        return high_corr_pairs
    
    def partial_correlation(self, x, y, z):
        """Calculate partial correlation controlling for z"""
        from pingouin import partial_corr
        
        df = pd.DataFrame({'x': x, 'y': y, 'z': z})
        return partial_corr(data=df, x='x', y='y', covar='z')