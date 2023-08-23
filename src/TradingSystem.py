import pandas as pd
import numpy as np
import pandas_datareader as pdr
import matplotlib.pyplot as plt

# I was getting a weird error with numpy and plotting, this next line seemed to fix.
pd.plotting.register_matplotlib_converters()

# Trading system class, creates trading system object.
class TradingSystem(object):
    def __init__(self,ticker,start,end,mavg1,mavg2):
        self.symbol = ticker
        self.start = start
        self.end = end
        self.short = mavg1
        self.long = mavg2
        self.data_copy = pdr.get_data_yahoo(self.symbol,start=start,end=end)
        self.data_copy = self.data_copy.reset_index(drop=False)[['Date','Close']]
    
    # Trades and sets results using short and long ma
    def trade(self):
        self.data = self.data_copy.copy()
        self.data['ma_short'] = self.data.Close.rolling(self.short).mean()
        self.data['ma_long'] = self.data.Close.rolling(self.long).mean()
        self.data.dropna(inplace=True)
        self.data['trade'] = np.where(self.data.ma_long<self.data.ma_short,1,-1)
        self.set_results()
        
    # Plots only the "Close" column over time
    def plot_close(self):
        with plt.style.context('ggplot'):
            plt.figure(figsize=(8,6))
            plt.plot(self.data.Date,self.data.Close,label=self.symbol)
            plt.legend(loc=2)
            plt.show()
    
    # Plots the "Close", "Short", and "Long" columns over time
    def plot_ma(self):
        with plt.style.context('ggplot'):
            plt.figure(figsize=(8,6))
            plt.plot(self.data.Date,self.data.Close,label=self.symbol)
            plt.plot(self.data.Date,self.data.ma_short,label='Short Moving Average: {}'.format(self.short))
            plt.plot(self.data.Date,self.data.ma_long,label='Long Moving Average {}'.format(self.long))
            plt.legend(loc=2)
            plt.show()
       
    # Sets results from the trade() function
    def set_results(self):
        self.data['return'] = np.log(self.data.Close).diff()
        self.data['treturn'] = self.data['return']*self.data['trade']
        self.data.dropna(inplace=True)
    
    # Retrieves results computed by the trade function
    def get_results(self):
        system_return = np.sum(np.exp(self.data['treturn']))/100
        traditional_return = np.sum(np.exp(self.data['return']))/100
        return system_return, traditional_return
    
    # Returns single value of performance of trading system compared to traditional buy and hold
    def get_performance(self):
        system_return, traditional_return = self.get_results()
        return system_return/traditional_return
    
    # Prints the results of the trading system for this stock
    def print_results(self):
        system_return, traditional_return = self.get_results()
        print('Our trading system:{:>10.2%}'.format(system_return))
        print('Traditional system:{:>10.2%}'.format(traditional_return))
        
        performance_value = system_return/traditional_return
        if performance_value > 1:
            print('The trading system outperformed traditional by:{:>10.2%}'.format(performance_value-1))
        elif performance_value < 1:
            p_val = 1/performance_value
            print('Traditional outperformed the trading system by:{:>10.2%}'.format(p_val-1))
        else:
            print('The trading system performance was equivalent to traditional.')