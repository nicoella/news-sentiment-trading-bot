import tpqoa
from sentiment import calculate_sentiment
import backtrader as bt

# constants
DEFAULT_API = tpqoa.tpqoa("oanda.cfg")
DEFAULT_INSTRUMENT = "US SPX 500"
DEFAULT_UNITS = 100000

# real time trading bot
class TradingBot():
    # initialize function
    def __init__(self, api = DEFAULT_API, instrument = DEFAULT_INSTRUMENT, units = DEFAULT_UNITS):
        self.api = api
        self.instrument = instrument
        self.units = units
        self.bought = 0
        
    # function to buy stock once
    def buy_stock(self):
        self.api.create_order(instrument = self.instrument, units = self.units)
        self.bought += self.units

    # function to sell stock once
    def sell_stock(self):
        self.api.create_order(instrument = self.instrument, units = -self.units)
        self.bought -= self.units

    # function to check to buy
    def check_buy(self, probability, sentiment):
        if sentiment == "positive" and probability > 0.99:
            self.buy_stock()
        
    # function to check to sell
    def check_sell(self, probability, sentiment):
        if sentiment == "negative" and probability > 0.99:
            self.sell_stock()
        
    # function to check based on if we have stock bought
    def check(self, date):
        probability, sentiment = calculate_sentiment(date)
        probability_val = float(probability.item())
        print(sentiment)
        print(probability_val)
        if self.bought: # already have stock, check to sell
            self.check_sell(probability_val, sentiment)
        else: # don't have stock, check to buy
            self.check_buy(probability_val, sentiment)
      
# backtest trading bot      
class TradingBotBacktest(TradingBot, bt.Strategy):
    # override function to buy stock once
    def buy_stock(self):
        self.buy()
        self.bought += self.units
        print('buying')
    
    # override function to sell stock once
    def sell_stock(self):
        self.sell()
        self.bought -= self.units
        print('selling')
    
    # logging function
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.strftime("%m/%d/%Y"), txt))

    # initializer
    def __init__(self):
        super().__init__() 
        self.data = self.datas[0].open

    # next function for backtesting
    def next(self):
        # log opening price
        self.log('Open, %.2f' % self.data[0])
        
        # buy or sell stock
        self.check(self.datas[0].datetime.date(0).strftime("%m/%d/%Y"))