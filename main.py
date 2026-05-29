
import ccxt
import requests
import time
import numpy as np
from strategy import find_imbalance

# --- الإعدادات ---
TELEGRAM_TOKEN = "8821280523:AAH3kiwZgLmw5nkbRGxaU41g6_aVOBHxiw"
CHAT_ID = "6397157109"
SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
MIN_IMBALANCES = 3
TRADE_AMOUNT = 0.001  # كمية العملة للتداول (قم بتعديلها حسب رصيدك)

# إعداد الربط بالمنصة (يجب إضافة API Key و Secret عند التفعيل الحقيقي)
exchange = ccxt.kucoin({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET_KEY',
})

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def execute_trade(symbol, side, amount):
    try:
        order = exchange.create_market_order(symbol, side, amount)
        return order
    except Exception as e:
        print(f"خطأ في تنفيذ الصفقة: {e}")
        return None

def run_analysis_pro(symbol):
    candles = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=200)
    closes = [c[4] for c in candles]
    ema200 = np.mean(closes[-200:])
    current_price = closes[-1]
    
    imbalances = find_imbalance(candles)
    
    if len(imbalances) >= MIN_IMBALANCES:
        # تحديد الاتجاه للتداول
        side = 'buy' if current_price > ema200 else 'sell'
        trend = "صاعد" if side == 'buy' else "هابط"
        
        msg = f"🚀 فرصة قوية على {symbol}\n📈 الاتجاه: {trend}\n✅ تنفيذ {side} آلياً..."
        send_telegram_alert(msg)
        
        # تنفيذ الصفقة
        trade_result = execute_trade(symbol, side, TRADE_AMOUNT)
        if trade_result:
            send_telegram_alert("✅ تم تنفيذ الصفقة بنجاح!")
        else:
            send_telegram_alert("⚠️ فشل تنفيذ الصفقة.")

if __name__ == "__main__":
    while True:
        for symbol in SYMBOLS:
            try:
                run_analysis_pro(symbol)
            except Exception as e:
                print(f"⚠️ خطأ في {symbol}: {e}")
        time.sleep(3600) # انتظار ساعة
