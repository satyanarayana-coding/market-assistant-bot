from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from datetime import time

from config import BOT_TOKEN, CHAT_ID, IST
from bots.dashboard import market_dashboard
from bots.nifty_daily import nifty_daily_plan


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Market Assistant Bot Active\n\n"
        "/dashboard → Market overview\n"
        "/nifty → Today’s NIFTY plan\n"
        "/help → Commands"
    )


async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(market_dashboard())


async def nifty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(nifty_daily_plan())


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/dashboard\n"
        "/nifty\n"
        "/help"
    )


async def auto_nifty_plan(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=nifty_daily_plan()
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dashboard", dashboard))
    app.add_handler(CommandHandler("nifty", nifty))
    app.add_handler(CommandHandler("help", help_cmd))

    # Auto-send NIFTY plan at 8:45 AM IST
    app.job_queue.run_daily(
        auto_nifty_plan,
        time=time(hour=8, minute=45, tzinfo=IST),
        name="nifty_daily"
    )

    print("✅ Market Assistant Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
