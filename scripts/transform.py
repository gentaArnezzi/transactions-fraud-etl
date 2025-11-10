import os, json
import pandas as pd
from dotenv import load_dotenv
import logging
import sys

# Add scripts directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import setup_logging
from data_quality import check_data_quality, validate_transaction_data

# Setup logging
logger = setup_logging()

load_dotenv()
DATA_DIR = os.getenv("DATA_DIR", "./data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROC_DIR = os.path.join(DATA_DIR, "processed")
os.makedirs(PROC_DIR, exist_ok=True)

logger.info("Starting Transform process...")

# Read API
try:
    logger.info("Reading API data...")
    with open(os.path.join(RAW_DIR, "api_extracted.json"), "r") as f:
        api = pd.DataFrame(json.load(f))
    logger.info(f"API data loaded: {len(api)} rows")
except FileNotFoundError:
    logger.error(f"API file not found: {os.path.join(RAW_DIR, 'api_extracted.json')}")
    raise
except Exception as e:
    logger.error(f"Error reading API data: {e}")
    raise

# Read DB
try:
    logger.info("Reading DB data...")
    db = pd.read_csv(os.path.join(RAW_DIR, "db_extracted.csv"))
    logger.info(f"DB data loaded: {len(db)} rows")
except FileNotFoundError:
    logger.error(f"DB file not found: {os.path.join(RAW_DIR, 'db_extracted.csv')}")
    raise
except Exception as e:
    logger.error(f"Error reading DB data: {e}")
    raise

# Normalize schema API
api_df = pd.DataFrame({
    "transaction_id": api.get("transaction_id"),
    "user_id": api.get("user_id"),
    "account_number": None,
    "amount": api.get("amount"),
    "currency": api.get("currency", "IDR"),
    "merchant": api.get("merchant"),
    "transaction_type": None,
    "status": api.get("status"),
    "location": api.get("location"),
    "event_time": pd.to_datetime(api.get("timestamp"), errors="coerce"),
    "source": "API"
})

# Normalize schema DB
db_df = pd.DataFrame({
    "transaction_id": db["id"].astype(str),
    "user_id": db["user_id"],
    "account_number": db["account_number"].astype(str),
    "amount": db["amount"],
    "currency": "IDR",
    "merchant": None,
    "transaction_type": db["transaction_type"],
    "status": None,
    "location": db["location"],
    "event_time": pd.to_datetime(db["date"], errors="coerce"),
    "source": "DB"
})

# Union (schema aligned)
all_df = pd.concat([api_df, db_df], ignore_index=True)

# Basic cleaning
all_df = all_df.dropna(subset=["event_time", "amount"])  # buang yang fatal
all_df["amount"] = all_df["amount"].astype(float).abs()
all_df = all_df.drop_duplicates(subset=["transaction_id"], keep="last")

# ---- Fraud rules (baseline) ----
all_df["is_fraud"] = 0
all_df["fraud_reason"] = None

# 1) Amount di atas 50 juta IDR
mask_high = all_df["amount"] > 50_000_000
all_df.loc[mask_high, ["is_fraud", "fraud_reason"]] = [1, "high_amount"]

# 2) Merchant crypto (API)
mask_crypto = all_df["merchant"].fillna("").str.contains(r"binance|crypto|kraken|okx", case=False, regex=True)
all_df.loc[mask_crypto, ["is_fraud", "fraud_reason"]] = [1, "crypto_merchant"]

# 3) Burst activity: >=5 transaksi per user per 10 menit
# Sort by user_id and event_time untuk memastikan monotonic per group
all_df_sorted = all_df.sort_values(["user_id", "event_time"]).copy()

# Set index event_time untuk rolling window (harus sorted per group)
all_df_indexed = all_df_sorted.set_index("event_time").copy()

# Hitung rolling count per user (10 menit window)
# Pastikan index sudah sorted per group sebelum rolling
burst = (all_df_indexed
         .groupby("user_id")["transaction_id"]
         .rolling("10min", closed="left")
         .count()
         .reset_index(name="tx_in_10m"))

# Merge kembali ke dataframe asli berdasarkan user_id dan event_time
all_df = all_df.merge(burst[["user_id", "event_time", "tx_in_10m"]], on=["user_id", "event_time"], how="left")
all_df["tx_in_10m"] = all_df["tx_in_10m"].fillna(0).astype(int)

# Flag burst activity (hanya jika belum di-flag sebagai fraud)
mask_burst = all_df["tx_in_10m"] >= 5
all_df.loc[mask_burst & (all_df["is_fraud"] == 0), ["is_fraud", "fraud_reason"]] = [1, "burst_activity"]

# Drop kolom helper sebelum output
all_df = all_df.drop(columns=["tx_in_10m"], errors="ignore")

# Data quality check
try:
    logger.info("Performing data quality checks...")
    quality_results = check_data_quality(all_df)
    logger.info(f"Data quality check completed: {quality_results['checks']}")
    
    # Validate transaction data
    validate_transaction_data(all_df)
    logger.info("Transaction data validation passed")
except Exception as e:
    logger.error(f"Data quality check failed: {e}")
    raise

# Output
try:
    OUT_FILE = os.path.join(PROC_DIR, "cleaned_transactions.csv")
    all_df.to_csv(OUT_FILE, index=False)
    logger.info(f"✅ Transform → {OUT_FILE} (rows={len(all_df)})")
    print("✅ Transform →", OUT_FILE, "rows=", len(all_df))
except Exception as e:
    logger.error(f"Error saving output file: {e}")
    raise

