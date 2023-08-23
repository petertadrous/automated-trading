from dataclasses import dataclass


import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
pd.plotting.register_matplotlib_converters()


from src.stock import Stock
from src.base import TradingStrategy


@dataclass
class StockTrader(Stock, TradingStrategy):
    """Creates stock ticker object"""
    short_window: int
    long_window: int
    
    @property
    def ma_short(self) -> np.ndarray:
        return self.data['Close'].rolling(self.short_window).mean()[self._date_filter].to_numpy()
    @property
    def ma_long(self) -> np.ndarray:
        return self.data['Close'].rolling(self.long_window).mean()[self._date_filter].to_numpy()
    @property
    def trade_decisions(self) -> np.ndarray:
        return np.where(self.ma_long < self.ma_short, 1 , 0)
    @property
    def managed_returns(self) -> np.ndarray:
        return self.trade_decisions * self.log_returns
    @property
    def total_managed_return(self) -> float:
        return self.managed_returns.sum()
    @property
    def managed_performance(self) -> float:
        return ((self.total_managed_return + 1) / (self.total_baseline_return + 1)) - 1

    # Plots the "Close", "Short", and "Long" columns over time
    def plot_moving_averages(self):
        with plt.style.context('ggplot'): # type: ignore
            plt.figure(figsize=(8,6))
            plt.plot(self.data[self._date_filter]['Date'],
                     self.data[self._date_filter]['Close'],
                     label=self.symbol)
            plt.plot(self.data[self._date_filter]['Date'],
                     self.ma_short,
                     label='Short Moving Average: {}'.format(self.short_window))
            plt.plot(self.data[self._date_filter]['Date'],
                     self.ma_long,
                     label='Long Moving Average {}'.format(self.long_window))
            plt.legend(loc=2)
            plt.show()
    
    
    # Prints the results of the trading system for this stock
    def print_results(self):
        print(f'"{self.symbol}"')
        print(f'Our strategy :{self.total_managed_return:>10.2%}')
        print(f'Baseline     :{self.total_baseline_return:>10.2%}')
        
        if self.managed_performance > 0:
            print(f'The trading system outperformed baseline by:{self.managed_performance:>10.2%}')
        elif self.managed_performance < 0:
            inverted_performance = (1 / (self.managed_performance+1)) - 1
            print(f'Baseline outperformed the trading system by:{inverted_performance:>10.2%}')
        else:
            print('The trading system performance was equivalent to baseline.')
