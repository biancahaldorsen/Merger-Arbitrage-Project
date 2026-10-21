import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import plotly.graph_objects as go

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
    figure = go.Figure()
    figure.update_yaxes(tickformat = ".2%")
    figure.update_xaxes(rangebreaks = [dict(bounds=["sat", "mon"])])
    figure.update_layout(title = title, xaxis_title="Date", yaxis_title="Spread Percentage")

#adds information when mous hovers over graph points 
    hover_columns = ["Target_Price", "Offer_Value", "Implied_P"]
    hover_template= "%{x|%b %d, %Y}<br>Spread: %{y:.2%}<br>Target price: %{customdata[0]:$.2f}" \
    "<br>Offer value: %{customdata[1]:$.2f}<br>Implied p: %{customdata[2]:.1%} "
    
    if "Acquirer_Price" in history_df.columns:
        hover_columns.append("Acquirer_Price")
        hover_template = hover_template + "<br>Acquirer price: %{customdata[3]:$.2f}"
    hover_template = hover_template + "<extra></extra>"
    
    figure.add_trace(go.Scatter(x=history_df.index, y=history_df.loc[:, "Spread_Pct"], mode="lines+markers", 
                                name = "Spread", customdata= history_df[hover_columns], hovertemplate=hover_template))
    
    return figure 
