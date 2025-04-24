import json
import os
import re 
from web3 import Web3
import streamlit as st
import numpy as np 
import pandas as pd
from stock_data import get_price
from fetch_abi import fetch_abi

def init_portfolio():
    portfolio_data = {
            'Contract Address': [],
            'Buy or Sell Side': [],
            'Asset': [],
            'Price': [],
            'Strike Price': [],
            'Payout': [],
            'Position': [], 
            'In the Money': [],
            'Terminated': []
        }

    portfolio_data = pd.DataFrame(portfolio_data)
    
    return portfolio_data


def refresh_portfolio(factory_address, portfolio_data, address, w3):
    """
    Refreshes portfolio data by retrieving contract details from the blockchain.

    :param factory_address: The address of the Factory contract.
    :param portfolio_data: Pandas DataFrame storing existing portfolio data.
    :param w3: Web3 instance.
    :return: Updated portfolio data DataFrame.
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

            buy_side = None

            buyer = contract_instance.functions.buyer().call()
            creator = contract_instance.functions.creator().call()
            if buyer or creator == address:
                if buyer == address:
                    # Buyer address is the user's address
                    buy_side = True
                else:
                    # Creator address is the user's address
                    buy_side = False  
                # Retrieve contract details
                asset = contract_instance.functions.ticker().call()
                asset = str(asset).strip()
                asset = re.sub(r'[^A-Z]', '', asset)  # Keep only uppercase letters

                price = int(contract_instance.functions.contractPrice().call()) /1e18
                strike_price = int(contract_instance.functions.strikePrice().call())
                payout = int(contract_instance.functions.payout().call()) /1e18
                position = int(contract_instance.functions.position().call())
                if position == 0:
                    position = False
                else:
                    position = True

                if buy_side:
                    postion = not(position)

                # Determine if the contract is "in the money"
                if position == 0:
                    in_the_money = get_price(asset) < strike_price
                else:
                    in_the_money = get_price(asset) > strike_price


                if in_the_money:
                    in_the_money = 'In the Money'
                else:
                    in_the_money = 'Out of the Money'

                terminated = bool(contract_instance.functions.isExpired().call())
                if terminated:
                    terminated = 'Expired'
                else:
                    terminated = 'Active'

                # Convert large integers to strings to prevent Pandas OverflowError
                price = str(price)
                strike_price = str(strike_price)
                payout = str(payout)
                position = str(position)

                if contract not in portfolio_data['Contract Address'].values:
                    # Append new data to the DataFrame
                    new_data = pd.DataFrame([{
                        'Contract Address': contract,
                        'Buy or Sell Side': 'Buy' if buy_side else 'Sell',
                        'Asset': asset,
                        'Price': price,
                        'Strike Price': strike_price,
                        'Payout': payout,
                        'Position': position,
                        'In the Money': in_the_money,
                        'Terminated': terminated
                    }])
                    portfolio_data = pd.concat([portfolio_data, new_data], ignore_index=True)
        
        except Exception as e:
            print(f"Error processing contract {contract}: {e}")
            continue  # Skip
    
    return portfolio_data


def view_portfolio(portfolio_data):
    # Clear the Streamlit display before rendering new content
    container = st.empty()

    # Use the container to build the refreshed UI
    with container.container():
        st.title('Portfolio')
        st.write('Welcome to your portfolio page: Here you can view your trading history.')

        if portfolio_data.empty:
            st.info("No contract data available yet. Please refresh.")
            return

        # Display each contract in an expandable section
        for idx, row in portfolio_data.iterrows():
            with st.expander(f"{row['Asset']} Option ({row['Terminated']})"):
                st.markdown("**Contract Address:**")
                st.code(row['Contract Address'], language=None)  # Enables copy to clipboard

                st.markdown(f"""
                - **Price:** {row['Price']} ETH  
                - **Strike Price:** {row['Strike Price']}  
                - **Payout:** {row['Payout']} ETH  
                - **Position:** {"Long" if row['Position'] == '1' else "Short"}  
                - **Terminated:** {row['Terminated']}  
                - **In the Money:** {row['In the Money']}
                """)

        st.divider()
        st.caption("Use the refresh button above to load new contracts.")
