import logging
import json
from datetime import datetime
from functools import wraps

class AuditLogger:
    def __init__(self, log_file='audit_trail.jsonl'):
        self.log_file = log_file
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """Configure structured logging"""
        logger = logging.getLogger('MLOpsAudit')
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler(self.log_file)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def log_event(self, event_type, user_id, details):
        """Log auditable event"""
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'details': details
        }

        self.logger.info(json.dumps(event))

    def audit_prediction(self, func):
        """Decorator to audit model predictions"""
        @wraps(func)
        def wrapper(self_model, *args, **kwargs):
            # Before prediction
            start_time = datetime.utcnow()

            try:
                result = func(self_model, *args, **kwargs)

                # After successful prediction
                self.log_event(
                    event_type='prediction',
                    user_id=kwargs.get('user_id', 'system'),
                    details={
                        'model_version': self_model.version,
                        'input_shape': args[0].shape if args else None,
                        'prediction': result.tolist() if hasattr(result, 'tolist') else str(result),
                        'latency_ms': (datetime.utcnow() - start_time).total_seconds() * 1000,
                        'status': 'success'
                    }
                )

                return result

            except Exception as e:
                # Log failures
                self.log_event(
                    event_type='prediction_error',
                    user_id=kwargs.get('user_id', 'system'),
                    details={
                        'model_version': self_model.version,
                        'error': str(e),
                        'status': 'failed'
                    }
                )
                raise

        return wrapper

    def log_model_deployment(self, model_id, version, deployed_by, environment):
        """Log model deployment"""
        self.log_event(
            event_type='model_deployment',
            user_id=deployed_by,
            details={
                'model_id': model_id,
                'version': version,
                'environment': environment
            }
        )

    def log_data_access(self, dataset_id, user_id, access_type):
        """Log data access for GDPR compliance"""
        self.log_event(
            event_type='data_access',
            user_id=user_id,
            details={
                'dataset_id': dataset_id,
                'access_type': access_type
            }
        )

    def get_audit_report(self, start_date, end_date, event_type=None):
        """Generate audit report for date range"""
        events = []

        with open(self.log_file, 'r') as f:
            for line in f:
                event = json.loads(line)
                event_time = datetime.fromisoformat(event['timestamp'])

                if start_date <= event_time <= end_date:
                    if event_type is None or event['event_type'] == event_type:
                        events.append(event)

        return events