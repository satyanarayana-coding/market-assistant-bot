from datetime import datetime
from utils.data import get_index, NIFTY, BANKNIFTY, SENSEX
from config import IST


def market_dashboard():
    now = datetime.now(IST).strftime("%d-%m-%Y %I:%M %p")

    message = f"📊 MARKET DASHBOARD\n🕒 {now}\n\n"

    indices = {
        "NIFTY": NIFTY,
        "BANKNIFTY": BANKNIFTY,
        "SENSEX": SENSEX,
    }

    for name, symbol in indices.items():
        data = get_index(symbol)

        if not data:
            message += f"{name}: ⚠️ Data unavailable\n\n"
            continue

        spot, open_price, _ = data
        change = round(spot - open_price, 2)

        if change > 25:
            bias = "🟢 Bullish"
        elif change < -25:
            bias = "🔴 Bearish"
        else:
            bias = "⚠️ Volatile"

        message += (
            f"{name}\n"
            f"Price: {spot}\n"
            f"Change: {change}\n"
            f"Bias: {bias}\n\n"
        )

    return message
