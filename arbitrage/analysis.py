
#takes a given row from deals.csv and returns a dictionary of target, acquirer, price, offer value, spread percentage
#days to close, annualized return, and implied probability 
from arbitrage.metrics import calculate_annualized_return, calculate_implied_p, calculate_offer_value, calculate_spread, calculate_adjusted_fallback
from arbitrage.data import get_latest_price, get_price_on 
import pandas as pd

def analyze_deal(row, index_ticker = None): 
    target_ticker = row["Target_Ticker"]
    acquirer_ticker = row["Acquirer_Ticker"]
    cash_per_share = row["Cash_Per_Share"]
    exchange_ratio = row["Exchange_Ratio"] 
    unaffected_date = row["Unaffected_Date"]
    expected_close = row["Expected_Close"]
    if pd.isna(exchange_ratio) or exchange_ratio == 0: 
        deal_offer_value = calculate_offer_value(cash_per_share) 
    else:
        acquirer_price = get_latest_price(acquirer_ticker)
        if acquirer_price is None: 
            print(f"The acquirer price for {acquirer_ticker} does not exist.")
            return None
        deal_offer_value = calculate_offer_value(cash_per_share, exchange_ratio, acquirer_price)

    target_price = get_latest_price(target_ticker)
    if target_price is None: 
        print(f"The target price for {target_ticker} does not exist.")
        return None
    spread_info = calculate_spread(deal_offer_value,target_price)
    deal_spread_percent = spread_info[1]

    day_today = pd.Timestamp.today().normalize()
    difference = expected_close - day_today
    days_to_close = difference.days
    deal_annualized_return = calculate_annualized_return(deal_offer_value, target_price, days_to_close)
    
    deal_fallback_price = get_price_on(target_ticker, unaffected_date)
    if deal_fallback_price is None: 
        print (f"Skipping implied probability for {target_ticker}")
        deal_implied_probability = None
    else: 
        deal_implied_probability = calculate_implied_p(deal_offer_value, target_price, deal_fallback_price)
    
    adjusted_fallback = None 
    adjusted_implied_p = None 
    index_change = None 

#if the user inputs an index_ticker also calculate the adjusted fallback price so they can compare between the 
#unaffected date fallback price and the unaffected date fallback price scaled for market movements
    if index_ticker is not None: 
        index_then = get_price_on(index_ticker, unaffected_date)
        index_now = get_latest_price(index_ticker)
        adjusted_fallback = calculate_adjusted_fallback(deal_fallback_price, index_then, index_now)
        if adjusted_fallback is not None: 
            adjusted_implied_p = calculate_implied_p (deal_offer_value, target_price, adjusted_fallback) 
        if index_then is not None and index_now is not None and index_then > 0: 
            index_change = (index_now - index_then)/index_then

    return {"Target":target_ticker, "Acquirer":acquirer_ticker, 
            "Price":target_price, "Offer_Value":deal_offer_value, 
            "Spread_Pct":deal_spread_percent, "Days_To_Close":days_to_close, 
            "Annualized":deal_annualized_return, "Implied_P":deal_implied_probability,
            "Fallback":deal_fallback_price, "Fallback_Adjusted":adjusted_fallback,
            "Adjusted_Implied_P":adjusted_implied_p, "Index_Change":index_change}

analyze_deal