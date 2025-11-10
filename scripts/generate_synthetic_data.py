import os, uuid, random, json
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()
DATA_DIR = os.getenv("DATA_DIR", "./data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
os.makedirs(RAW_DIR, exist_ok=True)


fake = Faker('id_ID')


MERCHANTS_API = ["Tokopedia", "Shopee", "Binance", "Alfamart", "GoPay", "OVO", "Bukalapak"]
MERCHANTS_DB = ["Indomaret", "Grab", "PLN", "PDAM", "Binance", "Pertamina"]
CITIES = ["Jakarta", "Bali", "Surabaya", "Medan", "Bandung", "Makassar"]


start_date = datetime.now() - timedelta(days=30)


# 1) Simulasi transaksi dari API (JSON)
api_rows = []
for _ in range(1200):
    ts = start_date + timedelta(seconds=random.randint(0, 30*24*3600))
    api_rows.append({
        "transaction_id": str(uuid.uuid4())[:12],
        "user_id": random.randint(1000, 2000),
        "amount": round(random.uniform(1e4, 1e8), 2),
        "currency": "IDR",
        "timestamp": ts.isoformat(),
        "merchant": random.choice(MERCHANTS_API),
        "status": random.choice(["completed", "failed", "pending"]),
        "location": random.choice(CITIES),
        "source": "API"
    })


with open(os.path.join(RAW_DIR, "api_transactions.json"), "w") as f:
    json.dump(api_rows, f, ensure_ascii=False, indent=2)


# 2) Simulasi transaksi dari DB (CSV)
db_rows = []
for _ in range(1000):
    ts = start_date + timedelta(seconds=random.randint(0, 30*24*3600))
    db_rows.append({
        "id": random.randint(10_000, 99_999),
        "user_id": random.randint(900, 2100),
        "account_number": str(random.randint(10**9, 10**10-1)),
        "amount": round(random.uniform(1e4, 5e7), 2),
        "transaction_type": random.choice(["debit", "credit"]),
        "date": ts.strftime("%Y-%m-%d %H:%M:%S"),
        "location": random.choice(CITIES)
    })


pd.DataFrame(db_rows).to_csv(os.path.join(RAW_DIR, "db_transactions.csv"), index=False)


print("✅ Synthetic datasets generated in", RAW_DIR)