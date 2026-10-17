import pandas as pd
##########################################################################################
#loading data drom deals.csv 
deals_table = pd.read_csv("deals.csv", parse_dates=["Announce_Date", "Unaffected_Date", "Expected_Close"])
print (deals_table)
print (deals_table.dtypes)

