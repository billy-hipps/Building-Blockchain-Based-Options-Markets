import requests
import time

FINNHUB_API_KEY = "d0d4obpr01qm2sk7uue0d0d4obpr01qm2sk7uueg"  # Replace with your actual key

def get_price(ticker, retries=3, delay=2):
    try:
        if not ticker or not isinstance(ticker, str):
            raise ValueError("Invalid ticker symbol provided")

        ticker = ticker.strip().upper()

        url = f"https://finnhub.io/api/v1/quote"
        params = {
            "symbol": ticker,
            "token": FINNHUB_API_KEY
        }

        for attempt in range(retries):
            try:
                response = requests.get(url, params=params, timeout=10)
                data = response.json()

                if "c" in data and data["c"] > 0:
                    # "c" is the current price
                    return int(data["c"])

                else:
                    raise Exception(f"Invalid price data: {data}")

            except Exception as e:
                print(f"⚠ Attempt {attempt + 1} failed for {ticker}: {e}")
                time.sleep(delay * (2 ** attempt))  # exponential backoff

        print(f"❌ Failed to fetch price for {ticker} after {retries} attempts.")
        return None

    except Exception as e:
        print(f"⚠ Error in get_price for {ticker}: {e}")
        return None
