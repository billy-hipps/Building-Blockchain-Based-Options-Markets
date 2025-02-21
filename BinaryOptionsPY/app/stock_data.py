import requests 
import pandas as pd

def get_stock_data(symbol):
    API_key = "ZY03UDMEHO5SPNLL"
    BASE_URL = "https://www.alphavantage.co/query"

    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': API_key
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()
    timeSeries = data.get(f"Time Series (1min)", {})
    df = pd.DataFrame.from_dict(timeSeries, orient='index')
    df = df.rename(columns=lambda x: x.split(' ')[1])
    return df

df = get_stock_data("AAPL")
print(df.head())