import streamlit as st
import pandas as pd
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
    
    pd_announcement_date = pd.Timestamp(announcement_date)
    pd_unaffected_date = pd.Timestamp(unaffected_date)
    pd_expected_close = pd.Timestamp(expected_close)

    current_deal_dictionary = {"Target_Ticker" : target_ticker_cleaned, "Acquirer_Ticker" : acquirer_ticker_cleaned, 
                               "Cash_Per_Share": cash_per_share, "Exchange_Ratio": exchange_ratio,
                               "Announce_Date": pd_announcement_date, "Unaffected_Date": pd_unaffected_date,
                               "Expected_Close": pd_expected_close}
    deal_row = pd.Series(current_deal_dictionary)



    #GIT COMMIT 
    #Suggested messages: "Add Streamlit app skeleton", "Move analyze_deal into package", 
    # "Add deal input form", "Build deal row from inputs", "Show metrics and chart", 
    # "Add input validation", "Cache price downloads", "Add how-to-read note".