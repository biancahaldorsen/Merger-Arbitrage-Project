import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
def plot_spread(history_df, title):
    figure, axis = plt.subplots()
    axis.plot(history_df.index, history_df.loc[:, "Spread_Pct"], marker ='o')
    
    #ensures number of date lables is appropriately assinged depending on table size 
    n = len(history_df)
    step = max(1, n // 8)
    positions = list(range(0, n, step))
    last = n - 1   
    if positions[-1] != last:
        if last - positions[-1] < step/2: 
            positions[-1] = last 
        else:
            positions.append(last)
    axis.set_xticks(history_df.index[positions])

    axis.set_title(title)
    axis.set_xlabel("Date")
    axis.set_ylabel("Spread Percentage")
    axis.yaxis.set_major_formatter(PercentFormatter(1.0))
    figure.autofmt_xdate()
    return figure
