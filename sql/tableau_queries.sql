-- SQL Queries untuk Tableau Dashboard
-- File ini berisi query-query yang berguna untuk visualisasi di Tableau

-- ============================================
-- 1. DAILY SUMMARY
-- ============================================
-- Menampilkan summary transaksi per hari
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

-- ============================================
-- 2. MERCHANT SUMMARY
-- ============================================
-- Menampilkan summary transaksi per merchant
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

-- ============================================
-- 3. USER SUMMARY
-- ============================================
-- Menampilkan summary transaksi per user
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
LIMIT 50;

-- ============================================
-- 4. FRAUD BY REASON
-- ============================================
-- Breakdown fraud berdasarkan reason
SELECT 
    COALESCE(fraud_reason, 'no_fraud') as fraud_reason,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount
FROM fact_transactions
WHERE is_fraud = 1
GROUP BY fraud_reason
ORDER BY transaction_count DESC;

-- ============================================
-- 5. HOURLY SUMMARY
-- ============================================
-- Menampilkan transaksi per jam
SELECT 
    EXTRACT(HOUR FROM event_time) as transaction_hour,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
    ROUND(100.0 * SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as fraud_rate_pct
FROM fact_transactions
GROUP BY EXTRACT(HOUR FROM event_time)
ORDER BY transaction_hour;

-- ============================================
-- 6. DAY OF WEEK SUMMARY
-- ============================================
-- Menampilkan transaksi per hari dalam seminggu
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

-- ============================================
-- 7. LOCATION SUMMARY
-- ============================================
-- Menampilkan transaksi per location
SELECT 
    COALESCE(location, '(unknown)') as location,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
    ROUND(100.0 * SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) as fraud_rate_pct,
    SUM(amount) as total_amount
FROM fact_transactions
GROUP BY location
ORDER BY fraud_rate_pct DESC NULLS LAST;

-- ============================================
-- 8. SOURCE SUMMARY (API vs DB)
-- ============================================
-- Menampilkan perbandingan transaksi dari API vs DB
SELECT 
    source,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
    ROUND(100.0 * SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as fraud_rate_pct,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount
FROM fact_transactions
GROUP BY source
ORDER BY source;

-- ============================================
-- 9. AMOUNT DISTRIBUTION
-- ============================================
-- Menampilkan distribusi amount untuk fraud vs normal
SELECT 
    CASE WHEN is_fraud = 1 THEN 'Fraud' ELSE 'Normal' END as transaction_type,
    COUNT(*) as transaction_count,
    MIN(amount) as min_amount,
    MAX(amount) as max_amount,
    AVG(amount) as avg_amount,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) as median_amount,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY amount) as q1_amount,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY amount) as q3_amount
FROM fact_transactions
GROUP BY transaction_type;

-- ============================================
-- 10. TOP FRAUD TRANSACTIONS
-- ============================================
-- Menampilkan top fraud transactions
SELECT 
    transaction_id,
    user_id,
    merchant,
    amount,
    fraud_reason,
    event_time,
    location
FROM fact_transactions
WHERE is_fraud = 1
ORDER BY amount DESC
LIMIT 50;

-- ============================================
-- 11. TRANSACTION STATUS SUMMARY
-- ============================================
-- Menampilkan transaksi berdasarkan status (jika ada)
SELECT 
    COALESCE(status, '(unknown)') as status,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
    ROUND(100.0 * SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) as fraud_rate_pct
FROM fact_transactions
GROUP BY status
ORDER BY fraud_rate_pct DESC NULLS LAST;

-- ============================================
-- 12. MONTHLY TREND
-- ============================================
-- Menampilkan trend bulanan
SELECT 
    DATE_TRUNC('month', event_time) as month,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
    ROUND(100.0 * SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as fraud_rate_pct,
    SUM(amount) as total_amount
FROM fact_transactions
GROUP BY DATE_TRUNC('month', event_time)
ORDER BY month;

-- ============================================
-- 13. MERCHANT FRAUD RATE (Top 20)
-- ============================================
-- Top 20 merchants dengan fraud rate tertinggi
SELECT 
    merchant,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
    ROUND(100.0 * SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) as fraud_rate_pct
FROM fact_transactions
WHERE merchant IS NOT NULL
GROUP BY merchant
HAVING COUNT(*) >= 10  -- Minimum 10 transactions
ORDER BY fraud_rate_pct DESC
LIMIT 20;

-- ============================================
-- 14. TIME SERIES FOR FRAUD DETECTION
-- ============================================
-- Data time series untuk line chart
SELECT 
    event_time,
    COUNT(*) as transaction_count,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
    SUM(amount) as total_amount
FROM fact_transactions
GROUP BY event_time
ORDER BY event_time;

-- ============================================
-- 15. COMPLETE VIEW (untuk Tableau)
-- ============================================
-- View lengkap dengan calculated fields untuk Tableau
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
    -- Calculated fields
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
FROM fact_transactions;

