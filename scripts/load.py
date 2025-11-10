import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import logging
import sys

# Add scripts directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import setup_logging

# Setup logging
logger = setup_logging()

load_dotenv()
POSTGRES_URI = os.getenv("POSTGRES_URI")
if not POSTGRES_URI:
    logger.error("POSTGRES_URI is required but not found in environment variables")
    raise ValueError("POSTGRES_URI is required")

try:
    engine = create_engine(POSTGRES_URI)
    logger.info("Database connection established")
except Exception as e:
    logger.error(f"Error connecting to database: {e}")
    raise

# Read processed data
try:
    data_file = os.path.join(os.getenv("DATA_DIR", "./data"), "processed", "cleaned_transactions.csv")
    logger.info(f"Reading processed data from {data_file}...")
    df = pd.read_csv(data_file)
    logger.info(f"Data loaded: {len(df)} rows")
except FileNotFoundError:
    logger.error(f"Processed data file not found: {data_file}")
    raise
except Exception as e:
    logger.error(f"Error reading processed data: {e}")
    raise

# Ensure table exists (idempotent if schema sudah dibuat)
try:
    logger.info("Creating table if not exists...")
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS fact_transactions (
          transaction_id     VARCHAR(64) PRIMARY KEY,
          user_id            BIGINT,
          account_number     VARCHAR(64),
          amount             NUMERIC(18,2) NOT NULL,
          currency           VARCHAR(8) DEFAULT 'IDR',
          merchant           VARCHAR(128),
          transaction_type   VARCHAR(32),
          status             VARCHAR(32),
          location           VARCHAR(64),
          event_time         TIMESTAMPTZ NOT NULL,
          source             VARCHAR(16),
          is_fraud           SMALLINT DEFAULT 0,
          fraud_reason       VARCHAR(256),
          ingestion_time     TIMESTAMPTZ DEFAULT NOW()
        );
        """))
    logger.info("Table creation/verification completed")
except Exception as e:
    logger.error(f"Error creating table: {e}")
    raise

# UPSERT using INSERT ... ON CONFLICT
cols = [
    "transaction_id","user_id","account_number","amount","currency","merchant",
    "transaction_type","status","location","event_time","source","is_fraud","fraud_reason"
]

# Validate DataFrame has required columns
missing_cols = [c for c in cols if c not in df.columns]
if missing_cols:
    error_msg = f"Missing required columns: {missing_cols}"
    logger.error(error_msg)
    raise ValueError(error_msg)
logger.info(f"DataFrame validation passed. Shape: {df.shape}")

# Filter hanya kolom yang diperlukan
df_load = df[cols].copy()

# Convert event_time ke datetime jika belum
if df_load["event_time"].dtype == "object":
    df_load["event_time"] = pd.to_datetime(df_load["event_time"])

# Convert is_fraud ke int jika belum
df_load["is_fraud"] = df_load["is_fraud"].astype(int)

# Handle NaN values untuk kolom yang bisa NULL (replace NaN dengan None untuk SQL)
for col in ["account_number", "merchant", "transaction_type", "status", "location", "fraud_reason"]:
    df_load[col] = df_load[col].where(pd.notna(df_load[col]), None)

placeholders = ",".join([f":{c}" for c in cols])
updates = ",".join([f"{c}=EXCLUDED.{c}" for c in cols if c != "transaction_id"])  # keep PK

insert_sql = text(f"""
    INSERT INTO fact_transactions ({','.join(cols)})
    VALUES ({placeholders})
    ON CONFLICT (transaction_id)
    DO UPDATE SET {updates};
""")

records = df_load.to_dict(orient="records")

# Load data to database
try:
    logger.info(f"Loading {len(records)} records to database...")
    with engine.begin() as conn:
        conn.execute(insert_sql, records)
    logger.info(f"✅ Load → fact_transactions (upserted {len(records)} rows)")
    print(f"✅ Load → fact_transactions (upserted {len(records)} rows)")
except Exception as e:
    logger.error(f"Error loading data to database: {e}")
    raise

