import websocket
import json
import threading
import logging
import time
import coloredlogs

# Setup loggeru
logging.basicConfig(
    level=logging.INFO,  # Default level (INFO, můžeš změnit na DEBUG)
    format="%(asctime)s [%(levelname)s] %(message)s",  # Formát výpisu
    datefmt="%H:%M:%S",  # Formát času
)

# Install colored logs
coloredlogs.install(level='INFO', fmt="%(asctime)s [%(levelname)s] %(message)s")

class BinanceWebSocketsClient:
    def __init__(self, symbol):
        self.symbol = symbol.lower()
        self.ws = None

    def on_message(self, ws, message):
        data = json.loads(message)
        price = data['p']  # nebo 'c' podle payloadu
        logging.info(f"Realtime cena {self.symbol.upper()}: {price} $")

    def on_error(self, ws, error):
        logging.error(f"Chyba WebSocketu: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logging.info("Spojení uzavřeno")
        time.sleep(5)
        self.connect()

    def send_ping(self):
        while self.keep_running:
            time.sleep(180)  # každých 3 minuty
            if self.ws and self.ws.sock and self.ws.sock.connected:
                try:
                    logging.debug("Odesílám ping na server...")
                    self.ws.send('{"method": "PING", "id": 1}')
                except Exception as e:
                    logging.error(f"Ping selhal: {e}")


    def connect(self):
        socket = f"wss://stream.binance.com:9443/ws/{self.symbol}@trade"
        self.ws = websocket.WebSocketApp(socket,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()
         # Spustíme pinger v novém vlákně
        ping_thread = threading.Thread(target=self.send_ping)
        ping_thread.daemon = True
        ping_thread.start()

    def disconnect(self):
        if self.ws:
            self.ws.close()
