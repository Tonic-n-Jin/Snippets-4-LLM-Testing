# AWS Lambda handler

import json
import boto3
import joblib

# Load model from S3 at cold start

s3 = boto3.client('s3')
s3.download_file('models-bucket', 'model.pkl', '/tmp/model.pkl')
model = joblib.load('/tmp/model.pkl')

def lambda_handler(event, context):
"""Process prediction request"""
try: # Parse input
body = json.loads(event['body'])
features = preprocess(body)

        # Make prediction
        prediction = model.predict(features)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'prediction': prediction.tolist(),
                'model_version': os.environ.get('MODEL_VERSION')
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }