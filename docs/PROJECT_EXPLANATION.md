# 📊 Penjelasan Proyek: Financial Transactions ETL Pipeline

## 🎯 Apa itu Proyek Ini?

Ini adalah **ETL (Extract, Transform, Load) Pipeline** untuk mengolah data transaksi keuangan. Proyek ini menggabungkan data dari **2 sumber berbeda** (API dan Database) menjadi satu data warehouse untuk analisis fraud detection dan reporting.

### Analogi Sederhana:
Bayangkan Anda punya toko dengan 2 kasir:
- **Kasir 1 (API)**: Mencatat transaksi di sistem online
- **Kasir 2 (Database)**: Mencatat transaksi di sistem offline

ETL Pipeline ini mengambil data dari kedua kasir, membersihkan dan menyatukannya, lalu menyimpannya di gudang data (warehouse) untuk dianalisis. Selain itu, sistem juga bisa **mendeteksi transaksi mencurigakan (fraud)** secara otomatis.

---

## 🏗️ Arsitektur Proyek

```
┌─────────────┐         ┌─────────────┐
│   External  │         │   Internal  │
│     API     │         │  MySQL DB   │
│  (JSON)     │         │   (CSV)     │
└──────┬──────┘         └──────┬──────┘
       │                        │
       │    EXTRACT             │
       │    (Ambil Data)        │
       └────────┬───────────────┘
                │
                ▼
        ┌───────────────┐
        │   TRANSFORM   │
        │  (Olah Data)  │
        │  - Cleaning   │
        │  - Unify      │
        │  - Fraud Det. │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │     LOAD      │
        │ (Simpan Data) │
        │  PostgreSQL   │
        │   Warehouse   │
        └───────────────┘
```

---

## 📁 Struktur File dan Fungsinya

### 1. **Scripts/** - Script ETL

#### `generate_synthetic_data.py`
**Fungsi**: Membuat data dummy/sintetik untuk testing
- Menghasilkan 1200 transaksi dari API (format JSON)
- Menghasilkan 1000 transaksi dari Database (format CSV)
- Data dibuat realistis dengan Faker library
- **Kenapa penting?**: Untuk testing tanpa data real (aman untuk portfolio)

#### `extract_api.py`
**Fungsi**: Mengambil data dari API eksternal
- Membaca dari file JSON (mock) atau API endpoint
- Menyimpan hasil extract ke `data/raw/api_extracted.json`
- **Kenapa penting?**: Menunjukkan kemampuan integrasi dengan API

#### `extract_db.py`
**Fungsi**: Mengambil data dari database internal
- Membaca dari file CSV (mock) atau MySQL database
- Menyimpan hasil extract ke `data/raw/db_extracted.csv`
- **Kenapa penting?**: Menunjukkan kemampuan integrasi dengan database

#### `transform.py`
**Fungsi**: Mengolah dan membersihkan data
- **Normalisasi**: Menyamakan format data dari API dan DB
- **Cleaning**: Menghapus data duplikat, null, invalid
- **Fraud Detection**: Mengidentifikasi transaksi mencurigakan
  - High amount (>50 juta IDR)
  - Crypto merchant (Binance, dll)
  - Burst activity (≥5 transaksi dalam 10 menit)
- **Kenapa penting?**: Menunjukkan skill data cleaning dan business logic

#### `load.py`
**Fungsi**: Memuat data ke PostgreSQL
- Menggunakan UPSERT (Insert atau Update jika sudah ada)
- Menggunakan SQLAlchemy untuk koneksi database
- **Kenapa penting?**: Menunjukkan kemampuan database operations

---

### 2. **SQL/** - Database Schema

#### `warehouse_schema.sql`
**Fungsi**: Definisi struktur tabel di PostgreSQL
- Tabel `fact_transactions`: Menyimpan semua transaksi
- Indeks untuk performa query (user_id, merchant, is_fraud)
- **Kenapa penting?**: Menunjukkan pemahaman database design

---

### 3. **DAGS/** - Airflow Orchestration

#### `financial_etl_dag.py`
**Fungsi**: Mengatur alur eksekusi ETL
- Menjalankan script secara berurutan (Extract → Transform → Load)
- Dapat dijadwalkan (misalnya setiap hari jam 2 pagi)
- **Kenapa penting?**: Menunjukkan kemampuan orchestration (opsional)

---

### 4. **Config/** - Konfigurasi

#### `db_config.yaml`
**Fungsi**: Konfigurasi koneksi database
- Menyimpan setting database, API, paths
- **Kenapa penting?**: Best practice untuk memisahkan config dari code

---

### 5. **Data/** - Data Files

#### `data/raw/`
- Data mentah dari sumber (API JSON, DB CSV)
- **Kenapa penting?**: Menunjukkan data pipeline flow

#### `data/processed/`
- Data yang sudah diolah (cleaned_transactions.csv)
- **Kenapa penting?**: Output dari transform step

---

### 6. **File Konfigurasi**

#### `docker-compose.yml`
**Fungsi**: Setup PostgreSQL dengan Docker
- Menjalankan PostgreSQL dalam container
- Port 5433 (menghindari konflik dengan PostgreSQL lokal)
- **Kenapa penting?**: Menunjukkan kemampuan Docker dan containerization

#### `requirements.txt`
**Fungsi**: Daftar library Python yang dibutuhkan
- pandas, numpy: Data processing
- SQLAlchemy: Database ORM
- psycopg2: PostgreSQL driver
- **Kenapa penting?**: Dependency management

#### `.env.example`
**Fungsi**: Template untuk environment variables
- Koneksi database, API URL, dll
- **Kenapa penting?**: Security best practice (tidak hardcode credentials)

---

## 🔄 Alur Kerja (Workflow)

### Step 1: Generate Data
```bash
python scripts/generate_synthetic_data.py
```
**Hasil**: Data dummy di `data/raw/`

### Step 2: Extract
```bash
python scripts/extract_api.py    # Ambil dari API
python scripts/extract_db.py     # Ambil dari DB
```
**Hasil**: Data extract di `data/raw/`

### Step 3: Transform
```bash
python scripts/transform.py
```
**Hasil**: Data cleaned di `data/processed/cleaned_transactions.csv`

### Step 4: Load
```bash
python scripts/load.py
```
**Hasil**: Data di PostgreSQL warehouse

---

## 🎨 Fitur-Fitur Utama

### 1. **Data Integration**
- Menggabungkan data dari 2 sumber berbeda (API + DB)
- Menyamakan format yang berbeda menjadi satu schema

### 2. **Data Cleaning**
- Menghapus duplikat
- Menangani missing values
- Validasi data

### 3. **Fraud Detection**
- **Rule-based detection**: 3 aturan dasar
  - High amount transactions
  - Crypto merchant transactions
  - Burst activity detection
- **Hasil**: 694 dari 2195 transaksi terdeteksi sebagai fraud (31.6%)

### 4. **Data Warehouse**
- PostgreSQL sebagai data warehouse
- Tabel terstruktur dengan indeks untuk performa
- Siap untuk analisis dan reporting

---

## 💼 Kenapa Ini Bagus untuk Portfolio?

### 1. **End-to-End Pipeline**
- Menunjukkan kemampuan membuat sistem lengkap dari awal sampai akhir
- Bukan hanya script, tapi sistem yang terorganisir

### 2. **Multiple Technologies**
- **Python**: Data processing
- **PostgreSQL**: Database
- **Docker**: Containerization
- **SQL**: Database queries
- **Airflow**: Orchestration (opsional)

### 3. **Real-World Problem**
- Fraud detection adalah masalah nyata di industri fintech
- Menunjukkan pemahaman business logic

### 4. **Best Practices**
- Modular code (setiap step terpisah)
- Configuration management (.env, YAML)
- Error handling
- Documentation

### 5. **Scalability**
- Dapat dijadwalkan dengan Airflow
- Dapat di-scale dengan Docker
- Dapat di-extend untuk ML models

---

## 📊 Hasil dan Statistik

### Data yang Diproses:
- **Total Transaksi**: 2,195
- **Fraud Transactions**: 694 (31.6%)
- **Fraud Breakdown**:
  - High amount: 525 transaksi
  - Crypto merchant: 169 transaksi
  - Burst activity: 0 transaksi

### Database:
- Tabel: `fact_transactions`
- Indeks: 3 indeks untuk optimasi query
- UPSERT: Data dapat di-update tanpa duplikasi

---

## 🚀 Cara Menggunakan untuk Portfolio

### 1. **Repository di GitHub**
- Upload semua file ke GitHub
- Pastikan README.md jelas dan lengkap
- Tambahkan screenshots jika ada

### 2. **Penjelasan di README**
- Problem statement
- Solution approach
- Technologies used
- Results/Statistics

### 3. **Demo/Video**
- Rekam video menjalankan pipeline
- Tunjukkan hasil di database
- Jelaskan setiap step

### 4. **LinkedIn/Portfolio Website**
- Jelaskan proyek dengan singkat
- Highlight technologies dan skills
- Link ke GitHub repository

---

## 🔧 Technologies Stack

| Kategori | Technology | Kenapa Dipilih |
|----------|-----------|----------------|
| Language | Python | Populer untuk data engineering |
| Data Processing | pandas, numpy | Standard library untuk data manipulation |
| Database | PostgreSQL | Powerful untuk data warehouse |
| ORM | SQLAlchemy | Python-friendly database interface |
| Container | Docker | Easy deployment dan reproducibility |
| Orchestration | Airflow (opsional) | Industry standard untuk ETL |
| Data Generation | Faker | Generate realistic test data |

---

## 📈 Next Steps (Untuk Improvement)

1. **Machine Learning**: Tambah ML model untuk fraud detection
2. **Dashboard**: Buat dashboard dengan Metabase/Tableau
3. **Testing**: Tambah unit tests dan integration tests
4. **CI/CD**: Setup GitHub Actions untuk automated testing
5. **Monitoring**: Tambah logging dan monitoring
6. **Data Quality**: Tambah data quality checks
7. **Dimensional Modeling**: Tambah dim tables (dim_user, dim_merchant)

---

## 🎓 Skills yang Ditunjukkan

✅ **Data Engineering**: ETL pipeline design
✅ **Python Programming**: Scripting, data processing
✅ **SQL**: Database design, queries
✅ **Docker**: Containerization
✅ **Data Cleaning**: Handling missing values, duplicates
✅ **Business Logic**: Fraud detection rules
✅ **Database Design**: Schema design, indexing
✅ **Version Control**: Git, GitHub
✅ **Documentation**: README, code comments

---

## 💡 Tips untuk Presentasi Portfolio

1. **Storytelling**: Ceritakan masalah yang diselesaikan
2. **Visualization**: Tunjukkan diagram arsitektur
3. **Results**: Highlight statistik dan hasil
4. **Code Quality**: Pastikan code bersih dan terorganisir
5. **Documentation**: README yang jelas dan lengkap

---

## 📞 Pertanyaan yang Sering Ditanyakan

### Q: Kenapa menggunakan data sintetik?
A: Untuk portfolio, data sintetik lebih aman (tidak expose data real) dan tetap realistis.

### Q: Kenapa 2 sumber data?
A: Menunjukkan kemampuan integrasi multiple data sources, yang sering terjadi di real-world.

### Q: Apakah ini production-ready?
A: Untuk portfolio, ini sudah cukup. Untuk production, perlu tambahan: monitoring, error handling, testing, dll.

### Q: Bagaimana cara extend proyek ini?
A: Bisa tambah ML models, dashboard, real-time processing, dll.

---

## 🎯 Kesimpulan

Proyek ini adalah **ETL Pipeline lengkap** yang menunjukkan:
- Kemampuan data engineering
- Pemahaman end-to-end data pipeline
- Skill Python, SQL, Docker
- Business logic (fraud detection)
- Best practices dalam software development

**Cocok untuk**: Data Engineer, Data Analyst, Backend Developer, atau siapa saja yang ingin menunjukkan kemampuan data processing.

---

**Selamat! Proyek Anda sudah siap untuk portfolio! 🚀**

