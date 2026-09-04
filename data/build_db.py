import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "financial.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

COMPANIES = [
    # Tech
    ("AAPL", "Apple Inc.", "Tech", "Consumer electronics and software", 161000, "Slowing hiring in hardware, accelerating in AI research"),
    ("MSFT", "Microsoft Corp.", "Tech", "Enterprise software and cloud computing", 221000, "Active hiring in Azure and AI divisions"),
    ("CSCO", "Cisco Systems", "Tech", "Networking hardware", 84900, "Recent layoffs in core networking, hiring in cybersecurity"),
    ("SNOW", "Snowflake", "Tech", "Cloud data warehousing", 7000, "Aggressive hiring in sales and engineering"),
    
    # Retail
    ("WMT", "Walmart Inc.", "Retail", "Omnichannel retail and groceries", 2100000, "Automating warehouses, reducing manual retail headcount"),
    ("TGT", "Target Corp.", "Retail", "General merchandise retailer", 440000, "Seasonal hiring flat year-over-year"),
    ("M", "Macy's Inc.", "Retail", "Department stores", 94000, "Closing stores, freezing corporate hiring"),
    ("LULU", "Lululemon", "Retail", "Athleisure apparel", 34000, "Strong hiring in international expansion roles"),
    
    # Logistics
    ("UPS", "United Parcel Service", "Logistics", "Global package delivery", 500000, "Reducing management headcount, union workforce stable"),
    ("FDX", "FedEx Corp.", "Logistics", "Global courier and logistics", 529000, "Consolidating operating companies, hiring freeze in effect"),
    ("XPO", "XPO Logistics", "Logistics", "LTL freight shipping", 38000, "Expanding driver headcount, opening new terminals"),
    ("CHRW", "C.H. Robinson", "Logistics", "Freight brokerage", 17000, "Reducing broker headcount through automation")
]

FINANCIALS = [
    # Ticker, rev_growth, ebitda_margin, pe, ev_ebitda, debt_equity, fcf_yield
    ("AAPL", 2.1, 33.4, 28.5, 21.0, 1.4, 4.5),
    ("MSFT", 14.0, 48.0, 35.0, 24.5, 0.4, 3.8),
    ("CSCO", -5.5, 29.0, 15.2, 11.0, 0.8, 7.2),
    ("SNOW", 32.0, 5.5, -1.0, 85.0, 0.1, 1.2),
    
    ("WMT", 6.0, 6.2, 24.0, 12.5, 0.6, 4.1),
    ("TGT", -1.5, 5.8, 16.5, 9.0, 1.1, 5.5),
    ("M", -6.0, 7.1, 7.5, 5.2, 1.5, 12.0),
    ("LULU", 18.5, 22.3, 31.0, 20.1, 0.2, 2.5),
    
    ("UPS", -7.8, 13.5, 18.0, 11.2, 1.2, 5.0),
    ("FDX", -2.1, 9.5, 14.5, 8.5, 0.9, 6.5),
    ("XPO", 1.5, 11.0, 22.0, 12.5, 2.1, 3.0),
    ("CHRW", -22.0, 4.5, 25.0, 15.0, 1.0, 2.0)
]

OPERATIONAL = [
    # Ticker, metric_name, metric_value, operational_lever, benchmark_comparison
    ("AAPL", "Active Devices", "2.2 Billion", "Supply chain diversification", "Growth lags NASDAQ, but margins superior"),
    ("MSFT", "Commercial Cloud Rev", "$33B/qtr", "AI integration pricing power", "Core portfolio holding, outperforming S&P 500"),
    ("CSCO", "Software Rev %", "45%", "Transition to recurring revenue", "Value trap risk, underperforming tech index"),
    ("SNOW", "Net Retention Rate", "131%", "Optimize cloud infrastructure costs", "High growth premium vs software index"),
    
    ("WMT", "E-commerce Growth", "21%", "Retail media network expansion", "Defensive staple, outperforming XRT index"),
    ("TGT", "Inventory Shrink", "1.2%", "Supply chain footprint optimization", "Losing share to WMT, underperforming retail"),
    ("M", "Real Estate Value", "$8B+", "Sale-leaseback of flagship stores", "Deep value, highly levered vs peers"),
    ("LULU", "Direct to Consumer %", "45%", "International market penetration", "Premium valuation justified by growth vs peers"),
    
    ("UPS", "Rev per Piece", "$13.50", "Network automation and routing", "Yield focused, matching transport index"),
    ("FDX", "Drive Program Savings", "$4B target", "Merge Express and Ground networks", "Margin expansion story vs UPS"),
    ("XPO", "LTL Yield", "Up 5%", "Terminal network density improvement", "Gaining market share from Yellow bankruptcy"),
    ("CHRW", "Brokerage Margin", "14%", "Digital brokerage automation", "Asset-light, struggling in current freight cycle")
]

def build_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    with open(SCHEMA_PATH, 'r') as f:
        cursor.executescript(f.read())
        
    cursor.executemany("INSERT INTO companies VALUES (?, ?, ?, ?, ?, ?)", COMPANIES)
    cursor.executemany("INSERT INTO financials VALUES (?, ?, ?, ?, ?, ?, ?)", FINANCIALS)
    cursor.executemany("INSERT INTO operational_metrics VALUES (?, ?, ?, ?, ?)", OPERATIONAL)
    
    conn.commit()
    conn.close()
    print("Database built successfully at", DB_PATH)

if __name__ == "__main__":
    build_database()
