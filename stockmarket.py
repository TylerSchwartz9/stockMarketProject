import pandas as pd
import yfinance as yf
import requests
from datetime import datetime
import time
import streamlit as st
import asyncio
import aiohttp
import concurrent.futures

api_key = '39046e3ba5fd49fca9f2a6a4f4defa40'

# get a stocks current trading volume

# def get_stock_volume(ticker_symbol, api):
#     url = f"https://api.twelvedata.com/time_series?symbol={ticker_symbol}&interval=1min&apikey={api}"
#     response = requests.get(url).json()

#     # Check if the response contains the 'values' key
#     if 'values' in response:
#         data = response['values']

#         # Assuming 'datetime' is the key for the date times and 'volume' is the key for the volume in the response
#         date_volume_list = [(datetime.fromisoformat(candle['datetime']), float(candle['volume'])) for candle in data]

#         # Sort the list by most recent time
#         sorted_data = sorted(date_volume_list, key=lambda x: x[0], reverse=True)

#         # Return the volume corresponding to the most recent time
#         if sorted_data:
#             most_recent_time, most_recent_volume = sorted_data[0]
#             return most_recent_volume
#         else:
#             return None
#     else:
#         return None

# # need to find the average volume of a stock over a certain period of time

# def average_trading_volume(ticker_symbol, duration_days):
#     stock_data = yf.download(ticker_symbol, period = f"{duration_days}d", progress = False)
#     average_volume = round(float(stock_data['Volume'].mean()), 3)
#     return average_volume

 
# #determine if current trading volume if 5x average trading volume over the last 30 days
# def check_volume(ticker, api_key):
#     recent_volume = float(get_stock_volume(ticker, api_key))
#     average_volume = float(average_trading_volume(ticker, 30))

#     if (recent_volume >= (5 * average_volume)):
#         return True
#     else:
#         return False
    
 # gets a stocks most updated price

def get_stock_price(ticker_symbol, api):
    url = f"https://api.twelvedata.com/price?symbol={ticker_symbol}&apikey={api}"
    response = requests.get(url).json()
    price = response['price']
    return price

 

# finds the first open price

def first_open_price(ticker_symbol, api):
    url = f"https://api.twelvedata.com/time_series?symbol={ticker_symbol}&interval=1day&apikey={api}"
    response = requests.get(url).json()
    # Check if the response contains the 'values' key
    if 'values' in response:
        data = response['values']

        # Assuming 'datetime' is the key for the date times and 'open' is the key for the opening prices in the response
        datetime_open_list = [(datetime.fromisoformat(candle['datetime']), float(candle['open'])) for candle in data]

        # Sort the list by datetime in descending order
        sorted_data = sorted(datetime_open_list, key=lambda x: x[0], reverse=True)

        # Return the opening price corresponding to the most recent day
        if sorted_data:
            most_recent_datetime, most_recent_open_price = sorted_data[0]
            return most_recent_open_price
        else:
            return None
    else:
        return None
    

 
def calculating_percent_change(ticker, api):
    opening_price = float(first_open_price(ticker, api))
    current_price = float(get_stock_price(ticker, api))
    percent_change = ((current_price - opening_price) / opening_price) * 100
    return percent_change

print(calculating_percent_change('RXRX', api_key))
      
# # Trying to put it all together

# def stock_quality_checker(ticker, api_key):
#     max_iterations = 1
#     iterations = 0
#     while iterations < max_iterations:
        
#         # calling check_volume function // returns boolean after checking if current volume is 5x the 30 day average volume
#         enough_volume = check_volume(ticker, api_key)
#         # calling the calculating_percent_change function // returns the percent change from stock opening to current price
#         percent_change = calculating_percent_change(ticker, api_key)
#         # calling the current_price function // returns stock's current price
#         current_price = get_stock_price(ticker, api_key)
#         if enough_volume and percent_change >= 10 and 1 <= current_price <= 20:
#             return True  # If conditions are met, return True immediately

#         iterations += 1  

#     return False  
        

# # Function to update DataFrame for a list of stocks
# def update_dataframe_for_stocks(df, stocks, api_key):
#     for stock in stocks:
#         # Function to fetch stock volume
#         def get_stock_volume_async(ticker, api_key):
#             return float(get_stock_volume(ticker, api_key))

#         # Function to fetch percent change
#         def calculating_percent_change_async(ticker, api_key):
#             return float(calculating_percent_change(ticker, api_key))

#         # Function to fetch current price
#         def get_stock_price_async(ticker, api_key):
#             return float(get_stock_price(ticker, api_key))

#         # Function to check stock quality
#         def stock_quality_checker_async(ticker, api_key):
#             return stock_quality_checker(ticker, api_key)

#         # Create a ThreadPoolExecutor with 4 threads (adjust as needed)
#         with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
#             # Submit tasks for fetching each variable asynchronously
#             volume_future = executor.submit(get_stock_volume_async, stock, api_key)
#             percent_change_future = executor.submit(calculating_percent_change_async, stock, api_key)
#             price_future = executor.submit(get_stock_price_async, stock, api_key)
#             quality_checker_future = executor.submit(stock_quality_checker_async, stock, api_key)

#             # Wait for all futures to complete
#             concurrent.futures.wait([volume_future, percent_change_future, price_future, quality_checker_future])

#             # Retrieve the results
#             current_volume = volume_future.result()
#             percent_change = percent_change_future.result()
#             current_price = price_future.result()
#             meets_conditions = str(quality_checker_future.result())

#         # Append a new row to the DataFrame with the calculated values
#         df.loc[len(df)] = [stock, current_price, current_volume, percent_change, meets_conditions]

#     return df

# # List of stocks
# stock_list = ['MSFT', 'AAPL', 'HLIT', 'KRP','EVRI', 'ROOT','CVOSF']  # Add more stocks as needed

# df = pd.DataFrame(columns=["Stock", "Price", "Volume", "Percent Increase", "Meets Conditions"])

# def display_dataframe(df):
#     st.dataframe(df)

# st.title("Stock Data Tracker")

# if st.button("Update and Display DataFrame"):
#     df = update_dataframe_for_stocks(df, stock_list, api_key).sort_values(by = 'Meets Conditions', ascending = False)
#     display_dataframe(df)