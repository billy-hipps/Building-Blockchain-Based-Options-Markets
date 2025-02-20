#==== GET ACCOUNT INFO ====

def eth_balance(w3, address):
    return w3.eth.get_balance(address) / 10**18