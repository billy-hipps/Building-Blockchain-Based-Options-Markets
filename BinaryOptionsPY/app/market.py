import json
import os
import re
from web3 import Web3
import streamlit as st
import numpy as np
import pandas as pd
from stock_data import get_price
from fetch_abi import fetch_abi

# Initialize an empty market DataFrame with standard columns
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
        'Terminated': []
    }
    market_data = pd.DataFrame(market_data)
    return market_data

# Refresh market data by querying deployed CreateBO contracts from the Factory
# Parameters:
# - factory_address: string, address of the Factory contract
# - market_data: pd.DataFrame, existing table to be updated
# - w3: Web3 instance
# Returns:
# - Updated DataFrame with latest contract data
def refresh(factory_address, market_data, w3):
    factory_abi = fetch_abi('Factory')
    contract_abi = fetch_abi('CreateBO')

    factory_contract = w3.eth.contract(address=factory_address, abi=factory_abi)
    contracts = factory_contract.functions.getDeployedContracts().call()  # Get all CreateBO contracts

    for contract in contracts:
        try:
            contract_instance = w3.eth.contract(address=contract, abi=contract_abi)

            asset = contract_instance.functions.ticker().call()
            asset = str(asset).strip()
            asset = re.sub(r'[^A-Z]', '', asset)  # Sanitize asset ticker

            price = int(contract_instance.functions.contractPrice().call()) / 1e18
            strike_price = int(contract_instance.functions.strikePrice().call())
            payout = int(contract_instance.functions.payout().call()) / 1e18
            position = int(contract_instance.functions.position().call())  # 0 = short, 1 = long

            if position == 0:
                position = 1
            elif position == 1:
                position = 0

            # Evaluate "in the money" status
            if position == 0:
                in_the_money = get_price(asset) < strike_price
            else:
                in_the_money = get_price(asset) > strike_price
            in_the_money = 'In the Money' if in_the_money else 'Out of the Money'

            # Check purchase status
            status = 'Bought' if contract_instance.functions.isBought().call() else 'Available'

            # Check expiry status
            terminated = 'Expired' if contract_instance.functions.isExpired().call() else 'Active'

            # Convert to strings for DataFrame compatibility
            price = str(price)
            strike_price = str(strike_price)
            payout = str(payout)
            position = str(position)

            # Append or update contract in the market data
            if contract not in market_data['Contract Address'].values:
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
                market_data = pd.concat([market_data, data], ignore_index=True)
            else:
                market_data.loc[market_data['Contract Address'] == contract, [
                    'Asset', 'Price', 'Strike Price', 'Payout',
                    'Position', 'In the Money', 'Status', 'Terminated'
                ]] = [asset, price, strike_price, payout, position, in_the_money, status, terminated]

        except Exception as e:
            print(f"Error processing contract {contract}: {e}")
            continue

    return market_data

# Display market data using Streamlit UI
# Parameters:
# - market_data: pd.DataFrame, table of available contracts
def primary_market(market_data):
    container = st.empty()  # Reset Streamlit display

    with container.container():
        st.title('Primary Market')
        st.write('Welcome to the Market page! Here you view contracts that have not been bought yet.')

        if market_data.empty:
            st.info("No contract data available yet. Please refresh.")
            return

        # Display each contract in an expandable view
        for idx, row in market_data.iterrows():
            with st.expander(f"{row['Asset']} Option ({row['Status']})"):
                st.markdown("**Contract Address:**")
                st.code(row['Contract Address'])

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
