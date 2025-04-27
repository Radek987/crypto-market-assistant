from services.realtime import BinanceWebSocketClient
import time

client = BinanceWebSocketClient('btcusdt')
client.connect()

time.sleep(10)  # sleduj 10 sekund

client.disconnect()
