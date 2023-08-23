from dataclasses import dataclass
from functools import cached_property
from typing import List, Dict


import numpy as np
import pandas as pd

from src.base import TradingStrategy
from src.trading import StockTrader


try:
    from multiprocessing import Pool
    CAN_USE_MP = True
except:
    CAN_USE_MP = False

# I was getting a weird error with numpy and plotting, this next line seemed to fix.
pd.plotting.register_matplotlib_converters()

@dataclass
class PortfolioTrader(TradingStrategy):
    
    symbols: List[str]
    min_short: int = 2
    max_short: int = 50
    min_window_diff: int = 5
    max_long: int = 100
    parallelize: bool = False

    def __post_init__(self):
        self.max_short += 1
        self.max_long = self.max_long + 1
        print('Created portfolio.\n{}\n\n'.format(self.symbols))
    
    @cached_property
    def data(self) -> Dict[str, StockTrader]:
        data = {}
        for s in self.symbols:
            data[s] = StockTrader(
                symbol=s,
                start_date=self.start_date,
                end_date=self.end_date,
                short_window=self.min_short,
                long_window=self.min_short + self.min_window_diff,
                buffer=self.max_long,
            )
        return data

    @property
    def managed_returns(self) -> pd.DataFrame:
        return pd.DataFrame([
            {
                'Ticker': symbol,
                'Start Price': stock.start_price,
                'Start': self.start_date,
                'End': self.end_date,
                'Short': stock.short_window,
                'Long': stock.long_window,
                'Baseline': stock.total_baseline_return,
                'Managed': stock.total_managed_return,
                '% Difference': 100 * stock.managed_performance,
                '$ Profit': stock.start_price * (stock.total_managed_return+1),
            }
            for symbol, stock in self.data.items()
        ])

    @cached_property
    def total_baseline_return(self) -> float:
        ret = np.exp(self.managed_returns['Baseline'])
        weights = self.managed_returns['Start Price'] / self.managed_returns['Start Price'].sum()
        return (ret * weights).sum()

    @property
    def total_managed_return(self) -> float:
        ret = np.exp(self.managed_returns['Managed'])
        weights = self.managed_returns['Start Price'] / self.managed_returns['Start Price'].sum()
        return (ret * weights).sum()

    @cached_property
    def managed_performance(self) -> float:
        # https://quant.stackexchange.com/a/71078
        return np.log(self.total_managed_return - self.total_baseline_return + 1)
    
    # Calls find_best_moving_averages() and saves results
    def grid_search(self):
        self.__dict__.pop('managed_performance', None)
        if self.parallelize:
            if CAN_USE_MP:
                return self._mp_gridsearch()
            print('Cannot use multiprocessing because the package is not installed.')
        for ticker in self.symbols:
            self._search(ticker)
    
    # Takes a multiprocessing approach of previous function for better performance
    def _mp_gridsearch(self):
        print('Beginning multiprocessing.')
        pool = None
        try:
            pool = Pool()
            self.ts_list = []
            return pool.map(self._search, self.symbols)
        finally:
            if pool is not None:
                pool.close()
                pool.join()
    
    # Programatically calculates each moving average in given winddow and finds optimal short and long
    def _search(self,ticker):
        optimal_short = -1
        optimal_long = -1
        ts_return = -np.inf
        print(f'Creating instance of trading system for {ticker}.')
        ts = self.data[ticker]
        for short in range(self.min_short, self.max_short):
            for long in range(short+self.min_window_diff, self.max_long):
                ts.short_window = short
                ts.long_window = long
                temp_return = ts.total_managed_return
                if temp_return > ts_return:
                    ts_return = temp_return
                    optimal_short = short
                    optimal_long = long

        ts.short_window = optimal_short
        ts.long_window = optimal_long
        print((
            f'Found optimal moving averages for {ticker: <6}.'
            f'\tShort: {optimal_short}, Long: {optimal_long}'
        ))

    
    # Plots only the "Close" column over time
    def plot_close(self):
        for stock in self.data.values():
            stock.plot_close()

    # Prints the results of the portfolio, with the option of displaying the graphs of each stock and ma's
    def print_results(self, display_plots: bool):
        if display_plots == True:
            for symbol in self.symbols:
                self.data[symbol].plot_moving_averages()
                self.data[symbol].print_results()
                print('\n{}\n'.format('*'*75))
        print('\n')
        if self.managed_performance > 0:
            print(('On average, the trading system portfolio outperformed '
                   f'traditional portfolio by:{self.managed_performance:>10.2%}'))
        elif self.managed_performance < 0:
            inverse_performance = (1/(self.managed_performance + 1)) - 1
            print(('On average, traditional portfolio outperformed the '
                   f'trading system portfolio by:{inverse_performance:>10.2%}'))
        else:
            print('The trading system portfolio performance was equivalent to traditional portfolio.')
        print(self.managed_returns)
        