import schedule
import time
from trading_bot import TradingBot
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

bot = TradingBot()

# define time to check
schedule.every().day.at("09:30").do(bot.check)

# run scheduler loop
def main():
    while True:
        schedule.run_pending()
        time.sleep(60)
    
if __name__ == "__main__":
    main()
