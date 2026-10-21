import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

#builds an interactive plotly chart

def plot_spread_interactive (history_df, title):
    figure = make_subplots(specs = [[{"secondary_y":True}]]) # []list of rows in grid then [] list of charts in a row {}settings for one chart
    figure.update_yaxes(tickformat = ".2%", secondary_y = False, title_text = "Spread")
    figure.update_yaxes(secondary_y= True, title_text = "Implied Probability", tickformat = ".1%")

    range_buttons = [dict(count = 7, label = "1w", step = "day", stepmode = "backward" ),
                     dict(count = 1, label = "1mon", step = "month", stepmode = "backward"),
                     dict(step = "all", label = "All")] #we count backward from most recent date in order to show the most recent week 

    figure.update_xaxes(rangebreaks = [dict(bounds=["sat", "mon"])], rangeselector = dict(buttons = range_buttons))
    figure.update_layout(title = title, xaxis_title="Date")

#adds information when mouse hovers over graph points 
    hover_columns = ["Target_Price", "Offer_Value", "Implied_P"]
    hover_template= "%{x|%b %d, %Y}<br>Spread: %{y:.2%}<br>Target price: %{customdata[0]:$.2f}" \
    "<br>Offer value: %{customdata[1]:$.2f}<br>Implied p: %{customdata[2]:.1%} "
    
    if "Acquirer_Price" in history_df.columns:
        hover_columns.append("Acquirer_Price")
        hover_template = hover_template + "<br>Acquirer price: %{customdata[3]:$.2f}"
    hover_template = hover_template + "<extra></extra>"
    
    figure.add_trace(go.Scatter(x=history_df.index, y=history_df.loc[:, "Spread_Pct"], mode="lines+markers", 
                                name = "Spread", customdata= history_df[hover_columns], hovertemplate=hover_template), secondary_y= False)
    
    if history_df["Implied_P"].notna().any():
        hover_template2 = "%{x|%b %d, %Y}<br>Implied p: %{y:.1%}<extra></extra>" 
        figure.add_trace(go.Scatter(x=history_df.index, y=history_df.loc[:, "Implied_P"], mode="lines+markers", 
                                name = "Implied Probability", hovertemplate=hover_template2), secondary_y= True)
    
    if "Adjusted_Implied_P" in history_df.columns and history_df["Adjusted_Implied_P"].notna().any():
        hover_template3 = "%{x|%b %d, %Y}<br>Adjusted Implied p: %{y:.1%}<extra></extra>" 
        figure.add_trace(go.Scatter(x=history_df.index, y=history_df.loc[:, "Adjusted_Implied_P"], mode="lines+markers", 
                                name = "Adjusted Implied Probability", hovertemplate=hover_template3, line= dict(dash = "dash"), visible="legendonly"), secondary_y= True)
    return figure 
