import yfinance as yf
import pandas as pd

#In all cash deal buyer pays a fixed dollar amount per share and the spread is the gap
#between that offer and the target's current price. 
#Gross Spread = Offer - Target 
#Spread % = (Offer - Target)/Target
#Calculates gross spread and spread percent! 
def calculate_spread(offerprice, targetprice): 
    gross_spread = offerprice - targetprice
    spread_percent = (gross_spread)/targetprice
    return gross_spread, spread_percent

##########################################################################################
# Offer value = exchange ratio * acquirer price + cash per share 
def calculate_offer_value(cash_per_share, exchange_ratio = 0, acquirer_p = 0): 
    offer_value = exchange_ratio * acquirer_p + cash_per_share
    return offer_value
#Annualized return = (offer - target)/target * 365/(Days Expected to Close)
def calculate_annualized_return(offer_price, target_price, days_to_close): 
    if days_to_close == 0: 
        print ("The days to close is 0 meaning that the deal is expected to close today.")
        return None
    if days_to_close < 0: 
        print ("The expected close day for the deal has already passed.") 
        return None
    if target_price <= 0: 
        print ("The target price is 0 or negative, this is likely an error.")
        return None
    annualized_return = (offer_price - target_price)/(target_price) * (365/days_to_close)
    if offer_price < target_price: 
        print (f"The annualized return is {annualized_return:.2%}, meaning the market may expect a higher offer value in the future.")
    return annualized_return
    
#implied probability of deal completion where if the deal fails we assume target falls back to price before deal announced
# Note that this version of implied P can result in cases where P>100% or <0% so we will need to account for that
    #Implied P = (target price - fallback price)/(offer - fallback price)
def calculate_implied_p(offer_price, target_price, fallback_price):
    if offer_price - fallback_price == 0:
        print ("The offer price is equal to the fallback price, meaning the divisor is 0 and the function cannot complete.")
        return None
    implied_p = (target_price - fallback_price)/(offer_price - fallback_price)
    if  implied_p <= 1 and implied_p >= 0:
        return implied_p
    else:
        print (f"The implied probability is {implied_p:.2%} meaning the market price has gone past the boundaries of the model's assumptions.")
        return implied_p

#calculates and returns the deal fallback price based on the unaffected date but is scaled 
# by how much comparable stocks have moved since

def calculate_adjusted_fallback(unaffected_price, index_price_then, index_price_now): 
    if unaffected_price is None or index_price_then is None or index_price_now is None:
        print("The function inputs are not complete. At least one argument is None.")
        return None
    if index_price_then <= 0: 
        print (f"The index price on the unaffected 0 or negative. The fallback price cannot be calculated.")
        return None
    adjusted_fallback_price = unaffected_price *(index_price_now/index_price_then)
    return adjusted_fallback_price