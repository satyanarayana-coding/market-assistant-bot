import requests
import math

NSE_OPTION_CHAIN_URL = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br"
}


def get_nifty_oi(atm_strike: int):
    """
    Returns OI and change in OI for ATM CE & PE
    """
    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        response = session.get(NSE_OPTION_CHAIN_URL, timeout=5)
        data = response.json()
    except Exception:
        return None

    ce_oi = pe_oi = ce_chg = pe_chg = None

    for item in data["records"]["data"]:
        if item.get("strikePrice") == atm_strike:
            if "CE" in item:
                ce_oi = item["CE"]["openInterest"]
                ce_chg = item["CE"]["changeinOpenInterest"]
            if "PE" in item:
                pe_oi = item["PE"]["openInterest"]
                pe_chg = item["PE"]["changeinOpenInterest"]
            break

    if None in (ce_oi, pe_oi):
        return None

    return {
        "ce_oi": ce_oi,
        "pe_oi": pe_oi,
        "ce_chg": ce_chg,
        "pe_chg": pe_chg
    }
