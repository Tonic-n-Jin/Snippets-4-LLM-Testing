from jinja2 import Template
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from datetime import datetime

class ReportGenerator:
    def __init__(self, template_path=None):
        self.template = self._load_template(template_path)

    def _load_template(self, path):
        """Load HTML template for report"""
        if path:
            with open(path, 'r') as f:
                return Template(f.read())

        # Default template
        return Template('''
        
        
        
            {{ title }}
            
        
        
            {{ title }}
            Generated on: {{ date }}
            Key Metrics
            {% for metric in metrics %}
            
                {{ metric.value }}
                {{ metric.label }}
            
            {% endfor %}

            Visualizations
            {% for plot in plots %}
            
                {{ plot.title }}
                
            
            {% endfor %}

            Key Insights
            
            {% for insight in insights %}
                {{ insight }}
            {% endfor %}
            
        
        
        ''')

    def _fig_to_base64(self, fig):
        """Convert matplotlib figure to base64 string"""
        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        return image_base64

    def generate_report(self, title, metrics, plots, insights, output_path):
        """Generate HTML report"""
        # Prepare plots
        plot_data = []
        for plot_title, fig in plots.items():
            plot_data.append({
                'title': plot_title,
                'image': self._fig_to_base64(fig)
            })

        # Render template
        html = self.template.render(
            title=title,
            date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            metrics=metrics,
            plots=plot_data,
            insights=insights
        )

        # Save report
        with open(output_path, 'w') as f:
            f.write(html)

        print(f"Report saved to: {output_path}")

# Example usage
generator = ReportGenerator()
generator.generate_report(
    title="Weekly Model Performance Report",
    metrics=[
        {'label': 'Accuracy', 'value': '94.2%'},
        {'label': 'Predictions', 'value': '12,543'},
        {'label': 'Latency (P95)', 'value': '45ms'}
    ],
    plots={'Performance Trend': fig1, 'Confusion Matrix': fig2},
    insights=[
        "Model accuracy improved by 2.1% compared to last week",
        "False positive rate decreased to 3.2%",
        "Peak usage hours: 9-11 AM and 2-4 PM"
    ],
    output_path='weekly_report.html'
)