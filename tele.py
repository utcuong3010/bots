import ccxt
import time
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Telegram bot configuration
telegram_bot_token = '6730502276:AAFmOESXnxwwv5tZugCgMNzA0a-Wo4g6xjg'
telegram_chat_id = '1478894343'


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
    while True:
        message = "testing"
        # Send profit update to Telegram
        # message = f"Arbitrage trade executed for {pair}:\nStrategy: {strategy}\nProfit: {profit:.2f} USDT\nTotal Profit: {total_profit:.2f} USDT"
        send_telegram_message(message)
                
        logging.info("logging.....")
        # Wait before next check
        time.sleep(5)

if __name__ == "__main__":
    main()
