from eth_balance import eth_balance
from get_parameters import get_parameters
from create_contract import create_contract
from buy import buy
from login import login
from BO_status import BO_status
from market import init_market, refresh, primary_market
from view_portfolio import init_portfolio, refresh_portfolio, view_portfolio

import pandas as pd
import traceback
from eth_utils.address import is_address

def home_page(creator, accountAddress, privateKey, factoryAddress, w3):

    market_data = init_market()
    portfolio_data = init_portfolio()

    print('\n')
    if creator == True:
        print("You are logged in as a contract creator!")


        while True:
            try:
                action = input("What do you want to do?\n1. View Balances (1)\n2. View Portfolio (2)\n3. Create Contract (3)\n4. Logout (4)\n").strip()

                if action == '1':
                    try:
                        balance = eth_balance(w3, accountAddress)
                        print(f"ETH Balance: {balance}")
                    except Exception as e:
                        print(f"[Error] Could not fetch balance: {e}")
                    break

                elif action == '2':
                    print("View Portfolio")
                    try:
                        portfolio_data = refresh_portfolio(factoryAddress, portfolio_data, accountAddress, w3)
                        view_portfolio(portfolio_data)
                    except Exception as e:
                        print(f"[Error] Failed to load portfolio: {e}")
                    break

                elif action == '3':
                    print("Create Contract")
                    try:
                        parameters = get_parameters()
                        if parameters:
                            deployer_address = create_contract(factoryAddress, parameters, accountAddress, privateKey, w3)
                        else:
                            print("Contract creation cancelled due to invalid parameters.")
                    except Exception as e:
                        print(f"[Error] Failed to create contract: {e}")
                        traceback.print_exc()
                    break

                elif action == '4':
                    print("Logging out...!")
                    login()
                    break

                else:
                    print("Invalid action. Please choose 1–4.")

            except KeyboardInterrupt:
                print("\nExiting to home.")
                break

    # Buyer dashboard
    elif creator is False:
        print("You are logged in as a contract buyer!")

        while True:
            try:
                action = input("What do you want to do?\n1. View Balances (1)\n2. View Portfolio (2)\n3. Browse contracts (3)\n4. Logout (4)\n").strip()

                if action == '1':
                    try:
                        balance = eth_balance(w3, accountAddress)
                        print(f"ETH Balance: {balance}")
                    except Exception as e:
                        print(f"[Error] Could not fetch balance: {e}")
                    break

                elif action == '2':
                    print("View Portfolio")
                    try:
                        portfolio_data = refresh_portfolio(factoryAddress, portfolio_data, accountAddress, w3)
                        view_portfolio(portfolio_data)
                    except Exception as e:
                        print(f"[Error] Failed to load portfolio: {e}")
                    break

                elif action == '3':
                    print("Browse contracts")
                    try:
                        market_data = refresh(factoryAddress, market_data, w3)
                        primary_market(market_data)

                        contract_to_buy = input("Enter the contract accountAddress you want to buy: ").strip()
                        if not is_address(contract_to_buy):
                            raise ValueError("Invalid Ethereum accountAddress format.")
                        contract_to_buy = w3.to_checksum_address(contract_to_buy)

                        try:
                            buy(accountAddress, privateKey, contract_to_buy, w3)
                            print("Contract bought successfully.")
                            market_data = refresh(factoryAddress, market_data, w3)
                        except Exception as e:
                            print(f"[Error] Buy transaction failed: {e}")
                    except Exception as e:
                        print(f"[Error] Failed to browse contracts: {e}")
                    break

                elif action == '4':
                    print("Logging out...!")
                    login()
                    break

                else:
                    print("Invalid action. Please choose 1–4.")

            except KeyboardInterrupt:
                print("\nExiting to home.")
                break
