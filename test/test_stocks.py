'''
Created on 10 May 2018

@author: agocsi
'''
import unittest
from stocks import StockManager, CommonStock, PreferredStock, Stock
from ddt import ddt, data, unpack

@ddt
class Test(unittest.TestCase):
    @data(('TEA',0,100),
          ('POP',8,100),
          ('ALE',23,60),
          ('JOE',13,250))
    @unpack
    def test_create_common_stocks_good(self, symbol_, last_dividend_, par_value_):
        c = CommonStock(symbol_, last_dividend_, par_value_)
        self.assertTrue(isinstance(c, CommonStock))
        
    @data(('GIN',8, 0.02,100),)
    @unpack
    def test_create_preferred_stocks_good(self, symbol_, last_dividend_, fixed_dividend_, par_value_):
        c = PreferredStock(symbol_, last_dividend_, fixed_dividend_, par_value_)
        self.assertTrue(isinstance(c, PreferredStock))

    @data(('TEA',0,100),
          ('POP',8,100),
          ('ALE',23,60),
          ('JOE',13,250))
    @unpack
    def test_create_stock(self, symbol_, last_dividend_, par_value_):
        with self.assertRaises(TypeError):
            Stock(symbol_, last_dividend_, par_value_)
    
    @data(('TEA',0,100,100, 0),
          ('POP',8,100,100, 0.08),
          ('ALE',23,60,100, 0.23),
          ('JOE',13,250,100, 0.13))
    @unpack
    def test_dividend_yield_common(self, symbol_, last_dividend_, par_value_, price_, expected_value_):
        c = CommonStock(symbol_, last_dividend_, par_value_)
        self.assertEqual(c.dividend_yield(price_), expected_value_)
        
    @data(('GIN',8, 0.02, 100, 100, 0.02),)
    @unpack
    def test_dividend_yield_preferred(self, symbol_, last_dividend_, fixed_dividend_, par_value_, price_, expected_value_):
        c = PreferredStock(symbol_, last_dividend_, fixed_dividend_, par_value_)
        self.assertEqual(c.dividend_yield(price_), expected_value_)
        
    def test_stock_manager_singleton(self):
        sm1 = StockManager()
        sm2 = StockManager()
        self.assertEqual(sm1, sm2)
        StockManager._clear()
    
    @data(('TEA',0,100),
          ('POP',8,100),
          ('ALE',23,60),
          ('JOE',13,250))
    @unpack
    def test_adding_stocks(self, symbol_, last_dividend_, par_value_):
        c = CommonStock(symbol_, last_dividend_, par_value_)
        sm = StockManager()
        current_lenght = len(sm) #singleton, it was not killed
        sm[symbol_] = c
        self.assertTrue(len(sm)==current_lenght+1)
        
    @data(('GIN',8, 0.02,100),)
    @unpack
    def test_adding_preferred_stocks(self, symbol_, last_dividend_, fixed_dividend_, par_value_):
        c = PreferredStock(symbol_, last_dividend_, fixed_dividend_, par_value_)
        sm = StockManager() 
        current_lenght = len(sm)
        sm[symbol_] = c
        self.assertTrue(len(sm)==current_lenght+1)
    
    @data(('common', {'symbol_': 'TEA', 'last_dividend_' : 0, 'par_value_' : 100}),
          ('common', {'symbol_': 'POP', 'last_dividend_' : 8, 'par_value_' : 100}),
          ('common', {'symbol_': 'ALE', 'last_dividend_' : 23,'par_value_' : 60}),
          ('common', {'symbol_': 'JOE', 'last_dividend_' : 13,'par_value_' : 250}),
          ('preferred', {'symbol_': 'GIN', 'last_dividend_' : 8, 'par_value_' : 100, 'fixed_dividend_': 0.02})
        )
    @unpack
    def test_adding_stocks(self, type_, value):
        StockManager._clear()
        sm = StockManager()
        
        sm.create_stocks(type_, **value)
        self.assertTrue(len(sm)==1)
        

        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()