import hashlib
import json
from datetime import datetime
from pathlib import Path

class LineageTracker:
    def __init__(self, storage_path='lineage.json'):
        self.storage_path = Path(storage_path)
        self.lineage = self._load_lineage()

    def _load_lineage(self):
        """Load existing lineage"""
        if self.storage_path.exists():
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {'datasets': {}, 'models': {}, 'relationships': []}

    def _save_lineage(self):
        """Persist lineage to disk"""
        with open(self.storage_path, 'w') as f:
            json.dump(self.lineage, f, indent=2)

    def _compute_hash(self, data):
        """Compute hash of data for versioning"""
        if isinstance(data, str):
            return hashlib.sha256(data.encode()).hexdigest()[:16]
        return hashlib.sha256(str(data).encode()).hexdigest()[:16]

    def register_dataset(self, dataset_id, metadata):
        """Register dataset with metadata"""
        dataset_hash = self._compute_hash(str(metadata))

        self.lineage['datasets'][dataset_id] = {
            'hash': dataset_hash,
            'metadata': metadata,
            'created_at': datetime.now().isoformat(),
            'version': len([k for k in self.lineage['datasets']
                           if k.startswith(dataset_id.split('_v')[0])]) + 1
        }

        self._save_lineage()
        return dataset_hash

    def register_model(self, model_id, model_version, training_metadata):
        """Register model with full training context"""
        model_key = f"{model_id}_v{model_version}"

        self.lineage['models'][model_key] = {
            'model_id': model_id,
            'version': model_version,
            'training_metadata': training_metadata,
            'created_at': datetime.now().isoformat(),
            'deployed_at': None,
            'status': 'trained'
        }

        self._save_lineage()
        return model_key

    def link_model_to_dataset(self, model_key, dataset_id, relationship_type='trained_on'):
        """Establish relationship between model and dataset"""
        self.lineage['relationships'].append({
            'source': dataset_id,
            'target': model_key,
            'type': relationship_type,
            'created_at': datetime.now().isoformat()
        })

        self._save_lineage()

    def get_model_lineage(self, model_key):
        """Get full lineage for a model"""
        if model_key not in self.lineage['models']:
            return None

        model_info = self.lineage['models'][model_key]

        # Find all datasets used
        datasets_used = [
            rel for rel in self.lineage['relationships']
            if rel['target'] == model_key and rel['type'] == 'trained_on'
        ]

        lineage_info = {
            'model': model_info,
            'datasets': [
                self.lineage['datasets'][rel['source']]
                for rel in datasets_used
                if rel['source'] in self.lineage['datasets']
            ]
        }

        return lineage_info

    def trace_dataset_impact(self, dataset_id):
        """Find all models trained on a dataset"""
        affected_models = [
            rel['target'] for rel in self.lineage['relationships']
            if rel['source'] == dataset_id
        ]

        return [
            self.lineage['models'][model_key]
            for model_key in affected_models
            if model_key in self.lineage['models']
        ]