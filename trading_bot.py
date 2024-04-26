import tpqoa
from sentiment import calculate_sentiment
import backtrader as bt

# constants
DEFAULT_API = tpqoa.tpqoa("oanda.cfg")
DEFAULT_INSTRUMENT = "US SPX 500"
DEFAULT_UNITS = 1000

# real time trading bot
class TradingBot():
    # initialize function
    def __init__(self, api = DEFAULT_API, instrument = DEFAULT_INSTRUMENT, units = DEFAULT_UNITS):
        self.api = api
        self.instrument = instrument
        self.units = units
        self.bought = 0
        self.profit_margin = 1.02
        self.loss_margin = 0.95
        
    # function to buy stock once
    def buy_stock(self):
        self.api.create_order(instrument = self.instrument, units = self.units)
        self.bought = self.api.get_current_price(self.instrument)

    # function to sell stock once
    def sell_stock(self):
        self.api.create_order(instrument = self.instrument, units = -self.units)
        self.bought = 0

    # function to check to buy
    def check_buy(self, probability, sentiment):
        if sentiment == "positive" and probability > 0.9:
            self.buy_stock()
            
    # function to check profit / loss margin
    def check_profit_loss(self):
        current_price = self.api.get_current_price(self.instrument)
        return current_price > self.bought * self.profit_margin or current_price < self.bought * self.loss_margin
        
    # function to check to sell
    def check_sell(self, probability, sentiment):
        if self.check_profit_loss():
            self.sell_stock()
        
    # function to check based on if we have stock bought
    def check(self, date):
        probability, sentiment = calculate_sentiment(date)
        if probability is None or sentiment is None:
            return
        probability_val = float(probability.item())
        if self.bought > 0: # already have stock, check to sell
            self.check_sell(probability_val, sentiment)
        else: # don't have stock, check to buy
            self.check_buy(probability_val, sentiment)
      
# backtest trading bot      
class TradingBotBacktest(TradingBot, bt.Strategy):
    # override function to buy stock once
    def buy_stock(self):
        self.buy(size = 20)
        self.bought = self.data[0]
        # log messages
        self.log('close, %.2f' % self.data[0])
        print('buying')
        
    
    # override function to sell stock once
    def sell_stock(self):
        self.sell(size = 20)
        self.bought = 0
        # log messages
        self.log('close, %.2f' % self.data[0])
        print('selling')
        
    # override check profit / loss margin
    def check_profit_loss(self):
        return self.data[0] > self.bought * self.profit_margin or self.data[0] < self.bought * self.loss_margin
    
    # logging function
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.strftime("%m/%d/%Y"), txt))

    # initializer
    def __init__(self):
        super().__init__() 
        self.data = self.datas[0].close

    # next function for backtesting
    def next(self):        
        # buy or sell stock
        self.check(self.datas[0].datetime.date(0).strftime("%m/%d/%Y"))