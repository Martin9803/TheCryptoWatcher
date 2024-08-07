from flask import Flask, request, jsonify, render_template
import requests
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

# Email configuration
sender_email = 'Cryptowatcher2023@gmail.com'
app_key = 'ktvtnuazhwoxruvl'

# Mapping of carrier email gateways
CARRIER_GATEWAYS = {
    'att': 'txt.att.net',
    'verizon': 'vtext.com',
    'tmobile': 'tmomail.net',
    'sprint': 'messaging.sprintpcs.com'
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

def send_text_via_email(phone_number, carrier, message):
    receiver_email = f"{phone_number}@{CARRIER_GATEWAYS[carrier]}"
    msg = EmailMessage()
    msg.set_content(message)
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Crypto Watcher Alert"

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_key)
        server.send_message(msg)
        server.quit()
        print(f"Message sent to {receiver_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-prices', methods=['POST'])
def get_prices():
    crypto_ids = request.json.get('crypto_ids', [])
    prices = get_crypto_prices(crypto_ids)
    return jsonify(prices)

@app.route('/send-text', methods=['POST'])
def send_text():
    data = request.json
    phone_number = data.get('phone_number')
    carrier = data.get('carrier')
    selected_cryptos = data.get('selected_cryptos')
    prices = get_crypto_prices(selected_cryptos)

    message_lines = []
    for crypto in selected_cryptos:
        current_price = prices[crypto]['usd']
        message_lines.append(f"{crypto.capitalize()}: ${current_price:,.2f}")

    message = "\n".join(message_lines)
    success = send_text_via_email(phone_number, carrier, message)

    if success:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    app.run(debug=True)


