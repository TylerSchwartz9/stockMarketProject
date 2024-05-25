from playwright.async_api import async_playwright
import pandas as pd
import time
import streamlit as st
import asyncio

async def scrape(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        elements = await page.query_selector_all('xpath=//td[@aria-label="Name"]/parent::*')
        data = []
        for el in elements:
            children = await el.query_selector_all('*')
            entry = {}
            for child in children:
                if await child.is_visible() and await child.get_attribute('aria-label'):
                    key = await child.get_attribute('aria-label')
                    try:
                        value = await child.inner_text()
                    except Exception as e:
                        value = ""  # Set default value as empty string if there's an error or no text
                    entry[key] = value
            if entry:
                data.append(entry)
        await browser.close()
    return data


# Iterate through each entry and extract relevant data
def extract_important_data(elements):
    stocks = []
    for entry in elements:
        stock_data = {
            'Symbol': entry['Symbol'],
            'Name': entry['Name'],
            'Price (Intraday)': entry['Price (Intraday)'],
            'Change': entry['Change'],
            '% Change': entry['% Change'],
            'Volume': entry['Volume'],
            'avg 3 month volume': entry['Avg Vol (3 month)']
        }
        stocks.append(stock_data)
    return stocks

async def main():
    start_time = time.time()
    elements = await scrape("https://finance.yahoo.com/gainers/?count=100")
    important_data = extract_important_data(elements)
    
    # what I need to do
    # Drop the m and b, and convert to numbers
    # See if it meets list of conditions
    # Create the refresh and display button
    # See if it can be quicker
    
    df = pd.DataFrame(important_data)
  
    
    
    #end_time = time.time()

    #print(f"Scraping and DataFrame creation took {end_time - start_time:.2f} seconds.")

    st.dataframe(df)

if __name__=='__main__':
    loop = asyncio.ProactorEventLoop()
    loop.run_until_complete(main())
