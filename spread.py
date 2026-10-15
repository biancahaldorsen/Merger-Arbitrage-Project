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

##########################################################################################

#annualized return will be simple and non-compounded here, also dividends are ignored. 
    #Annualized return = (offer - target)/target * 365/(Days Expected to Close)
#implied probability of deal completion where if the deal fails we assume target falls back to price before deal announced
# Note that this version of implied P can result in cases where P>100% or <0% so we will need to account for that
    #Implied P = (target price - fallback price)/(offer - fallback price)

#Stock for stock deals, holders receive a fixed number of acquirer shares (the exchange ratio) per target share,
#so the offer value moves with the acquirer's price:
    # Offer value = exchange ratio * acquirer price + cash per share 

def calculate_offer_value(cash_per_share, exchange_ratio = 0, acquirer_p = 0): 
    offer_value = exchange_ratio * acquirer_p + cash_per_share
    return offer_value

def calculate_annualized_return(offer_price, target_price, days_to_close): 
    annualized_return = (offer_price - target_price)/(target_price) * (365/days_to_close)
    return annualized_return

def calculate_implied_p(offer_price, target_price, fallback_price):
    implied_p = (target_price - fallback_price)/(offer_price - fallback_price)
    return implied_p


 