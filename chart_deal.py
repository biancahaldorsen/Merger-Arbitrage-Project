import pandas as pd
from arbitrage.history import calculate_spread_history
from arbitrage.charts import plot_spread
import matplotlib.pyplot as plt

deals_table = pd.read_csv("deals.csv", parse_dates=["Announce_Date", "Unaffected_Date", "Expected_Close"])
#ensures that the correct ticker is called by creating a single table that only contains the selected ticker's ticker name
ticker = "CBNK"
matches = deals_table[deals_table["Target_Ticker"] == ticker]
if matches.empty:
    print(f"{ticker} is not in table deals.csv")
else:
    row = matches.iloc[0]

    spread_history = calculate_spread_history(row)
    print (spread_history)

    figure = plot_spread(spread_history, f"{ticker} Arb Spread")
    figure.savefig("output/test_chart.png")
    plt.show()