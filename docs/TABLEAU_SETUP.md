# 📊 Panduan Setup Tableau Dashboard untuk Financial ETL

## 🎯 Overview

Dashboard ini akan menampilkan:
- **Transaction Overview**: Total transaksi, jumlah fraud, fraud rate
- **Fraud Analysis**: Breakdown by reason, trend over time
- **Merchant Analysis**: Fraud rate per merchant
- **User Analysis**: Top users dengan fraud
- **Time Analysis**: Trend transaksi dan fraud over time

---

## 📋 Prerequisites

1. **Tableau Desktop** atau **Tableau Public** (gratis)
2. **PostgreSQL Database** sudah running
3. **Koneksi database** dari Tableau ke PostgreSQL

---

## 🔌 Step 1: Koneksi Tableau ke PostgreSQL

### 1.1. Buka Tableau Desktop/Public

### 1.2. Connect to Data
- Pilih **"PostgreSQL"** dari daftar connectors
- Atau pilih **"More Servers"** → **"PostgreSQL"**

### 1.3. Isi Koneksi Database

```
Server: localhost (atau 127.0.0.1)
Port: 5433
Database: etl_warehouse
Username: etl_user
Password: etl_pass
```

**Catatan**: 
- Jika menggunakan Docker, pastikan container running
- Port 5433 (bukan 5432) karena kita ubah di docker-compose.yml
- Jika menggunakan PostgreSQL lokal, sesuaikan dengan konfigurasi Anda

### 1.4. Test Connection
- Klik **"Sign In"** atau **"Test Connection"**
- Jika berhasil, Anda akan melihat daftar tables
- Pilih **"fact_transactions"** table

---

## 📊 Step 2: Query untuk Dashboard

### 2.1. Custom SQL Query (Opsional)

Jika ingin menggunakan custom query, buat **Custom SQL**:

```sql
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
    CASE 
        WHEN is_fraud = 1 THEN 'Fraud'
        ELSE 'Normal'
    END as transaction_status
FROM fact_transactions
```

### 2.2. Atau Langsung Gunakan Table

- Drag **"fact_transactions"** ke canvas
- Tableau akan load semua kolom
- Kita akan membuat calculated fields nanti di Tableau

---

## 📈 Step 3: Buat Calculated Fields

### 3.1. Transaction Status
```
IF [is_fraud] = 1 THEN "Fraud"
ELSE "Normal"
END
```
**Name**: `Transaction Status`

### 3.2. Fraud Reason (Clean)
```
IF [fraud_reason] = "high_amount" THEN "High Amount"
ELSEIF [fraud_reason] = "crypto_merchant" THEN "Crypto Merchant"
ELSEIF [fraud_reason] = "burst_activity" THEN "Burst Activity"
ELSE "No Fraud"
END
```
**Name**: `Fraud Reason Clean`

### 3.3. Transaction Date
```
DATE([event_time])
```
**Name**: `Transaction Date`

### 3.4. Transaction Hour
```
HOUR([event_time])
```
**Name**: `Transaction Hour`

### 3.5. Day of Week
```
DATENAME('weekday', [event_time])
```
**Name**: `Day of Week`

### 3.6. Amount in Millions
```
[amount] / 1000000
```
**Name**: `Amount (Millions)`

### 3.7. Fraud Rate
```
SUM(IF [is_fraud] = 1 THEN 1 ELSE 0 END) / COUNT([transaction_id]) * 100
```
**Name**: `Fraud Rate %`

---

## 🎨 Step 4: Buat Visualizations

### 4.1. **Dashboard 1: Overview Metrics**

#### Card 1: Total Transactions
- **Measure**: `COUNT([transaction_id])`
- **Format**: Number (0 decimal)
- **Label**: "Total Transactions"

#### Card 2: Fraud Transactions
- **Measure**: `SUM(IF [is_fraud] = 1 THEN 1 ELSE 0 END)`
- **Format**: Number (0 decimal)
- **Label**: "Fraud Transactions"

#### Card 3: Fraud Rate
- **Measure**: `SUM(IF [is_fraud] = 1 THEN 1 ELSE 0 END) / COUNT([transaction_id]) * 100`
- **Format**: Percentage (1 decimal)
- **Label**: "Fraud Rate"

#### Card 4: Total Amount
- **Measure**: `SUM([amount])`
- **Format**: Currency (IDR)
- **Label**: "Total Amount"

---

### 4.2. **Dashboard 2: Fraud Analysis**

#### Visualization 1: Fraud by Reason (Bar Chart)
- **Rows**: `Fraud Reason Clean`
- **Columns**: `COUNT([transaction_id])`
- **Color**: `Fraud Reason Clean`
- **Filter**: `Transaction Status` = "Fraud"

#### Visualization 2: Fraud Trend Over Time (Line Chart)
- **Rows**: `SUM(IF [is_fraud] = 1 THEN 1 ELSE 0 END)`
- **Columns**: `Transaction Date` (continuous, day)
- **Color**: `Transaction Status`
- **Show**: Dual axis dengan Total Transactions

#### Visualization 3: Fraud Rate by Merchant (Bar Chart)
- **Rows**: `merchant`
- **Columns**: `Fraud Rate %`
- **Sort**: Descending
- **Filter**: Top 10 merchants

---

### 4.3. **Dashboard 3: Transaction Analysis**

#### Visualization 1: Transactions Over Time (Line Chart)
- **Rows**: `COUNT([transaction_id])`
- **Columns**: `Transaction Date` (continuous, day)
- **Color**: `Transaction Status`

#### Visualization 2: Transactions by Hour (Bar Chart)
- **Rows**: `Transaction Hour`
- **Columns**: `COUNT([transaction_id])`
- **Color**: `Transaction Status`

#### Visualization 3: Transactions by Day of Week (Bar Chart)
- **Rows**: `Day of Week`
- **Columns**: `COUNT([transaction_id])`
- **Color**: `Transaction Status`

---

### 4.4. **Dashboard 4: Merchant Analysis**

#### Visualization 1: Top Merchants by Transaction Count
- **Rows**: `merchant`
- **Columns**: `COUNT([transaction_id])`
- **Sort**: Descending
- **Limit**: Top 10

#### Visualization 2: Fraud Rate by Merchant (Heatmap)
- **Rows**: `merchant`
- **Columns**: `Fraud Rate %`
- **Color**: `Fraud Rate %` (gradient)
- **Size**: `COUNT([transaction_id])`

#### Visualization 3: Amount by Merchant (Treemap)
- **Size**: `SUM([amount])`
- **Color**: `Fraud Rate %`
- **Label**: `merchant`

---

### 4.5. **Dashboard 5: User Analysis**

#### Visualization 1: Top Users with Fraud
- **Rows**: `user_id`
- **Columns**: `SUM(IF [is_fraud] = 1 THEN 1 ELSE 0 END)`
- **Sort**: Descending
- **Limit**: Top 10
- **Filter**: `Transaction Status` = "Fraud"

#### Visualization 2: User Transaction Distribution
- **Rows**: `COUNT(DISTINCT [user_id])`
- **Columns**: `COUNT([transaction_id])` (binned)
- **Show**: Histogram

---

## 🎯 Step 5: Buat Dashboard Layout

### 5.1. Create New Dashboard
- Klik **"New Dashboard"** di bottom tabs
- Set size: **"Desktop"** atau **"Fixed Size"** (1200x800)

### 5.2. Arrange Visualizations
- Drag visualizations dari sheets ke dashboard
- Arrange secara logical:
  - **Top**: Overview metrics (4 cards)
  - **Middle Left**: Fraud analysis
  - **Middle Right**: Transaction analysis
  - **Bottom**: Merchant and user analysis

### 5.3. Add Filters
- Drag `Transaction Status` ke filter area
- Drag `merchant` ke filter area
- Drag `Transaction Date` ke filter area
- Set filters sebagai **"Apply to All"**

### 5.4. Add Title and Description
- Add title: **"Financial Transactions Fraud Detection Dashboard"**
- Add description: **"Real-time monitoring of financial transactions and fraud detection"**

---

## 🔍 Step 6: Advanced Features

### 6.1. Parameters

#### Parameter 1: Fraud Threshold
- **Data Type**: Float
- **Current Value**: 50000000
- **Allowable Values**: Range (0 to 100000000)
- **Use**: Filter transactions above threshold

#### Parameter 2: Date Range
- **Data Type**: Date
- **Current Value**: Last 30 days
- **Use**: Filter transactions by date range

### 6.2. Actions

#### Filter Action
- **Source**: Merchant chart
- **Target**: All sheets
- **Action**: Filter
- **Effect**: Click merchant → filter all visualizations

#### Highlight Action
- **Source**: Transaction Status
- **Target**: All sheets
- **Action**: Highlight
- **Effect**: Highlight fraud transactions across all charts

---

## 📊 Step 7: Export dan Share

### 7.1. Export Dashboard
- **File** → **Export** → **Packaged Workbook**
- Save as `.twbx` file
- File ini bisa dibuka di Tableau Reader (gratis)

### 7.2. Publish to Tableau Public (Gratis)
- **Server** → **Tableau Public** → **Save to Tableau Public**
- Login dengan Tableau Public account
- Dashboard akan terpublish online (public)

### 7.3. Export as Image/PDF
- **Worksheet** → **Export** → **Image** atau **PDF**
- Useful untuk dokumentasi atau presentasi

---

## 🎨 Tips untuk Dashboard yang Menarik

### 1. **Color Scheme**
- Use consistent colors:
  - **Fraud**: Red (#FF6B6B)
  - **Normal**: Green (#51CF66)
  - **Warning**: Orange (#FFA726)

### 2. **Layout**
- Use grid layout untuk alignment
- Leave whitespace untuk readability
- Group related visualizations

### 3. **Interactivity**
- Add tooltips dengan informasi detail
- Add filters untuk user exploration
- Add actions untuk cross-filtering

### 4. **Performance**
- Use extracts jika data besar
- Limit data dengan filters
- Use aggregation untuk large datasets

---

## 🐛 Troubleshooting

### Problem: Cannot connect to PostgreSQL
**Solution**:
- Pastikan Docker container running: `docker ps | grep postgres`
- Pastikan port 5433 accessible
- Check firewall settings
- Try connection dengan psql terlebih dahulu

### Problem: Data tidak muncul
**Solution**:
- Refresh data source
- Check query syntax
- Verify table name: `fact_transactions`
- Check data di PostgreSQL: `SELECT COUNT(*) FROM fact_transactions;`

### Problem: Slow performance
**Solution**:
- Create extract (File → Extract Data)
- Use filters untuk limit data
- Aggregate data di database level
- Use indexes di PostgreSQL

---

## 📝 Query SQL untuk Tableau

### Query 1: Daily Summary
```sql
SELECT 
    DATE(event_time) as transaction_date,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount
FROM fact_transactions
GROUP BY DATE(event_time)
ORDER BY transaction_date;
```

### Query 2: Merchant Summary
```sql
SELECT 
    merchant,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
    ROUND(100.0 * SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as fraud_rate,
    SUM(amount) as total_amount
FROM fact_transactions
WHERE merchant IS NOT NULL
GROUP BY merchant
ORDER BY fraud_rate DESC;
```

### Query 3: User Summary
```sql
SELECT 
    user_id,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
    SUM(amount) as total_amount
FROM fact_transactions
GROUP BY user_id
HAVING SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) > 0
ORDER BY fraud_count DESC
LIMIT 20;
```

---

## ✅ Checklist Dashboard

- [ ] Koneksi ke PostgreSQL berhasil
- [ ] Data fact_transactions loaded
- [ ] Calculated fields dibuat
- [ ] Overview metrics (4 cards)
- [ ] Fraud analysis charts
- [ ] Transaction analysis charts
- [ ] Merchant analysis charts
- [ ] User analysis charts
- [ ] Filters added
- [ ] Dashboard layout arranged
- [ ] Colors dan styling applied
- [ ] Tooltips added
- [ ] Dashboard exported/shared

---

## 🚀 Next Steps

1. **Add more visualizations**: Geographic analysis, time series forecasting
2. **Add alerts**: Set thresholds untuk fraud rate
3. **Add drill-down**: Detail view untuk specific transactions
4. **Add comparisons**: Compare current period dengan previous period
5. **Add predictions**: Use Tableau's forecasting features

---

**Selamat! Dashboard Tableau Anda siap! 🎉**

