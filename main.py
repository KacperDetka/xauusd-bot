import os
import time
import threading
from flask import Flask
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(message):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

def track_gold_price():
    last_price = None
    while True:
        try:
            # Pobieranie ceny złota z darmowego API Binance (token PAXG oparty na złocie)
            response = requests.get("https://binance.com").json()
            current_price = float(response['price'])
            
            # Jeśli cena zmieni się o więcej niż 1 dolara, bot wyśle alert
            if last_price and abs(current_price - last_price) >= 1.0:
                send_telegram_message(f"🚨 Zmiana na Złocie! Obecna cena: {current_price} USD")
                
            last_price = current_price
        except Exception as e:
            print("Błąd ceny:", e)
        
        time.sleep(60) # Sprawdzaj cenę automatycznie co 60 sekund

@app.route('/', methods=['GET'])
def home():
    return "Bot działa autonomicznie!", 200

if __name__ == '__main__':
    # Uruchomienie śledzenia ceny złota w osobnym wątku w tle
    threading.Thread(target=track_gold_price, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

