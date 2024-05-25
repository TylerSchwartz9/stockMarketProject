import yfinance as yf
from datetime import datetime, timedelta
import concurrent.futures
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup




def get_recent_price(ticker_symbol):
    stock_ticker = yf.Ticker(ticker_symbol)
    minute_data = stock_ticker.history(period='1d', interval='1m')
    if not minute_data.empty:
        latest_minute_data = minute_data.iloc[-1]
        recent_price = latest_minute_data['Close']
        return recent_price
    else:
        return None

def first_open_price(ticker_symbol):
    stock_ticker = yf.Ticker(ticker_symbol)
    intraday_data = stock_ticker.history(period='1d', interval='1m')
    
    today_date = datetime.today().date()
    filtered_data = intraday_data.loc[intraday_data.index.date == today_date, 'Open']
    
    return filtered_data.iloc[0]
    
    
# def get_last_close(ticker_symbol):
#     now = datetime.today().strftime('%Y-%m-%d')

#     # Fetch historical data for the past 2 days (including today)
#     data = yf.download(ticker_symbol, end=now, period='2d')

#     # Extract the closing price of the day before
#     closing_price_day_before = data['Close'].iloc[-2]

#     return closing_price_day_before


def get_recent_volume(ticker_symbol):
    stock_ticker = yf.Ticker(ticker_symbol)
    minute_data = stock_ticker.history(period='1d', interval='1m', prepost=True)
    total_volume = minute_data['Volume'].sum()
    return total_volume

def average_volume_stock(ticker_symbol):
    stock_ticker = yf.Ticker(ticker_symbol)
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')
    historical_data = stock_ticker.history(start=start_date, end=end_date)
    average_volume = historical_data['Volume'].mean()
    return average_volume

def check_volume(ticker_symbol):
    average_volume = average_volume_stock(ticker_symbol)
    current_volume = get_recent_volume(ticker_symbol)
    return current_volume >= 5 * average_volume

def quality_stock(ticker_symbol):
    recent_price = float(get_recent_price(ticker_symbol))
    first_open = float(first_open_price(ticker_symbol))
    enough_volume = check_volume(ticker_symbol)
    return (recent_price >= 5 and recent_price <= 20) and (((recent_price - first_open) / first_open) * 100 >= 10) and (enough_volume == True)

def fetch_stock_data(ticker):
    recent_price = get_recent_price(ticker)
    recent_volume = get_recent_volume(ticker)
    first_open = first_open_price(ticker)
    percent_increase = ((recent_price - first_open) / first_open) * 100 if first_open is not None else None
    meets_conditions = quality_stock(ticker) if all([recent_price is not None, first_open is not None, recent_volume is not None]) else None

    return {
        "Stock": ticker,
        "Price": recent_price,
        "Volume": recent_volume,
        "Percent Increase": percent_increase,
        "Meets Conditions": meets_conditions
    }

def update_df_parallel(stock_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor:
        results = list(executor.map(fetch_stock_data, stock_list))

    return pd.DataFrame(results)

# webscraping code
stock_list1 = []
stock_list2 = []

url1 = 'https://finance.yahoo.com/gainers'
#url2 = 'https://finance.yahoo.com/gainers?offset=25&count=25'
response1 = requests.get(url1)
#response2 = requests.get(url2)

soup1 = BeautifulSoup(response1.text, 'html.parser')
#soup2 = BeautifulSoup(response2.text, 'html.parser')

stock_name1 = [name.text for name in soup1.find_all(attrs={'data-test': 'quoteLink'})]
#stock_name2 = [name.text for name in soup2.find_all(attrs={'data-test': 'quoteLink'})]

#extended_list = stock_name1 + stock_name2



######################################################################################################





df = update_df_parallel(stock_name1) 

st.title('Stock Analysis Table')

if st.button("Update and Display DataFrame"):
    df_sorted = update_df_parallel(stock_name1).sort_values(by=['Meets Conditions', 'Percent Increase'], ascending=False)
    st.dataframe(df_sorted)





