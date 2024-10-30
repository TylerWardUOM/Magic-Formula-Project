import yfinance as yf  # Library for fetching financial data from Yahoo Finance
import scrapers as scrapers  # Custom scrapers for fetching financial metrics
import sqlite3  # SQLite library for database operations

# This script fetches financial data for the top companies, specifically the 
# price-to-earnings (P/E) ratio and return on capital (ROC), ranks them, 
# and stores the information in an SQLite database.

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
sheets_list = [
    ("JPM", "NYSE"), ("BAC", "NYSE"), ("PDD", "NASDAQ"), ("MRK", "NYSE"),
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
    ("AMD", "NASDAQ")
]

# Connect to SQLite database (create if it doesn't exist)
conn = sqlite3.connect('data\companies.db')
c = conn.cursor()

# Create table to store company data, including the exchange column
c.execute(''' 
    CREATE TABLE IF NOT EXISTS company_data (
        ticker TEXT PRIMARY KEY,
        exchange TEXT,            -- Column to store the stock exchange
        pe_ratio REAL,
        roc REAL,
        combined_rank REAL
    )
''')

# Function to rank values in ascending order
def rank_values(values):
    """Assign ranks to a list of values."""
    sorted_values = sorted(enumerate(values), key=lambda x: x[1])  # Sort values and retain indices
    ranks = [0] * len(values)  # Initialize ranks
    for rank, (index, _) in enumerate(sorted_values):
        ranks[index] = rank + 1  # Assign ranks starting from 1
    return ranks

# List to hold the data for insertion into the database
data = []

# Loop through each ticker and exchange pair in the sheets list
for ticker, exchange in sheets_list:
    # Try to fetch the P/E ratio using the custom scraper
    try:
        pe_ratio = scrapers.scrape_pe_ratio(ticker, exchange)
        if pe_ratio is None:
            raise ValueError("No PE Ratio found from scrapers.")
    except Exception:
        # If scraper fails, fetch trailing P/E using yfinance
        try:
            stock = yf.Ticker(ticker)  # Create a Ticker object for the stock
            pe_ratio = stock.info.get("trailingPE")  # Get the trailing P/E ratio
            if pe_ratio is None:
                raise ValueError("No trailing P/E available from yfinance.")
        except Exception as e:
            print(f"Failed to get P/E for {ticker}: {e}")  # Log error
            pe_ratio = None  # Set to None if both attempts fail

    # Fetch ROC using the custom scraper
    try:
        roc = scrapers.scrape_roc(ticker, exchange)
    except Exception as e:
        print(f"Failed to get ROC for {ticker}: {e}")  # Log error
        roc = None  # Set to None if the scraping fails

    # Check if both P/E and ROC are valid numbers before adding to the data list
    if isinstance(pe_ratio, (float, int)) and isinstance(roc, (float, int)):
        # Round the values to two decimal places
        pe_ratio = round(pe_ratio, 2)  # Round P/E ratio
        roc = round(roc, 2)             # Round ROC
        data.append((ticker, exchange, pe_ratio, roc))  # Store the data tuple

# Check if there is any valid data to process
if data:
    # Separate P/E and ROC values for ranking
    pe_values = [d[2] for d in data]  # Extract P/E ratios
    roc_values = [d[3] for d in data]  # Extract ROC values
    pe_ranks = rank_values(pe_values)  # Rank P/E values (lower is better)
    roc_ranks = rank_values([-roc for roc in roc_values])  # Rank ROC values (higher is better, inverted for ranking)

    # Calculate combined ranks from P/E and ROC ranks
    combined_ranks = [pe_rank + roc_rank for pe_rank, roc_rank in zip(pe_ranks, roc_ranks)]

    # Insert data into the database with combined ranks
    for (ticker, exchange, pe_ratio, roc), combined_rank in zip(data, combined_ranks):
        c.execute('INSERT OR REPLACE INTO company_data (ticker, exchange, pe_ratio, roc, combined_rank) VALUES (?, ?, ?, ?, ?)',
                  (ticker, exchange, pe_ratio, roc, combined_rank))

    # Commit the changes to the database
    conn.commit()

    # Now fetch and sort the data based on combined ranks from the database
    c.execute(''' 
        SELECT ticker, exchange, pe_ratio, roc 
        FROM company_data
        ORDER BY combined_rank DESC  -- Sort by combined rank in descending order
    ''')

    # Display the sorted data
    sorted_data = c.fetchall()
    for row in sorted_data:
        print(row)  # Print each row of sorted data

# Close the database connection
conn.close()  # Close the SQLite connection
