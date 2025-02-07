from eth_balance import eth_balance
from select_situation import select_situation
from create_contract import create_contract

def home_page(creator, address, private_key, w3):
    print('\n')
    if creator == True:
        print("You are logged in as a contract creator!")
        while True:
            action = input("What do you want to do?\n1. View Balances (1)\n2. View Portfolio (2)\n3. Create Contract (3)\n")
            if action == '1':
                print(f"ETH Balance: {eth_balance(w3, address)}")
                break
            elif action == '2':
                print("View Portfolio")
                # call portfolio function
                break
            elif action == '3':
                parameters = select_situation()
                contract, contract_address = create_contract(parameters, address, private_key, w3)
                break
            else:
                print("Invalid action")

    elif creator == False:
        print("You are logged in as a contract buyer!")
        while True:
            action = input("What do you want to do?\n1. View Balances (1)\n2. View Portfolio (2)\n3. Browse contracts (3)\n")
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
                break
            else:
                print("Invalid action")

    print('\n')