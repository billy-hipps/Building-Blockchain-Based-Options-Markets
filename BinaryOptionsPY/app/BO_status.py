from web3 import Web3
from compile import compile

# Get status of a BinaryOption contract
def BO_status(address, abi, w3):
    contract = w3.eth.contract(address=address, abi=abi)  # Instantiate contract with address and ABI

    # Call get_BO_status function to retrieve contract state
    isBought, isExpired, contractBuyer, contractBalance = contract.functions.get_BO_status().call()

    print("\n")
    print("Binary Option Status:")
    print("Contract is bought: ", isBought)  # Uncomment to show if contract is bought
    print("Contract is expired: ", isExpired)  # Uncomment to show if contract is expired
    print("Contract buyer: ", contractBuyer)  # Uncomment to show buyer's address
    print("Contract balance (ETH): ", contractBalance / 10**18)  # Uncomment to show balance in ETH
    # print("BO address", contract.functions.binaryOptionAddress().call())  # Print binary option address
    # print("Time Oracle address: ", contract.functions.timeOracleAddress().call())  # Print time oracle address
    print("\n")
