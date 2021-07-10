import streamlit as st
import pandas as pd
from PIL import Image
import requests

st.write("""
#Stock Market Web Application
**Visually** show data on a stock! Date range from Jan 2, 2020 - Aug 4, 2020
""")

st.sidebar.header('User Input')

def get_input():
    start_date = st.sidebar.text_input("Start Date", "2021-02-12")
    end_date = st.sidebar.text_input("End Date", "2021-07-09")
    stock_symbol = st.sidebar.text_input("Stock Symbol", "RELIANCE.BSE")
    return start_date, end_date, stock_symbol

def get_company_name(symbol):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+symbol+'&apikey=demo'
    r = requests.get(url)
    data = r.json()
    return data['Meta Data']['2. Symbol']

def download_data(symbol):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+symbol+'&apikey=demo'
    r = requests.get(url)
    data = r.json()
    price_array=[]
    price_array.append('Date,Open,High,Low,Close,Volume')

    for i in list(data['Time Series (Daily)'].keys()):
        to_insert=i+','+data['Time Series (Daily)'][i]['1. open']+','+data['Time Series (Daily)'][i]['2. high']+','+data['Time Series (Daily)'][i]['3. low']+','+data['Time Series (Daily)'][i]['4. close']+','+data['Time Series (Daily)'][i]['5. volume']
        price_array.append(to_insert)
    
    return price_array

def get_data(symbol, start, end):
    downloaded = download_data(symbol)
    df = pd.DataFrame(downloaded)
    
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
            end_row = j
            break

    df = df.set_index(pd.DatetimeIndex(df['Date'].values))

    return df.iloc[start_row:end_row+1, :]

start, end, symbol = get_input()

df = get_data(symbol, start, end)

company_name = get_company_name(symbol.upper())

st.header(company_name+ " Close Price\n")
st.line_chart(df['Close'])

st.header(company_name+ " Volume Price\n")
st.line_chart(df['Volume'])

st.header("Data Statistics")
st.write(df.describe())