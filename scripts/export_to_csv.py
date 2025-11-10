"""
Script untuk export data dari PostgreSQL ke CSV untuk Tableau Public
Tableau Public tidak bisa connect langsung ke database, jadi perlu export ke CSV
"""

import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def export_data():
    """Export data dari PostgreSQL ke CSV files"""
    
    # Connect to database
    postgres_uri = os.getenv("POSTGRES_URI")
    if not postgres_uri:
        print("❌ POSTGRES_URI not found in .env file")
        return
    
    engine = create_engine(postgres_uri)
    output_dir = os.path.join(os.getenv("DATA_DIR", "./data"), "tableau")
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("Exporting data to CSV for Tableau Public")
    print("=" * 60)
    
    # 1. Export full fact_transactions dengan calculated fields
    print("\n1. Exporting fact_transactions (full data)...")
    query_full = """
    SELECT 
        transaction_id,
        user_id,
        account_number,
        amount,
        currency,
        merchant,
        transaction_type,
        status,
        location,
        event_time,
        source,
        is_fraud,
        fraud_reason,
        ingestion_time,
        -- Calculated fields untuk Tableau
        DATE(event_time) as transaction_date,
        EXTRACT(HOUR FROM event_time) as transaction_hour,
        EXTRACT(DOW FROM event_time) as day_of_week,
        EXTRACT(MONTH FROM event_time) as transaction_month,
        EXTRACT(YEAR FROM event_time) as transaction_year,
        CASE 
            WHEN is_fraud = 1 THEN 'Fraud'
            ELSE 'Normal'
        END as transaction_status,
        CASE 
            WHEN fraud_reason = 'high_amount' THEN 'High Amount'
            WHEN fraud_reason = 'crypto_merchant' THEN 'Crypto Merchant'
            WHEN fraud_reason = 'burst_activity' THEN 'Burst Activity'
            ELSE 'No Fraud'
        END as fraud_reason_clean,
        CASE 
            WHEN amount > 50000000 THEN 'High Amount'
            WHEN amount > 10000000 THEN 'Medium Amount'
            ELSE 'Low Amount'
        END as amount_category
    FROM fact_transactions
    ORDER BY event_time;
    """
    
    df_full = pd.read_sql(query_full, engine)
    output_file = os.path.join(output_dir, "fact_transactions.csv")
    df_full.to_csv(output_file, index=False)
    print(f"   ✅ Exported {len(df_full):,} rows to {output_file}")
    
    # 2. Export daily summary
    print("\n2. Exporting daily summary...")
    query_daily = """
    SELECT 
        DATE(event_time) as transaction_date,
        COUNT(*) as total_transactions,
        SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
        ROUND(100.0 * SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as fraud_rate_pct,
        SUM(amount) as total_amount,
        AVG(amount) as avg_amount,
        MIN(amount) as min_amount,
        MAX(amount) as max_amount
    FROM fact_transactions
    GROUP BY DATE(event_time)
    ORDER BY transaction_date;
    """
    
    df_daily = pd.read_sql(query_daily, engine)
    output_file = os.path.join(output_dir, "daily_summary.csv")
    df_daily.to_csv(output_file, index=False)
    print(f"   ✅ Exported {len(df_daily):,} rows to {output_file}")
    
    # 3. Export merchant summary
    print("\n3. Exporting merchant summary...")
    query_merchant = """
    SELECT 
        COALESCE(merchant, '(unknown)') as merchant,
        COUNT(*) as total_transactions,
        SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
        ROUND(100.0 * SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) as fraud_rate_pct,
        SUM(amount) as total_amount,
        AVG(amount) as avg_amount
    FROM fact_transactions
    GROUP BY merchant
    ORDER BY fraud_rate_pct DESC NULLS LAST;
    """
    
    df_merchant = pd.read_sql(query_merchant, engine)
    output_file = os.path.join(output_dir, "merchant_summary.csv")
    df_merchant.to_csv(output_file, index=False)
    print(f"   ✅ Exported {len(df_merchant):,} rows to {output_file}")
    
    # 4. Export user summary
    print("\n4. Exporting user summary...")
    query_user = """
    SELECT 
        user_id,
        COUNT(*) as total_transactions,
        SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
        ROUND(100.0 * SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as fraud_rate_pct,
        SUM(amount) as total_amount,
        AVG(amount) as avg_amount
    FROM fact_transactions
    GROUP BY user_id
    HAVING SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) > 0
    ORDER BY fraud_count DESC
    LIMIT 100;
    """
    
    df_user = pd.read_sql(query_user, engine)
    output_file = os.path.join(output_dir, "user_summary.csv")
    df_user.to_csv(output_file, index=False)
    print(f"   ✅ Exported {len(df_user):,} rows to {output_file}")
    
    # 5. Export fraud by reason
    print("\n5. Exporting fraud by reason...")
    query_fraud_reason = """
    SELECT 
        COALESCE(fraud_reason, 'no_fraud') as fraud_reason,
        CASE 
            WHEN fraud_reason = 'high_amount' THEN 'High Amount'
            WHEN fraud_reason = 'crypto_merchant' THEN 'Crypto Merchant'
            WHEN fraud_reason = 'burst_activity' THEN 'Burst Activity'
            ELSE 'No Fraud'
        END as fraud_reason_clean,
        COUNT(*) as transaction_count,
        SUM(amount) as total_amount,
        AVG(amount) as avg_amount
    FROM fact_transactions
    WHERE is_fraud = 1
    GROUP BY fraud_reason
    ORDER BY transaction_count DESC;
    """
    
    df_fraud_reason = pd.read_sql(query_fraud_reason, engine)
    output_file = os.path.join(output_dir, "fraud_by_reason.csv")
    df_fraud_reason.to_csv(output_file, index=False)
    print(f"   ✅ Exported {len(df_fraud_reason):,} rows to {output_file}")
    
    # 6. Export hourly summary
    print("\n6. Exporting hourly summary...")
    query_hourly = """
    SELECT 
        EXTRACT(HOUR FROM event_time) as transaction_hour,
        COUNT(*) as total_transactions,
        SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
        ROUND(100.0 * SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as fraud_rate_pct
    FROM fact_transactions
    GROUP BY EXTRACT(HOUR FROM event_time)
    ORDER BY transaction_hour;
    """
    
    df_hourly = pd.read_sql(query_hourly, engine)
    output_file = os.path.join(output_dir, "hourly_summary.csv")
    df_hourly.to_csv(output_file, index=False)
    print(f"   ✅ Exported {len(df_hourly):,} rows to {output_file}")
    
    # 7. Export day of week summary
    print("\n7. Exporting day of week summary...")
    query_dow = """
    SELECT 
        EXTRACT(DOW FROM event_time) as day_of_week,
        CASE EXTRACT(DOW FROM event_time)
            WHEN 0 THEN 'Sunday'
            WHEN 1 THEN 'Monday'
            WHEN 2 THEN 'Tuesday'
            WHEN 3 THEN 'Wednesday'
            WHEN 4 THEN 'Thursday'
            WHEN 5 THEN 'Friday'
            WHEN 6 THEN 'Saturday'
        END as day_name,
        COUNT(*) as total_transactions,
        SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
        ROUND(100.0 * SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as fraud_rate_pct
    FROM fact_transactions
    GROUP BY EXTRACT(DOW FROM event_time)
    ORDER BY day_of_week;
    """
    
    df_dow = pd.read_sql(query_dow, engine)
    output_file = os.path.join(output_dir, "day_of_week_summary.csv")
    df_dow.to_csv(output_file, index=False)
    print(f"   ✅ Exported {len(df_dow):,} rows to {output_file}")
    
    # 8. Export location summary
    print("\n8. Exporting location summary...")
    query_location = """
    SELECT 
        COALESCE(location, '(unknown)') as location,
        COUNT(*) as total_transactions,
        SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
        ROUND(100.0 * SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) as fraud_rate_pct,
        SUM(amount) as total_amount
    FROM fact_transactions
    GROUP BY location
    ORDER BY fraud_rate_pct DESC NULLS LAST;
    """
    
    df_location = pd.read_sql(query_location, engine)
    output_file = os.path.join(output_dir, "location_summary.csv")
    df_location.to_csv(output_file, index=False)
    print(f"   ✅ Exported {len(df_location):,} rows to {output_file}")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Export completed!")
    print("=" * 60)
    print(f"\n📁 Files exported to: {output_dir}")
    print("\n📊 Files created:")
    print("   1. fact_transactions.csv - Full transaction data (for detailed analysis)")
    print("   2. daily_summary.csv - Daily aggregated data (for time series)")
    print("   3. merchant_summary.csv - Merchant aggregated data (for merchant analysis)")
    print("   4. user_summary.csv - User aggregated data (for user analysis)")
    print("   5. fraud_by_reason.csv - Fraud breakdown by reason")
    print("   6. hourly_summary.csv - Hourly aggregated data")
    print("   7. day_of_week_summary.csv - Day of week aggregated data")
    print("   8. location_summary.csv - Location aggregated data")
    print("\n💡 Tip: Use 'fact_transactions.csv' as main data source in Tableau Public")
    print("=" * 60)

if __name__ == "__main__":
    export_data()

