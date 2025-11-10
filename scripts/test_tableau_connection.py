"""
Script untuk test koneksi Tableau ke PostgreSQL
Jalankan script ini sebelum connect Tableau untuk memastikan database accessible
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    """Test koneksi ke PostgreSQL database"""
    try:
        # Parse POSTGRES_URI
        postgres_uri = os.getenv("POSTGRES_URI", "")
        
        # Extract connection details
        # Format: postgresql+psycopg2://user:pass@host:port/database
        if not postgres_uri:
            print("❌ POSTGRES_URI not found in .env file")
            return False
        
        # Remove postgresql+psycopg2:// prefix
        conn_str = postgres_uri.replace("postgresql+psycopg2://", "")
        
        # Parse connection string
        if "@" in conn_str:
            auth, host_db = conn_str.split("@")
            user, password = auth.split(":")
            host_port, database = host_db.split("/")
            if ":" in host_port:
                host, port = host_port.split(":")
            else:
                host = host_port
                port = "5432"
        else:
            print("❌ Invalid POSTGRES_URI format")
            return False
        
        print(f"🔌 Connecting to PostgreSQL...")
        print(f"   Host: {host}")
        print(f"   Port: {port}")
        print(f"   Database: {database}")
        print(f"   User: {user}")
        
        # Connect to database
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM fact_transactions;")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM fact_transactions WHERE is_fraud = 1;")
        fraud = cursor.fetchone()[0]
        
        cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'fact_transactions' ORDER BY ordinal_position;")
        columns = cursor.fetchall()
        
        print(f"\n✅ Connection successful!")
        print(f"\n📊 Database Info:")
        print(f"   Total transactions: {total:,}")
        print(f"   Fraud transactions: {fraud:,}")
        print(f"   Fraud rate: {(fraud/total*100):.2f}%")
        
        print(f"\n📋 Table Columns:")
        for col_name, col_type in columns:
            print(f"   - {col_name}: {col_type}")
        
        # Close connection
        cursor.close()
        conn.close()
        
        print(f"\n✅ Database is ready for Tableau connection!")
        print(f"\n📝 Tableau Connection Settings:")
        print(f"   Server: {host}")
        print(f"   Port: {port}")
        print(f"   Database: {database}")
        print(f"   Username: {user}")
        print(f"   Password: {password}")
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Database connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Tableau Connection Test")
    print("=" * 60)
    test_connection()
    print("=" * 60)

