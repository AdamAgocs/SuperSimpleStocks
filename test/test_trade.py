'''
Created on 11 May 2018

@author: agocsi
'''
import unittest
from trades import Trade, TradeManager, TradeManagerException, TradeException
from stocks import Stock, StockManager
from ddt import ddt, data, unpack


HEADER = ['symbol_', 'type', 'last_dividend_', 'fixed_dividend_', 'par_value_']
STOCKS = [['TEA', 'Common', 0, '', 100], ['POP', 'Common', 8, '', 100], 
          ['ALE', 'Common', 23, '', 60], ['GIN', 'Preferred', 8, 0.02, 100], 
          ['JOE', 'Common', 13, '',250]]

@ddt
class TestTrade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._sm = StockManager()
        cls._sm.create_stocks_header(HEADER, STOCKS)
        
    @classmethod
    def tearDownClass(cls):
        cls._sm._clear()
    
    @data(('TEA', '2015-JAN-21 00:12:11', 1000, Trade.BUY, 1000),
          ('ALE', '2015-JAN-21 00:12:11', 1000, Trade.SELL, 1000))
    @unpack
    def testCreateATrade(self, stock_symbol_, timestamp_, quantity_, buy_or_sell_, trade_price_):
        t = Trade(stock_symbol_, timestamp_, quantity_, buy_or_sell_, trade_price_)
        self.assertTrue(t.valid())

    @data(('TEA1', '2015-JAN-21 00:12:11', 1000, Trade.BUY, 1000),
          ('TEA', '2015-JAN-42 00:12:11', -111, Trade.BUY, 1000),
          ('TEA', '2015-JANUAR-21 00:12:11', 1000, Trade.BUY, 1000),
          ('TEA', '2015-JAN-21 00:12:11', 0, Trade.BUY, 1000),
          ('TEA', '2015-JAN-21 00:12:11', -1000, Trade.BUY, 1000),
          ('TEA', '2015-JAN-21 00:12:11', 1000, Trade.BUY, -1000),
          ('TEA', '2015-JAN-21 00:12:11', 1000, Trade.BUY, 0))
    @unpack
    def testInvalidTrade(self, stock_symbol_, timestamp_, quantity_, buy_or_sell_, trade_price_):
        with self.assertRaises(TradeException):
            t = Trade(stock_symbol_, timestamp_, quantity_, buy_or_sell_, trade_price_)
            
            
    @data(('TEA', 1000, Trade.BUY, 1000),
          ('ALE', 1000, Trade.SELL, 1000))
    @unpack
    def testCreateATrade2(self, stock_symbol_, quantity_, buy_or_sell_, trade_price_):
        t = Trade.create_trade(stock_symbol_, quantity_, buy_or_sell_, trade_price_)
        self.assertTrue(t.valid())

    @data(('TEA1', 1000, Trade.BUY, 1000),
          ('TEA', 0, Trade.BUY, 1000),
          ('TEA', -1000, Trade.BUY, 1000),
          ('TEA', 1000, Trade.BUY, -1000),
          ('TEA', 1000, Trade.BUY, 0))
    @unpack
    def testInvalidTrade2(self, stock_symbol_, quantity_, buy_or_sell_, trade_price_):
        with self.assertRaises(TradeException):
            t = Trade.create_trade(stock_symbol_, quantity_, buy_or_sell_, trade_price_)

@ddt
class TestTradeManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._sm = StockManager()
        cls._sm.create_stocks_header(HEADER, STOCKS)
        
    @classmethod
    def tearDownClass(cls):
        cls._sm._clear()
        
    
    def tearDown(self):
        TradeManager._clear()
        
    def testSingleton(self):
        tm1 = TradeManager()
        tm2 = TradeManager()
        self.assertEqual(tm1, tm2)
    
    @data(('TEA', '2015-JAN-21 00:12:11', 1000, Trade.BUY, 1000),
          ('ALE', '2015-JAN-21 00:12:11', 1000, Trade.SELL, 1000))
    @unpack
    def testAddingTrade(self, stock_symbol_, timestamp_, quantity_, buy_or_sell_, trade_price_):
        t = Trade(stock_symbol_, timestamp_, quantity_, buy_or_sell_, trade_price_)
        tm = TradeManager()    
        tm.add(t)
        self.assertEqual(len(tm), 1)
        
    @data(1, 'a', True, 0.1)
    def testAddingFalseTrade(self, data):
        tm = TradeManager()
        with self.assertRaises(TradeManagerException):
            tm.add(data)
            
    
        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()