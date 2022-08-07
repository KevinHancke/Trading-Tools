-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Trading-Tools
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
This is a Library of technical indicators, trading tools and scripts for use in algorhythmic trading


1. Prerequisites:(I recommend downloading the graphical installer from anaconda.com)
    -Python 3.8 of greater
    -jupyter notbooks
    -pandas
    -ta
    -numpy
    -yfinance
    
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Journal:
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1. 03-08-2022:Found a library called tradingview-ta can give OHLC and the infamous "buy/sell" or "strong buy/sell" indicator based on the trading view calculation, alongside some indicator values added a python notebook to pull this data.
2. 04-08-2022:tradingview-ta library has no means of gaining historical data, uploaded a script to generate a buy/sell signal
3. 05-08-2022:Uploaded a simple backtest using the backtesting.py with an SMA cross strategy.
4. 06-08-2022:Uploaded incomplete script for backtesting a simple stoch RSI and SMA cross strategy
5. 07-08-2022: *NB* FOUND an 84.9% winning strategy, using fibonnaci SMA and the Stoch RSI cross (uploaded the notebook) this seems really unrealistic and I will backtest on multiple platforms
