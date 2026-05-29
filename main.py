import os
import ccxt
import requests
import time
import numpy as np
from strategy import find_imbalance

# إعداد الربط الآمن للمنصة
exchange = ccxt.kucoin({
    'apiKey': os.environ['KUCOIN_API_KEY'],
    'secret': os.environ['KUCOIN_SECRET'],
    'password': os.environ['KUCOIN_PASSPHRASE'],
})

# إعداد التليجرام (يفضل وضعه أيضاً في Secrets باسم TELEGRAM_TOKEN و CHAT_ID)
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
MIN_IMBALANCES = 3
TRADE_AMOUNT = 0.001  # حدد الكمية المناسبة

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def execute_trade(symbol, side, amount):
    try:
        # تنفيذ طلب شراء أو بيع بسعر السوق
        order = exchange.create_market_order(symbol, side, amount)
        return order
    except Exception as e:
        print(f"خطأ في تنفيذ الصفقة على {symbol}: {e}")
        return None

def run_analysis_pro(symbol):
    candles = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=200)
    closes = [c[4] for c in candles]
    ema200 = np.mean(closes[-200:])
    current_price = closes[-1]
    
    imbalances = find_imbalance(candles)
    
    if len(imbalances) >= MIN_IMBALANCES:
        side = 'buy' if current_price > ema200 else 'sell'
        msg = f"🚀 فرصة قوية على {symbol} | الاتجاه: {'صاعد' if side == 'buy' else 'هابط'}"
        send_telegram_alert(msg)
        
        # تنفيذ التداول الآلي
        execute_trade(symbol, side, TRADE_AMOUNT)

if __name__ == "__main__":
    while True:
        for symbol in SYMBOLS:
            try:
                run_analysis_pro(symbol)
            except Exception as e:
                print(f"⚠️ خطأ في {symbol}: {e}")
        time.sleep(3600) # فحص كل ساعة
