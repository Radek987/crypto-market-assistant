import asyncio
from services.market import get_market_info

data = get_market_info("BTCUSDT")

if data:
    print(f"Cena BTC je {data['price']:.2f} $.")
    print(f"24h Volume: {data['volume']:.2f} BTC.")
else:
    print("Nepodařilo se získat data.")
