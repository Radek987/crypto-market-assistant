import os
from dotenv import load_dotenv
from binance.client import Client

# Načteme klíče z .env souboru
load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')

client = Client(API_KEY, API_SECRET)

def get_market_info(symbol: str) -> dict:
    try:
        ticker = client.get_ticker(symbol=symbol)
        return {
            "price": float(ticker["lastPrice"]),
            "volume": float(ticker["volume"])
        }
    except Exception as e:
        print(f"Chyba při získávání dat pro {symbol}: {e}")
        return {}