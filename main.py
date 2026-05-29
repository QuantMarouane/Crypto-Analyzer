def run_analysis_pro(symbol):
    # 1. جلب البيانات
    candles = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100)
    
    # 2. التحقق من اتجاه السوق (فلتر EMA 200)
    # 3. البحث عن FVG
    imbalances = find_imbalance(candles)
    
    # 4. التنبيه الاحترافي
    if imbalances:
        msg = f"🚀 فرصة محتملة على {symbol}\n" \
              f"🛑 وقف الخسارة المقترح: {price_below_fvg}\n" \
              f"🎯 الهدف: {target_price}"
        send_telegram_alert(msg)
