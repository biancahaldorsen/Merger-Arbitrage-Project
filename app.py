import streamlit as st
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


    #GIT COMMIT 
    #Suggested messages: "Add Streamlit app skeleton", "Move analyze_deal into package", 
    # "Add deal input form", "Build deal row from inputs", "Show metrics and chart", 
    # "Add input validation", "Cache price downloads", "Add how-to-read note".