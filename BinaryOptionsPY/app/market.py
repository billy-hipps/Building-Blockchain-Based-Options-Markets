import json
import os
from web3 import Web3
import streamlit as st
import pandas as pd
from stock_data import get_price
from fetch_abi import fetch_abi

def init_market():
    market_data = {
            'Contract Address': [],
            'Asset': [],
            'Price': [],
            'Strike Price': [],
            'Payout': [],
            'Position': [], 
            'In the Money': [],
            'Status': [],
            'Terminated:': []
        }

    market_data = pd.DataFrame(market_data)
    
    return market_data


def refresh(factory_address, market_data, w3):
    """
    Refreshes market data by retrieving contract details from the blockchain.

    :param factory_address: The address of the Factory contract.
    :param market_data: Pandas DataFrame storing existing market data.
    :param w3: Web3 instance.
    :return: Updated market data DataFrame.
    """
    # Fetch ABIs
    factory_abi = fetch_abi('Factory')
    contract_abi = fetch_abi('CreateBO')

    # Convert `factory_address` to a contract instance
    factory_contract = w3.eth.contract(address=factory_address, abi=factory_abi)

    # Get all deployed contract addresses from the factory contract
    contracts = factory_contract.functions.getDeployedContracts().call()

    for contract in contracts:
        # Create contract instance
        contract_instance = w3.eth.contract(address=contract, abi=contract_abi)

        # Retrieve contract details
        asset = contract_instance.functions.ticker().call()
        price = contract_instance.functions.contractPrice().call()
        strike_price = contract_instance.functions.strikePrice().call()
        payout = contract_instance.functions.payout().call()
        position = contract_instance.functions.position().call()

        # Determine if the contract is "in the money"
        in_the_money = get_price(asset) > strike_price

        # Get contract status
        status = contract_instance.functions.isBought().call()
        terminated = contract_instance.functions.isTerminated().call()

        # Check if contract is already in `market_data`
        if contract not in market_data['Contract Address'].values:
            # Create a new row of data
            data = pd.DataFrame([{
                'Contract Address': contract,
                'Asset': asset,
                'Price': price,
                'Strike Price': strike_price,
                'Payout': payout,
                'Position': position,
                'In the Money': in_the_money,
                'Status': status,
                'Terminated': terminated
            }])

            # Append the new data
            market_data = pd.concat([market_data, data], ignore_index=True)

        else:
            # Update existing contract entry
            market_data.loc[market_data['Contract Address'] == contract, 'Asset'] = asset
            market_data.loc[market_data['Contract Address'] == contract, 'Price'] = price
            market_data.loc[market_data['Contract Address'] == contract, 'Strike Price'] = strike_price
            market_data.loc[market_data['Contract Address'] == contract, 'Payout'] = payout
            market_data.loc[market_data['Contract Address'] == contract, 'Position'] = position
            market_data.loc[market_data['Contract Address'] == contract, 'In the Money'] = in_the_money
            market_data.loc[market_data['Contract Address'] == contract, 'Status'] = status
            market_data.loc[market_data['Contract Address'] == contract, 'Terminated'] = terminated

    return market_data



def primary_market(primary_market):
    st.title('Primary Market')
    st.write('Welcome to the Market page! Here you view contracts that have not been bought yet.')

    data = st.dataframe(primary_market)