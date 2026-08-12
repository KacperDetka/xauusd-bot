import os
from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(message):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

@app.route('/', methods=['GET'])
def home():
    return "Bot działa!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    signal_data = request.data.decode('utf-8')
    if signal_data:
        send_telegram_message(signal_data)
        return "Sygnał wysłany na Telegram", 200
    return "Pusty sygnał", 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
