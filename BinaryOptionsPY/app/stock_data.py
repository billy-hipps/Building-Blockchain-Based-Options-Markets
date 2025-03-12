import yfinance as yf

def get_price(ticker):
    try:
        if not ticker or not isinstance(ticker, str):
            raise ValueError("Invalid ticker symbol provided")

        ticker = ticker.strip().upper()  # Remove spaces & enforce uppercase

        stock = yf.Ticker(ticker)
        stock_info = stock.info

        if not stock_info or "regularMarketPrice" not in stock_info:
            raise ValueError(f"No market data found for ticker: {ticker}")

        market_price = stock_info.get("regularMarketPrice", None)
        if market_price is None:
            return f"⚠ No live price found for {ticker}."

        return int(market_price)

    except Exception as e:
        print(f"⚠ Error fetching price for {ticker}: {e}")
        return None
