# 💳 Financial Transactions ETL Pipeline

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11%2F3.12-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-blue.svg)
![Tableau](https://img.shields.io/badge/Tableau-Public-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**End-to-end ETL pipeline for financial transaction fraud detection**

[Features](#-features) • [Quick Start](#-quick-start) • [Dashboard](#-dashboard) • [Documentation](#-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Dashboard](#-dashboard)
- [Project Structure](#-project-structure)
- [Fraud Detection Rules](#-fraud-detection-rules)
- [Results](#-results)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

This project implements a complete **ETL (Extract, Transform, Load) pipeline** for financial transaction fraud detection. It consolidates transaction data from multiple sources (API and Database), applies fraud detection rules, and stores the results in a PostgreSQL data warehouse for analysis and visualization.

### Key Highlights

- ✅ **End-to-end ETL pipeline** from data extraction to visualization
- ✅ **Fraud detection** using rule-based algorithms
- ✅ **Multiple data sources** (API JSON + Database CSV/MySQL)
- ✅ **Data warehouse** with PostgreSQL
- ✅ **Interactive dashboard** with Tableau Public
- ✅ **Docker support** for easy deployment
- ✅ **Synthetic data generation** for testing

---

## ✨ Features

### Data Processing
- **Extract**: Pull data from external API (JSON) and internal database (CSV/MySQL)
- **Transform**: Clean, normalize, and unify data from multiple sources
- **Load**: Store processed data in PostgreSQL data warehouse with UPSERT capability

### Fraud Detection
- **High Amount Detection**: Flags transactions > 50,000,000 IDR
- **Crypto Merchant Detection**: Identifies transactions with crypto-related merchants
- **Burst Activity Detection**: Detects users with ≥5 transactions in 10 minutes

### Analytics & Visualization
- **Tableau Dashboard**: Interactive visualizations for fraud analysis
- **Real-time Monitoring**: Track fraud patterns and trends
- **Merchant Analysis**: Fraud rate analysis by merchant
- **Time-based Analysis**: Transaction patterns by hour, day, and date

---

## 🏗️ Architecture

```
┌─────────────┐         ┌─────────────┐
│   External  │         │   Internal  │
│     API     │         │  MySQL DB   │
│   (JSON)    │         │   (CSV)     │
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
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │   TABLEAU     │
        │   Dashboard   │
        │  (Analytics)  │
        └───────────────┘
```

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Language** | Python 3.11/3.12 | Data processing |
| **Data Processing** | pandas, numpy | Data manipulation and cleaning |
| **Database** | PostgreSQL 14+ | Data warehouse |
| **ORM** | SQLAlchemy | Database operations |
| **Containerization** | Docker | PostgreSQL deployment |
| **Visualization** | Tableau Public | Data visualization |
| **Orchestration** | Apache Airflow | ETL scheduling (optional) |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or 3.12
- Docker (optional, for PostgreSQL)
- Tableau Public (for visualization)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/gentaArnezzi/transactions-fraud-etl.git
   cd transactions-fraud-etl
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and configure PostgreSQL connection
   ```

5. **Start PostgreSQL (Docker)**
   ```bash
   docker compose up -d postgres
   sleep 5
   docker cp sql/warehouse_schema.sql etl_postgres:/tmp/schema.sql
   docker exec etl_postgres psql -U etl_user -d etl_warehouse -f /tmp/schema.sql
   ```

6. **Run ETL Pipeline**
   ```bash
   # Generate synthetic data
   python scripts/generate_synthetic_data.py
   
   # Extract data
   python scripts/extract_api.py
   python scripts/extract_db.py
   
   # Transform data
   python scripts/transform.py
   
   # Load to database
   python scripts/load.py
   ```

7. **Verify results**
   ```bash
   python scripts/test_tableau_connection.py
   ```

---

## 📊 Dashboard

### Tableau Public Dashboard

The project includes an interactive Tableau Public dashboard for fraud analysis.

![Dashboard](data/tableau/Dashboard.png)

### Features

- **Overview Metrics**: Total transactions, fraud count, fraud rate, total amount
- **Fraud Trend Analysis**: Daily fraud count over time
- **Fraud by Reason**: Breakdown of fraud by detection rule
- **Day of Week Analysis**: Fraud patterns by day of week
- **Hourly Analysis**: Fraud share by transaction hour
- **Merchant Analysis**: Fraud rate by merchant

### Access Dashboard

1. **Export data to CSV** (for Tableau Public):
   ```bash
   python scripts/export_to_csv.py
   ```

2. **Import to Tableau Public**:
   - Open Tableau Public
   - Connect to Text file
   - Select `data/tableau/fact_transactions.csv`
   - Follow guide in `TABLEAU_PUBLIC_GUIDE.md`

3. **View online**: [Tableau Public Link](https://public.tableau.com/app/profile/irgya.arnezzi/viz/Book1_17628100395780/Dashboard1) 


### Dashboard Guide

- **Quick Start**: See `docs/TABLEAU_PUBLIC_GUIDE.md`
- **Full Guide**: See `docs/TABLEAU_SETUP.md`
- **SQL Queries**: See `sql/tableau_queries.sql`

---

## 📁 Project Structure

```
financial-etl-project/
├── scripts/                  # ETL scripts
│   ├── generate_synthetic_data.py
│   ├── extract_api.py
│   ├── extract_db.py
│   ├── transform.py
│   ├── load.py
│   ├── export_to_csv.py
│   └── test_tableau_connection.py
├── sql/                      # Database schema
│   ├── warehouse_schema.sql
│   └── tableau_queries.sql
├── dags/                     # Airflow DAGs (optional)
│   └── financial_etl_dag.py
├── config/                   # Configuration files
│   └── db_config.yaml
├── data/                     # Data files
│   ├── raw/                  # Raw data
│   ├── processed/            # Processed data
│   └── tableau/              # Tableau CSV files
│       └── Dashboard.png     # Dashboard screenshot
├── docker-compose.yml        # Docker setup
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

---

## 🔍 Fraud Detection Rules

The pipeline implements three fraud detection rules:

### 1. High Amount Detection
- **Rule**: Transaction amount > 50,000,000 IDR
- **Reason**: `high_amount`
- **Rationale**: Large transactions may indicate fraudulent activity

### 2. Crypto Merchant Detection
- **Rule**: Merchant name contains "binance", "crypto", "kraken", or "okx"
- **Reason**: `crypto_merchant`
- **Rationale**: Crypto-related transactions may be high-risk

### 3. Burst Activity Detection
- **Rule**: ≥5 transactions per user within 10 minutes
- **Reason**: `burst_activity`
- **Rationale**: Unusual transaction frequency may indicate fraud

---

## 📈 Results

### Dataset Statistics

- **Total Transactions**: 2,195
- **Fraud Transactions**: 694 (31.6%)
- **Normal Transactions**: 1,501 (68.4%)
- **Total Amount**: Rp86 Billion

### Fraud Breakdown

| Fraud Reason | Count | Percentage |
|-------------|-------|------------|
| High Amount | 525 | 75.6% |
| Crypto Merchant | 169 | 24.4% |
| Burst Activity | 0 | 0% |

### Key Insights

- **Fraud Rate**: 31.6% of all transactions flagged as fraud
- **Peak Fraud Hours**: Hours 20, 10, 21 (evening and morning)
- **Highest Fraud Day**: Day 5 (Friday) with 34.6% fraud rate
- **Merchant Analysis**: Binance has 100% fraud rate (all transactions flagged)

---

## 📚 Documentation

### Main Documentation

- **[docs/PROJECT_EXPLANATION.md](docs/PROJECT_EXPLANATION.md)**: Comprehensive project explanation
- **[docs/TABLEAU_PUBLIC_GUIDE.md](docs/TABLEAU_PUBLIC_GUIDE.md)**: Tableau Public setup guide
- **[docs/TABLEAU_SETUP.md](docs/TABLEAU_SETUP.md)**: Full Tableau setup guide
- **[docs/TABLEAU_QUICKSTART.md](docs/TABLEAU_QUICKSTART.md)**: Quick start guide for Tableau
- **[docs/DASHBOARD_TITLES.md](docs/DASHBOARD_TITLES.md)**: Dashboard title suggestions
- **[GITHUB_SETUP.md](GITHUB_SETUP.md)**: GitHub repository setup guide

### Scripts Documentation

- **generate_synthetic_data.py**: Generates synthetic transaction data
- **extract_api.py**: Extracts data from API or JSON file
- **extract_db.py**: Extracts data from database or CSV file
- **transform.py**: Transforms and cleans data, applies fraud detection
- **load.py**: Loads data to PostgreSQL with UPSERT
- **export_to_csv.py**: Exports data to CSV for Tableau Public

### SQL Documentation

- **warehouse_schema.sql**: PostgreSQL database schema
- **tableau_queries.sql**: SQL queries for Tableau visualization

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file from `.env.example`:

```env
# PostgreSQL Connection
POSTGRES_URI=postgresql+psycopg2://etl_user:etl_pass@127.0.0.1:5433/etl_warehouse

# Data Directory
DATA_DIR=./data

# Optional: MySQL Connection (for real database)
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=secret
MYSQL_DATABASE=core_banking

# Optional: API URL (for real API)
API_URL=
```

### Docker Compose

The project includes `docker-compose.yml` for easy PostgreSQL setup:

```yaml
services:
  postgres:
    image: postgres:15
    container_name: etl_postgres
    environment:
      POSTGRES_PASSWORD: etl_pass
      POSTGRES_USER: etl_user
      POSTGRES_DB: etl_warehouse
    ports: ["5433:5432"]
    volumes:
      - pgdata:/var/lib/postgresql/data
```

---

## 🧪 Testing

### Test Database Connection

```bash
python scripts/test_tableau_connection.py
```

### Verify Data

```sql
-- Check total transactions
SELECT COUNT(*) FROM fact_transactions;

-- Check fraud transactions
SELECT COUNT(*) FROM fact_transactions WHERE is_fraud = 1;

-- Check fraud rate
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
    ROUND(100.0 * SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as fraud_rate_pct
FROM fact_transactions;
```

---

## 🚀 Deployment

### Local Deployment

1. Follow [Quick Start](#-quick-start) instructions
2. Run ETL pipeline manually or schedule with Airflow

### Airflow Deployment

1. Install Airflow:
   ```bash
   pip install apache-airflow==2.10.2
   ```

2. Setup Airflow:
   ```bash
   export AIRFLOW_HOME=~/airflow
   airflow db init
   ```

3. Start Airflow:
   ```bash
   airflow webserver
   airflow scheduler
   ```

4. Enable DAG: `financial_etl_dag`

### Docker Deployment

```bash
# Start PostgreSQL
docker compose up -d postgres

# Run ETL pipeline
python scripts/generate_synthetic_data.py
python scripts/extract_api.py
python scripts/extract_db.py
python scripts/transform.py
python scripts/load.py
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🧪 Testing

### Run Tests

```bash
# Install pytest (optional)
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=scripts --cov-report=html
```

### Test Coverage

- **Unit Tests**: Basic unit tests for data quality functions
- **Integration Tests**: End-to-end ETL pipeline tests (to be added)
- **Data Quality Tests**: Data validation and quality checks

---

## 🔧 Improvements & Future Work

### Current Features
- ✅ End-to-end ETL pipeline
- ✅ Fraud detection with rule-based algorithms
- ✅ Data quality checks
- ✅ Logging and error handling
- ✅ PostgreSQL data warehouse
- ✅ Tableau dashboard

### Planned Improvements
- [ ] Add comprehensive unit tests
- [ ] Add integration tests
- [ ] Add data profiling reports
- [ ] Add incremental loading strategy
- [ ] Add monitoring dashboard
- [ ] Add CI/CD pipeline
- [ ] Add machine learning models for fraud detection
- [ ] Add data partitioning strategy
- [ ] Add performance optimization
- [ ] Add data lineage documentation

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Irgy Genta Arnezzi**
- GitHub: [@gentaArnezzi](https://github.com/gentaArnezzi)
- LinkedIn: [Irgy Genta Arnezzi](https://www.linkedin.com/in/irgyagentaarnezzi/)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- Thanks to all contributors who have helped improve this project
- Built with [Python](https://www.python.org/), [PostgreSQL](https://www.postgresql.org/), and [Tableau](https://www.tableau.com/)

---

## 📊 Project Status

![Status](https://img.shields.io/badge/Status-Active-success.svg)
![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)

**Last Updated**: November 2024

---

<div align="center">

**⭐ If you find this project helpful, please give it a star! ⭐**

Made with ❤️ for data engineering and fraud detection

</div>
