def get_parameters():
    parameters = {
        'ticker': None,
        'strike_price': None,
        'strike_date': None,
        'contract_price': None,
        'payout': None,
        'position': None
    }

    print('\n')

    # Ticker
    ticker = input("Enter the asset ticker (e.g., AAPL): ").strip()
    if not ticker or len(ticker) > 32:
        print("Invalid ticker. Must be 1–32 characters.")
        return None
    parameters['ticker'] = ticker

    # Numeric inputs with validation
    try:
        parameters['strike_date'] = int(input("Enter the contract term in seconds: "))
        parameters['contract_price'] = float(input("Enter the contract price in ETH: "))
        parameters['payout'] = float(input("Enter the payout in ETH (ensure you have sufficient balance): "))
    except ValueError:
        print("Invalid number format. Please enter numeric values for price, date, and ETH amounts.")
        return None

    # Position (long/short)
    position_input = input("Enter the position (long or short): ").strip().lower()
    if position_input == 'long':
        parameters['position'] = True
    elif position_input == 'short':
        parameters['position'] = False
    else:
        print("Invalid position. Must be 'long' or 'short'.")
        return None

    return parameters


