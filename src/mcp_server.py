from mcp.server.fastmcp import FastMCP
import sqlite3
import os
import json

# Initialize FastMCP server
mcp = FastMCP("Financial Data Server")

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "financial.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@mcp.tool()
def get_companies_by_sector(sector: str) -> str:
    """Get a list of all companies in a specific sector (Tech, Retail, or Logistics)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ticker, name, description, headcount, recent_hiring_signal FROM companies WHERE sector = ? COLLATE NOCASE", (sector,))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return f"No companies found in sector: {sector}"
    
    return json.dumps([dict(row) for row in rows], indent=2)

@mcp.tool()
def get_company_financials(ticker: str) -> str:
    """Get core financial metrics (growth, margins, valuation, debt) for a specific company by ticker."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM financials WHERE ticker = ? COLLATE NOCASE", (ticker,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return f"No financial data found for ticker: {ticker}"
    
    return json.dumps(dict(row), indent=2)

@mcp.tool()
def get_company_operational_metrics(ticker: str) -> str:
    """Get operational metrics, PE operational levers, and MF benchmark comparisons for a company by ticker."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM operational_metrics WHERE ticker = ? COLLATE NOCASE", (ticker,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return f"No operational metrics found for ticker: {ticker}"
    
    return json.dumps(dict(row), indent=2)

@mcp.tool()
def search_all_data_for_sector(sector: str) -> str:
    """Get all companies, financials, and operational metrics for an entire sector at once."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
    SELECT 
        c.ticker, c.name, c.description, c.headcount, c.recent_hiring_signal,
        f.revenue_growth_pct, f.ebitda_margin_pct, f.pe_ratio, f.ev_to_ebitda, f.debt_to_equity, f.free_cash_flow_yield_pct,
        o.key_metric_name, o.key_metric_value, o.operational_lever, o.benchmark_comparison
    FROM companies c
    LEFT JOIN financials f ON c.ticker = f.ticker
    LEFT JOIN operational_metrics o ON c.ticker = o.ticker
    WHERE c.sector = ? COLLATE NOCASE
    '''
    cursor.execute(query, (sector,))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return f"No data found for sector: {sector}"
        
    return json.dumps([dict(row) for row in rows], indent=2)

if __name__ == "__main__":
    # Run the server via stdio
    mcp.run()
