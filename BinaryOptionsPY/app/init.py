from web3 import Web3

from home_page import home_page
from login import login

#==== INITIALISE THE APP ====
def init():
    # connect to local Hardhat blockchain
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

    #==== LOGIN ====
    creator, accountAddress, privateKey = login()


    #==== MAIN MENU ====
    while True:
        home_page(creator, accountAddress, privateKey, w3)


if __name__ == "__main__":
    init()
    