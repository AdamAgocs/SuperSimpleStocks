'''
Created on 10 May 2018

@author: agocsi
'''

from abc import ABC, ABCMeta, abstractmethod
from collections import MutableMapping


class StockException(Exception):
    def __init__(self, message_):
        super(StockException, self).__init__(message_)

class StockManagerException(Exception):
    def __init__(self, message_):
        super(StockManagerException, self).__init__(message_)


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
    '''
    Class for handling Preferred Stocks.
    '''
    def __init__(self, symbol_, last_dividend_, fixed_dividend_, par_value_):
        '''
        Constructor
         
        @symbol_ - Symbol of the given stock
        @last_dividend_ - The last dividend value of the stock 
        @fixed_dividend_ - The fixed dividend value of the stock
        @par_value_ - The par value of the stock
        '''
        super(PreferredStock, self).__init__(symbol_, last_dividend_, par_value_)
        self.fixed_dividend = float(fixed_dividend_)
        self.par_value = par_value_
        
    def dividend_yield(self, market_price_):
        '''
        See at Stock class
        
        The used formula is \frac{fixed dividend * par value}{market price}
        '''
        return self.fixed_dividend * self.par_value / market_price_ if market_price_ != 0 else 0

class CommonStock(Stock):
    '''
    Class for handling Common Stocks
    '''
    def __init__(self, symbol_, last_dividend_, par_value_):
        '''
        Constuctor 
        
        @symbol_ - The symbol of the given stock
        @last_dividend_ - The last dividend value of the given stock
        @par_value_ - Par value of the given stock
        '''
        super(CommonStock, self).__init__(symbol_, last_dividend_, par_value_)
        
    def dividend_yield(self, market_price_):
        '''
        See at Stock class
        
        The used formula is \frac{last dividend}{market price}
        '''
        return (self.last_dividend / market_price_) if market_price_ != 0 else 0

class _SingletonStockManager(type):
    '''
    The meta class of Stock Manager.
    This is an elegant way to handle singletons.
    '''
    
    _instance = None
    def __call__(cls):
        if cls._instance == None:
            cls._instance = super(_SingletonStockManager, cls).__call__()
        return cls._instance 
    
class _CombinedSingletonStockManager(ABCMeta, _SingletonStockManager):
    '''
    Because Stock Manager is a subclass of MutableMapping Abstract Class and MutableMapping's meta class
    is ABCMeta, we have to combine our meta classes. Just for technical purpose!!!
    '''
    pass

class StockManager(MutableMapping, metaclass=_CombinedSingletonStockManager):
    '''
    Stock Manager class.
    1) Subclass of MutableMapping
    2) Meta classes: ABCMeta and _SingletonStockManager
    3) Singleton
    '''
    def __init__(self):
        '''
        Constructor for initialisation
        '''
        self.__stocks = {}
        self.__type = {'Common' : CommonStock,
            'Preferred' : PreferredStock,
        }
    
    def __iter__(self):
        '''
        Inherited abstract function - iterator
        
        @return - Iterator on the stocks symbols!!!!
        '''
        return iter(self.__stocks)

    def __len__(self):
        '''
        Inherited abstract function - length
        
        @return - Number of stored stocks
        '''
        return len(self.__stocks)
    
    def __getitem__(self, key):
        '''
        Inherited abstract function - getter
        
        @return - give back the corresponding value of a key
        '''
        return self.__stocks[key]
    
    def __setitem__(self, key, value):
        '''
        Inherited abstract function - setter
        '''
        if isinstance(value, Stock):
            self.__stocks[key] = value
        else:
            raise StockManager('Invalid Value')
            
    def __delitem__(self, key):
        '''
        Inherited abstract function - delete
        '''
        del self.__stocks[key]
    
    
    def create_stocks(self, type_, **kwargs):
        '''
        Generate single stock
        
        @type_ - Type of the stock (Common or Preferred)
        @kwargs - Attributes of the given stock
        '''
        self.__stocks[kwargs['symbol_']] = self.__type[type_](**kwargs)
    
        
    def create_stocks_header(self, header, stocks):
        '''
        Generate multiple stocks
        
        @header - The attribute list of the stocks
        @stocks - List of stocks
        '''
        for stock in stocks:
            input = dict(filter(lambda x: x[1] != '', zip(header, stock)))
            self.create_stocks(input.pop('type'), **input)
    
    @classmethod
    def _clear(cls):
        '''
        Class method for testing if the class is singleton or not 
        '''
        cls._instance = None 
