import pandas as pd
import tpqoa
from sentiment import total_sentiment

# constants
API = tpqoa.tpqoa("oanda.cfg")
INSTRUMENT = "US SPX 500"
UNITS = 100000

# variables
bought = 0

# function to buy stock once
def buy_stock():
    API.create_order(instrument = INSTRUMENT, units = UNITS)
    bought += UNITS

# function to sell stock once
def sell_stock():
    API.create_order(instrument = INSTRUMENT, units = -UNITS)
    bought -= UNITS

# function to check to buy
def check_buy(sentiment):
    if sentiment == 1:
        buy_stock()
    
# function to check to sell
def check_sell(sentiment):
    if sentiment == -1:
        sell_stock()
    
# function to check based on if we have stock bought
def check():
    sentiment = total_sentiment()
    if bought: # already have stock, check to sell
        check_sell(sentiment)
    else: # don't have stock, check to buy
        check_buy(sentiment)