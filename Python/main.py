import scrapers
import sqlite3

# Define the top 50 companies with their tickers and exchanges
top_50_companies = [
    ("AAPL", "NASDAQ"),    # Apple Inc.
    ("MSFT", "NASDAQ"),    # Microsoft Corp.
    ("GOOGL", "NASDAQ"),   # Alphabet Inc. (Class A)
    ("GOOG", "NASDAQ"),    # Alphabet Inc. (Class C)
    ("AMZN", "NASDAQ"),    # Amazon.com Inc.
    ("NVDA", "NASDAQ"),    # NVIDIA Corp.
    ("TSLA", "NASDAQ"),    # Tesla Inc.
    ("META", "NASDAQ"),    # Meta Platforms Inc.
    ("BRK.B", "NYSE"),     # Berkshire Hathaway Inc. (Class B)
    ("V", "NYSE"),         # Visa Inc.
    ("JNJ", "NYSE"),       # Johnson & Johnson
    ("XOM", "NYSE"),       # Exxon Mobil Corp.
    ("WMT", "NYSE"),       # Walmart Inc.
    ("JPM", "NYSE"),       # JPMorgan Chase & Co.
    ("PG", "NYSE"),        # Procter & Gamble Co.
    ("MA", "NYSE"),        # Mastercard Inc.
    ("LLY", "NYSE"),       # Eli Lilly and Co.
    ("CVX", "NYSE"),       # Chevron Corp.
    ("KO", "NYSE"),        # Coca-Cola Co.
    ("PEP", "NASDAQ"),     # PepsiCo Inc.
    ("MRK", "NYSE"),       # Merck & Co. Inc.
    ("ABBV", "NYSE"),      # AbbVie Inc.
    ("AVGO", "NASDAQ"),    # Broadcom Inc.
    ("COST", "NASDAQ"),    # Costco Wholesale Corp.
    ("CSCO", "NASDAQ"),    # Cisco Systems Inc.
    ("TMO", "NYSE"),       # Thermo Fisher Scientific Inc.
    ("NKE", "NYSE"),       # Nike Inc.
    ("MCD", "NYSE"),       # McDonald's Corp.
    ("ORCL", "NYSE"),      # Oracle Corp.
    ("ACN", "NYSE"),       # Accenture plc
    ("LIN", "NYSE"),       # Linde plc
    ("TXN", "NASDAQ"),     # Texas Instruments Inc.
    ("VZ", "NYSE"),        # Verizon Communications Inc.
    ("ABT", "NYSE"),       # Abbott Laboratories
    ("PM", "NYSE"),        # Philip Morris International Inc.
    ("DHR", "NYSE"),       # Danaher Corp.
    ("MDT", "NYSE"),       # Medtronic plc
    ("MS", "NYSE"),        # Morgan Stanley
    ("NEE", "NYSE"),       # NextEra Energy Inc.
    ("UPS", "NYSE"),       # United Parcel Service Inc.
    ("UNH", "NYSE"),       # UnitedHealth Group Inc.
    ("CMCSA", "NASDAQ"),   # Comcast Corp.
    ("ADBE", "NASDAQ"),    # Adobe Inc.
    ("QCOM", "NASDAQ"),    # Qualcomm Inc.
    ("HON", "NASDAQ"),     # Honeywell International Inc.
    ("PYPL", "NASDAQ"),    # PayPal Holdings Inc.
    ("IBM", "NYSE"),       # IBM Corp.
    ("NFLX", "NASDAQ"),    # Netflix Inc.
    ("BMY", "NYSE"),       # Bristol-Myers Squibb Co.
    ("AMD", "NASDAQ"),     # Advanced Micro Devices Inc.
    ("INTC", "NASDAQ")     # Intel Corp.
]

sheets_list = [
    ("JPM", "NYSE"),
    ("BAC", "NYSE"),
    ("PDD", "NASDAQ"),
    ("MRK", "NYSE"),
    ("GOOG", "NASDAQ"),
    ("HD", "NYSE"),
    ("NVS", "NYSE"),
    ("BRK.A", "NYSE"),
    ("AAPL", "NASDAQ"),
    ("PEP", "NASDAQ"),
    ("XOM", "NYSE"),
    ("V", "NYSE"),
    ("MCD", "NYSE"),
    ("SHEL", "NYSE"),
    ("NVO", "NYSE"),
    ("META", "NASDAQ"),
    ("MA", "NYSE"),
    ("ASML", "NASDAQ"),
    ("PG", "NYSE"),
    ("TSM", "NYSE"),
    ("ACN", "NYSE"),
    ("JNJ", "NYSE"),
    ("NVDA", "NASDAQ"),
    ("MSFT", "NASDAQ"),
    ("CVX", "NYSE"),
    ("ADBE", "NASDAQ"),
    ("CSCO", "NASDAQ"),
    ("KO", "NYSE"),
    ("KO", "NYSE"),  # Duplicate entry
    ("COST", "NASDAQ"),
    ("BABA", "NYSE"),
    ("LLY", "NYSE"),
    ("TMUS", "NASDAQ"),
    ("UNH", "NYSE"),
    ("WMT", "NYSE"),
    ("AZN", "NASDAQ"),
    ("ABBV", "NYSE"),
    ("IBM", "NYSE"),
    ("ORCL", "NYSE"),
    ("TMO", "NYSE"),
    ("AMZN", "NASDAQ"),
    ("SAP", "NYSE"),
    ("TSLA", "NASDAQ"),
    ("CRM", "NYSE"),
    ("AVGO", "NASDAQ"),
    ("AMD", "NASDAQ")
]


# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('companies.db')
c = conn.cursor()

# Create table for storing company data if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS company_data (
        ticker TEXT PRIMARY KEY,
        pe_ratio REAL,
        roc REAL
    )
''')

# Function to rank the values
def rank_values(values):
    sorted_values = sorted(enumerate(values), key=lambda x: x[1])
    ranks = [0] * len(values)
    for rank, (index, _) in enumerate(sorted_values):
        ranks[index] = rank + 1  # Ranks start from 1
    return ranks

# Fetch data and insert into the database
data = []

for ticker, exchange in sheets_list:
    pe_ratio = scrapers.scrape_pe_ratio(ticker, exchange)
    roc = scrapers.scrape_roc(ticker, exchange)

    # Check if both pe_ratio and roc are valid numbers (floats)
    if isinstance(pe_ratio, (float, int)) and isinstance(roc, (float, int)):
        data.append((ticker, pe_ratio, roc))

# Check if data has at least 1 entry before proceeding
if data:
    # Rank P/E and ROC values
    pe_values = [d[1] for d in data]
    roc_values = [d[2] for d in data]
    pe_ranks = rank_values(pe_values)  # Lower P/E is better
    roc_ranks = rank_values([-roc for roc in roc_values])  # Higher ROC is better (inverting ROC)

    # Insert data into the database
    for (ticker, pe_ratio, roc), pe_rank, roc_rank in zip(data, pe_ranks, roc_ranks):
        c.execute('INSERT OR REPLACE INTO company_data (ticker, pe_ratio, roc) VALUES (?, ?, ?)',
                  (ticker, pe_ratio, roc))

    # Commit changes
    conn.commit()

    # Now fetch and sort the data based on combined ranks
    c.execute('''
        SELECT ticker, pe_ratio, roc 
        FROM company_data
        ORDER BY (SELECT COUNT(*) FROM company_data) - pe_ratio + roc DESC
    ''')

    # Display the sorted data
    sorted_data = c.fetchall()
    for row in sorted_data:
        print(row)

# Close the database connection
conn.close()
