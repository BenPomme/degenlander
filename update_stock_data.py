import requests
import json
import time

# List of 20 stocks with ticker and company name
stock_list = [
    {"ticker": "AAPL", "name": "Apple Inc."},
    {"ticker": "MSFT", "name": "Microsoft Corporation"},
    {"ticker": "GOOGL", "name": "Alphabet Inc."},
    {"ticker": "AMZN", "name": "Amazon.com Inc."},
    {"ticker": "TSLA", "name": "Tesla Inc."},
    {"ticker": "META", "name": "Meta Platforms Inc."},
    {"ticker": "NVDA", "name": "NVIDIA Corporation"},
    {"ticker": "NFLX", "name": "Netflix Inc."},
    {"ticker": "BABA", "name": "Alibaba Group"},
    {"ticker": "JPM", "name": "JPMorgan Chase"},
    {"ticker": "BAC", "name": "Bank of America"},
    {"ticker": "V", "name": "Visa Inc."},
    {"ticker": "MA", "name": "Mastercard Inc."},
    {"ticker": "WMT", "name": "Walmart Inc."},
    {"ticker": "DIS", "name": "Walt Disney"},
    {"ticker": "PFE", "name": "Pfizer Inc."},
    {"ticker": "KO", "name": "Coca-Cola Co."},
    {"ticker": "MCD", "name": "McDonald's Corp"},
    {"ticker": "BA", "name": "Boeing Co."},
    {"ticker": "UNH", "name": "UnitedHealth Group"}
]

# Use your API key
api_key = "KGONF7JN3HYIGUWO"

results = []

# Loop through each stock, fetch the latest price, and build an entry
for stock in stock_list:
    ticker = stock["ticker"]
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={api_key}"
    print(f"Fetching data for {ticker} from: {url}")
    try:
        response = requests.get(url)
        data = response.json()
        if "Global Quote" in data and data["Global Quote"].get("05. price"):
            price = float(data["Global Quote"]["05. price"])
        else:
            price = None
            print(f"Warning: No price data found for {ticker}.")
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        price = None

    results.append({
        "ticker": ticker,
        "name": stock["name"],
        "price": price
    })

    # Respect rate limits: wait 15 seconds between calls
    time.sleep(15)

# Write the results to a JSON file named stocks.json
with open("stocks.json", "w") as f:
    json.dump(results, f, indent=4)

print("Stock data updated and saved to stocks.json")