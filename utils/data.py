import yfinance as yf
import math

# Index symbols
NIFTY = "^NSEI"
BANKNIFTY = "^NSEBANK"
SENSEX = "^BSESN"


def atm_strike(price: float) -> int:
    """Round price to nearest 50 for option strike"""
    return int(round(price / 50) * 50)


def get_index(symbol: str):
    """
    Returns:
    spot, open_price, vwap
    """
    df = yf.Ticker(symbol).history(period="1d", interval="1m")

    if df.empty:
        return None

    spot = round(float(df["Close"].iloc[-1]), 2)
    open_price = round(float(df["Open"].iloc[0]), 2)

    volume = df["Volume"].sum()

    if volume == 0:
        vwap = float("nan")
    else:
        vwap = round(
            (df["Close"] * df["Volume"]).sum() / volume,
            2
        )

    return spot, open_price, vwap
