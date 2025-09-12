import argparse
import logging
import time
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET
from utils import load_client, validate_symbol, get_lot_size, round_qty

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    parser.add_argument("--total_qty", required=True, type=float)
    parser.add_argument("--slices", required=True, type=int)
    parser.add_argument("--delay", required=True, type=float, help="Seconds between slices")
    args = parser.parse_args()

    client = load_client()
    symbol = args.symbol.upper()

    if not validate_symbol(client, symbol):
        print("❌ Invalid symbol")
        return

    step = get_lot_size(client, symbol)
    per_slice = round_qty(args.total_qty / args.slices, step)
    if per_slice <= 0:
        print("❌ Quantity too small per slice")
        return

    side = SIDE_BUY if args.side == "BUY" else SIDE_SELL
    print(f"TWAP: {args.slices} slices of {per_slice}, {args.delay}s apart")

    try:
        for i in range(args.slices):
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=per_slice
            )
            logging.info(f"TWAP slice {i+1}: {order}")
            print(f"✅ Slice {i+1} placed: {order['orderId']}")
            time.sleep(args.delay)
    except Exception as e:
        logging.error(f"TWAP error: {e}")
        print("❌ Error:", e)

if __name__ == "__main__":
    main()
