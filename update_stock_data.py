import requests
import json
import time

API_KEY = "KGONF7JN3HYIGUWO"

stocks = [
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

main_stock_list = []

for stock in stocks:
    ticker = stock["ticker"]
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={API_KEY}"
    print(f"Fetching data for {ticker} from {url}")
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        continue

    if "Time Series (Daily)" not in data:
        print(f"Error: No time series data for {ticker}. Response: {data}")
        continue

    time_series = data["Time Series (Daily)"]
    dates = sorted(time_series.keys(), reverse=True)
    if not dates:
        print(f"No dates found for {ticker}.")
        continue
    latest_date = dates[0]
    try:
        last_close = float(time_series[latest_date]["4. close"])
    except Exception as e:
        print(f"Error parsing closing price for {ticker}: {e}")
        continue

    main_stock_list.append({
        "ticker": ticker,
        "name": stock["name"],
        "price": last_close
    })

    # For terrain data, get the 30 oldest dates from the last 30 available days (sorted ascending)
    last_30_dates = sorted(dates[-30:])
    terrain_data = []
    for d in last_30_dates:
        try:
            close_value = time_series[d]["4. close"]
            terrain_data.append({"4. close": close_value})
        except Exception as e:
            print(f"Error parsing data for date {d} of {ticker}: {e}")
    filename = f"stock_{ticker}.json"
    try:
        with open(filename, "w") as f:
            json.dump(terrain_data, f, indent=4)
        print(f"Saved terrain data for {ticker} to {filename}")
    except Exception as e:
        print(f"Error writing file {filename}: {e}")

    time.sleep(15)

try:
    with open("stocks.json", "w") as f:
        json.dump(main_stock_list, f, indent=4)
    print("Saved main stock list to stocks.json")
except Exception as e:
    print(f"Error writing stocks.json: {e}")