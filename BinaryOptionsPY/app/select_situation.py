#==== CHOOSE A CASE TO DEMONSTRATE ====

buyer_win_long = {
    'payout': 20,
    'strike_price': 100,
    'strike_date': 120,
    'expiry_price': 120,
    'contract_price': 10,
    'position' : True
}

buyer_win_short = {
    'payout': 20,
    'strike_price': 100,
    'strike_date': 120,
    'expiry_price': 80,
    'contract_price': 10,
    'position' : False
}

buyer_lose_long = {
    'payout': 20,
    'strike_price': 100,
    'strike_date': 120,
    'expiry_price': 80,
    'contract_price': 10,
    'position' : True
}

buyer_lose_short = {
    'payout': 20,
    'strike_price': 100,
    'strike_date': 120,
    'expiry_price': 120,
    'contract_price': 10,
    'position' : False
}

creator_insufficient_eth = {
    'payout': 10000000000000000000000,
    'strike_price': 100,
    'strike_date': 120,
    'expiry_price': 120,
    'contract_price': 10,
    'position' : True
}


def select_situation():
    # choose a situation
    while True:
        print("\n1. Buyer wins (long)\n2. Buyer wins (short)\n3. Buyer loses (long)\n4. Buyer loses (short)\n5. Creator has insufficient ETH\n")
        situation = input("Choose a situation (1-5): ")
        if situation in ['1', '2', '3', '4', '5']:
            break
        else:
            print("Invalid input. Please try again.")

    if situation == '1':
        parameters = buyer_win_long
    elif situation == '2':
        parameters = buyer_win_short
    elif situation == '3':
        parameters = buyer_lose_long
    elif situation == '4':
        parameters = buyer_lose_short
    else :
        parameters = creator_insufficient_eth

    return parameters
