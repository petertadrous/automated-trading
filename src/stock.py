from dataclasses import dataclass, field
from functools import cached_property


from  pandas_datareader import data as pdr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
yf.pdr_override()


from src.utils import strfdate, add_days
from src.base import _DateHandler


def get_stock_data(
        symbol: str,
        start: str,
        end: str,
) -> pd.DataFrame:
    data: pd.DataFrame = pdr.get_data_yahoo(symbol, start=start, end=end) # type: ignore
    data.reset_index(drop=False, inplace=True)
    return data


@dataclass
class Stock(_DateHandler):
    symbol: str
    buffer: int = field(default=0, kw_only=True)

    @cached_property
    def data(self) -> pd.DataFrame:
        data = get_stock_data(
            self.symbol,
            strfdate(add_days(self.start_date, -self.buffer)),
            self.end_date)
        data = data[['Date','Adj Close']].copy()
        data.rename(columns={'Adj Close':'Close'}, inplace=True)
        return data
    
    @cached_property
    def _date_filter(self) -> np.ndarray:
        return (self.data['Date'] >= self.start_date).to_numpy()
    
    @cached_property
    def start_price(self) -> float:
        return self.data[self._date_filter]['Close'].values[0]
    @cached_property
    def end_price(self) -> float:
        return self.data[self._date_filter]['Close'].values[-1]
    
    @cached_property
    def log_returns(self) -> np.ndarray:
        close_price = self.data['Close'][self._date_filter]
        return np.log(close_price) - np.log(close_price.shift(1))

    @cached_property
    def total_baseline_return(self) -> float:
        # BUY
        #  - buy one share everyday
        return (self.log_returns.sum())

        # ## NAIVE
        # ##  - if today's price is lower than yesterday, sell everything
        # ##  - once today's price is back, buy back all your shares plus one more
        # today = self.data[self._date_filter]['Close']
        # yesterday = self.data[self._date_filter]['Close'].shift(1)
        # naive_decisions = np.where(today < yesterday, 1 , 0)
        # return (naive_decisions * self.log_returns).sum()

    # Plots only the "Close" column over time
    def plot_close(self):
        with plt.style.context('ggplot'): # type: ignore
            plt.figure(figsize=(8,6))
            plt.plot(self.data[self._date_filter]['Date'],
                     self.data[self._date_filter]['Close'],
                     label=self.symbol)
            plt.legend(loc=2)
            plt.show()
    