# 📊 Panduan Tableau Public - Menggunakan CSV Files

## 🎯 Overview

Tableau Public tidak bisa connect langsung ke database, jadi kita perlu export data ke CSV terlebih dahulu. Panduan ini akan membantu Anda membuat dashboard menggunakan file CSV yang sudah di-export.

---

## 📋 Step 1: Export Data ke CSV

### 1.1. Pastikan Database Running
```bash
# Cek Docker container
docker ps | grep postgres

# Jika tidak running, start container
docker compose up -d postgres
```

### 1.2. Export Data
```bash
# Jalankan script export
python scripts/export_to_csv.py
```

### 1.3. Hasil Export
File CSV akan tersimpan di folder `data/tableau/`:
- `fact_transactions.csv` - **File utama** (2,195 rows) ⭐
- `daily_summary.csv` - Summary harian (31 rows)
- `merchant_summary.csv` - Summary merchant (8 rows)
- `user_summary.csv` - Summary user (100 rows)
- `fraud_by_reason.csv` - Breakdown fraud by reason (2 rows)
- `hourly_summary.csv` - Summary per jam (24 rows)
- `day_of_week_summary.csv` - Summary per hari (7 rows)
- `location_summary.csv` - Summary per lokasi (6 rows)

---

## 🚀 Step 2: Import ke Tableau Public

### 2.1. Buka Tableau Public
1. Download dan install **Tableau Public** (gratis): https://public.tableau.com/
2. Buka Tableau Public
3. Klik **"Open"** atau **"Connect to Data"**

### 2.2. Import CSV File
1. Pilih **"Text file"** atau **"Microsoft Excel"** (jika CSV)
2. Browse ke folder `data/tableau/`
3. Pilih **`fact_transactions.csv`** (file utama)
4. Klik **"Open"**

### 2.3. Load Data
1. Tableau akan menampilkan preview data
2. Pastikan semua kolom terdeteksi dengan benar
3. Klik **"Sheet 1"** untuk mulai membuat visualization

---

## 📊 Step 3: Buat Visualizations

### 3.1. Overview Metrics (4 Cards)

#### Card 1: Total Transactions
1. Drag **`transaction_id`** ke canvas
2. Klik kanan → **"Measure"** → **"Count"**
3. Format: Number (0 decimal)
4. Label: "Total Transactions"

#### Card 2: Fraud Transactions
1. Buat calculated field: `Fraud Count`
   ```
   SUM(IF [is_fraud] = 1 THEN 1 ELSE 0 END)
   ```
2. Drag **`Fraud Count`** ke canvas
3. Format: Number (0 decimal)
4. Label: "Fraud Transactions"

#### Card 3: Fraud Rate
1. Buat calculated field: `Fraud Rate %`
   ```
   SUM(IF [is_fraud] = 1 THEN 1 ELSE 0 END) / COUNT([transaction_id]) * 100
   ```
2. Drag **`Fraud Rate %`** ke canvas
3. Format: Percentage (1 decimal)
4. Label: "Fraud Rate"

#### Card 4: Total Amount
1. Drag **`amount`** ke canvas
2. Klik kanan → **"Measure"** → **"Sum"**
3. Format: Currency (IDR)
4. Label: "Total Amount"

---

### 3.2. Fraud by Reason (Bar Chart)

1. Drag **`fraud_reason_clean`** ke **Rows**
2. Drag **`transaction_id`** ke **Columns**
3. Klik kanan pada **`transaction_id`** → **"Measure"** → **"Count"**
4. Drag **`fraud_reason_clean`** ke **Color**
5. Add filter: **`transaction_status`** = "Fraud"

**Result**: Bar chart menampilkan jumlah fraud berdasarkan reason

---

### 3.3. Fraud Trend Over Time (Line Chart)

1. Drag **`transaction_date`** ke **Columns**
2. Drag **`Fraud Count`** (calculated field) ke **Rows**
3. Drag **`transaction_status`** ke **Color**
4. Change chart type to **Line Chart**

**Result**: Line chart menampilkan trend fraud over time

---

### 3.4. Merchant Analysis (Bar Chart)

1. Drag **`merchant`** ke **Rows**
2. Drag **`Fraud Rate %`** (calculated field) ke **Columns**
3. Sort: **Descending**
4. Limit: **Top 10** (Right-click on merchant → Filter → Top → By field)

**Result**: Bar chart menampilkan fraud rate per merchant

---

### 3.5. Transactions by Hour (Bar Chart)

1. Drag **`transaction_hour`** ke **Rows**
2. Drag **`transaction_id`** ke **Columns**
3. Klik kanan pada **`transaction_id`** → **"Measure"** → **"Count"**
4. Drag **`transaction_status`** ke **Color**

**Result**: Bar chart menampilkan distribusi transaksi per jam

---

### 3.6. Transactions by Day of Week (Bar Chart)

1. Drag **`day_of_week`** ke **Rows**
2. Drag **`transaction_id`** ke **Columns**
3. Klik kanan pada **`transaction_id`** → **"Measure"** → **"Count"**
4. Drag **`transaction_status`** ke **Color**
5. Sort: **Manual** (Sunday, Monday, Tuesday, ..., Saturday)

**Result**: Bar chart menampilkan distribusi transaksi per hari

---

## 🎨 Step 4: Calculated Fields

### 4.1. Transaction Status
```
IF [is_fraud] = 1 THEN "Fraud"
ELSE "Normal"
END
```
**Name**: `Transaction Status`

### 4.2. Fraud Count
```
SUM(IF [is_fraud] = 1 THEN 1 ELSE 0 END)
```
**Name**: `Fraud Count`

### 4.3. Fraud Rate %
```
SUM(IF [is_fraud] = 1 THEN 1 ELSE 0 END) / COUNT([transaction_id]) * 100
```
**Name**: `Fraud Rate %`

### 4.4. Amount Category (jika belum ada)
```
IF [amount] > 50000000 THEN "High Amount"
ELSEIF [amount] > 10000000 THEN "Medium Amount"
ELSE "Low Amount"
END
```
**Name**: `Amount Category`

---

## 📱 Step 5: Buat Dashboard

### 5.1. Create New Dashboard
1. Klik **"New Dashboard"** di bottom tabs
2. Set size: **"Desktop"** (1000x800) atau **"Fixed Size"** (1200x800)

### 5.2. Arrange Visualizations
1. Drag visualizations dari sheets ke dashboard
2. Arrange secara logical:
   - **Top**: Overview metrics (4 cards)
   - **Middle Left**: Fraud analysis (Fraud by Reason, Fraud Trend)
   - **Middle Right**: Transaction analysis (Hourly, Day of Week)
   - **Bottom**: Merchant analysis

### 5.3. Add Filters
1. Drag **`transaction_status`** ke filter area
2. Drag **`merchant`** ke filter area
3. Drag **`transaction_date`** ke filter area
4. Set filters sebagai **"Apply to All"**

### 5.4. Add Title
1. Double-click title area
2. Title: **"Financial Transactions Fraud Detection Dashboard"**
3. Subtitle: **"Real-time monitoring of financial transactions and fraud detection"**

---

## 🎨 Step 6: Styling

### 6.1. Color Scheme
- **Fraud**: Red (#FF6B6B)
- **Normal**: Green (#51CF66)
- **Warning**: Orange (#FFA726)

### 6.2. Fonts
- Title: **Bold**, Size 16-18
- Labels: **Regular**, Size 10-12
- Numbers: **Bold**, Size 14-16

### 6.3. Layout
- Use grid layout untuk alignment
- Leave whitespace untuk readability
- Group related visualizations

---

## 💾 Step 7: Save dan Publish

### 7.1. Save Local
1. **File** → **Save As**
2. Save as `.twbx` file
3. File ini bisa dibuka di Tableau Public

### 7.2. Publish to Tableau Public
1. **Server** → **Tableau Public** → **Save to Tableau Public**
2. Login dengan Tableau Public account (gratis)
3. Dashboard akan terpublish online (public)
4. Dapat di-share via link

### 7.3. Export as Image/PDF
1. **Worksheet** → **Export** → **Image** atau **PDF**
2. Useful untuk dokumentasi atau presentasi

---

## 📊 File CSV yang Tersedia

### 1. fact_transactions.csv (⭐ Main File)
- **Rows**: 2,195
- **Size**: ~416 KB
- **Use**: Main data source untuk semua visualizations
- **Columns**: 
  - transaction_id, user_id, amount, merchant, etc.
  - transaction_date, transaction_hour, day_of_week (calculated)
  - transaction_status, fraud_reason_clean (calculated)
  - amount_category (calculated)

### 2. daily_summary.csv
- **Rows**: 31
- **Use**: Time series analysis, daily trends
- **Columns**: transaction_date, total_transactions, fraud_count, fraud_rate_pct, etc.

### 3. merchant_summary.csv
- **Rows**: 8
- **Use**: Merchant analysis, comparison
- **Columns**: merchant, total_transactions, fraud_count, fraud_rate_pct, etc.

### 4. user_summary.csv
- **Rows**: 100
- **Use**: User analysis, top users
- **Columns**: user_id, total_transactions, fraud_count, fraud_rate_pct, etc.

### 5. fraud_by_reason.csv
- **Rows**: 2
- **Use**: Fraud breakdown
- **Columns**: fraud_reason, fraud_reason_clean, transaction_count, etc.

### 6. hourly_summary.csv
- **Rows**: 24
- **Use**: Hourly analysis
- **Columns**: transaction_hour, total_transactions, fraud_count, etc.

### 7. day_of_week_summary.csv
- **Rows**: 7
- **Use**: Day of week analysis
- **Columns**: day_of_week, day_name, total_transactions, etc.

### 8. location_summary.csv
- **Rows**: 6
- **Use**: Location analysis
- **Columns**: location, total_transactions, fraud_count, etc.

---

## 🔄 Update Data

### Jika Data Berubah
1. Jalankan ETL pipeline:
   ```bash
   python scripts/extract_api.py
   python scripts/extract_db.py
   python scripts/transform.py
   python scripts/load.py
   ```

2. Export data lagi:
   ```bash
   python scripts/export_to_csv.py
   ```

3. Refresh data di Tableau Public:
   - **Data** → **Refresh Data Source**
   - Atau re-import file CSV yang baru

---

## 🎯 Tips untuk Tableau Public

### 1. Performance
- Use **extracts** jika data besar (File → Extract Data)
- Limit data dengan filters
- Use aggregation untuk large datasets

### 2. Interactivity
- Add **tooltips** dengan informasi detail
- Add **filters** untuk user exploration
- Add **actions** untuk cross-filtering

### 3. Sharing
- Publish ke Tableau Public untuk sharing
- Export as image/PDF untuk dokumentasi
- Screenshot untuk portfolio

---

## 🐛 Troubleshooting

### Problem: CSV file tidak terbaca
**Solution**:
- Pastikan file CSV di folder `data/tableau/`
- Check file encoding (should be UTF-8)
- Try open dengan Excel terlebih dahulu

### Problem: Data tidak muncul
**Solution**:
- Refresh data source
- Check column names
- Verify data di CSV file

### Problem: Calculated fields error
**Solution**:
- Check field names (case-sensitive)
- Verify data types
- Check syntax untuk calculated fields

---

## ✅ Checklist

- [ ] Data exported to CSV (`python scripts/export_to_csv.py`)
- [ ] CSV files di folder `data/tableau/`
- [ ] Tableau Public installed
- [ ] CSV file imported ke Tableau Public
- [ ] Calculated fields created
- [ ] Overview metrics (4 cards) created
- [ ] Fraud analysis charts created
- [ ] Transaction analysis charts created
- [ ] Merchant analysis charts created
- [ ] Dashboard arranged
- [ ] Filters added
- [ ] Dashboard styled
- [ ] Dashboard saved/published

---

## 📚 Resources

- **Export Script**: `scripts/export_to_csv.py`
- **CSV Files**: `data/tableau/`
- **Full Guide**: `TABLEAU_SETUP.md` (for PostgreSQL connection)
- **SQL Queries**: `sql/tableau_queries.sql`

---

## 🎉 Selamat!

Dashboard Tableau Public Anda siap! 

**Next Steps**:
1. Create visualizations sesuai panduan
2. Arrange dashboard layout
3. Add filters dan interactivity
4. Publish ke Tableau Public
5. Share link untuk portfolio

---

**Happy Dashboarding! 🚀**

