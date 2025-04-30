import json
import os
import re
import streamlit as st
import numpy as np
import pandas as pd
from web3 import Web3
from stock_data import get_price
from fetch_abi import fetch_abi

def init_portfolio():
    portfolio_data = {
        'Contract Address': [],
        'Asset': [],
        'Price': [],
        'Strike Price': [],
        'Payout': [],
        'Position': [],
        'In the Money': [],
        'Status': [],
        'Terminated': [],
        'Buy or Sell Side': [],
        'Winner': []
    }
    return pd.DataFrame(portfolio_data)

def refresh_portfolio(factory_address, portfolio_data, user_address, w3):
    factory_abi = fetch_abi('Factory')
    contract_abi = fetch_abi('CreateBO')

    factory_contract = w3.eth.contract(address=factory_address, abi=factory_abi)
    contracts = factory_contract.functions.getDeployedContracts().call()

    for contract in contracts:
        try:
            contract_instance = w3.eth.contract(address=contract, abi=contract_abi)

            asset = contract_instance.functions.ticker().call()
            asset = re.sub(r'[^A-Z]', '', str(asset).strip())

            price = int(contract_instance.functions.contractPrice().call()) / 1e18
            strike_price = int(contract_instance.functions.strikePrice().call())
            payout = int(contract_instance.functions.payout().call()) / 1e18
            position = int(contract_instance.functions.position().call())  # 0 = short, 1 = long

            # Determine if current user is buyer or seller
            buyer = contract_instance.functions.buyer().call()
            creator = contract_instance.functions.creator().call()
            if user_address != buyer and user_address != creator:
                continue  # Skip contracts not related to this user

            buy_side = (buyer == user_address)
            role = 'Buy' if buy_side else 'Sell'

            if role == 'Buy':
                position = 1 if position == 0 else 0

            # In-the-money evaluation
            if position == 0:
                in_the_money = get_price(asset) < strike_price
            else:
                in_the_money = get_price(asset) > strike_price
            in_the_money = 'In the Money' if in_the_money else 'Out of the Money'

            status = 'Bought' if contract_instance.functions.isBought().call() else 'Available'
            terminated = 'Expired' if contract_instance.functions.isExpired().call() else 'Active'

            # Winner logic
            if terminated == 'Expired':
                winner = contract_instance.functions.winner().call()
                winner = re.sub(r'[^A-Za-z]', '', str(winner).strip())
                winner = (
                    'Won' if (winner == 'Buyer' and buy_side) or (winner == 'Creator' and not buy_side)
                    else 'Lost'
                )
            else:
                winner = None

            # Convert all numeric fields to strings
            price = str(price)
            strike_price = str(strike_price)
            payout = str(payout)
            position = str(position)

            row_data = {
                'Contract Address': contract,
                'Asset': asset,
                'Price': price,
                'Strike Price': strike_price,
                'Payout': payout,
                'Position': position,
                'In the Money': in_the_money,
                'Status': status,
                'Terminated': terminated,
                'Buy or Sell Side': role,
                'Winner': winner
            }

            if contract in portfolio_data['Contract Address'].values:
                for key, value in row_data.items():
                    portfolio_data.loc[portfolio_data['Contract Address'] == contract, key] = value
            else:
                portfolio_data = pd.concat([portfolio_data, pd.DataFrame([row_data])], ignore_index=True)

        except Exception as e:
            print(f"[Portfolio] Error processing contract {contract}: {e}")
            continue

    return portfolio_data

def view_portfolio(portfolio_data):
    container = st.empty()

    with container.container():
        st.title('Portfolio')
        st.write('Your personal history of binary option contracts.')

        if portfolio_data.empty:
            st.info("No contracts found. Try refreshing.")
            return

        for idx, row in portfolio_data.iterrows():
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
                - **Side:** {row['Buy or Sell Side']}  
                - **Settlement:** {row['Winner'] if row['Winner'] else 'Pending'}
                """)

        st.divider()
        st.caption("Contracts are updated live on-chain. Refresh to see latest.")
