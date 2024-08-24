import ccxt

exchange = ccxt.binance()  # Use the exchange of your choice
ticker = exchange.fetch_ticker('BTC/USDT')
print(ticker)
