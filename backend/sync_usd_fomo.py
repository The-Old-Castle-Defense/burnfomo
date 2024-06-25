from db import db
from config import config
from config import bot

import requests
import traceback
import os

import datetime
import time

from web3 import Web3
import json

config.init_config()
db.connect_to_database(path=config.connectionString)

# Initialize a Web3 instance
infura_url = "https://base.publicnode.com"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Check connection
if web3.is_connected():
    print("Connected to Ethereum node")
else:
    print("Connection failed")


burn_txs = list(db.db.txs.find({"type": "burn", "value_usd" : 0}))
for _x in burn_txs:
    block_timestamp = web3.eth.get_block(int(_x['height']))['timestamp']
    _date = datetime.datetime.fromtimestamp(block_timestamp).strftime("%d-%m-%Y")
    print(_date)
    try:
        price_usd = requests.get(f"https://api.coingecko.com/api/v3/coins/fomo-tocd/history?date={_date}").json()['market_data']['current_price']['usd']
    except Exception:
        traceback.print_exc()
        price_usd = 0

    value_usd = float(int(_x['value'])/1e18 * price_usd)
    db.db.txs.update_one({"_id": _x['_id']}, {"$set": {"value_usd": value_usd}})
    print(f"USD Value of #{_x['_id']} updated to {value_usd}")
    time.sleep(2)


