import ccxt
import time
import pandas as pd
import numpy as np

# exchange = ccxt.binance({
#     'apiKey': 'YOUR_API_KEY',
#     'secret': 'YOUR_SECRET_KEY',
# })

exchange = ccxt.mexc({
    'apiKey': 'mx0vglWw8Idz0ZrgBw',
    'secret': 'da9a9884b6e24164ba85aa5723ca45ff',
})

def fetch_data(symbol, timeframe):
    data = exchange.fetch_ohlcv(symbol, timeframe)
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def moving_average_crossover(df):
    df['short_ma'] = df['close'].rolling(window=50).mean()
    df['long_ma'] = df['close'].rolling(window=200).mean()
    df['signal'] = 0
    df['signal'][50:] = np.where(df['short_ma'][50:] > df['long_ma'][50:], 1, 0)
    df['position'] = df['signal'].diff()
    return df

def trade(symbol, amount, action):
    try:
        if action == 'buy':
            order = exchange.create_market_buy_order(symbol, amount)
        elif action == 'sell':
            order = exchange.create_market_sell_order(symbol, amount)
        print(order)
    except Exception as e:
        print(f"Error: {e}")

def run_bot():
    symbol = 'BTC/USDT'
    amount = 0.001
    while True:
        df = fetch_data(symbol, '1h')
        df = moving_average_crossover(df)
        if df['position'].iloc[-1] == 1:
            trade(symbol, amount, 'buy')
        elif df['position'].iloc[-1] == -1:
            trade(symbol, amount, 'sell')
        time.sleep(3600)

if __name__ == "__main__":
    run_bot()
