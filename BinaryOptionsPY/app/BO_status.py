from web3 import Web3
from compile import compile

# Get status of a BinaryOption contract

def BO_status(address, abi, w3):
    contract = w3.eth.contract(address=address, abi=abi)

    isBought, isExpired, contractBuyer, contractBalance = contract.functions.get_BO_status().call()

    print("\n")
    print("Binary Option Status:")
    #print("Contract is bought: ", isBought)
    #print("Contract is expired: ", isExpired)
    #print("Contract buyer: ", contractBuyer)
    #print("Contract balance: ", contractBalance / 10**18)

    print("BO address", contract.functions.binaryOptionAddress().call())
    print("Time Oracle address: ", contract.functions.timeOracleAddress().call())
    print("\n")

