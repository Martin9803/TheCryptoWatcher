from flask import Flask, request, jsonify, render_template
import requests
from twilio.rest import Client
import os

app = Flask(__name__)

# Twilio configuration from environment variables
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_number = os.environ.get('TWILIO_NUMBER')

client = Client(account_sid, auth_token)

def get_crypto_prices(crypto_ids):
    url = 'https://api.coingecko.com/api/v3/simple/price'
    parameters = {
        'ids': ','.join(crypto_ids),
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=parameters)
    data = response.json()
    return data

def send_text(receiver_number, message):
    print(f"Sending text to {receiver_number}")
    client.messages.create(
        body=message,
        from_=twilio_number,
        to=receiver_number
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-prices', methods=['POST'])
def get_prices():
    crypto_ids = request.json.get('crypto_ids', [])
    prices = get_crypto_prices(crypto_ids)
    return jsonify(prices)

@app.route('/send-text', methods=['POST'])
def text():
    data = request.json
    receiver_number = data.get('receiver_number')
    selected_cryptos = data.get('selected_cryptos')
    prices = get_crypto_prices(selected_cryptos)

    message_lines = []
    for crypto in selected_cryptos:
        current_price = prices[crypto]['usd']
        message_lines.append(f"{crypto.capitalize()}: ${current_price:,.2f}")
    
    message = "\n".join(message_lines)
    send_text(receiver_number, message)

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)


