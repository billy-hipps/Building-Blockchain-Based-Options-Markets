from web3 import Web3
from compile import compile

# Get status of a BinaryOption contract

def BO_status(address, w3):
    compiledData = compile()
    BinaryOption = compiledData["BinaryOption"]

    contract = w3.eth.contract(address=address, abi=BinaryOption[0])

    buyer = contract.functions.get_contractBuyer().call()
    isBought = contract.functions.isBought().call()

    print(f"Buyer: {buyer}")
    print(f"IsBought: {isBought}")
