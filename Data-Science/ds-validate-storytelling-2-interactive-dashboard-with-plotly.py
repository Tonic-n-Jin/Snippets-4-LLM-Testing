import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

class InteractiveDashboard:
    def __init__(self, data):
        self.data = data

    def create_dashboard(self):
        """Create interactive dashboard with multiple views"""
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Key Performance Indicator',
                'Trend Analysis',
                'Distribution by Category',
                'Geographic Breakdown',
                'Model Performance',
                'Prediction Confidence'
            ),
            specs=[
                [{"type": "indicator"}, {"type": "scatter"}],
                [{"type": "bar"}, {"type": "scatter"}],
                [{"type": "scatter"}, {"type": "histogram"}]
            ],
            row_heights=[0.3, 0.35, 0.35]
        )

        # KPI Indicator
        current_value = self.data['value'].iloc[-1]
        previous_value = self.data['value'].iloc[-30]

        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=current_value,
            delta={'reference': previous_value, 'relative': True},
            title={'text': "Current Performance"},
            domain={'x': [0, 1], 'y': [0, 1]}
        ), row=1, col=1)

        # Trend line
        fig.add_trace(go.Scatter(
            x=self.data['date'],
            y=self.data['value'],
            mode='lines+markers',
            name='Actual',
            line=dict(width=2)
        ), row=1, col=2)

        # Add moving average
        self.data['ma_7'] = self.data['value'].rolling(7).mean()
        fig.add_trace(go.Scatter(
            x=self.data['date'],
            y=self.data['ma_7'],
            mode='lines',
            name='7-day MA',
            line=dict(dash='dash')
        ), row=1, col=2)

        # Category breakdown
        category_data = self.data.groupby('category')['value'].mean().sort_values()
        fig.add_trace(go.Bar(
            x=category_data.values,
            y=category_data.index,
            orientation='h',
            name='Category Performance'
        ), row=2, col=1)

        # Update layout
        fig.update_layout(
            title_text="ML Model Performance Dashboard",
            height=1200,
            showlegend=True,
            hovermode='x unified'
        )

        return fig

    def save_html(self, filename='dashboard.html'):
        """Save dashboard as standalone HTML"""
        fig = self.create_dashboard()
        fig.write_html(filename)