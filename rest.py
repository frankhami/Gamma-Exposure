import requests
import time
import pandas as pd


url = "https://www.deribit.com/api/v2/public/get_instruments"

params = {
    "currency": "BTC", 
    "kind": "option",
    "expired": "false"
}

response = requests.get(url, params=params)

data = response.json()
instruments = data.get("result", [])

instrument_ids = [item["instrument_id"] for item in instruments]

order_books = {}
order_data = {}
for i, instrument_id in enumerate(instrument_ids):
    order_url = "https://www.deribit.com/api/v2/public/get_order_book_by_instrument_id"
    order_params = {"instrument_id": instrument_id}
    
    try:
        r = requests.get(order_url, params=order_params)
        if r.status_code == 200:
            order_data[instrument_id] = r.json().get("result", {})
            
            greeks = order_data[instrument_id].get('greeks', {})
            
            extracted_info = {
                'instrument_name': order_data[instrument_id].get('instrument_name'),
                'gamma': greeks.get('gamma'),  # Access gamma inside greeks
                'open_interest': order_data[instrument_id].get('open_interest'),
                'index_price': order_data[instrument_id].get('index_price')
            }

            order_books[instrument_id] = extracted_info
            

        else:
            print(f"Error {r.status_code} for {instrument_id}: {r.text}")
    except Exception as e:
        print(f"Request failed for {instrument_id}: {e}")
    
    time.sleep(0.2)
    print(order_books[instrument_id])

df = pd.DataFrame(order_books.values())

df.to_csv("order_books.csv", index=False)

