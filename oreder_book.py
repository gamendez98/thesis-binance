import requests


ORDER_BOOK_URL = 'https://api1.binance.com/eapi/v1/depth'

def fetch_latest_order_book():
    try:
        response = requests.get(ORDER_BOOK_URL, params={
            'symbol': 'BNBBTC',
            'limit': 1000
        })
        response.raise_for_status()
        # Process the JSON data from response
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


# Example usage
url = "https://api.example.com/data"
data = fetch_latest_order_book()
if data:
    print(data)

#%%

fetch_latest_order_book()

#%%

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