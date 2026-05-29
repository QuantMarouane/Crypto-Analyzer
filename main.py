from strategy import find_imbalance
import ccxt

def get_market_price(symbol):
    exchange = ccxt.kucoin()
    ticker = exchange.fetch_ticker(symbol)
    return ticker['last']

def initialize_bot():
    print("Bot Initialized. Analyzing Market...")
    symbol = 'BTC/USDT'
    
    # جلب البيانات من المنصة
    exchange = ccxt.kucoin()
    candles = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100)
    
    # استخدام الدالة التي استوردتها لتحليل الفجوات
    imbalances = find_imbalance(candles)
    
    # طباعة النتائج
    if imbalances:
        print(f"✅ Found {len(imbalances)} imbalances in the last 100 candles.")
    else:
        print("🔍 No imbalances found.")

if __name__ == "__main__":
    initialize_bot()

