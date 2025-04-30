from web3 import Web3

from home_page import home_page
from login import login

# ==== INITIALISE THE APP ====
# Connects to local blockchain, logs in user, and launches the home page loop
def init():
    # Connect to local Hardhat blockchain node
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        
    creator, accountAddress, privateKey, factory_address = login()

    # ==== MAIN MENU ====
    # Loop user back to home page until manually exited
    while True:
        home_page(creator, accountAddress, privateKey, factory_address, w3)


# Entry point for script execution
if __name__ == "__main__":
    init()
