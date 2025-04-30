import yfinance as yf

# Fetch the latest market price for a given stock ticker
# Parameters:
# - ticker: string, asset symbol (e.g., "AAPL")
# Returns:
# - int: rounded current market price
# - None: if price fetch fails
def get_price(ticker):
    try:
        if not ticker or not isinstance(ticker, str):
            raise ValueError("Invalid ticker symbol provided")

        ticker = ticker.strip().upper()  # Sanitize and standardize input

        stock = yf.Ticker(ticker)
        stock_info = stock.info  # Retrieve stock metadata

        if not stock_info or "regularMarketPrice" not in stock_info:
            raise ValueError(f"No market data found for ticker: {ticker}")

        market_price = stock_info.get("regularMarketPrice", None)
        if market_price is None:
            return f"⚠ No live price found for {ticker}."

        return int(market_price)  # Return price as integer

    except Exception as e:
        print(f"⚠ Error fetching price for {ticker}: {e}")
        return None  # Return None on failure

