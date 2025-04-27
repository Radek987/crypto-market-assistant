import ccxt
exchange = ccxt.binance()
ticker = exchange.fetch_ticker("BTC/USDT")
print(f"cena přes REST API: {ticker['last']} $")
