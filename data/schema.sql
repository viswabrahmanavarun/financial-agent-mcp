CREATE TABLE IF NOT EXISTS companies (
    ticker TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    sector TEXT NOT NULL,
    description TEXT,
    headcount INTEGER,
    recent_hiring_signal TEXT
);

CREATE TABLE IF NOT EXISTS financials (
    ticker TEXT PRIMARY KEY,
    revenue_growth_pct REAL,
    ebitda_margin_pct REAL,
    pe_ratio REAL,
    ev_to_ebitda REAL,
    debt_to_equity REAL,
    free_cash_flow_yield_pct REAL,
    FOREIGN KEY(ticker) REFERENCES companies(ticker)
);

CREATE TABLE IF NOT EXISTS operational_metrics (
    ticker TEXT PRIMARY KEY,
    key_metric_name TEXT,
    key_metric_value TEXT,
    operational_lever TEXT, -- useful for PE persona
    benchmark_comparison TEXT, -- useful for MF persona
    FOREIGN KEY(ticker) REFERENCES companies(ticker)
);
