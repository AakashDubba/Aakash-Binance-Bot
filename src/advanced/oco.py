import argparse
import logging
import time
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_LIMIT, ORDER_TYPE_STOP_MARKET, TIME_IN_FORCE_GTC
from utils import load_client, validate_symbol, get_lot_size, round_qty

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    parser.add_argument("--qty", required=True, type=float)
    parser.add_argument("--tp", required=True, type=float)
    parser.add_argument("--sl", required=True, type=float)
    args = parser.parse_args()

    client = load_client()
    symbol = args.symbol.upper()

    if not validate_symbol(client, symbol):
        print("❌ Invalid symbol")
        return

    step = get_lot_size(client, symbol)
    qty = round_qty(args.qty, step)

    # If initial trade was BUY (long), TP/SL are SELL
    tp_side = SIDE_SELL if args.side == "BUY" else SIDE_BUY
    sl_side = tp_side

    try:
        tp_order = client.futures_create_order(
            symbol=symbol,
            side=tp_side,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=qty,
            price=str(args.tp)
        )
        sl_order = client.futures_create_order(
            symbol=symbol,
            side=sl_side,
            type=ORDER_TYPE_STOP_MARKET,
            stopPrice=str(args.sl),
            quantity=qty
        )
        print("✅ TP & SL orders placed")
        logging.info(f"OCO orders placed: TP={tp_order}, SL={sl_order}")

        tp_id, sl_id = tp_order['orderId'], sl_order['orderId']

        # Poll until one fills
        while True:
            tp_status = client.futures_get_order(symbol=symbol, orderId=tp_id)
            sl_status = client.futures_get_order(symbol=symbol, orderId=sl_id)

            if tp_status['status'] == 'FILLED' and sl_status['status'] != 'FILLED':
                client.futures_cancel_order(symbol=symbol, orderId=sl_id)
                print("✅ TP filled, SL canceled")
                break
            elif sl_status['status'] == 'FILLED' and tp_status['status'] != 'FILLED':
                client.futures_cancel_order(symbol=symbol, orderId=tp_id)
                print("✅ SL filled, TP canceled")
                break
            time.sleep(2)

    except Exception as e:
        logging.error(f"OCO error: {e}")
        print("❌ Error:", e)

if __name__ == "__main__":
    main()
