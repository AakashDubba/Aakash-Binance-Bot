import os
import math
import logging
from dotenv import load_dotenv
from binance.client import Client

# Setup logging
logging.basicConfig(filename="bot.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def load_client():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("API_KEY or API_SECRET missing in .env file")

    client = Client(api_key, api_secret, testnet=True)
    client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
    return client

def validate_symbol(client, symbol):
    info = client.futures_exchange_info()
    symbols = [s['symbol'] for s in info['symbols']]
    return symbol.upper() in symbols

def get_lot_size(client, symbol):
    info = client.futures_exchange_info()
    for s in info['symbols']:
        if s['symbol'] == symbol:
            for f in s['filters']:
                if f['filterType'] == 'LOT_SIZE':
                    return float(f['stepSize'])
    return 1.0

def round_qty(qty, step):
    return math.floor(qty / step) * step
