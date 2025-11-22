from opentelemetry import trace

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import logging

# Configure tracing

tracer = trace.get_tracer(**name**)

class MLObservability:
def **init**(self):
self.logger = self.setup_logging()
FastAPIInstrumentor.instrument(app)

    def setup_logging(self):
        """Centralized logging configuration"""
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(trace_id)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    @tracer.start_as_current_span("predict")
    def predict_with_tracing(self, request):
        """Add tracing to predictions"""
        span = trace.get_current_span()
        span.set_attribute("model.version", self.model_version)
        span.set_attribute("request.features", str(request))

        try:
            prediction = self.model.predict(request)
            span.set_attribute("prediction.result", str(prediction))
            return prediction
        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR))
            raise