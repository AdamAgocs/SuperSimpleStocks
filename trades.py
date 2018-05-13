'''
Created on 10 May 2018

@author: agocsi
'''


from abc import ABCMeta
from collections import Iterable
from pandas import DataFrame, Timestamp, Timedelta
from numpy import array
from math import log, exp
from stocks import StockManager

class TradeManagerException(Exception):
    def __init__(self, message_):
        super(TradeManagerException, self).__init__(message_)
        
class TradeException(Exception):
    def __init__(self, message_):
        super(TradeException, self).__init__(message_)

class Trade(dict):
    '''
    Class of Trade
    '''
    __sm = StockManager()
    
    BUY = True
    SELL = False
    
    def __init__(self, stock_symbol_, timestamp_, quantity_, buy_or_sell_, trade_price_):
        '''
        Constructor
        
        @stock_symbol_ - Symbol of the given stock
        @timestamp_ - Storing the time of the trade
        @quantity_ - Quantity of the stock
        @buy_or_sell_ - The stocks are bought or sold
        @trade_price_ - The price of the stocks
        '''
        
        try:
            self['stock'] = self.__sm[str(stock_symbol_)]
            self['timestamp'] = Timestamp(timestamp_)
            self['quantity'] = int(quantity_)
            self['buy_or_sell'] = bool(buy_or_sell_)
            self['trade_price'] = int(trade_price_)
        except (KeyError, ValueError) as error:
            raise TradeException(str(error))
        
        if not self.valid():
            raise TradeException('Non-valid input')
            
    @classmethod
    def create_trade(cls, stock_symbol_, quantity_, buy_or_sell_, trade_price_):
        '''
        Trade is created by using the current time
        
        @stock_symbol_ - Symbol of the given stock
        @quantity_ - Quantity of the stock
        @buy_or_sell_ - The stocks are bought or sold
        @trade_price_ - The price of the stocks
        '''
        return cls(stock_symbol_, Timestamp.now(), quantity_, buy_or_sell_, trade_price_)
    
    def valid(self):
        '''
        For validation
        '''
        return self['quantity'] > 0 and self['trade_price'] > 0
        
    
class _SingletonTradeManager(type):
    '''
    The meta class of Trade Manager.
    This is an elegant way to handle singletons.
    '''
    
    _instance = None
    def __call__(cls, *args, **kwargs):
        if cls._instance == None:
            cls._instance = super(_SingletonTradeManager, cls).__call__()
        return cls._instance 

class TradeManager(metaclass=_SingletonTradeManager):
    '''
    Trade Manager class.
    1) Meta classes: _SingletonStockManager
    2) Singleton
    '''
    def __init__(self):
        '''
        Constructor for initialisation
        
        Because dataframe creation is time consuming, we used timestamps for 
        checking if the previous dataframe is valid or not
        '''
        
        super(TradeManager, self).__init__()
        self.__storage = []
        
        self.__df_storage = None
        self.__df_time = None
        self.__append_time = None
        
    def add(self, trade_):
        '''
        adding a new trade
        
        @trade_ - The trade
        
        Note: appending time is saved for dataframe validation
        '''
        if isinstance(trade_, Trade):
            self.__storage.append(trade_)
            self.__append_time = Timestamp.now()
        else:
            raise TradeManagerException('Invalid trade')
        
    def __len__(self):
        return len(self.__storage)
        
    def volume_weighted_stock_price(self, interval_):
        '''
        Formula : \frac{\sum{i}{trade_price_i * qunatity_i}}{\sum{i}{quantity_i}}
        
        '''
        try:
            #unfortunately, pandas' DataFrame cannot be appended "in place".
            if self.__df_time == None or self.__append_time > self.__df_time:
                self.__df_storage = DataFrame(self.__storage)
                self.__df_storage.set_index('timestamp')
                self.__df_time = Timestamp.now()
            
            current_df = self.__df_storage[self.__df_storage.timestamp >= Timestamp.now()-Timedelta(seconds = int(interval_))]
            return sum(current_df.quantity * current_df.trade_price)/sum(current_df.quantity)
        except TypeError as te:
            raise TradeManagerException('Invalid time interval: {0}'.format(te))
    
    def gbce_all_share_index(self):
        '''
        Geometric mean for stock prices
        
        RELATIONSHIP WITH LOGARITHMS
        https://en.wikipedia.org/wiki/Geometric_mean#Relationship_with_logarithms
        '''
        try:
            return exp(sum([trade['quantity']*log(trade['trade_price']) for trade in self.__storage])/sum([trade['quantity'] for trade in self.__storage]))
        except ZeroDivisionError:
            return 0.0
        
    @classmethod
    def _clear(cls):
        TradeManager._instance = None
    
        
    
        