import ccxt
import requests
import time
from strategy import find_imbalance

# --- إعدادات البوت ---
TELEGRAM_TOKEN = "8821280523:AAH3kiwZgLmw5nkbRGxaU41g6_aVOBHxiw"
CHAT_ID = "ضع_رقم_الـ_ID_هنا" # احصل عليه من @userinfobot

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def run_analysis():
    print("🚀 جاري تحليل السوق...")
    exchange = ccxt.kucoin()
    candles = exchange.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=100)
    
    imbalances = find_imbalance(candles)
    
    if imbalances:
        msg = f"✅ وجد البوت {len(imbalances)} فجوة سعرية (FVG) جديدة!"
        print(msg)
        send_telegram_alert(msg)
    else:
        print("🔍 لم يتم العثور على فجوات حالياً.")

if __name__ == "__main__":
    run_analysis()
