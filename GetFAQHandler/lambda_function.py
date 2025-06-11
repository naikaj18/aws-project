import json
import boto3
from botocore.exceptions import ClientError
import os

# Initialize S3 client and read config from env
s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']
FAQ_FILE    = os.environ.get('FAQ_FILE', 'faq.json')

def lambda_handler(event, context):
    try:
        # 1. Read the 'q' query parameter
        question = event.get('queryStringParameters', {}).get('q')
        if not question:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing question parameter'}),
                'headers': {'Content-Type': 'application/json'}
            }

        # 2. Fetch the JSON from S3 (or treat as empty if not present)
        try:
            resp = s3.get_object(Bucket=BUCKET_NAME, Key=FAQ_FILE)
            data = json.loads(resp['Body'].read().decode('utf-8'))
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                data = {}
            else:
                raise

        # 3. Look up the answer
        answer = data.get(question)
        if answer:
            return {
                'statusCode': 200,
                'body': json.dumps({'answer': answer}),
                'headers': {'Content-Type': 'application/json'}
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Question not found'}),
                'headers': {'Content-Type': 'application/json'}
            }

    except Exception as e:
        # 4. Catch-all error handler
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }