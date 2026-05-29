def find_imbalance(candles):
    """
    البحث عن فجوة سعرية (Fair Value Gap)
    تحليل الفرق بين الشمعة n والشمعة n+2
    """
    imbalances = []
    # candles هي قائمة [timestamp, open, high, low, close, volume]
    for i in range(2, len(candles) - 1):
        # الشرط: قاع الشمعة الحالية أعلى من قمة الشمعة التي تسبقها بمرتين
        if candles[i][3] > candles[i-2][2]:
            imbalances.append(i)
    return imbalances
    
