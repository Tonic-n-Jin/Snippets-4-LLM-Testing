import hashlib
import pandas as pd
from cryptography.fernet import Fernet

class PrivacyProtection:
    def __init__(self, encryption_key=None):
        if encryption_key:
            self.cipher = Fernet(encryption_key)
        else:
            self.cipher = Fernet(Fernet.generate_key())

        self.pii_fields = ['name', 'email', 'phone', 'ssn', 'address']

    def anonymize_pii(self, data, method='hash'):
        """Anonymize personally identifiable information"""
        df = data.copy()

        for field in self.pii_fields:
            if field in df.columns:
                if method == 'hash':
                    df[field] = df[field].apply(self._hash_value)
                elif method == 'pseudonymize':
                    df[field] = df[field].apply(self._pseudonymize)
                elif method == 'redact':
                    df[field] = '[REDACTED]'

        return df

    def _hash_value(self, value):
        """One-way hash for anonymization"""
        if pd.isna(value):
            return value
        return hashlib.sha256(str(value).encode()).hexdigest()[:16]

    def _pseudonymize(self, value):
        """Reversible pseudonymization"""
        if pd.isna(value):
            return value
        encrypted = self.cipher.encrypt(str(value).encode())
        return encrypted.decode()

    def encrypt_sensitive_data(self, data):
        """Encrypt sensitive columns"""
        df = data.copy()

        for field in self.pii_fields:
            if field in df.columns:
                df[field] = df[field].apply(
                    lambda x: self.cipher.encrypt(str(x).encode()).decode()
                    if not pd.isna(x) else x
                )

        return df

    def decrypt_sensitive_data(self, data):
        """Decrypt sensitive columns"""
        df = data.copy()

        for field in self.pii_fields:
            if field in df.columns:
                df[field] = df[field].apply(
                    lambda x: self.cipher.decrypt(x.encode()).decode()
                    if not pd.isna(x) else x
                )

        return df

    def implement_right_to_be_forgotten(self, dataset, user_id):
        """GDPR: Remove all data for a specific user"""
        return dataset[dataset['user_id'] != user_id]

    def generate_data_export(self, dataset, user_id):
        """GDPR: Export all data for a specific user"""
        user_data = dataset[dataset['user_id'] == user_id]

        export = {
            'user_id': user_id,
            'export_date': datetime.utcnow().isoformat(),
            'data': user_data.to_dict('records')
        }

        return export