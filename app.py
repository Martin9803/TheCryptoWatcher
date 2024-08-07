import requests
import time
import smtplib
from email.message import EmailMessage
from flask import Flask, request, jsonify

app = Flask(__name__)

# Import the senderEmail, getawayAddress, and appKey from the content module
senderEmail = 'Cryptowatcher2023@gmail.com'
appKey = 'ktvtnuazhwoxruvl'

def get_crypto_prices(crypto_ids):
    url = 'https://api.coingecko.com/api/v3/simple/price'
    parameters = {
        'ids': ','.join(crypto_ids),
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=parameters)
    data = response.json()
    return data

@app.route('/track', methods=['POST'])
def track_prices():
    data = request.json
    phone_number = data['phone']
    provider = data['provider']
    cryptos = data['cryptos']
    
    email = phone_number + "@" + provider

    # Send thank you message
    thank_you_message = "Thank you for using the Crypto Watcher, you will be sent updates at 12pm and 12am"
    send_email(email, 'Welcome to Crypto Watcher', thank_you_message)
    
    # Initial price update
    prices = get_crypto_prices(cryptos)
    message = ""
    for crypto in cryptos:
        message += f"{crypto.capitalize()}: ${prices[crypto]['usd']:,.2f}\n"
    
    send_email(email, 'Price Update', message)
    
    return jsonify({"status": "success"}), 200

def send_email(to, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['From'] = senderEmail
    msg['To'] = to
    msg['Subject'] = subject

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(senderEmail, appKey)
    server.send_message(msg)
    server.quit()

if __name__ == '__main__':
    app.run(debug=True)
