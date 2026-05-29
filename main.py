import ccxt
import requests
import time
from strategy import find_imbalance

# --- إعدادات البوت ---
TELEGRAM_TOKEN = "8821280523:AAH3kiwZgLmw5nkbRGxaU41g6_aVOBHxiw"
CHAT_ID = "6397157109"

# قائمة الأزواج المراد مراقبتها (يمكنك إضافة أي عملة أو أصل متاح في المنصة)
SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XAU/USDT'] 

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def run_analysis():
    exchange = ccxt.kucoin()
    print("🚀 بدء دورة التحليل للسوق...")
    
    for symbol in SYMBOLS:
        try:
            print(f"🔍 تحليل: {symbol}")
            candles = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100)
            imbalances = find_imbalance(candles)
            
            if imbalances:
                msg = f"✅ وجد البوت {len(imbalances)} فجوة سعرية (FVG) في زوج {symbol}"
                print(msg)
                send_telegram_alert(msg)
        except Exception as e:
            print(f"⚠️ خطأ في تحليل {symbol}: {e}")

# --- الأتمتة ---
if __name__ == "__main__":
    while True:
        run_analysis()
        print("⏳ تم التحليل، بانتظار الساعة القادمة...")
        time.sleep(3600)
