#==== GET ACCOUNT INFO ====

def eth_balance(w3, account_address):
    return w3.eth.get_balance(account_address)