import faust
import joblib
import pandas as pd

# --- Model Loading ---
# Model must be loaded by each worker instance
def load_model(model_path="model.joblib"):
    print("Loading model...")
    return joblib.load(model_path)

model = load_model()

# --- Faust App & Kafka Topics ---
# Assumes Kafka is running on localhost:9092
app = faust.App('stream-predictor', broker='kafka://localhost:9092')

# Define the input data format (Faust Record)
class Transaction(faust.Record, validation=True):
    transaction_id: str
    feature_1: float
    feature_2: int
    feature_3: str

# Define Kafka topics
input_topic = app.topic('raw_transactions', value_type=Transaction)
output_topic = app.topic('scored_transactions')

# --- Stream Processing Agent ---
@app.agent(input_topic)
async def score_transaction(transactions):
    """
    This agent consumes from 'raw_transactions', predicts,
    and produces to 'scored_transactions'.
    """
    async for tx in transactions:
        # 1. Convert Faust Record to DataFrame for the model
        try:
            input_df = pd.DataFrame([tx.asdict()], index=[tx.transaction_id])
            
            # 2. Get prediction
            prediction = model.predict(input_df)[0]
            probability = model.predict_proba(input_df)[0][1] # Prob for class 1
            
            # 3. Create enriched output
            result = {
                "transaction_id": tx.transaction_id,
                "original_features": tx.asdict(),
                "prediction": int(prediction),
                "probability": float(probability)
            }
            
            # 4. Produce to output topic
            await output_topic.send(key=tx.transaction_id, value=result)
            
            print(f"Processed {tx.transaction_id}: Score={probability:.4f}")
            
        except Exception as e:
            print(f"Failed to process {tx.transaction_id}: {e}")
            # Optionally send to a dead-letter-queue topic
            
if __name__ == "__main__":
    # Run with: faust -A streaming_app worker -l info
    app.main()
