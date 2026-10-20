import streamlit as st
import pandas as pd
from arbitrage.analysis import analyze_deal
from arbitrage.history import calculate_spread_history
from arbitrage.charts import plot_spread
st.title("Merger Spread Information")
st.write("This application allows you to input basic information regarding an on-going merger deal and displays the relevant spread information.")

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
       st.stop
    if pd_announcement_date >=  pd.Timestamp.today().normalize():
        st.error("Your announcement date must take place in the past.")
        st.stop()
    if pd_expected_close <= pd.Timestamp.today().normalize(): 
        st.warning("Your expected close date should take place after today.")
    if exchange_ratio > 0 and acquirer_ticker_cleaned is None:
        st.error("You are recording a stock deal without an acquirer ticker listed.")
        st.stop()

    #displays the results of the user's inputs 
    deal_analysis = analyze_deal(deal_row)

    if deal_analysis is None:
        st.error("The analysis could not be completed. Most likely a mispelled ticker or a closed deal.")
        st.stop()

    else:
        col1, col2, col3 = st.columns(3)
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

        col4, col5, col6 = st.columns(3)
        days_to_close = f"{deal_analysis['Days_To_Close']} days" 
        current_price = f"${deal_analysis['Price']:.2f}" 
        offer_value = f"${deal_analysis['Offer_Value']:.2f}" 
        col4.metric("Days to Close",days_to_close)
        col5.metric("Current Price", current_price)
        col6.metric("Offer Value", offer_value)

        spread_history = calculate_spread_history(deal_row)
        if spread_history is None:
            st.warning("The spread history chart is unavailable for this deal.")
        else: 
            spread_plot = plot_spread(spread_history, f"{target_ticker_cleaned} Merger Spread")
            st.pyplot(spread_plot)