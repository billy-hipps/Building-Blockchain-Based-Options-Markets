import json
import os
import re 
from web3 import Web3
import streamlit as st
import numpy as np 
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
        try:
            # Create contract instance
            contract_instance = w3.eth.contract(address=contract, abi=contract_abi)

            # Retrieve contract details
            asset = contract_instance.functions.ticker().call()
            asset = str(asset).strip()
            asset = re.sub(r'[^A-Z]', '', asset)  # Keep only uppercase letters

            price = int(contract_instance.functions.contractPrice().call()) /1e18
            strike_price = int(contract_instance.functions.strikePrice().call())
            payout = int(contract_instance.functions.payout().call()) /1e18
            position = int(contract_instance.functions.position().call())

            # Determine if the contract is "in the money"
            if position == 0:
                in_the_money = get_price(asset) < strike_price
            else:
                in_the_money = get_price(asset) > strike_price

            if in_the_money:
                in_the_money = 'In the Money'
            else:
                in_the_money = 'Out of the Money'

            # Get contract status
            status = bool(contract_instance.functions.isBought().call())
            if status:
                status = 'Bought'
            else:
                status = 'Available'

            terminated = bool(contract_instance.functions.isExpired().call())  # Ensure correct function name
            if terminated:
                terminated = 'Expired'
            else:
                terminated = 'Active'

            # Convert large integers to strings to prevent Pandas OverflowError
            price = str(price)
            strike_price = str(strike_price)
            payout = str(payout)
            position = str(position)

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
                # Update existing contract entry efficiently
                market_data.loc[market_data['Contract Address'] == contract, [
                    'Asset', 'Price', 'Strike Price', 'Payout', 
                    'Position', 'In the Money', 'Status', 'Terminated'
                ]] = [asset, price, strike_price, payout, position, in_the_money, status, terminated]

        except Exception as e:
            print(f"Error processing contract {contract}: {e}")
            continue  # Skip

    return market_data


def primary_market(market_data):
    # Clear the Streamlit display before rendering new content
    container = st.empty()

    # Use the container to build the refreshed UI
    with container.container():
        st.title('Primary Market')
        st.write('Welcome to the Market page! Here you view contracts that have not been bought yet.')

        if market_data.empty:
            st.info("No contract data available yet. Please refresh.")
            return

        # Display each contract in an expandable section
        for idx, row in market_data.iterrows():
            with st.expander(f"{row['Asset']} Option ({row['Status']})"):
                st.markdown("**Contract Address:**")
                st.code(row['Contract Address'], language=None)  # Enables copy to clipboard

                st.markdown(f"""
                - **Price:** {row['Price']} ETH  
                - **Strike Price:** {row['Strike Price']}  
                - **Payout:** {row['Payout']} ETH  
                - **Position:** {"Long" if row['Position'] == '1' else "Short"}  
                - **Status:** {row['Status']}  
                - **Terminated:** {row['Terminated']}  
                - **In the Money:** {row['In the Money']}
                """)

        st.divider()
        st.caption("Use the refresh button above to load new contracts.")
    