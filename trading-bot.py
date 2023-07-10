import requests
from binance.client import Client
import pandas as pd
import numpy as np

# Binance Future API
API_Key = "8368d40730e2b4531161326ac034b5d7f7bfea1181466dc56c25ec2b3e7b12ec"
API_Secret = "fe1ede6407ba302a5246db92b8f1ce98a70ccb7245ee77184629f380ce7e70cd"

client = Client(API_Key, API_Secret, testnet=True)

# Constants
SYMBOL = "BTCUSDT"
TIME_PERIOD = "1m"  # Taking 1 minute time period
LIMIT = 200  # Taking 200 candles as limit
QNTY = 0.03
stock_price = []
pos_held = False

# Get our account information
account = client.futures_account_balance()
asset = pd.DataFrame(account)
print(asset)

# Calculate EMA
def calculate_ema(prices, days, smoothing=2):
    ema = [np.mean(prices[:days])]
    for price in prices[days:]:
        ema.append((price * (smoothing / (1 + days))) + ema[-1] * (1 - (smoothing / (1 + days))))
    return ema[-1]

# EMA Algorithm
while True:
    print("")
    print("Checking Price")
    
    # Get data from Binance
    url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval={TIME_PERIOD}&limit={LIMIT}"
    res = requests.get(url)
    data = res.json()
    close_prices = np.array([float(each[4]) for each in data])
    
    ema = calculate_ema(close_prices, len(close_prices))
    last_price = close_prices[-1]  # Most recent closing price
    
    print("Exponential Moving Average:", ema)
    print("Last Price:", last_price)
    
    # Buy
    if last_price > ema and not pos_held:  # If price is crossing EMA, and we haven't already bought -> so we buy it
        print("Buy")
        client.futures_create_order(symbol=SYMBOL, side="BUY", type="MARKET", quantity=QNTY)
        pos_held = True
        stock_price.append(last_price)
    print(stock_price)

    # Sell
    if len(stock_price) != 0:
        if last_price >= (stock_price[-1] + stock_price[-1] * 0.0013) and pos_held:
            print("Sell take profit")
            client.futures_create_order(symbol=SYMBOL, side="SELL", type="MARKET", quantity=QNTY)
            pos_held = False
            stock_price.clear()
        elif last_price <= (stock_price[-1] - stock_price[-1] * 0.05) and pos_held:
            print("Sell stop loss")
            client.futures_create_order(symbol=SYMBOL, side="SELL", type="MARKET", quantity=QNTY)
            pos_held = False
            stock_price.clear()
