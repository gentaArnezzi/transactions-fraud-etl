import os
import pandas as pd
from dotenv import load_dotenv


load_dotenv()
DATA_DIR = os.getenv("DATA_DIR", "./data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
CSV_FILE = os.path.join(RAW_DIR, "db_transactions.csv")
EXTRACTED_FILE = os.path.join(RAW_DIR, "db_extracted.csv")


# Mode A: pakai CSV (mock) — default
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    df.to_csv(EXTRACTED_FILE, index=False)
    print("✅ Extract DB (CSV mock) →", EXTRACTED_FILE)
else:
    # Mode B: contoh koneksi nyata ke MySQL
    import mysql.connector as mysql
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

    conn = mysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER,
                         password=MYSQL_PASSWORD, database=MYSQL_DATABASE)
    query = """
        SELECT id, user_id, account_number, amount, transaction_type, date, location
        FROM transactions
        WHERE date >= DATE_SUB(NOW(), INTERVAL 30 DAY);
    """
    df = pd.read_sql(query, conn)
    conn.close()
    df.to_csv(EXTRACTED_FILE, index=False)
    print("✅ Extract DB (MySQL) →", EXTRACTED_FILE)