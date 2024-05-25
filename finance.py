import yfinance as yf
from datetime import datetime, timedelta
import time
import streamlit as st
import pandas as pd

# Gets most recent price?
def get_recent_price(ticker_symbol):
    # Create a Ticker object for the specified stock
    stock_ticker = yf.Ticker(ticker_symbol)
    
            # Fetch historical data for the last trading day with 1-minute intervals
    minute_data = stock_ticker.history(period='1d', interval='1m')
        
            # Extract the most recent minute's data
    if not minute_data.empty:
        latest_minute_data = minute_data.iloc[-1]
            
            # Print or process the data as needed
        recent_price = latest_minute_data['Close']

        return recent_price
    else:
        return None

        
          # Wait for 1 minute before fetching the next update

def first_open_price(ticker_symbol):
    # Create a Ticker object for the specified stock
    stock_ticker = yf.Ticker(ticker_symbol)

    # Fetch historical intraday data for the current day with 1-minute intervals
    intraday_data = stock_ticker.history(period='1d', interval='1m')

    # Extract the first open price of the day
    first_open_price = intraday_data.loc[intraday_data.index.date == datetime.today().date(), 'Open'].iloc[0]

    return first_open_price


def get_recent_volume(ticker_symbol):
    # Create a Ticker object for the specified stock
    stock_ticker = yf.Ticker(ticker_symbol)
    
        # Fetch historical data for the last trading day with 1-minute intervals
    minute_data = stock_ticker.history(period='1d', interval='1m', prepost = True)
            
        # Extract the most recent minute's data
    total_volume = minute_data['Volume'].sum()
            
    return total_volume

def average_volume_stock(ticker_symbol):
     # Create a Ticker object for the specified stock
    stock_ticker = yf.Ticker(ticker_symbol)

    # Calculate the start and end dates for the last 30 trading days
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')

    # Get historical data for the last 3 trading days
    historical_data = stock_ticker.history(start=start_date, end=end_date)

    # Calculate the average volume for the last 30 days
    average_volume = historical_data['Volume'].mean()

    return average_volume

def check_volume(ticker_symbol):
    average_volume = average_volume_stock(ticker_symbol)
    current_volume = get_recent_volume(ticker_symbol)

    if current_volume >= 5 * average_volume:
        return True
    else:
        return False
    
def quality_stock(ticker_symbol):
    recent_price = float(get_recent_price(ticker_symbol))
    first_open = float(first_open_price(ticker_symbol))
    enough_volume = check_volume(ticker_symbol)

    return (recent_price >= 5 and recent_price <= 20) and (((recent_price - first_open) / first_open) * 100 >= 10) and (enough_volume == True)

def analyze_stocks(stock_list):
    results = {}
    for ticker in stock_list:
        results[ticker] = quality_stock(ticker)
    boolean_values = tuple(results.values())
    return boolean_values


def update_df(stock_list):
    data = []
    for ticker in stock_list:
        recent_price = get_recent_price(ticker)
        recent_volume = get_recent_volume(ticker)
        first_open = first_open_price(ticker)

        percent_increase = ((recent_price - first_open) / first_open) * 100
        meets_conditions = quality_stock(ticker)

        data.append({
            "Stock" : ticker,
            "Price" : recent_price,
            "Volume" : recent_volume,
            "Percent Increase" : percent_increase,
            "Meets Conditions" : meets_conditions
        })

    return pd.DataFrame(data)

stock_list = [
    "AVGR", "BLDP", "CETX", "CRIS","DMRC", "ELTK", "ENSV", "FTEK",
    "IMTE", "INUV", "KOPN", "LEDS", "LPTH", "MARK", "MVIS", "NNDM",
    "NURO", "ONTX", "PLUG", "PT", "PTN", "PXS", "RETO", "SENS", "SHIP",
    "SINT", "SOL", "SPI", "SQQQ","SYPR", "TELL","TENX", "TNXP", "UAVS", 
    "VXRT", "WKHS", "WWR", "ZOM", "ROOT", "DOGZ"
]
df = update_df(stock_list)

st.title('Stock Analysis Table')

if st.button("Update and Display DataFrame"):
    df = update_df(stock_list).sort_values(by=['Meets Conditions', 'Percent Increase'], ascending=False)
    st.dataframe(df)