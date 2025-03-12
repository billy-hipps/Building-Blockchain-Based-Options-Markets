def get_parameters():
    parameters = {
        'ticker': None,
        'Strike_Price': None,
        'Strike_Date': None,
        'Contract_Price': None,
        'Payout': None,
        'Position': None
    }

    print('\n')
    ticker = input("Enter the asset ticker: ")
    parameters['ticker'] = ticker

    Strike_Price = input("Enter the strike price: ")
    parameters['strike_price'] = int(Strike_Price)

    Strike_Date = input("Enter the contract term in seconds: ")
    parameters['strike_date'] = int(Strike_Date)

    Contract_Price = input("Enter the contract price in ETH: ")
    parameters['contract_price'] = int(Contract_Price)

    Payout = input("Enter the payout in ETH (ensure you have sufficient balance): ")
    parameters['payout'] = int(Payout)

    Position = input("Enter the position (long or short): ")
    if Position.strip() == 'long':
        Position = True
    elif Position.strip() == 'short':
        Position = False
        
    parameters['position'] = Position

    return parameters

