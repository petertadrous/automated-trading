import time
import pandas as pd
from src.Portfolio import Portfolio
from config import TRADECONFIG

# I was getting a weird error with numpy and plotting, this next line seemed to fix.
pd.plotting.register_matplotlib_converters()

def main():
    start_time = time.time()

    pf = Portfolio(
        tlist=TRADECONFIG.TICKER_LIST,
        start=TRADECONFIG.START_DATE,
        end=TRADECONFIG.END_DATE,
        min_short=TRADECONFIG.MIN_SHORT,
        max_short=TRADECONFIG.MAX_SHORT,
        min_long_diff=TRADECONFIG.MIN_LONG_DIFFERENCE,
        max_long=TRADECONFIG.MAX_LONG
    )
    
    if TRADECONFIG.USE_MULTIPROCESSING:
        # mp_trade() doesn't work on windows because the spawn method is 'spawn' not 'fork'
        pf.mp_trade()
    else:
        pf.trade()
    pf.create_portfolio()
    pf.print_results(TRADECONFIG.DISPLAY_INDIVIDUAL_PLOTS)

    end_time = time.time()
    run_time = end_time - start_time
    print('Portfolio took {:>10.2} minutes to run.'.format(run_time/60))

if __name__ == "__main__":
    main()