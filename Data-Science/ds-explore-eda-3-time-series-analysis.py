from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, acf, pacf

class TemporalAnalyzer:
    def __init__(self, time_series, freq='D'):
        self.ts = time_series
        self.freq = freq
        
    def decompose_time_series(self):
        """Decompose into trend, seasonal, and residual"""
        decomposition = seasonal_decompose(
            self.ts, 
            model='additive',
            period=self.infer_seasonality_period()
        )
        
        return {
            'trend': decomposition.trend,
            'seasonal': decomposition.seasonal,
            'residual': decomposition.resid,
            'strength_of_trend': self.calculate_trend_strength(decomposition),
            'strength_of_seasonality': self.calculate_seasonal_strength(decomposition)
        }
    
    def test_stationarity(self):
        """Test if time series is stationary"""
        # Augmented Dickey-Fuller test
        adf_result = adfuller(self.ts.dropna())
        
        return {
            'adf_statistic': adf_result[0],
            'p_value': adf_result[1],
            'is_stationary': adf_result[1] < 0.05,
            'critical_values': adf_result[4]
        }
    
    def find_optimal_lags(self):
        """Determine optimal lag for forecasting"""
        # ACF and PACF
        acf_values = acf(self.ts.dropna(), nlags=40)
        pacf_values = pacf(self.ts.dropna(), nlags=40)
        
        # Find significant lags
        confidence_interval = 1.96 / np.sqrt(len(self.ts))
        significant_acf = np.where(np.abs(acf_values) > confidence_interval)[0]
        significant_pacf = np.where(np.abs(pacf_values) > confidence_interval)[0]
        
        return {
            'acf_lags': significant_acf.tolist(),
            'pacf_lags': significant_pacf.tolist(),
            'suggested_ar_order': len(significant_pacf),
            'suggested_ma_order': len(significant_acf)
        }