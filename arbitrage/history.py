from arbitrage.data import get_price_history, get_price_on
import pandas as pd
from arbitrage.metrics import calculate_offer_value, calculate_spread
def calculate_spread_history(row): 
   target_ticker = row["Target_Ticker"]
   acquirer_ticker = row["Acquirer_Ticker"]
   cash_per_share = row["Cash_Per_Share"]
   exchange_ratio = row["Exchange_Ratio"] 
   unaffected_date = row["Unaffected_Date"]
   announce_date = row["Announce_Date"]
   expected_close = row["Expected_Close"]
   target_ticker_history = get_price_history(target_ticker, announce_date)
   if target_ticker_history is None:
      print(f"Unable to fetch price history for {target_ticker}")
      return None
   #Cash Deals 
   if pd.isna(exchange_ratio) or exchange_ratio == 0: 
      price_history_df_cleaned = pd.DataFrame({"Target_Price":target_ticker_history})
      price_history_df_cleaned["Offer_Value"] = cash_per_share #bc the cash offered per share will the same across the deal timeline
    #Stock Deals 
   else:  
        acquirer_ticker_history = get_price_history(acquirer_ticker, announce_date)
        if acquirer_ticker_history is None:
            print (f"Unable to fetch price history for {acquirer_ticker}")
            return None
        price_history_df = pd.DataFrame({"Target_Price":target_ticker_history, "Acquirer_Price":acquirer_ticker_history})
        price_history_df_cleaned = price_history_df.dropna()
        price_history_df_cleaned["Offer_Value"] = calculate_offer_value(cash_per_share, exchange_ratio, price_history_df_cleaned["Acquirer_Price"])
   #For both Cash and Stock Deals 
   price_history_df_cleaned["Spread_Pct"] = calculate_spread(price_history_df_cleaned["Offer_Value"],price_history_df_cleaned["Target_Price"])[1]
   fallback_price = get_price_on(target_ticker,unaffected_date)
   if fallback_price is None: 
       price_history_df_cleaned["Implied_P"] = None
   else: 
       price_history_df_cleaned["Implied_P"] = (price_history_df_cleaned["Target_Price"] - fallback_price)/(price_history_df_cleaned["Offer_Value"] - fallback_price)
       return price_history_df_cleaned
   
   


      
