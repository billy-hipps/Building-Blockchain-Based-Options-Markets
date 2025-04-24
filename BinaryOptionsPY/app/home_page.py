from eth_balance import eth_balance
from get_parameters import get_parameters
from create_contract import create_contract
from buy import buy
from login import login
from BO_status import BO_status
from market import init_market, refresh, primary_market
from view_portfolio import init_portfolio, refresh_portfolio, view_portfolio

import pandas as pd


def home_page(creator, address, privateKey, factory_address, w3):

    market_data = init_market()
    portfolio_data = init_portfolio()

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
                portfolio_data = refresh_portfolio(factory_address, portfolio_data, address, w3)
                print(portfolio_data)
                # Display portfolio data
                view_portfolio(portfolio_data)
                break

            elif action == '3':
                print("Create Contract")
                parameters = get_parameters()
                deployerAdress = create_contract(factory_address, parameters, address, privateKey, w3)
                break

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
                portfolio_data = refresh_portfolio(factory_address, portfolio_data, address, w3)
                print(portfolio_data)
                # Display portfolio data
                view_portfolio(portfolio_data)
                break

            elif action == '3':
                print("Browse contracts")
                # call contract browser function
                market_data = refresh(factory_address, market_data, w3)
                primary_market(market_data)

                # Buy contract function
                contract_to_buy = input("Enter the contract address you want to buy: ")
                contract_to_buy.strip()
                contract_to_buy = w3.to_checksum_address(contract_to_buy)
                # call buy function
                buy(address, privateKey, contract_to_buy, w3)

                # Refresh and re-display market data
                market_data = refresh(factory_address, market_data, w3)
                break

            elif action == '4':
                print("Logging out...!")
                login()
                
            else:
                print("Invalid action")

    print('\n')
