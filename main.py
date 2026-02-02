import os
import threading
from datetime import time

import pytz
import yfinance as yf
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# =========================
# CONFIG
# =========================
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # set in Render Environment
CHAT_ID = int(os.environ.get("CHAT_ID"))  # set in Render Environment

IST = pytz.timezone("Asia/Kolkata")

# =========================
# HEALTH CHECK SERVER
# =========================
app_web = Flask(__name__)

@app_web.route("/")
def health():
    return "OK", 200

def run_web():
    app_web.run(host="0.0.0.0", port=10000)

# =========================
# MARKET FUNCTIONS
# =========================
def get_nifty_data():
    df = yf.Ticker("^NSEI").history(period="2d", interval="1m")
    if df.empty:
        return None

    today = df[df.index.date == df.index[-1].date()]
    prev = df[df.index.date < df.index[-1].date()]

    spot = round(float(today["Close"].iloc[-1]), 2)
    open_price = round(float(today["Open"].iloc[0]), 2)
    prev_close = round(float(prev["Close"].iloc[-1]), 2)

    volume = today["Volume"].sum()
    vwap = spot if volume == 0 else round(
        (today["Close"] * today["Volume"]).sum() / volume, 2
    )

    gap = round(open_price - prev_close, 2)

    return spot, open_price, vwap, gap


def get_bias(open_price, vwap):
    if open_price > vwap:
        return "BULLISH"
    elif open_price < vwap:
        return "BEARISH"
    else:
        return "VOLATILE"


# =========================
# TELEGRAM COMMANDS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Market Assistant Bot is LIVE\n\n"
        "Commands:\n"
        "/nifty – Live NIFTY status\n"
        "/dashboard – Same as /nifty\n"
    )


async def nifty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_nifty_data()
    if not data:
        await update.message.reply_text("❌ Unable to fetch NIFTY data")
        return

    spot, open_price, vwap, gap = data
    bias = get_bias(open_price, vwap)

    msg = (
        "📊 *NIFTY LIVE STATUS*\n\n"
        f"SPOT: {spot}\n"
        f"OPEN: {open_price}\n"
        f"VWAP: {vwap}\n"
        f"GAP: {gap}\n\n"
        f"BIAS: *{bias}*\n"
        "🎯 Target System: +50 points\n"
    )

    await update.message.reply_text(msg, parse_mode="Markdown")


async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await nifty(update, context)


# =========================
# AUTO DAILY MESSAGE (8:45 AM)
# =========================
async def auto_nifty(context: ContextTypes.DEFAULT_TYPE):
    data = get_nifty_data()
    if not data:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="❌ NIFTY data fetch failed (pre-market)"
        )
        return

    spot, open_price, vwap, gap = data
    bias = get_bias(open_price, vwap)

    msg = (
        "⏰ *8:45 AM PRE-MARKET REPORT*\n\n"
        f"OPEN: {open_price}\n"
        f"VWAP: {vwap}\n"
        f"GAP: {gap}\n\n"
        f"DAY BIAS: *{bias}*\n\n"
        "⚠️ Rule: ONE TRADE ONLY\n"
        "🎯 Target: 50 points"
    )

    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=msg,
        parse_mode="Markdown"
    )


# =========================
# MAIN
# =========================
def main():
    # Start health server (for Render + UptimeRobot)
    threading.Thread(target=run_web).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("nifty", nifty))
    app.add_handler(CommandHandler("dashboard", dashboard))

    app.job_queue.run_daily(
        auto_nifty,
        time=time(hour=8, minute=45, tzinfo=IST),
        name="nifty_daily"
    )

    print("✅ Market Assistant Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
