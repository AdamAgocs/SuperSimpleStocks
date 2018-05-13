'''
Created on 13 May 2018

@author: agocsi
'''

from pandas import Timestamp, Timedelta, date_range
from random import randint
from stocks import StockManager, StockManagerException, StockException
from trades import Trade, TradeManager

# stock's header
HEADER = ['symbol_', 'type', 'last_dividend_', 'fixed_dividend_', 'par_value_']

# stocks
STOCKS = [['TEA', 'Common', 0, '', 100], ['POP', 'Common', 8, '', 100], 
          ['ALE', 'Common', 23, '', 60], ['GIN', 'Preferred', 8, 0.02, 100], 
          ['JOE', 'Common', 13, '',250]]

# when the data acquisition is started
SHIFT = 60 

NUMBER_OF_TRADES = 1000
QUANTITY_INTERVAL = (1000, 2000)
TRADE_PRICE_INTERVAL = (500, 1000)

_stock_manager = StockManager()
_stock_manager.create_stocks_header(HEADER, STOCKS)

BEGINING_OF_TRADES = Timestamp.now()-Timedelta(seconds=SHIFT)

def generate_trades():
    '''
    Generator of trades (attributes of trades)
    '''
    number_of_stocks = len(_stock_manager)
    list_of_stock_symbol = list(_stock_manager.keys())
    
    list_of_stocks = [list_of_stock_symbol[randint(0, number_of_stocks-1)] for x in range(0, NUMBER_OF_TRADES)]
    list_of_quantities = [randint(QUANTITY_INTERVAL[0], QUANTITY_INTERVAL[1]) for x in range(0, NUMBER_OF_TRADES)]
    list_of_buys_or_sells = [randint(0,1) for x in range(0, NUMBER_OF_TRADES)]
    list_of_trade_prices = [randint(TRADE_PRICE_INTERVAL[0], TRADE_PRICE_INTERVAL[1]) for x in range(0, NUMBER_OF_TRADES)]
    list_of_timestamps = date_range(BEGINING_OF_TRADES, periods=NUMBER_OF_TRADES, freq='200L')
    
    return zip(list_of_stocks, list_of_timestamps, list_of_quantities, list_of_buys_or_sells, list_of_trade_prices)


def simulation():
    '''
    It shows 
     - at each trade - DIVIDEND YIELD, P/E RATIO values
     - last 15 secs trades - Valume Weighted Stock Price
     - all trades - GBCE ALL Share Index
    '''
    trade_manager = TradeManager()
    list_of_trades = generate_trades()
    
    for trade in list_of_trades:
        print('TRADE: {0}'.format(trade))
        stock = _stock_manager[trade[0]]
        print('STOCKS -- SYMBOL: {0}, MARKET PRICE: {1}, DIVIDEND YEALD: {2}, P/E RATIO: {3}'. format(trade[0], trade[4], stock.dividend_yield(trade[4]), 
                                                                                                      stock.pe_ratio(trade[4])))
        trade_manager.add(Trade(*trade))
    
    print('TRADES -- Volume Weighted Stock Price in the last 15 seconds: {0}'.format(trade_manager.volume_weighted_stock_price(15)))
    print('TRADES -- GBCE All Share Index: {0}'.format(trade_manager.gbce_all_share_index()))
