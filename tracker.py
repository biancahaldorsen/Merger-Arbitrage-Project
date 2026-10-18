import pandas as pd
import yfinance as yf
from datetime import timedelta
from arbitrage.metrics import calculate_spread, calculate_offer_value, calculate_annualized_return, calculate_implied_p
from arbitrage.data import get_latest_price, get_price_on
##########################################################################################
#loading data from deals.csv 
deals_table = pd.read_csv("deals.csv", parse_dates=["Announce_Date", "Unaffected_Date", "Expected_Close"])

#takes a given row from deals.csv and returns a dictionary of target, acquirer, price, offer value, spread percentage
#days to close, annualized return, and implied probability 
def analyze_deal(row): 
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
    return {"Target":target_ticker, "Acquirer":acquirer_ticker, 
            "Price":target_price, "Offer_Value":deal_offer_value, 
            "Spread_Pct":deal_spread_percent, "Days_To_Close":days_to_close, 
            "Annualized":deal_annualized_return, "Implied_P":deal_implied_probability}

deal_information_list = []
for i, row in deals_table.iterrows(): #returns the position number of the row, and the data for that row
    deal_information = analyze_deal(row)
    if deal_information is not None:
        deal_information_list.append(deal_information)

deal_information_df = pd.DataFrame(deal_information_list)
deal_information_df_sorted = deal_information_df.sort_values(by = "Annualized", ascending = False)

deal_information_df_sorted.to_csv("output/spreads.csv", index=False)

###############################################################################################
