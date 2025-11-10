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
  source             VARCHAR(16),              -- API / DB
  is_fraud           SMALLINT DEFAULT 0,
  fraud_reason       VARCHAR(256),             -- alasan flag
  ingestion_time     TIMESTAMPTZ DEFAULT NOW()
);


-- Indeks untuk query performa
CREATE INDEX IF NOT EXISTS idx_fact_tx_user_time ON fact_transactions (user_id, event_time);
CREATE INDEX IF NOT EXISTS idx_fact_tx_merchant ON fact_transactions (merchant);
CREATE INDEX IF NOT EXISTS idx_fact_tx_is_fraud ON fact_transactions (is_fraud);