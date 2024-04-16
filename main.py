import schedule
import time
from trading_bot import check
    
# define time to check
schedule.every().day.at("09:20").do(check)

# run scheduler loop
def main():
    while True:
        schedule.run_pending()
        time.sleep(60)
    
if __name__ == "__main__":
    main()
