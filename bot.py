# Telegram bot sceleton
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from services.market import get_market_info


# 1) Definice příkazu /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Odpoví zprávou, když uživatel pošle /start.
    """
    await update.message.reply_text(
        "Ahoj! Jsem tvůj Crypto Market Assistant. Zadej /market SYMBOL pro info o trhu."
    )

# 2) Definice příkazu /market   
async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Reaguje na /market SYMBOL a vrátí informace o trhu.
    """
    if not context.args:
        await update.message.reply_text("Použij správně: /market SYMBOL (např. /market BTC)")
        return

    symbol = context.args[0].upper()
    info = await get_market_info(symbol)
    await update.message.reply_text(info)

def main():
    # 2) Načtení tokenu z proměnných prostředí
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_TOKEN nenalezen. Nastav ho v env proměnných.")

    # 3) Vytvoření aplikace a registrace handlerů
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("market", market))


    # 4) Spuštění bota v polling módu
    app.run_polling()

if __name__ == "__main__":
    main()