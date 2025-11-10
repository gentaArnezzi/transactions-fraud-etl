# 🚀 Tableau Quick Start Guide

## ⚡ Quick Setup (5 Menit)

### Step 1: Pastikan Database Running
```bash
# Cek Docker container
docker ps | grep postgres

# Jika tidak running, start container
docker compose up -d postgres

# Test connection
python scripts/test_tableau_connection.py
```

### Step 2: Buka Tableau
1. Buka **Tableau Desktop** atau **Tableau Public** (gratis)
2. Klik **"Connect to Data"**

### Step 3: Connect to PostgreSQL
1. Pilih **"PostgreSQL"** dari daftar
2. Isi connection details:
   ```
   Server: 127.0.0.1
   Port: 5433
   Database: etl_warehouse
   Username: etl_user
   Password: etl_pass
   ```
3. Klik **"Sign In"**

### Step 4: Load Data
1. Pilih schema: **"public"**
2. Drag **"fact_transactions"** ke canvas
3. Klik **"Sheet 1"** untuk mulai membuat visualization

---

## 📊 Visualizations yang Disarankan

### 1. Overview Dashboard (4 Cards)
```
Card 1: Total Transactions
- Measure: COUNT([transaction_id])
- Format: Number

Card 2: Fraud Transactions  
- Measure: SUM(IF [is_fraud] = 1 THEN 1 ELSE 0 END)
- Format: Number

Card 3: Fraud Rate
- Measure: SUM(IF [is_fraud] = 1 THEN 1 ELSE 0 END) / COUNT([transaction_id]) * 100
- Format: Percentage

Card 4: Total Amount
- Measure: SUM([amount])
- Format: Currency (IDR)
```

### 2. Fraud by Reason (Bar Chart)
```
Rows: [fraud_reason]
Columns: COUNT([transaction_id])
Color: [fraud_reason]
Filter: [is_fraud] = 1
```

### 3. Fraud Trend (Line Chart)
```
Rows: SUM(IF [is_fraud] = 1 THEN 1 ELSE 0 END)
Columns: DATE([event_time])
Color: [is_fraud]
```

### 4. Merchant Analysis (Bar Chart)
```
Rows: [merchant]
Columns: SUM(IF [is_fraud] = 1 THEN 1 ELSE 0 END) / COUNT([transaction_id]) * 100
Sort: Descending
Limit: Top 10
```

---

## 🎨 Calculated Fields yang Perlu Dibuat

### 1. Transaction Status
```
IF [is_fraud] = 1 THEN "Fraud"
ELSE "Normal"
END
```

### 2. Fraud Reason Clean
```
IF [fraud_reason] = "high_amount" THEN "High Amount"
ELSEIF [fraud_reason] = "crypto_merchant" THEN "Crypto Merchant"
ELSEIF [fraud_reason] = "burst_activity" THEN "Burst Activity"
ELSE "No Fraud"
END
```

### 3. Transaction Date
```
DATE([event_time])
```

### 4. Fraud Rate %
```
SUM(IF [is_fraud] = 1 THEN 1 ELSE 0 END) / COUNT([transaction_id]) * 100
```

---

## 📝 Checklist

- [ ] Database running
- [ ] Tableau connected to PostgreSQL
- [ ] Data loaded (fact_transactions)
- [ ] Calculated fields created
- [ ] Overview cards created
- [ ] Fraud analysis charts created
- [ ] Dashboard arranged
- [ ] Filters added
- [ ] Dashboard exported/shared

---

## 🆘 Troubleshooting

### Cannot connect?
1. Check Docker: `docker ps | grep postgres`
2. Check port: Should be 5433 (not 5432)
3. Test connection: `python scripts/test_tableau_connection.py`

### Data not showing?
1. Refresh data source in Tableau
2. Check table name: `fact_transactions`
3. Verify data in database: `SELECT COUNT(*) FROM fact_transactions;`

---

## 📚 Resources

- **Full Guide**: See `TABLEAU_SETUP.md`
- **SQL Queries**: See `sql/tableau_queries.sql`
- **Test Connection**: Run `python scripts/test_tableau_connection.py`

---

**Selamat! Dashboard Tableau Anda siap! 🎉**

