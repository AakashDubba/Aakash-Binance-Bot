import argparse
import logging
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET
from utils import load_client, validate_symbol, get_lot_size, round_qty

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    parser.add_argument("--qty", required=True, type=float)
    args = parser.parse_args()

    client = load_client()
    symbol = args.symbol.upper()

    if not validate_symbol(client, symbol):
        print("❌ Invalid symbol")
        return

    step = get_lot_size(client, symbol)
    qty = round_qty(args.qty, step)

    side = SIDE_BUY if args.side == "BUY" else SIDE_SELL

    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_MARKET,
            quantity=qty
        )
        logging.info(f"Market order placed: {order}")
        print("✅ Market order placed:", order)
    except Exception as e:
        logging.error(f"Market order error: {e}")
        print("❌ Error:", e)

if __name__ == "__main__":
    main()
