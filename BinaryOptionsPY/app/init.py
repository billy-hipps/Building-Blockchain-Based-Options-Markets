import keyboard
from web3 import Web3

from home_page import home_page
from login import login

#==== INITIALISE THE APP ====
# home hotkey
keyboard.add_hotkey('ctrl+shift+h', lambda: home_page(creator, account_address, private_key))
# logout hotkey
keyboard.add_hotkey('ctrl+shift+l', login)

# connect to local Hardhat blockchain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

#==== LOGIN ====
creator, account_address, private_key = login()

#==== MAIN MENU ====
while True:
    home_page(creator, account_address, private_key, w3)
