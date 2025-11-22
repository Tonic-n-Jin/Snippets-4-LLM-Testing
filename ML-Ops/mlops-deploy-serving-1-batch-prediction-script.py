import pandas as pd
import joblib
import argparse
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

class BatchPredictor:
    def __init__(self, model_path):
        """Loads the pre-trained model pipeline."""
        try:
            self.model = joblib.load(model_path)
            logging.info(f"Model loaded successfully from {model_path}")
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            raise
    
    def predict(self, input_data_path, output_data_path):
        """
        Loads data, runs predictions, and saves the results.
        Assumes input is Parquet/CSV and model pipeline handles preprocessing.
        """
        logging.info(f"Starting batch prediction on {input_data_path}")
        
        # 1. Load data
        if input_data_path.endswith('.parquet'):
            data = pd.read_parquet(input_data_path)
        else:
            data = pd.read_csv(input_data_path)
            
        logging.info(f"Loaded {len(data)} records for prediction.")
        
        # 2. Run predictions (assuming model is a pipeline)
        predictions = self.model.predict(data)
        prediction_probs = self.model.predict_proba(data)[:, 1] # Get prob for class 1
        
        # 3. Append results
        results_df = data.copy()
        results_df['prediction'] = predictions
        results_df['prediction_probability'] = prediction_probs
        results_df['prediction_timestamp'] = datetime.utcnow()
        
        # 4. Save results
        if output_data_path.endswith('.parquet'):
            results_df.to_parquet(output_data_path, index=False)
        else:
            results_df.to_csv(output_data_path, index=False)
            
        logging.info(f"Predictions saved to {output_data_path}")
        return len(results_df)

if __name__ == "__main__":
    # This script is designed to be run by a scheduler (e.g., Airflow, cron)
    parser = argparse.ArgumentParser(description="Batch Prediction Job")
    parser.add_argument("--model", required=True, help="Path to the .joblib model file")
    parser.add_argument("--input", required=True, help="Path to input data (Parquet/CSV)")
    parser.add_argument("--output", required=True, help="Path to save predictions (Parquet/CSV)")
    
    args = parser.parse_args()
    
    # Example: python batch_predict.py --model model.joblib --input features.parquet --output predictions.parquet
    predictor = BatchPredictor(model_path=args.model)
    predictor.predict(input_data_path=args.input, output_data_path=args.output)
