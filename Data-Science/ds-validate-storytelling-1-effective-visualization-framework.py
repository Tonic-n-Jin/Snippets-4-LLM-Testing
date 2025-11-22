import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class DataVisualizer:
    def __init__(self, style='seaborn-v0_8-darkgrid'):
        plt.style.use(style)
        sns.set_palette("husl")

    def create_executive_summary(self, data, key_metrics):
        """Create a one-page executive summary visualization"""
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

        # KPI Cards (top row)
        for idx, (metric_name, metric_value) in enumerate(key_metrics.items()):
            ax = fig.add_subplot(gs[0, idx])
            ax.text(0.5, 0.5, f'{metric_value:,.0f}',
                   ha='center', va='center',
                   fontsize=40, fontweight='bold')
            ax.text(0.5, 0.2, metric_name,
                   ha='center', va='center',
                   fontsize=14, color='gray')
            ax.axis('off')

        # Trend over time (middle left)
        ax1 = fig.add_subplot(gs[1, :2])
        data.groupby('date')['value'].mean().plot(
            ax=ax1, linewidth=2, marker='o'
        )
        ax1.set_title('Performance Trend', fontsize=14, fontweight='bold')
        ax1.set_xlabel('')
        ax1.grid(True, alpha=0.3)

        # Distribution (middle right)
        ax2 = fig.add_subplot(gs[1, 2])
        sns.boxplot(y=data['value'], ax=ax2)
        ax2.set_title('Distribution', fontsize=14, fontweight='bold')

        # Category breakdown (bottom)
        ax3 = fig.add_subplot(gs[2, :])
        category_means = data.groupby('category')['value'].mean().sort_values()
        category_means.plot(kind='barh', ax=ax3, color='steelblue')
        ax3.set_title('Performance by Category', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Average Value')

        plt.suptitle('Executive Summary Dashboard',
                    fontsize=18, fontweight='bold', y=0.98)

        return fig

    def create_comparison_chart(self, before, after, metric_name):
        """Create before/after comparison visualization"""
        fig, ax = plt.subplots(figsize=(10, 6))

        x = ['Before', 'After']
        values = [before, after]
        colors = ['#e74c3c' if after < before else '#2ecc71'] * 2

        bars = ax.bar(x, values, color=colors, alpha=0.7, edgecolor='black')

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:,.0f}',
                   ha='center', va='bottom', fontsize=14, fontweight='bold')

        # Add improvement percentage
        improvement = ((after - before) / before) * 100
        ax.text(0.5, max(values) * 0.5,
               f'{improvement:+.1f}% change',
               ha='center', va='center',
               fontsize=20, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        ax.set_ylabel(metric_name, fontsize=12)
        ax.set_title(f'{metric_name} Comparison', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')

        return fig