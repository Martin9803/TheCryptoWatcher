import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify

app = Flask(__name__)

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
    
    prices = get_crypto_prices(cryptos)
    message = ""
    for crypto in cryptos:
        message += f"{crypto.capitalize()}: ${prices[crypto]['usd']:,.2f}\n"
    
    send_email(email, 'Price Update', message)
    
    return jsonify({"status": "success"}), 200

def send_email(to, subject, body):
    sender_email = 'Cryptowatcher2023@gmail.com'
    app_key = 'ktvtnuazhwoxruvl'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, app_key)
    text = msg.as_string()
    server.sendmail(sender_email, to, text)
    server.quit()

if __name__ == '__main__':
    app.run(debug=True)

