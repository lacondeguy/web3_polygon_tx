import json
import time
from web3 import Web3
import ccxt


def gwei_to_usd(gwei, gas_limit, ticker):
    exchange = ccxt.binance()
    current_ticker_details = exchange.fetch_ticker(ticker)
    ticker_price = current_ticker_details['close']
    price_in_usd = float(gwei * gas_limit) * 0.000000001 * ticker_price
    return price_in_usd
 
# Settings
receiver = ''
RPC = 'https://polygon-rpc.com'
privateKey = ''
value = '' # Value to send
    
# Checksum
web3 = Web3(Web3.HTTPProvider(RPC))
account = web3.eth.account.privateKeyToAccount(privateKey)
address_wallet = account.address
checksum_address = Web3.toChecksumAddress(address_wallet)
print('Wallet: ',address_wallet)

# Balance
balance = web3.eth.get_balance(checksum_address)
ether_balance = Web3.fromWei(balance, 'ether')
print('Balance: ', checksum_address)

# Gas price
gas_limit = web3.eth.estimate_gas({"from":sender,"to":receiver}, "latest" )
print('Gas limit: ',gas_limit)
gas_price = web3.eth.gas_price
gas_price_in_gwei = web3.fromWei(gas_price, 'gwei')
print('Gas price: ', gas_price_in_gwei, 'Gwei')
print('Gas price: ', round(gwei_to_usd(gas_price_in_gwei, gas_limit, 'MATIC/USDT'), 5), '$')


# Build the transaction
tx = {
    "nonce" : web3.eth.getTransactionCount(sender),
    "to": receiver,
    "value": web3.toWei(value, "ether"), 
    "gas": gas_limit,
    "gasPrice" : web3.eth.gas_price,
    "chainId" : web3.eth.chain_id,
}

# Sign and send tx
signed_tx = web3.eth.account.signTransaction(tx, privateKey)
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
print("Transaction hash: ", web3.toHex(tx_hash))
