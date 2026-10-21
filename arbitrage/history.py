from arbitrage.data import get_price_history, get_price_on
import pandas as pd
from arbitrage.metrics import calculate_offer_value, calculate_spread, calculate_adjusted_fallback

#creates a new table of a deal spread history w target price, acquirer price, offer value,.. 
#..spread pct, implied p given a row from a table of basic deal information 
def calculate_spread_history(row, index_ticker = None): 
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

#calculate daily adjusted fallback column and  a daily adjusted implied probability column.
   if index_ticker is not None and fallback_price is not None: 
       index_price_history = get_price_history(index_ticker,announce_date )
       index_price_unaffected_date = get_price_on(index_ticker,unaffected_date)

       if index_price_history is not None and index_price_unaffected_date is not None:
           price_history_df_cleaned["Index_Price_History"] = index_price_history
           price_history_df_cleaned["Adjusted_Fallback_Price"] = calculate_adjusted_fallback(fallback_price, index_price_unaffected_date,
                                                                                             price_history_df_cleaned["Index_Price_History"])
           price_history_df_cleaned["Adjusted_Implied_P"] = (price_history_df_cleaned["Target_Price"] - price_history_df_cleaned["Adjusted_Fallback_Price"])/(price_history_df_cleaned["Offer_Value"] - price_history_df_cleaned["Adjusted_Fallback_Price"])
       else:
           print (f"Unable to fetch {index_ticker} price information.")
   return price_history_df_cleaned


      
