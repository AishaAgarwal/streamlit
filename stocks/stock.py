import yfinance as yf 
import streamlit as st
import pandas as pd 
import datetime 

st.write("""
         # Simple Stock Price App
         
         Shown are the stock closing price and volume of Google!
         """)

form = st.form('my_form')

option = form.selectbox(
             'Select the company you want to display stock data',
             ('Google', 'Apple', 'Microsoft', 'Meta', 'Tesla', 'Amazone'))

col1, col2 = form.columns(2)

start = col1.date_input(
    """Select the start date (format is yyyy-MM-dd)""",
    datetime.date(2010, 1, 1))
end = col2.date_input(
    """Select the end date (format is yyyy-MM-dd)""")



def display(option,  start_date, end_date):
    """
        Displays stock data for the selected company, frequency of data, 
        and time period.
        
        Parameters:
        option (str): The name of the company.
        period (str): The frequency of data to display.
        start (datetime): The start date of the time period.
        end (datetime): The end date of the time period.
        
        Returns:
        None
    """

    companies = {
        'Google':'GOOGL',
        'Apple':'AAPL',
        'Microsoft':'MSFT',
        'Meta':'Meta',
        'Tesla':'TSLA',
        'Amazone': 'AMZN'}

    tickerSymbol = companies[option]

    tickerData = yf.Ticker(tickerSymbol)

# Create a form to input the date range


# Button to fetch data
   
        # getting historical data  
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

    st.write("""
    Shown is the stock **closing price** of
    """+option+""" from """,start,""" to """,end)

    st.line_chart(tickerDf.Close)
   
    st.write("""
    Shown is the stock **volume** of
    """+option+""" from """,start,""" to """,end)
        
        # Display the data
    
    st.line_chart(tickerDf.Volume)

if form.form_submit_button("Fetch Data"):
    display(option, start, end)

