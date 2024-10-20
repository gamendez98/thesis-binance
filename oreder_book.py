import pandas as pd
import requests

ORDER_BOOK_URL = 'https://api.binance.com/api/v3/depth'
USD_M_FUTURES_OB_URL = 'https://testnet.binancefuture.com/fapi/v1/depth'

BTCUSDT = "BTCUSDT"


# %%

def fetch_order_book(symbol) -> pd.DataFrame:
    response = requests.get(USD_M_FUTURES_OB_URL, params={
        'symbol': symbol,
        'limit': 1000
    })
    response.raise_for_status()
    raw_data = response.json()
    bids = [
        {'price': price, 'quantity': quantity, 'type': 'bid', 'transaction_time': raw_data['T'],
         'message_out_time': raw_data['E']}
        for price, quantity in raw_data['bids']
    ]
    asks = [
        {'price': price, 'quantity': quantity, 'type': 'bid', 'transaction_time': raw_data['T'],
         'message_out_time': raw_data['E']}
        for price, quantity in raw_data['asks']
    ]
    return pd.DataFrame(bids + asks)


# %%

# Example usage
url = "https://api.example.com/data"
data = fetch_order_book(BTCUSDT)

# %%

fetch_latest_order_book()

# %%

j = "system"
n = 5

message = {
    "model": "gpt-4o",
    "messages": [
        {
            "role": j,
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": f"give me {n} ideas for a company"
        }
    ]
}

import json

print(json.dumps(message, indent=4))

# %%
import requests

# %%
r = requests.get("https://api.binance.com/api/v3/depth",
                 params=dict(symbol="BTCUSDT"))
results = r.json()
