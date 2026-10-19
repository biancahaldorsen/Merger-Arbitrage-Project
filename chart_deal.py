import pandas as pd
from arbitrage.history import calculate_spread_history

deals_table = pd.read_csv("deals.csv", parse_dates=["Announce_Date", "Unaffected_Date", "Expected_Close"])
print(calculate_spread_history(deals_table.iloc[0]))