from eth_balance import eth_balance
from select_situation import select_situation
from create_contract import create_contract
from buy import buy
from login import login
from BO_status import BO_status

def home_page(creator, address, privateKey, w3):
    print('\n')
    if creator == True:
        print("You are logged in as a contract creator!")
        while True:
            action = input("What do you want to do?\n1. View Balances (1)\n2. View Portfolio (2)\n3. Create Contract (3)\n4. Logout (4)\n")
            if action == '1':
                print(f"ETH Balance: {eth_balance(w3, address)}")
                break

            elif action == '2':
                print("View Portfolio")

                break

            elif action == '3':
                print("Create Contract")
                parameters = select_situation()
                deployerAdress = create_contract(parameters, address, privateKey, w3)

            elif action == '4':
                print("Logging out...!")
                login()

            else:
                print("Invalid action")

    elif creator == False:
        print("You are logged in as a contract buyer!")
        while True:
            action = input("What do you want to do?\n1. View Balances (1)\n2. View Portfolio (2)\n3. Browse contracts (3)\n4. Logout (4)\n")
            if action == '1':
                print(f"ETH Balance: {eth_balance(w3, address)}")
                break

            elif action == '2':
                print("View Portfolio")
                # call portfolio function
                break

            elif action == '3':
                print("Browse contracts")
                # call contract browser function
                contract_to_buy = input("Enter the contract address you want to buy: ")
                # call buy function
                buy(10, address, privateKey, contract_to_buy, w3)
                break

            elif action == '4':
                print("Logging out...!")
                login()
                
            else:
                print("Invalid action")

    print('\n')