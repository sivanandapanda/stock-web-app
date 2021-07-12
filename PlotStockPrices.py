import pandas as pd
import requests
import os
import plotly.express as px

apiKey = os.getenv('ALPHA_VANTAGE_API_KEY')

def download_data(symbol):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='+symbol+'&apikey='+apiKey
    r = requests.get(url)
    data = r.json()

    time_series_name = list(data.keys())[1]

    json_data = {}
    time_series_arr = []

    for i in list(data[time_series_name].keys()):
        one_time_series = {}
        one_time_series['Open'] = float(data[time_series_name][i]['1. open'])
        one_time_series['High'] = float(data[time_series_name][i]['2. high'])
        one_time_series['Low'] = float(data[time_series_name][i]['3. low'])
        one_time_series['Close'] = float(data[time_series_name][i]['4. close'])
        one_time_series['Volume'] = float(data[time_series_name][i]['5. volume'])
        one_time_series['Date'] = i
        
        time_series_arr[:0] = [one_time_series]

    json_data['time_series'] = time_series_arr
    return json_data

def get_data(symbol):
    downloaded = download_data(symbol)
    df = pd.json_normalize(downloaded, 'time_series')

    df = df.set_index(pd.DatetimeIndex(df['Date'].values))

    return df

symbol="RELIANCE.BSE"

df = get_data(symbol)

fig = px.line(df, x = df['Date'], y = df['Close'], title = symbol + ' Close Price')
fig.show()