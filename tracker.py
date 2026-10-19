import pandas as pd
import yfinance as yf
from datetime import timedelta
from arbitrage.metrics import calculate_spread, calculate_offer_value, calculate_annualized_return, calculate_implied_p
from arbitrage.data import get_latest_price, get_price_on
from arbitrage.analysis import analyze_deal
##########################################################################################
#loading data from deals.csv 
deals_table = pd.read_csv("deals.csv", parse_dates=["Announce_Date", "Unaffected_Date", "Expected_Close"])

deal_information_list = []
for i, row in deals_table.iterrows(): #returns the position number of the row, and the data for that row
    deal_information = analyze_deal(row)
    if deal_information is not None:
        deal_information_list.append(deal_information)

deal_information_df = pd.DataFrame(deal_information_list)
deal_information_df_sorted = deal_information_df.sort_values(by = "Annualized", ascending = False)

deal_information_df_sorted.to_csv("output/spreads.csv", index=False)

###############################################################################################
