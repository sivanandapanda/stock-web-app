import streamlit as st
import pandas as pd
from PIL import Image
import requests
import os

st.write("""
# Stock Market Web Application
**Visually** show data on a stock!
""")

st.sidebar.header('User Input')

apiKey = os.getenv('ALPHA_VANTAGE_API_KEY')

def get_input():
    start_date = st.sidebar.text_input("Start Date", "2021-02-12")
    end_date = st.sidebar.text_input("End Date", "2021-07-09")
    stock_symbol = st.sidebar.text_input("Stock Symbol", "RELIANCE.BSE")
    return start_date, end_date, stock_symbol

def get_company_name(symbol):
    return symbol

def download_data(symbol):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+symbol+'&apikey='+apiKey
    r = requests.get(url)
    data = r.json()

    time_series_name = list(data.keys())[1]

    json_data = {}
    time_series_arr = []

    for i in list(data[time_series_name].keys()):
        one_time_series = {}
        one_time_series['Date'] = i
        one_time_series['Open'] = data[time_series_name][i]['1. open']
        one_time_series['High'] = data[time_series_name][i]['2. high']
        one_time_series['Low'] = data[time_series_name][i]['3. low']
        one_time_series['Close'] = data[time_series_name][i]['4. close']
        one_time_series['Volume'] = data[time_series_name][i]['5. volume']
        
        #apend to the front of the list 

        #method 1
        #time_series_arr.insert(0, one_time_series)

        #method 2
        #time_series_arr = [one_time_series] + time_series_arr

        #method 3
        time_series_arr[:0] = [one_time_series]

    json_data['time_series'] = time_series_arr
    return json_data

def get_data(symbol, start, end):
    downloaded = download_data(symbol)
    df = pd.json_normalize(downloaded, 'time_series')
    
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    start_row=0
    end_row=0

    for i in range(0, len(df)):
        if start <= pd.to_datetime(df['Date'][i]):
            start_row = i
            break

    for j in range(0, len(df)):
        if end >= pd.to_datetime(df['Date'][j]):
            end_row = len(df) - 1 - j
            break

    df = df.set_index(pd.DatetimeIndex(df['Date'].values))

    return df.iloc[start_row:end_row+1, :]

start, end, symbol = get_input()

df = get_data(symbol, start, end)

#print(df.head(10))

company_name = get_company_name(symbol.upper())

st.header(company_name+ " Close Price\n")
st.line_chart(df['Close'])

st.header(company_name+ " Volume Price\n")
st.line_chart(df['Volume'])

st.header("Data Statistics")
st.write(df.describe())