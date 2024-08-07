from flask import Flask, request, jsonify, render_template
import requests
import smtplib
import os

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

def send_email(receiver_email, subject, message):
    email = "cryptowatcher2023@gmail.com"
    password = os.environ.get('EMAIL_PASSWORD')
    text = f"Subject: {subject}\n\n{message}"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, receiver_email, text)
        server.quit()
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

@app.route('/send-email', methods=['POST'])
def email():
    data = request.json
    receiver_email = data.get('receiver_email')
    subject = data.get('subject')
    message = data.get('message')
    success = send_email(receiver_email, subject, message)
    if success:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
