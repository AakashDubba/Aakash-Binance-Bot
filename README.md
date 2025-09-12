# Aakash Binance Bot

A simplified **Python trading bot** built for **Binance Futures Testnet (USDT-M)**.  
This bot allows users to place **Market orders, Limit orders, OCO (Take-Profit + Stop-Loss), and TWAP (time-weighted execution)** directly from the command line.  
All trades, errors, and execution details are logged for analysis.

---

## ⚙️ Setup Instructions

### 1. Clone / Create Project
```bash
git clone https://github.com/AakashDubba/Aakash-Binance-Bot
cd Aakash_binance_bot
````

Or if you have the project as a `.zip`, just unzip it.

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate the venv:

* **Windows (PowerShell)**

  ```bash
  .\venv\Scripts\activate
  ```
* **Mac/Linux**

  ```bash
  source venv/bin/activate
  ```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Setup API Keys

1. Go to [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Create an **API Key + Secret** from **API Management**.
3. Create a `.env` file in your project root:

```
API_KEY=your_testnet_api_key_here
API_SECRET=your_testnet_api_secret_here
```

⚠️ Never commit your `.env` file to GitHub.

---

## 📂 Project Structure

```
Aakash_binance_bot/
├── src/
│   ├── utils.py              # Utility functions (API client, validation, rounding)
│   ├── market_orders.py      # Place market buy/sell orders
│   ├── limit_orders.py       # Place limit buy/sell orders
│   └── advanced/
│       ├── oco.py            # OCO (Take-Profit + Stop-Loss)
│       └── twap.py           # TWAP (time-weighted split orders)
├── trading_bot.log           # Logs (API requests, responses, errors)
├── requirements.txt          # Python dependencies
├── README.md                 # Setup & usage instructions
└── report.pdf                # Analysis report (screenshots, logs, explanations)
```

---

## ▶️ Usage

Run scripts from the **project root**:

### Market Order

```bash
python src/market_orders.py --symbol BTCUSDT --side BUY --qty 0.001
```

### Limit Order

```bash
python src/limit_orders.py --symbol BTCUSDT --side SELL --qty 0.001 --price 50000
```

### OCO (Take-Profit + Stop-Loss)

```bash
python src/advanced/oco.py --symbol BTCUSDT --side BUY --qty 0.001 --tp 35000 --sl 28000
```

### TWAP (Split into smaller orders)

```bash
python src/advanced/twap.py --symbol BTCUSDT --side BUY --total_qty 0.01 --slices 5 --delay 10
```

---

## 📜 Logs

All actions (orders placed, errors, responses) are stored in:

```
trading_bot.log
```

Each entry includes timestamp, type of order, and execution details.

---


## 🚀 Features

* Market orders (Buy/Sell)
* Limit orders (Buy/Sell at set price)
* OCO orders (Take-Profit + Stop-Loss together)
* TWAP strategy (split order into time intervals)
* Logging of all trades and errors
