import ccxt
import requests
import time
import numpy as np # ضروري لحساب المتوسطات
from strategy import find_imbalance

# إعدادات البوت
TELEGRAM_TOKEN = "8821280523:AAH3kiwZgLmw5nkbRGxaU41g6_aVOBHxiw"
CHAT_ID = "6397157109"
SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT'] # الأزواج التي تراقبها
exchange = ccxt.kucoin()

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

# هذه هي الدالة الاحترافية التي أضفتها أنت، قمنا بتكملة منطقها:
def run_analysis_pro(symbol):
    # 1. جلب البيانات
    candles = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=200)
    
    # 2. فلتر EMA 200 (نحسب متوسط آخر 200 شمعة)
    closes = [c[4] for c in candles]
    ema200 = np.mean(closes[-200:])
    current_price = closes[-1]
    
    # 3. البحث عن FVG
    imbalances = find_imbalance(candles)
    
    # 4. التنبيه الاحترافي
    if imbalances:
        trend = "صاعد (Buy Opportunity)" if current_price > ema200 else "هابط (Sell Opportunity)"
        msg = f"🚀 فرصة محتملة على {symbol}\n" \
              f"📈 الاتجاه العام: {trend}\n" \
              f"✅ تم العثور على {len(imbalances)} فجوة FVG"
        send_telegram_alert(msg)
        print(msg)

# الأتمتة الكاملة
if __name__ == "__main__":
    while True:
        for symbol in SYMBOLS:
            try:
                run_analysis_pro(symbol)
            except Exception as e:
                print(f"⚠️ خطأ في {symbol}: {e}")
        
        print("⏳ انتظر ساعة للتحليل القادم...")
        time.sleep(3600)
