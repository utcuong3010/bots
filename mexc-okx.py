import ccxt
import time
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize exchanges
mexc = ccxt.mexc({
    'apiKey': 'mx0vglWw8Idz0ZrgBw',
    'secret': 'da9a9884b6e24164ba85aa5723ca45ff',
})

okx = ccxt.okx({
    'apiKey': 'your_okx_api_key',
    'secret': 'your_okx_secret_key'
})

# Telegram bot configuration
telegram_bot_token = '6730502276:AAFmOESXnxwwv5tZugCgMNzA0a-Wo4g6xjg'
telegram_chat_id = '1478894343'

# List of trading pairs
trading_pairs = ['BTC/USDT', 'ETH/USDT', 'LTC/USDT', 'XRP/USDT']  # Add more pairs as needed

# Function to get price data for a specific pair
def get_price_data(pair):
    try:
        mexc_ticker = mexc.fetch_ticker(pair)
        okx_ticker = okx.fetch_ticker(pair)
        
        mexc_price = mexc_ticker['last']
        okx_price = okx_ticker['last']
        
        return mexc_price, okx_price
    except Exception as e:
        logging.error(f"Error fetching price data for {pair}: {e}")
        return None, None

# Function to check for arbitrage opportunities
def check_arbitrage_opportunity(mexc_price, okx_price):
    if okx_price > mexc_price:
        profit_percent = (okx_price - mexc_price) / mexc_price * 100
        if profit_percent > 1:  # Example threshold
            return "buy_mexc_sell_okx", profit_percent
    elif mexc_price > okx_price:
        profit_percent = (mexc_price - okx_price) / okx_price * 100
        if profit_percent > 1:  # Example threshold
            return "buy_okx_sell_mexc", profit_percent
    return None, 0

# Function to execute trades and calculate profit
def execute_trade(strategy, pair, amount):
    try:
        if strategy == "buy_mexc_sell_okx":
            logging.info(f"Executing buy on MEXC and sell on OKX for {pair}")
            mexc.create_market_buy_order(pair, amount)
            okx.create_market_sell_order(pair, amount)
            
            # Calculate profit
            mexc_price, okx_price = get_price_data(pair)
            profit = (okx_price - mexc_price) * amount
            logging.info(f"Profit for {pair}: {profit:.2f} USDT")
            return profit
        
        elif strategy == "buy_okx_sell_mexc":
            logging.info(f"Executing buy on OKX and sell on MEXC for {pair}")
            okx.create_market_buy_order(pair, amount)
            mexc.create_market_sell_order(pair, amount)
            
            # Calculate profit
            mexc_price, okx_price = get_price_data(pair)
            profit = (mexc_price - okx_price) * amount
            logging.info(f"Profit for {pair}: {profit:.2f} USDT")
            return profit
    
    except Exception as e:
        logging.error(f"Error executing trade for {pair}: {e}")
        return 0

# Function to get account balances
def get_balances():
    try:
        mexc_balance = mexc.fetch_balance()
        okx_balance = okx.fetch_balance()
        
        mexc_usdt = mexc_balance['total']['USDT']
        okx_usdt = okx_balance['total']['USDT']
        
        return mexc_usdt, okx_usdt
    except Exception as e:
        logging.error(f"Error fetching balances: {e}")
        return 0, 0

# Function to send a message to the Telegram bot
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {
        'chat_id': telegram_chat_id,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            logging.info("Telegram message sent successfully")
        else:
            logging.error(f"Failed to send Telegram message: {response.text}")
    except Exception as e:
        logging.error(f"Error sending Telegram message: {e}")

# Main loop
def main():
    trade_amount = 0.01  # Adjust according to your risk tolerance and capital
    total_profit = 0
    
    while True:
        mexc_usdt, okx_usdt = get_balances()
        logging.info(f"MEXC Balance: {mexc_usdt:.2f} USDT, OKX Balance: {okx_usdt:.2f} USDT")
        
        for pair in trading_pairs:
            mexc_price, okx_price = get_price_data(pair)
            
            if mexc_price and okx_price:
                strategy, profit_percent = check_arbitrage_opportunity(mexc_price, okx_price)
                
                if strategy:
                    logging.info(f"Arbitrage opportunity found for {pair}: {strategy} with profit {profit_percent:.2f}%")
                    profit = execute_trade(strategy, pair, trade_amount)
                    total_profit += profit
                    
                    # Send profit update to Telegram
                    message = f"Arbitrage trade executed for {pair}:\nStrategy: {strategy}\nProfit: {profit:.2f} USDT\nTotal Profit: {total_profit:.2f} USDT"
                    send_telegram_message(message)
                    
                else:
                    logging.info(f"No arbitrage opportunity found for {pair}")
        
        logging.info(f"Total Profit: {total_profit:.2f} USDT")
        
        # Wait before next check
        time.sleep(5)

if __name__ == "__main__":
    main()
