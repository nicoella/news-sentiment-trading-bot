from datetime import datetime 
import yfinance as yf
import backtrader as bt
from trading_bot import TradingBotBacktest
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def backtest():
    cerebro = bt.Cerebro()
    
    cerebro.addstrategy(TradingBotBacktest)
    
    # get SPX 500 data
    df = yf.download('^SPX', start='2020-01-01', end='2024-02-29')
    
    # convert to feed
    feed = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(feed)
    
    # set starting cash
    cerebro.broker.setcash(100000.0)
    
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    # run
    cerebro.run()
    
    # cerebro.plot() 
    
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
backtest()