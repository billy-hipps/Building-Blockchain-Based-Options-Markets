# Returns the ETH balance of a given address
def eth_balance(w3, address):
    return w3.eth.get_balance(address) / 10**18  # Convert from Wei to Ether
