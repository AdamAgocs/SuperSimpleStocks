'''
Created on 10 May 2018

@author: agocsi
'''

from abc import ABC, ABCMeta, abstractmethod
from collections import MutableMapping


class StockException(Exception):
    def __init__(self, message_):
        self.message = message_

class Stock(ABC):
    '''
    Abstract class for stocks
    '''
    
    def __init__(self, symbol_, last_dividend_, par_value_):
        '''
        Constructor
        
        @symbol_ - The symbol of the given stock
        @last_dividend_ - The last dividend value of the given stock
        @par_value_ - Par value of the given stock
        '''
        
        self.symbol = str(symbol_)
        self.last_dividend = int(last_dividend_)
        self.par_value = int(par_value_)
    
    def pe_ratio(self, market_price_):
        '''
        P/E ratio : $\frac{Market Price}{Dividend}$
        
        @market_price_ - The current value of the given stock
        '''
        return int(market_price_) / self.last_dividend if self.last_dividend != 0 else 0
    
    @abstractmethod
    def dividend_yield(self, market_price_):
        '''
        Abstract function of Stock class
        Because there are two different stock type, namely, common and preferred.
        
        @market_price_ - The current price of the given stock
        '''
        
        raise StockException('Abstract function of Stock Abstract class')
        
class PreferredStock(Stock):
    def __init__(self, symbol_, last_dividend_, fixed_dividend_, par_value_):
        super(PreferredStock, self).__init__(symbol_, last_dividend_, par_value_)
        self.fixed_dividend = float(fixed_dividend_)
        self.par_value = par_value_
        
    def dividend_yield(self, market_price_):
        return self.fixed_dividend * self.par_value / market_price_

class CommonStock(Stock):
    def __init__(self, symbol_, last_dividend_, par_value_):
        super(CommonStock, self).__init__(symbol_, last_dividend_, par_value_)
        
    def dividend_yield(self, market_price):
        return self.last_dividend / market_price

class _SingletonStockManager(type):
    _instance = None
    def __call__(cls):
        if cls._instance == None:
            cls._instance = super(_SingletonStockManager, cls).__call__()
        return cls._instance 
    
class _CombinedSingletonStockManager(ABCMeta, _SingletonStockManager):
    pass

class StockManager(MutableMapping, metaclass=_CombinedSingletonStockManager):
    def __init__(self):
        self.__stocks = {}
        self.__type = {'common' : CommonStock,
            'preferred' : PreferredStock,
        }
    
    def __iter__(self):
        return iter(self.__stocks)

    def __len__(self):
        return len(self.__stocks)
    
    def __getitem__(self, key):
        return self.__stocks[key]
    
    def __setitem__(self, key, value):
        if isinstance(value, Stock):
            self.__stocks[key] = value
            
    def __delitem__(self, key):
        del self.__stocks[key]
        
    def create_stocks(self, type_, **kwargs):
        self.__stocks[kwargs['symbol_']] = self.__type[type_](**kwargs)
        
    @classmethod
    def _clear(cls):
        cls._instance = None 
