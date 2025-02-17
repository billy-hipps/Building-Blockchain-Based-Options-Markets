import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"

st.title("🪙 Binary Option Token Dashboard")

# Fetch Token Info
st.sidebar.header("🔍 Token Info")
if st.sidebar.button("Get Token Info"):
    res = requests.get(f"{API_URL}/token-info").json()
    st.sidebar.write(f"**Name:** {res['name']}")
    st.sidebar.write(f"**Symbol:** {res['symbol']}")
    st.sidebar.write(f"**Total Supply:** {res['total_supply']}")

# Check Balance
st.header("🔹 Check Balance")
user_address = st.text_input("Enter your wallet address")
if st.button("Get Balance"):
    res = requests.get(f"{API_URL}/balance?address={user_address}").json()
    st.write(f"💰 Balance: {res['balance']} tokens")

# Transfer Tokens
st.header("💸 Transfer Tokens")
sender = st.text_input("Sender Address", key="sender")
recipient = st.text_input("Recipient Address", key="recipient")
amount = st.number_input("Amount", min_value=1, step=1)
if st.button("Send Transaction"):
    payload = {"sender": sender, "recipient": recipient, "amount": amount}
    res = requests.post(f"{API_URL}/transfer", json=payload).json()
    st.write(f"✅ Transaction Sent! Tx Hash: {res['tx_hash']}")

