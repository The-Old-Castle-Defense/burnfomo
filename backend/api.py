from db import db
from config import config
from config import bot

from fastapi import FastAPI
from pymongo import MongoClient
import datetime 



async def _lifespan(app):
  import asyncio
  try:
    yield
  except asyncio.exceptions.CancelledError:
    pass

app = FastAPI(
    title="BURN $FOMO - The Old Castle Defense API V1.0.0",
    #root_path="/api/",
    openapi_url="/api/openapi.json",
    redoc_url="/api/redoc",
    docs_url="/api/docs",
)

# MongoDB setup
config.init_config()
db.connect_to_database(path=config.connectionString)

# Helper function to fetch and calculate statistics
def fetch_and_calculate_statistics():
    latest_stats = db.db.data.find().sort("timestamp", -1).limit(1)[0]
    total_fomo_supply_reduced = float(latest_stats["total_supply_reduced"])

    # Calculate the circulating supply over time
    chart_data = []
    circulating_supply = int(float(latest_stats['total_supply']))
    burn_transactions = db.db.txs.find({"type": "burn"}).sort("timestamp", 1)
    for tx in burn_transactions:
        burn_amount = int(tx["value"])
        circulating_supply -= burn_amount
        chart_data.append({
            "date": datetime.datetime.fromtimestamp(tx["timestamp"]).isoformat(),
            "circulating_supply": str(circulating_supply)
        })

    # Fetch and process top wallets manually
    raw_top_wallets = list(db.db.txs.find({"type": "burn"}))
    wallets = {}
    for tx in raw_top_wallets:
        from_address = tx["from_address"]
        wallets.setdefault(from_address, {"totals": 0, "count": 0})
        value = int(tx["value"])
        value_usd = int(tx.get('value_usd', 0))
        wallets[from_address]['totals'] += value
        wallets[from_address]['count'] += 1

    top_wallets = sorted(wallets.items(), key=lambda x: x[1]['totals'], reverse=True)[:5]
    top_wallets = [{"_id": k, "total_burned": str(v["totals"]), "burn_count": v["count"]} for k, v in top_wallets]

    burn_details = []
    for tx in db.db.txs.find({"type": "burn"}).sort("height", -1).limit(50):
        burn_details.append({
            "tokens_burned": str(tx["value"]),
            "tokens_burned_usd": str(tx["value_usd"]),
            "transaction_details": tx["tx_hash"],
            "burn_triggered_by": tx["from_address"],
            "height": tx["height"],
            "timestamp": tx['timestamp'],
        })

    biggest_burn = max(db.db.txs.find({"type": "burn"}), key=lambda x: int(x["value"]))
    biggest_burn_amount = int(biggest_burn["value"])
    biggest_burn_date = biggest_burn["created_at"]

    total_burns = db.db.txs.count_documents({"type": "burn"})
    burned_supply = sum(int(tx["value"]) for tx in db.db.txs.find({"type": "burn"}))
    average_burn_size = burned_supply / total_burns

    statistics = {
        "total_fomo_supply_reduced": str(total_fomo_supply_reduced),
        "fomo_total_supply_chart": chart_data,
        "top_5_burn_triggered_by_wallets": top_wallets,
        "burn_details": burn_details,
        "burn_statistics": {
            "biggest_burn": {
                "amount": str(biggest_burn_amount),
                "date": biggest_burn_date
            },
            "burns_to_date": str(total_burns),
            "average_burn_size": str(average_burn_size)
        }
    }
    
    return statistics


@app.get("/api/burn_statistics")
def burn_statistics():
    # Check cache for existing data
    cache = db.db.cache.find_one({"name": "burn_statistics"})
    now = datetime.datetime.utcnow()

    if cache and (now - cache["last_updated"] < datetime.timedelta(minutes=10)):
        return cache["data"]

    # Fetch and calculate statistics
    statistics = fetch_and_calculate_statistics()

    # Update cache
    db.db.cache.update_one(
        {"name": "burn_statistics"},
        {"$set": {"data": statistics, "last_updated": now}},
        upsert=True
    )

    return statistics

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.config['port'])



