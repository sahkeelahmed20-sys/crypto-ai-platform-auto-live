
import requests, pandas as pd

def get_price_history(symbol, interval="5m", limit=200):
    url = "https://fapi.binance.com/fapi/v1/klines"
    r = requests.get(url, params={"symbol":symbol,"interval":interval,"limit":limit})
    data = r.json()
    df = pd.DataFrame(data, columns=["t","o","h","l","c","v","_","_","_","_","_","_"])
    df["c"] = df["c"].astype(float)
    return df.rename(columns={"c":"close"})
