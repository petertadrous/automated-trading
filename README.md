
# Automated Trading Program

## About

Automatically buys or sells stock based on the short and long running averages.

## Goal

This was a project for my CUS690 - Applied Analytics Project in which we had to use the `pandas_datareader` api to find the optimal `short_moving_average` and `long_moving_average` for a given portfolio of stock tickers.  
We were given free reign to implement this however we saw fit. My implementation uses a `TradingSystem` class for handling the data of a single ticker, and a `Portfolio` class for handling multiple `TradingSystem` objects.

## Requirements

The required packages are:
- pandas
- numpy
- pandas_datareader
- matplotlib

One optional package (for improved speed) is:
- multiprocessing

## Usage

1. Clone this repo
```git clone https://github.com/petertadrous/automated-trading.git```
2. Install the required packages
```pip install -U -r requirements.txt```
3. Optionally install additional package
```pip install -U -r optional-requirements.txt```
4. Modify the parameters `TRADECONFIG.py`
5. Run the main script
```python main.py```

## License

MIT License

Copyright (c) 2021 petertadrous

## Contact

Peter Tadrous - petertadrous@gmail.com  
Project Link: https://github.com/petertadrous/automated-trading