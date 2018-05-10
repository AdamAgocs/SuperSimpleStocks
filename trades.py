'''
Created on 10 May 2018

@author: agocsi
'''


from abc import ABCMeta
from collections import Iterable
from pandas import DataFrame, Timestamp, Timedelta
from numpy import array
from stocks import StockManager

class TradeManagerException(Exception):
    def __init__(self, message_):
        super(TradeManagerException, self).__init__(message_)
        
class Trade(dict):
    def __init__(self, stock_, timestamp_, quantity_, buy_or_sell_, trade_price_):
        self['stock'] = str(stock_)
        self['timestamp'] = Timestamp(timestamp_)
        self['quantity'] = int(quantity_)
        self['buy_or_sell'] = bool(buy_or_sell_)
        self['trade_price'] = int(trade_price_)

class _SingletonTradeManager(type):
    _instance = None
    
    def __call__(cls, *args, **kwargs):
        if cls._instance == None:
            cls._instance = super(_SingletonTradeManager, cls).__call__()
        return cls._instance 

class TradeManager(metaclass=_SingletonTradeManager):
    def __init__(self):
        super(TradeManager, self).__init__()
        self.__storage = []
        
    def add(self, trade_):
        self.__storage.append(trade_)
        
    def volume_weighted_stock_price(self, interval_):
        try:
            #unfortunately, pandas' DataFrame cannot be appended "in place".
            df = DataFrame(self.__storage)
            df.set_index('timestamp')
            
            current_df = df[df.timestamp >= Timestamp.now('CET')-Timedelta(seconds = int(interval_))]
            return sum(current_df.quantity * current_df.trade_price)/sum(current_df.quantity)
        except TypeError:
            raise TradeManagerException('Invalid time interval')
    
    def gbce_all_share_index():
        return array([trade['quantity']*trade['trade_price'] for trade in self.__storage]).prod()**(1.0/len(self.__storage))
    
        
    
        