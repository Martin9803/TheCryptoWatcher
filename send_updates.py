import smtplib
from email.message import EmailMessage
import requests
import boto3

sender_email = 'Cryptowatcher2023@gmail.com'
app_key = 'ktvtnuazhwoxruvl'

sms_gateways = {
    '1': '@vtext.com',
    '2': '@txt.att.net',
    '3': '@tmomail.net',
    '4': '@messaging.sprintpcs.com'
}

def get_crypto_prices(crypto_ids):
    url = 'https://api.coingecko.com/api/v3/simple/price'
    parameters = {
        'ids': ','.join(crypto_ids),
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=parameters)
    data = response.json()
    return data

def send_sms(gateway_address, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['From'] = sender_email
    msg['To'] = gateway_address
    msg['Subject'] = subject

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, app_key)
    server.send_message(msg)
    server.quit()

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CryptoWatcherSubscribers')

    # Scan the table to get all subscribers
    response = table.scan()
    subscribers = response['Items']

    for subscriber in subscribers:
        phone = subscriber['phone']
        provider = subscriber['provider']
        cryptos = subscriber['cryptos']
        gateway_address = phone + sms_gateways[provider]

        # Get the current prices
        prices = get_crypto_prices(cryptos)
        message_body = ""
        for crypto in cryptos:
            current_price = prices[crypto]['usd']
            message_body += f"{crypto.capitalize()}: ${current_price:,.2f}\n"

        send_sms(gateway_address, "Price Update", message_body.strip())
