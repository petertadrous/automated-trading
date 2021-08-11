import time
import pandas as pd
from Portfolio import Portfolio
import TRADECONFIG

# I was getting a weird error with numpy and plotting, this next line seemed to fix.
pd.plotting.register_matplotlib_converters()

def main():
    start_time = time.time()

    tlist = TRADECONFIG.TICKER_LIST
    start = TRADECONFIG.START_DATE
    end = TRADECONFIG.END_DATE
    max_short = TRADECONFIG.MAX_SHORT
    max_long = TRADECONFIG.MAX_LONG
    display_individual_plots = TRADECONFIG.DISPLAY_INDIVIDUAL_PLOTS

    pf = Portfolio(tlist,start,end,max_short,max_long)
    # Can use pf.trade() or multiprocessing computation with pf.mp_trade().
    # mp_trade() doesn't work on windows because the spawn method is 'spawn' not 'fork'
    pf.mp_trade()
    pf.create_portfolio()
    pf.print_results(display_individual_plots)

    end_time = time.time()
    run_time = end_time - start_time
    print('Portfolio took {:>10.2} minutes to run.'.format(run_time/60))

if __name__ == "__main__":
    main()