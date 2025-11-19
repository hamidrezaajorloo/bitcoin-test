import requests
from datetime import datetime
import sqlite3
from fastapi import FastAPI
import uvicorn

# -------- دیتابیس SQLite ساده ----------
conn = sqlite3.connect("btc_prices.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS prices (
    ts TEXT,
    price REAL
)
""")
conn.commit()

# -------- گرفتن قیمت از باینسس ----------
BINANCE_API = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

def get_btc_price():
    resp = requests.get(BINANCE_API)
    resp.raise_for_status()
    data = resp.json()
    price = float(data["price"])
    ts = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    return ts, price

def save_price(ts, price):
    cursor.execute("INSERT INTO prices (ts, price) VALUES (?, ?)", (ts, price))
    conn.commit()

# -------- FastAPI برای نمایش آخرین قیمت ----------
app = FastAPI()

@app.get("/last_price")
def last_price():
    cursor.execute("SELECT ts, price FROM prices ORDER BY ts DESC LIMIT 1")
    row = cursor.fetchone()
    if row:
        return {"timestamp": row[0], "price": row[1]}
    return {"error": "No data yet"}

# -------- گرفتن قیمت و ذخیره هر بار اجرا ---------
ts, price = get_btc_price()
save_price(ts, price)
print("ذخیره شد:", ts, price)

# -------- اجرای سرور FastAPI ----------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
