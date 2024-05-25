import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import yfinance as yf



def ticker_symbol(url):
    stocks =[]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    names = soup.find_all(attrs={'data-test': 'quoteLink'})
    for stock in names:
        stocks.append(stock.text)
    return stocks

def convert_volume(entry):
    if 'M' in entry:
        return float(entry.replace(',', '').rstrip('M')) * 1000000
    else:
        return float(entry.replace(',', ''))

#@st.cache_data
def get_important_data(_soup):
    data = []
    prices = []
    percent_change = []
    current_volume = []
    average_volume = []
    all_data = soup.find_all(attrs={'data-test': 'colorChange'})
    average_volume_data = soup.find_all(attrs={'aria-label': 'Avg Vol (3 month)'})
    for value in average_volume_data:
        average_volume.append(value.text)

    for values in all_data:
        data.append(values.text)
    prices = [float(entry.replace(',', '')) for entry in data[::5]]
    percent_change = [float(entry[:-1]) for entry in data[2::5]]
    current_volume = [convert_volume(entry) for entry in data[3::5]]
    market_size = [entry for entry in data[4::5]]
    new_average_volume = [convert_volume(entry) for entry in average_volume]

    meets_conditions = [
        (current_val >= (5 * avg_val)) and (5 <= price <= 20) and (percent_change >= 10)
        for current_val, avg_val, price, percent_change in zip(current_volume, new_average_volume, prices, percent_change)
    ]

    return prices, percent_change, current_volume, new_average_volume, market_size, meets_conditions

st.title('Stock Analysis Table')
if st.button("Update and Display DataFrame"):
    url = 'https://finance.yahoo.com/gainers?count=100'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    stock_names = ticker_symbol(url)
    prices, percent_change, current_volume, average_volume, market_size, meets_conditions = get_important_data(soup)

    rounded_prices = [round(price, 3) for price in prices]
    rounded_percent_change = [round(percent, 3) for percent in percent_change]
    rounded_current_volume = [round(volume, 3) for volume in current_volume]

    df = pd.DataFrame({
        'Stock Name': stock_names,
        'Prices ($)': rounded_prices,
        'Percent Change (%)': rounded_percent_change,
        'Current Volume': rounded_current_volume,
        'Market Size': market_size,
        'Meets Conditions': meets_conditions
    })

    sorted_df = df.sort_values(by='Meets Conditions', ascending=False)

    st.dataframe(sorted_df)
