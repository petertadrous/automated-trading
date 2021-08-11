import pandas as pd
try:
    from multiprocessing import Pool
    CAN_USE_MP = True
except:
    CAN_USE_MP = False
from TradingSystem import TradingSystem

# I was getting a weird error with numpy and plotting, this next line seemed to fix.
pd.plotting.register_matplotlib_converters()

# Portfolio class, takes a list of tickers, a start date, end date, max short, and max long to create a portfolio
class Portfolio(object):
    def __init__(self,tlist,start,end,max_short,max_long):
        self.ticker_list = tlist
        self.start = start
        self.end = end
        self.max_short = max_short + 1
        self.max_long = max_long + 1
        self.portfolio_list = []
        self.trading_systems = {}
        print('Created portfolio.\n{}\n\n'.format(tlist))
    
    # Calls find_best_moving_averages() and saves results
    def trade(self):
        for ticker in self.ticker_list:
            self.trading_systems[ticker], ts_res = self.find_best_moving_averages(ticker)
            self.portfolio_list.append(ts_res)
    
    # Takes a multiprocessing approach of previous function for better performance
    def mp_trade(self):
        if CAN_USE_MP:
            print('Beginning multiprocessing.')
            try:
                pool = Pool()
                self.ts_list = []
                ts_res = pool.map(self.find_best_moving_averages, self.ticker_list)
                for res in ts_res:
                    self.trading_systems[res[0].symbol] = res[0]
                    self.portfolio_list.append(res[1])
            finally:
                pool.close()
                pool.join()
        else:
            print('Cannot use multiprocessing because the package is not installed.')
            self.trade()
    
    # Programatically calculates each moving average in given winddow and finds optimal short and long
    def find_best_moving_averages(self,ticker):
        ts_ret = 0
        tr_ret = 0
        optimal_short = 0
        optimal_long = 0
        ts_perf = 0
        print('Creating instance of trading system for {}.'.format(ticker))
        ts = TradingSystem(ticker,self.start,self.end,optimal_short,optimal_long)
        for short in range(2,self.max_short):
            for long in range(short+3,self.max_long):
                ts.short = short
                ts.long = long
                ts.trade()
                temp_perf = ts.get_performance()
                if temp_perf > ts_perf:
                    ts_ret, tr_ret = ts.get_results()
                    ts_perf = temp_perf
                    optimal_short = short
                    optimal_long = long
        print('Found optimal moving averages for {}.\tShort: {}, Long: {}'.format(ticker,
                                                                                    optimal_short,
                                                                                    optimal_long))
        ts.short = optimal_short
        ts.long = optimal_long
        ts.trade()
        return ts, [ticker,self.start,self.end,optimal_short,optimal_long,ts_ret,tr_ret,ts_perf]
    
    # Creates a dataframe with the results
    def create_portfolio(self):
        self.portfolio_results_df = pd.DataFrame(self.portfolio_list, columns = ['Ticker',
                                                                                 'Start',
                                                                                 'End',
                                                                                 'Short',
                                                                                 'Long',
                                                                                 'TS_Return',
                                                                                 'Trad_Return',
                                                                                 'Performance'])
    
    # Prints the results of the portfolio, with the option of displaying the graphs of each stock and ma's
    def print_results(self,display_plots):
        if display_plots:
            for ticker in self.ticker_list:
                self.trading_systems[ticker].plot_ma()
                self.trading_systems[ticker].print_results()
                print('\n{}\n'.format('*'*75))
        print('\n')
        performance_value = self.portfolio_results_df.Performance.mean()
        print(performance_value)
        if performance_value > 1:
            print('On average, the trading system portfolio outperformed traditional portfolio by:{:>10.2%}'.format(performance_value-1))
        elif performance_value < 1:
            p_val = 1/performance_value
            print('On average, traditional portfolio outperformed the trading system portfolio by:{:>10.2%}'.format(p_val-1))
        else:
            print('The trading system portfolio performance was equivalent to traditional portfolio.')
        print(self.portfolio_results_df)
        