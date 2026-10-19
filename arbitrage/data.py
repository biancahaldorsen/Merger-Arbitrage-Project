import pandas as pd
import yfinance as yf
from datetime import timedelta

#gets the most recent closing price for a given ticker and returns it as a float
def get_latest_price(ticker):
    if pd.isna(ticker):
        return None
    this_ticker = yf.Ticker(ticker) #sets ticker string from data frame to a yfinance ticker
    history = this_ticker.history(period = "5d")
    if history.empty:
        print(f"There is no data available for ticker {ticker}.  Check that the ticker is spelled correctly, or the stock may be delisted (deal closed).")
        return None
    history_clean = history.dropna(subset = "Close")
    if history_clean.empty:
        print(f"There are no valid closing prices for {ticker}.")
        return None
    closing_prices = history_clean.loc[:, "Close"]
    price = closing_prices.iloc[-1]
    return price

#gets the stock price on a ticker for a given date 
def get_price_on(ticker, date):
    if pd.isna(ticker):
        return None
    if pd.isna(date):
        return None
    this_ticker = yf.Ticker(ticker)
    history = this_ticker.history(start = date, end = date + timedelta(days =1)) #end in yfinance.history is exclusive so start date is given date and end is next day
    if history.empty:
        print(f"There is no data available for ticker {ticker}. Check to make sure ticker is spelled correctly or {date:%Y-%m-%d} was not a weekend or holiday.")
        return None
    history_clean = history.dropna(subset = "Close")
    if history_clean.empty:
        print(f"There are no valid closing prices for {ticker} on {date}. It may have been a weekend or holiday.")
        return None
    closing_prices = history_clean.loc[:, "Close"]
    price = closing_prices.iloc[-1]
    return price

def get_price_history(ticker, start_date): 
    if pd.isna(ticker):
        return None
    this_ticker = yf.Ticker(ticker)
    ticker_history = this_ticker.history(start = start_date)
    if ticker_history.empty:
        print(f"There is no data available for ticker {ticker}. Check that the ticker is spelled correctly, or the stock may be delisted (deal closed).")
        return None
    ticker_history_cleaned = ticker_history.dropna(subset = "Close")
    if ticker_history_cleaned.empty:
        print(f"There are no valid closing prices for {ticker}.")
        return None
    closing_prices = ticker_history_cleaned.loc[:, "Close"]
    closing_prices.index = closing_prices.index.tz_localize(None)
    return closing_prices
    
    # Returns a pandas Series of daily closing prices from start_date to today,
    # or None if the ticker is blank or no data comes back