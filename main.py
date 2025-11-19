import requests
from datetime import datetime
import time

BINANCE_API = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

def get_btc_price():
    resp = requests.get(BINANCE_API)
    resp.raise_for_status()
    data = resp.json()
    price = float(data["price"])
    ts = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    return ts, price

if __name__ == "_main_":
    while True:
        timestamp, price = get_btc_price()
        print(timestamp, "BTC/USDT =", price, flush=True)
        time.sleep(10)   # هر 10 ثانیه
