import ccxt
import requests
import time
import numpy as np
from strategy import find_imbalance

# --- الإعدادات ---
TELEGRAM_TOKEN = "8821280523:AAH3kiwZgLmw5nkbRGxaU41g6_aVOBHxiw"
CHAT_ID = "6397157109"
SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
MIN_IMBALANCES = 3  # الحد الأدنى للفجوات لإرسال التنبيه
exchange = ccxt.kucoin()

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def run_analysis_pro(symbol):
    candles = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=200)
    closes = [c[4] for c in candles]
    ema200 = np.mean(closes[-200:])
    current_price = closes[-1]
    
    imbalances = find_imbalance(candles)
    
    # الشرط الجديد: التنبيه فقط إذا كانت الفجوات >= 3
    if len(imbalances) >= MIN_IMBALANCES:
        trend = "صاعد" if current_price > ema200 else "هابط"
        msg = f"🚀 فرصة قوية على {symbol}\n" \
              f"📈 الاتجاه العام: {trend}\n" \
              f"✅ عدد الفجوات المكتشفة: {len(imbalances)}"
        send_telegram_alert(msg)
        print(msg)

if __name__ == "__main__":
    while True:
        for symbol in SYMBOLS:
            try:
                run_analysis_pro(symbol)
            except Exception as e:
                print(f"⚠️ خطأ في {symbol}: {e}")
        
        print("⏳ تم التحليل، بانتظار الساعة القادمة...")
        time.sleep(3600)
