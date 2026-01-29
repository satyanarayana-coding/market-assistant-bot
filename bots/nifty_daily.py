from datetime import datetime
from utils.data import get_index, atm_strike, NIFTY
from config import IST


def nifty_daily_plan():
    """
    Generates the 8:45 AM NIFTY one-trade plan
    """
    now = datetime.now(IST).strftime("%d-%m-%Y %I:%M %p")

    data = get_index(NIFTY)
    if not data:
        return "⚠️ NIFTY data not available. Please wait."

    spot, open_price, vwap = data
    gap = round(spot - open_price, 2)
    strike = atm_strike(spot)

    if gap >= 25:
        bias = "BULLISH"
        option = "CE"
        mode = "DIRECTIONAL"
    elif gap <= -25:
        bias = "BEARISH"
        option = "PE"
        mode = "DIRECTIONAL"
    else:
        bias = "WAIT / RANGE"
        option = "CE & PE"
        mode = "DEFENSIVE"

    vwap_status = "ABOVE" if spot > vwap else "BELOW"

    return f"""
📊 NIFTY DAILY PLAN (8:45 AM)

🕒 {now}

SPOT: {spot}
VWAP: {vwap}
VWAP STATUS: {vwap_status}

MODE: {mode}
BIAS: {bias}

FOCUS STRIKE: {strike} {option}

TARGET: +50 POINTS
RULE: ONLY ONE TRADE
""".strip()
