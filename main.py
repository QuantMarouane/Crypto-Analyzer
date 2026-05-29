
import ccxt
import requests
import time

# --- إعدادات البوت ---
TELEGRAM_TOKEN = "8821280523:AAH3kiwZgLmw5nkbRGxaU41g6_aVOBHxiw"
CHAT_ID = "هنا_يجب_أن_تضع_الـ_Chat_ID_الخاص_بك" # شرح كيف تحصله أدناه

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def run_analysis():
    print("🚀 جاري تحليل السوق...")
    # استخدام ccxt للاتصال بـ KuCoin
    exchange = ccxt.kucoin()
    # جلب 100 شمعة للساعة الواحدة
    candles = exchange.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=100)
    
    # هنا يتم استدعاء دالة تحليل الفجوات الموجودة في مشروعك
    # (افترضنا أن find_imbalance موجودة في ملف strategy.py)
    from strategy import find_imbalance
    imbalances = find_imbalance(candles)
    
    if imbalances:
        msg = f"✅ وجد البوت {len(imbalances)} فجوة سعرية (FVG) جديدة!"
        print(msg)
        send_telegram_alert(msg)
    else:
        print("🔍 لم يتم العثور على فجوات حالياً.")

# تشغيل البوت
if __name__ == "__main__":
    run_analysis()
