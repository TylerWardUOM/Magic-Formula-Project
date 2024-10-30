import yfinance as yf
import src.server.scrapers as scrapers
import sqlite3

# Define the top 50 companies with their tickers and exchanges
top_50_companies = [
    ("AAPL", "NASDAQ"), ("MSFT", "NASDAQ"), ("GOOGL", "NASDAQ"), ("GOOG", "NASDAQ"),
    ("AMZN", "NASDAQ"), ("NVDA", "NASDAQ"), ("TSLA", "NASDAQ"), ("META", "NASDAQ"),
    ("BRK.B", "NYSE"), ("V", "NYSE"), ("JNJ", "NYSE"), ("XOM", "NYSE"), ("WMT", "NYSE"),
    ("JPM", "NYSE"), ("PG", "NYSE"), ("MA", "NYSE"), ("LLY", "NYSE"), ("CVX", "NYSE"),
    ("KO", "NYSE"), ("PEP", "NASDAQ"), ("MRK", "NYSE"), ("ABBV", "NYSE"), ("AVGO", "NASDAQ"),
    ("COST", "NASDAQ"), ("CSCO", "NASDAQ"), ("TMO", "NYSE"), ("NKE", "NYSE"), ("MCD", "NYSE"),
    ("ORCL", "NYSE"), ("ACN", "NYSE"), ("LIN", "NYSE"), ("TXN", "NASDAQ"), ("VZ", "NYSE"),
    ("ABT", "NYSE"), ("PM", "NYSE"), ("DHR", "NYSE"), ("MDT", "NYSE"), ("MS", "NYSE"),
    ("NEE", "NYSE"), ("UPS", "NYSE"), ("UNH", "NYSE"), ("CMCSA", "NASDAQ"), ("ADBE", "NASDAQ"),
    ("QCOM", "NASDAQ"), ("HON", "NASDAQ"), ("PYPL", "NASDAQ"), ("IBM", "NYSE"), ("NFLX", "NASDAQ"),
    ("BMY", "NYSE"), ("AMD", "NASDAQ"), ("INTC", "NASDAQ")
]

# Define a list of (ticker, exchange) pairs to process
sheets_list = [("JPM", "NYSE"), ("BAC", "NYSE"), ("PDD", "NASDAQ"), ("MRK", "NYSE"),
               ("GOOG", "NASDAQ"), ("HD", "NYSE"), ("NVS", "NYSE"), ("BRK.A", "NYSE"),
               ("AAPL", "NASDAQ"), ("PEP", "NASDAQ"), ("XOM", "NYSE"), ("V", "NYSE"),
               ("MCD", "NYSE"), ("SHEL", "NYSE"), ("NVO", "NYSE"), ("META", "NASDAQ"),
               ("MA", "NYSE"), ("ASML", "NASDAQ"), ("PG", "NYSE"), ("TSM", "NYSE"),
               ("ACN", "NYSE"), ("JNJ", "NYSE"), ("NVDA", "NASDAQ"), ("MSFT", "NASDAQ"),
               ("CVX", "NYSE"), ("ADBE", "NASDAQ"), ("CSCO", "NASDAQ"), ("KO", "NYSE"),
               ("COST", "NASDAQ"), ("BABA", "NYSE"), ("LLY", "NYSE"), ("TMUS", "NASDAQ"),
               ("UNH", "NYSE"), ("WMT", "NYSE"), ("AZN", "NASDAQ"), ("ABBV", "NYSE"),
               ("IBM", "NYSE"), ("ORCL", "NYSE"), ("TMO", "NYSE"), ("AMZN", "NASDAQ"),
               ("SAP", "NYSE"), ("TSLA", "NASDAQ"), ("CRM", "NYSE"), ("AVGO", "NASDAQ"),
               ("AMD", "NASDAQ")]

# Connect to SQLite database
conn = sqlite3.connect('companies.db')
c = conn.cursor()

# Create table if it doesn't exist, including exchange column
c.execute(''' 
    CREATE TABLE IF NOT EXISTS company_data (
        ticker TEXT PRIMARY KEY,
        exchange TEXT,            -- Add exchange column
        pe_ratio REAL,
        roc REAL,
        combined_rank REAL
    )
''')

# Function to rank values
def rank_values(values):
    sorted_values = sorted(enumerate(values), key=lambda x: x[1])
    ranks = [0] * len(values)
    for rank, (index, _) in enumerate(sorted_values):
        ranks[index] = rank + 1  # Ranks start from 1
    return ranks

# Fetch data and insert into the database
data = []

for ticker, exchange in sheets_list:
    # Try to fetch P/E from scraper
    try:
        pe_ratio = scrapers.scrape_pe_ratio(ticker, exchange)
        if pe_ratio is None:
            raise ValueError("No PE Ratio found from scrapers.")
    except:
        # Fetch trailing P/E using yfinance if scraper fails
        try:
            stock = yf.Ticker(ticker)
            pe_ratio = stock.info.get("trailingPE")
            if pe_ratio is None:
                raise ValueError("No trailing P/E available from yfinance.")
        except Exception as e:
            print(f"Failed to get P/E for {ticker}: {e}")
            pe_ratio = None

    # Fetch ROC from scrapers
    try:
        roc = scrapers.scrape_roc(ticker, exchange)
    except Exception as e:
        print(f"Failed to get ROC for {ticker}: {e}")
        roc = None

    # Check if both P/E and ROC are valid numbers before adding to data
    if isinstance(pe_ratio, (float, int)) and isinstance(roc, (float, int)):
        # Format values to two decimal places
        pe_ratio = round(pe_ratio, 2)  # Round to 2 decimal places
        roc = round(roc, 2)             # Round to 2 decimal places
        data.append((ticker, exchange, pe_ratio, roc))  # Include exchange in data

# Check if data has at least 1 entry before proceeding
if data:
    # Rank P/E and ROC values
    pe_values = [d[2] for d in data]  # Updated index for pe_ratio
    roc_values = [d[3] for d in data]  # Updated index for roc
    pe_ranks = rank_values(pe_values)  # Lower P/E is better
    roc_ranks = rank_values([-roc for roc in roc_values])  # Higher ROC is better (inverting ROC)

    # Calculate combined ranks
    combined_ranks = [pe_rank + roc_rank for pe_rank, roc_rank in zip(pe_ranks, roc_ranks)]

    # Insert data with combined ranks into the database
    for (ticker, exchange, pe_ratio, roc), combined_rank in zip(data, combined_ranks):
        c.execute('INSERT OR REPLACE INTO company_data (ticker, exchange, pe_ratio, roc, combined_rank) VALUES (?, ?, ?, ?, ?) ',
                  (ticker, exchange, pe_ratio, roc, combined_rank))
    # Commit changes
    conn.commit()

    # Now fetch and sort the data based on combined ranks
    c.execute(''' 
        SELECT ticker, exchange, pe_ratio, roc 
        FROM company_data
        ORDER BY combined_rank DESC
    ''')

    # Display the sorted data
    sorted_data = c.fetchall()
    for row in sorted_data:
        print(row)

# Close the database connection
conn.close()
