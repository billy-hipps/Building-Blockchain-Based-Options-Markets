from stock_data import get_price

# Prompt user for Binary Option contract parameters
# Returns:
# - dict: Validated parameter values
def get_parameters():
    while True:
        parameters = {}

        print("\n--- Create a Binary Option Contract ---")

        # Validate ticker
        while True:
            ticker = input("Enter the asset ticker (e.g., AAPL): ").strip().upper()
            if ticker and 1 <= len(ticker) <= 32:
                parameters['ticker'] = ticker
                break
            print("❌ Invalid ticker. Must be 1–32 characters.")

        # Display current price of the asset
        try:
            current_price = get_price(parameters['ticker'])
            print(f"📈 Current price of {parameters['ticker']}: {current_price}")
        except Exception as e:
            print(f"⚠ Could not fetch current price: {e}")
            current_price = "Unavailable"

        # Validate position
        while True:
            position_input = input("Enter the position (long or short): ").strip().lower()
            if position_input == 'long':
                parameters['position'] = True
                break
            elif position_input == 'short':
                parameters['position'] = False
                break
            else:
                print("❌ Invalid position. Type 'long' or 'short'.")

        # Validate strike_date (in seconds)
        while True:
            try:
                strike_date = int(input("Enter the contract term in seconds: ").strip())
                if strike_date > 0:
                    parameters['strike_date'] = strike_date
                    break
                else:
                    print("❌ Contract term must be a positive number.")
            except ValueError:
                print("❌ Invalid input. Please enter an integer (e.g., 300).")

        # Validate contract price in ETH
        while True:
            try:
                contract_price = float(input("Enter the contract price in ETH: ").strip())
                if contract_price > 0:
                    parameters['contract_price'] = contract_price
                    break
                else:
                    print("❌ Price must be greater than 0.")
            except ValueError:
                print("❌ Invalid input. Please enter a numeric value (e.g., 0.5).")

        # Validate payout in ETH
        while True:
            try:
                payout = float(input("Enter the payout in ETH (ensure sufficient balance): ").strip())
                if payout > 0:
                    parameters['payout'] = payout
                    break
                else:
                    print("❌ Payout must be greater than 0.")
            except ValueError:
                print("❌ Invalid input. Please enter a numeric value (e.g., 1.0).")

        # === Summary ===
        print("\n✅ Please review your contract parameters:")
        print(f"  • Ticker: {parameters['ticker']}")
        print(f"  • Current Price: {current_price}")
        print(f"  • Position: {'Long' if parameters['position'] else 'Short'}")
        print(f"  • Term (seconds): {parameters['strike_date']}")
        print(f"  • Contract Price: {parameters['contract_price']} ETH")
        print(f"  • Payout: {parameters['payout']} ETH")

        # Confirm or retry
        confirm = input("\nSubmit these parameters? (yes/no): ").strip().lower()
        if confirm in ['yes', 'y']:
            return parameters
        else:
            print("🔁 Restarting parameter entry...\n")
