import ccxt
import pandas as pd

exchange = ccxt.mexc()
symbol = 'BTC/USDT'
timeframe = '1h'
data = exchange.fetch_ohlcv(symbol, timeframe)
df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
print(df.head())
