import json
import boto3
from botocore.exceptions import ClientError
import os

# Initialize S3 client and read config from env
s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']
FAQ_FILE    = os.environ.get('FAQ_FILE', 'faq.json')
# Adding a line to dev to check if CI/CD is working and promoting it to PROD
def lambda_handler(event, context):
    try:
        # 1. Parse the incoming JSON body
        body = json.loads(event.get('body') or '{}')
        question = body.get('question')
        answer   = body.get('answer')
        if not question or not answer:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing question or answer'}),
                'headers': {'Content-Type': 'application/json'}
            }

        # 2. Fetch existing FAQs (or start fresh)
        try:
            resp = s3.get_object(Bucket=BUCKET_NAME, Key=FAQ_FILE)
            data = json.loads(resp['Body'].read().decode('utf-8'))
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                data = {}
            else:
                raise

        # 3. Add or overwrite the entry, then save back to S3
        data[question] = answer
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=FAQ_FILE,
            Body=json.dumps(data)
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'FAQ added successfully'}),
            'headers': {'Content-Type': 'application/json'}
        }

    except Exception as e:
        # 4. General error response
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }