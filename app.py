import streamlit as st
import pandas as pd
from arbitrage.analysis import analyze_deal
from arbitrage.history import calculate_spread_history
from arbitrage.charts import plot_spread
st.title("Merger Spread Information")
st.write("This application allows you to input basic information regarding an on-going merger deal and displays the relevant spread information.")

with st.expander ("See website information"):
    st.write("This merger arbitrage spread tool uses python and information drawn from Yahoo Finance via Ran Aroussi's yfinance" \
    " to allow the user to input the basic deal information regarding an upcoming merger and observe the spread chart, the deal's " \
    "offer value, the annualized return, and the implied probability of the deal taking place.")
    st.write("Please note that the implied probability is derived from the current trading price of the target " \
             "company relative to both the deal's offer price and a fallback price pulled from the entered "\
             "unaffected date. This means there is an assumption that the target company stock would simply return "\
             "to its old valuation pre-deal announcement if the deal were to fail.")
    st.write("The user can receive an adjusted implied probability and adjusted fallback price by inputting " \
    "the target's sector as a benchmark to scale the target's unaffected price by how much " \
              " its sector has moved since the unaffected date.")
    st.caption("WARNING: This tool is not investment advice and should be used at the user's discretion.")

with st.form ("deal_form"): 
    st.write("Enter deal details below.")
    acquirer_ticker = st.text_input ("Enter Acquirer Ticker (optional, stock deals only)")
    target_ticker = st.text_input ("Enter Target Ticker")
    cash_per_share = st.number_input(label = "Enter Cash Per Share",value = 0.00, min_value= 0.00, placeholder= "Type a number...",
                                     step = 0.01, format = "%0.2f")
    exchange_ratio = st.number_input(label = "Enter Exchange Ratio", value = 0.00, min_value = 0.00, placeholder = "Type a number...",
                                     step = 0.0001, format = "%0.4f")
    announcement_date = st.date_input(label ="Enter Announcement Date", value = None) 
    unaffected_date = st.date_input(label ="Enter Unaffected Date", value = None) 
    expected_close =  st.date_input(label ="Enter Expected Close Date", value = None) 

    converted_benchmark = {"General market (SPY)": "SPY", "Communication services (XLC)": "XLC", 
                           "Consumer discretionary (XLY)":"XLY", "Consumer staples (XLP)":"XLP",
                            "Energy (XLE)": "XLE", "Financials (XLF)":"XLF",
                            "Regional banks (KRE)":"KRE", "Health care (XLV)": "XLV","Industrials (XLI)":"XLI",
                              "Materials (XLB)":"XLB", "Real estate (XLRE)" : "XLRE","Technology (XLK)":"XLK",
                               "Utilities (XLU)": "XLU", "None, simple fallback only" : None } 
    chosen_benchmark = st.selectbox(label = "Choose a benchmark for the target company's fallback price:", 
                                    options = list(converted_benchmark.keys()), 
                                    help = "To find a target's sector, check its profile on Yahoo Finance or look in its 10-K.")

    #note that now converted_benchmark[chosen_benchmark]is the chosen ticker
    benchmark_ticker = converted_benchmark[chosen_benchmark]

    submitted = st.form_submit_button("Submit Deal")


if submitted: 
    acquirer_ticker_cleaned = acquirer_ticker.strip().upper()
    target_ticker_cleaned = target_ticker.strip().upper()

    if not acquirer_ticker_cleaned: 
        acquirer_ticker_cleaned = None

    if announcement_date is None or unaffected_date is None or expected_close is None: 
        st.error("You are missing either your announcement date, your unaffected date, or your expected close date.")
        st.stop()
    
    pd_announcement_date = pd.Timestamp(announcement_date)
    pd_unaffected_date = pd.Timestamp(unaffected_date)
    pd_expected_close = pd.Timestamp(expected_close)

    #creates a deal dictionary with user's given inputs and changes to row format so later functions can be called 
    current_deal_dictionary = {"Target_Ticker" : target_ticker_cleaned, "Acquirer_Ticker" : acquirer_ticker_cleaned, 
                               "Cash_Per_Share": cash_per_share, "Exchange_Ratio": exchange_ratio,
                               "Announce_Date": pd_announcement_date, "Unaffected_Date": pd_unaffected_date,
                               "Expected_Close": pd_expected_close}
    deal_row = pd.Series(current_deal_dictionary)

    if not target_ticker_cleaned: 
        st.error("The target ticker has not been input. Please ensure that you have not placed " \
        "your target ticker in the acquirer ticker block.")
        st.stop()
    if cash_per_share == 0 and exchange_ratio == 0: 
        st.error("Your deal lacks consideration. Please input either the cash per share or the exchange ratio.")
        st.stop()
    if pd_announcement_date <= pd_unaffected_date: 
        st.error("Your unaffected date is listed as taking place after your announcement date. The unaffected date " \
        "must be a date before the deal has been announced.")
        st.stop()
    if pd_unaffected_date >= pd.Timestamp.today().normalize():
       st.error("Your unaffected date must take place in the past.")
       st.stop()
    if pd_announcement_date >=  pd.Timestamp.today().normalize():
        st.error("Your announcement date must take place in the past.")
        st.stop()
    if pd_expected_close <= pd.Timestamp.today().normalize(): 
        st.warning("Your expected close date should take place after today.")
    if exchange_ratio > 0 and acquirer_ticker_cleaned is None:
        st.error("You are recording a stock deal without an acquirer ticker listed.")
        st.stop()

    #displays the results of the user's inputs 
    deal_analysis = analyze_deal(deal_row, index_ticker=benchmark_ticker)

    if deal_analysis is None:
        st.error("The analysis could not be completed. Most likely a misspelled ticker or a closed deal.")
        st.stop()

    else:
        col1, col2, col3 = st.columns(3) #1st row of columns 
        spread_percent = f"{deal_analysis['Spread_Pct']:.2%}"
        col1.metric("Spread %", spread_percent)

        if deal_analysis["Annualized"] is None:
            col2.metric ("Annualized Return", "N/A")
        else: 
            annualized_return = f"{deal_analysis['Annualized']:.2%}"
            col2.metric("Annualized Return", annualized_return)
        if deal_analysis["Implied_P"] is None:
            col3.metric ("Implied P", "N/A")
        else:
            implied_p = f"{deal_analysis['Implied_P']:.1%}"
            col3.metric("Implied P",implied_p)

        col4, col5, col6 = st.columns(3) #2nd row of columns 
        days_to_close = f"{deal_analysis['Days_To_Close']} days" 
        current_price = f"${deal_analysis['Price']:.2f}" 
        offer_value = f"${deal_analysis['Offer_Value']:.2f}" 
        col4.metric("Days to Close",days_to_close)
        col5.metric("Current Price", current_price)
        col6.metric("Offer Value", offer_value)

        if benchmark_ticker is not None: 
            col7, col8, col9 = st.columns(3) #3rd row of columns

            # Column 7(Fallback Price error checks)
            if deal_analysis["Fallback"] is None:
                col7.metric("Fallback Price", "N/A")
            else:
                fallback_price = f"${deal_analysis['Fallback']:.2f}"
                col7.metric("Fallback Price",fallback_price )

            # Column 8 (Adjusted Fallback Price error checks)
            if deal_analysis["Fallback_Adjusted"] is None: 
                col8.metric("Adjusted Fallback Price", "N/A")
            else:
                adjusted_fallback_price = f"${deal_analysis['Fallback_Adjusted']:.2f}"
                index_change_text= f"{deal_analysis['Index_Change']:+.1%} ({benchmark_ticker})"
                col8.metric("Adjusted Fallback Price",adjusted_fallback_price, delta = index_change_text)
            
            # Column 9 (Adjusted Implied P's error checks)
            if deal_analysis["Adjusted_Implied_P"] is None:
                col9.metric("Adjusted Implied P", "N/A")
            else:
                adjusted_implied_p = f"{deal_analysis['Adjusted_Implied_P']:.1%}"
                if deal_analysis["Implied_P"] is not None: 
                    probability_change = (deal_analysis['Adjusted_Implied_P'] - deal_analysis['Implied_P'])*100
                    col9.metric("Adjusted Implied P",adjusted_implied_p, delta = f"{probability_change:+.1f} pts")
                else:
                    col9.metric("Adjusted Implied P",adjusted_implied_p) 

            #Caption
            if deal_analysis['Index_Change'] is not None: 
                index_change = deal_analysis["Index_Change"]
                if index_change > 0: 
                    st.caption(f"{benchmark_ticker} is up {abs(index_change):.1%} since the unaffected date.")
                elif index_change < 0: 
                    st.caption(f"{benchmark_ticker} is down {abs(index_change):.1%} since the unaffected date.")
                elif index_change == 0: 
                    st.caption(f"{benchmark_ticker} is unchanged since the unaffected date.")
            else: 
                st.caption(f"{benchmark_ticker} data unavailable.")



        spread_history = calculate_spread_history(deal_row)
        if spread_history is None:
            st.warning("The spread history chart is unavailable for this deal.")
        else: 
            spread_plot = plot_spread(spread_history, f"{target_ticker_cleaned} Merger Spread")
            st.pyplot(spread_plot)

#Test: run the app and enter CBNK's deal (target CBNK, acquirer PEBO, ratio 1.1100, cash 0, 
# announced 2026-09-30, unaffected 2026-09-29, close 2027-03-31), choose "Regional banks (KRE)",
#  and submit. The third row should show roughly $35.65 | $36.05 with "+1.1% (KRE)" | 78.7% with "−1.4 pts" 
# (it shifts a little as prices update daily). Then commit.

