import pandas as pd

def calculate_sma(data, period):
    return data['close'].rolling(window=period).mean()

def trading_signal(data):
    data['sma_short'] = calculate_sma(data, 20)
    data['sma_long'] = calculate_sma(data, 50)
    
    if data['sma_short'].iloc[-1] > data['sma_long'].iloc[-1]:
        return 'buy'
    elif data['sma_short'].iloc[-1] < data['sma_long'].iloc[-1]:
        return 'sell'
    else:
        return 'hold'


def place_order(symbol, side, amount, price):
    order = exchange.create_limit_order(symbol, side, amount, price)
    print(order)
