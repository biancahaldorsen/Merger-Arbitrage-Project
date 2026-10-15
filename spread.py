import yfinance as yf
import pandas as pd

#In all cash deal buyer pays a fixed dollar amount per share and the spread is the gap
#between that offer and the target's current price. 
#Gross Spread = Offer - Target 
#Spread % = (Offer - Target)/Target
target_ticker = "BMBL" 
offer_price = 6.05 
bumble = yf.Ticker(target_ticker)
history = bumble.history(period="5d")

#Calculates gross spread and spread percent! 
def calculate_spread(offerprice, targetprice): 
    gross_spread = offerprice - targetprice
    spread_percent = (gross_spread)/targetprice
    return gross_spread, spread_percent

#checks if data table is empty or can be called
if history.empty:
    print (f"No price data found for {target_ticker}, maybe confirm ticker spelling.")
else:
    print(history)
    #clean NaNs from close column and get the most recent closing price using loc and iloc on data frame 
    history_clean = history.dropna(subset = "Close")
    closing_prices = history_clean.loc[:, "Close"]
    current_target_price = closing_prices.iloc[-1]

    spread_information = calculate_spread(offer_price, current_target_price)
    gspread, spreadp = spread_information
    print(f"The gross spread for today is ${gspread:.2f} and the spread percentage is {spreadp:.2%}.")
 