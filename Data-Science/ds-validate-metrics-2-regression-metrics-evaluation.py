from sklearn.metrics import (
    mean_absolute_error, mean_squared_error,
    r2_score, mean_absolute_percentage_error
)
import numpy as np

class RegressionEvaluator:
    def __init__(self, y_true, y_pred):
        self.y_true = y_true
        self.y_pred = y_pred

    def compute_all_metrics(self):
        """Calculate comprehensive regression metrics"""
        metrics = {}

        # Basic metrics
        metrics['mae'] = mean_absolute_error(self.y_true, self.y_pred)
        metrics['mse'] = mean_squared_error(self.y_true, self.y_pred)
        metrics['rmse'] = np.sqrt(metrics['mse'])
        metrics['r2'] = r2_score(self.y_true, self.y_pred)

        # Percentage errors
        metrics['mape'] = mean_absolute_percentage_error(
            self.y_true, self.y_pred
        ) * 100

        # Adjusted R²
        n = len(self.y_true)
        p = 1  # number of predictors
        metrics['adjusted_r2'] = 1 - (1 - metrics['r2']) * (n - 1) / (n - p - 1)

        # Mean Absolute Scaled Error (MASE)
        naive_forecast = np.roll(self.y_true, 1)[1:]
        naive_mae = mean_absolute_error(self.y_true[1:], naive_forecast)
        metrics['mase'] = metrics['mae'] / naive_mae if naive_mae != 0 else np.inf

        # Residual analysis
        residuals = self.y_true - self.y_pred
        metrics['residual_std'] = np.std(residuals)
        metrics['residual_mean'] = np.mean(residuals)

        return metrics

    def plot_diagnostics(self):
        """Plot regression diagnostic plots"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

        residuals = self.y_true - self.y_pred

        # Actual vs Predicted
        ax1.scatter(self.y_true, self.y_pred, alpha=0.5)
        ax1.plot([self.y_true.min(), self.y_true.max()],
                [self.y_true.min(), self.y_true.max()], 'r--')
        ax1.set_xlabel('Actual')
        ax1.set_ylabel('Predicted')
        ax1.set_title('Actual vs Predicted')

        # Residuals vs Predicted
        ax2.scatter(self.y_pred, residuals, alpha=0.5)
        ax2.axhline(y=0, color='r', linestyle='--')
        ax2.set_xlabel('Predicted')
        ax2.set_ylabel('Residuals')
        ax2.set_title('Residual Plot')

        # Histogram of Residuals
        ax3.hist(residuals, bins=30, edgecolor='black')
        ax3.set_xlabel('Residuals')
        ax3.set_ylabel('Frequency')
        ax3.set_title('Distribution of Residuals')

        # Q-Q Plot
        from scipy import stats
        stats.probplot(residuals, dist="norm", plot=ax4)
        ax4.set_title('Q-Q Plot')

        plt.tight_layout()
        return fig