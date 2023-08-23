
import matplotlib
matplotlib.use('TkAgg')

import time
import pandas as pd
from src.portfolio import TradingPortfolio
import yaml

# I was getting a weird error with numpy and plotting, this next line seemed to fix.
pd.plotting.register_matplotlib_converters()

def main():
    with open('./config/config.yaml') as f:
        TRADECONFIG = yaml.safe_load(f)
    start_time = time.time()

    pf = TradingPortfolio(
        symbols=TRADECONFIG['TICKER_LIST'],
        start_date=TRADECONFIG['START_DATE'],
        end_date=TRADECONFIG['END_DATE'],
        min_short=TRADECONFIG['MIN_SHORT'],
        max_short=TRADECONFIG['MAX_SHORT'],
        min_window_diff=TRADECONFIG['MIN_LONG_DIFFERENCE'],
        max_long=TRADECONFIG['MAX_LONG'],
        parallelize=TRADECONFIG.get('USE_MULTIPROCESSING', False),
    )
    
    # NOTE: mp_trade() doesn't work on windows because the spawn method is 'spawn' not 'fork'
    pf.grid_search()
    pf.print_results(TRADECONFIG['DISPLAY_INDIVIDUAL_PLOTS'])

    end_time = time.time()
    run_time = end_time - start_time
    print('Portfolio took {:>10.2} minutes to run.'.format(run_time/60))
    pf.managed_returns.to_csv('./examples/example_results.csv', index=False)

if __name__ == "__main__":
    main()