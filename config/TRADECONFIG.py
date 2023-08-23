# The list of ticker strings to add to the portfolio
TICKER_LIST = ['ZM','DOCU','WMT','AAPL','GE','TSLA','INTC','WORK','VVNT','EL.PA']

# The start and end dates strings, in 'YYYYMMDD' format
START_DATE = '20200101'
END_DATE = '20201231'

# The minimum and maximum (inclusive) 'short' to check between
MIN_SHORT = 2
MAX_SHORT = 25

# The minimum 'long' to check is the current 'short' in the loop plus this value
MIN_LONG_DIFFERENCE = 3 
# The maximum 'long' to check
MAX_LONG = 50

# Whether or not to display the individual plots for each ticker
DISPLAY_INDIVIDUAL_PLOTS = False

# Whether or not to use multiprocessing to speed up the calculations
# (does not work on windows)
USE_MULTIPROCESSING = False
