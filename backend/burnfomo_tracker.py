from db import db
from config import config
from config import bot

import requests
import traceback
import os

import datetime

from web3 import Web3
import json

config.init_config()
secret_key = config.config['secret_key']
os.environ.setdefault("SECRET_KEY", str(secret_key))
db.connect_to_database(path=config.connectionString)

# Initialize a Web3 instance
infura_url = "https://base.publicnode.com"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Check connection
if web3.is_connected():
    print("Connected to Ethereum node")
else:
    print("Connection failed")

# Token contract address
token_contract_address = "0xa7ea9d5d4d4c7cF7dbde5871E6D108603C6942a5"
# ABI for ERC20 token (minimal)
token_abi = json.loads('[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}]')
token_contract = web3.eth.contract(address=token_contract_address, abi=token_abi)


# ERC20 Transfer event signature
transfer_event_signature = web3.keccak(text="Transfer(address,address,uint256)").hex()

# Zero addresses
zero_address1 = "0x000000000000000000000000000000000000dEaD"
zero_address2 = "0x0000000000000000000000000000000000000000"
non_circulating_address = "0xa57B2d1F1059C6CDa44C49F72B8e2c4f323f6DF1"


# Define the filter for the Transfer event
event_filter = {
    "address": token_contract_address,
    "topics": [transfer_event_signature]
}

# Function to decode event logs
def decode_transfer_event(log):
    topics = log['topics']
    data = log['data']
    from_address = web3.to_checksum_address('0x' + topics[1].hex()[-40:])
    to_address = web3.to_checksum_address('0x' + topics[2].hex()[-40:])
    value = int(data.hex(), 16)
    return from_address, to_address, value

# Function to filter and process burn transactions
def process_burn_transactions(logs):
    for log in logs:
        from_address, to_address, value = decode_transfer_event(log)
        if to_address.lower() in [zero_address1.lower(), zero_address2.lower()]:
            tx_hash = log['transactionHash'].hex()
            is_exist = db.db.txs.find_one({"_id": tx_hash})
            block_timestamp = web3.eth.get_block(log['blockNumber'])['timestamp']
            _date = datetime.datetime.fromtimestamp(block_timestamp).strftime("%d-%m-%Y")
            try:
                print(_date)
                price_usd = requests.get(f"https://api.coingecko.com/api/v3/coins/fomo-tocd/history?date={_date}").json()['market_data']['current_price']['usd']
            except Exception:
                traceback.print_exc()
                price_usd = 0

            if is_exist:
                continue
            print(log)
            print(f"Tx Hash: {log['transactionHash'].hex()}")
            print(f"From: {from_address}, To: {to_address}, Value: {value}")
            print("--------------------------------------------------")
            db.db.txs.insert_one({
                "_id": tx_hash,
                "tx_hash": tx_hash,
                "from_address": from_address,
                "to_address": to_address,
                "value": str(value),
                "value_usd": float(int(value)/1e18 * price_usd),
                "type": "burn",
                "created_at": datetime.datetime.utcnow(),
                "height": str(log['blockNumber']),
                "timestamp": web3.eth.get_block(log['blockNumber'])['timestamp']
            })


# Function to get logs in batches
def get_logs_in_batches(start_block, end_block, batch_size):
    for i in range(start_block, end_block, batch_size):
        batch_end_block = min(i + batch_size - 1, end_block)
        print(f"Fetching logs from block {i} to {batch_end_block}...")
        event_filter["fromBlock"] = i
        event_filter["toBlock"] = batch_end_block
        logs = web3.eth.get_logs(event_filter)
        process_burn_transactions(logs)

        db.db.config.update_one({"name": "last_processed_block"}, {"$set": {"value": batch_end_block}}, upsert=True)

def get_token_balance(address):
    return token_contract.functions.balanceOf(address).call()

def calculate_statistics():
    total_supply = 100_000_000 * 1e18
    burned_supply = sum(int(tx["value"]) for tx in list(db.db.txs.find({"type": "burn"})))

    non_circulating_balance = get_token_balance(non_circulating_address) + get_token_balance(zero_address1) + get_token_balance(zero_address2)
    
    circulating_supply = total_supply - non_circulating_balance
    
    stats = {
        "total_supply_reduced": burned_supply / total_supply * 100,
        "circulating_supply": str(circulating_supply),
        "total_supply": str(total_supply),
        "burned_supply": str(burned_supply),
        "timestamp": web3.eth.get_block('latest')['timestamp']
    }
    
    print(f"Total Supply by: {total_supply}")
    print(f"Total Burned by: {stats['burned_supply']}")
    print(f"Total Supply Reduced by: {stats['total_supply_reduced']:.2f}%")
    print(f"Circulating Supply: {stats['circulating_supply']}")

    # Save statistics to MongoDB
    db.db.data.update_one(
        {"_id": "fomo_stats"},
        {"$set": stats},
        upsert=True
    )


if __name__ == "__main__":
    # Get the last processed block from the config collection
    config = db.db.config.find_one({"name": "last_processed_block"})
    start_block = config["value"] + 1 if config else 13650157 # Adjust start block as needed
    end_block = web3.eth.block_number  # Current block
    batch_size = 50000  # Number of blocks to process in each batch

    get_logs_in_batches(start_block, end_block, batch_size)
    calculate_statistics()
