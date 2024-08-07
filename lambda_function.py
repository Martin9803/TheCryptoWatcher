import json
import boto3
from urllib.parse import parse_qs

def lambda_handler(event, context):
    # Parse form data
    body = parse_qs(event['body'])
    phone = body.get('phone', [None])[0]
    provider = body.get('provider', [None])[0]
    cryptos = body.get('cryptos', [])

    if not phone or not provider or not cryptos:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing required fields')
        }

    # Store user data in DynamoDB (or any other database)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CryptoWatcherSubscribers')
    table.put_item(
        Item={
            'phone': phone,
            'provider': provider,
            'cryptos': cryptos
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Subscription successful!')
    }
