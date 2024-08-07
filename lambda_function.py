import json
import boto3

def lambda_handler(event, context):
    # Parse form data
    phone = event['phone']
    provider = event['provider']
    cryptos = event['cryptos']

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
