import json
import sqlite3

# 1. Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('results.db')
# Create a cursor object using the connection
cur = conn.cursor()
# 2. Create a table

cur.execute('''
    CREATE TABLE IF NOT EXISTS companies (
        symbol TEXT NOT NULL,
        company_name TEXT NOT NULL,
        earnings_yield REAL NOT NULL,
        return_on_equity REAL NOT NULL
    )
''')
cur.execute('''
    DELETE FROM companies
''')
# Commit the transaction to save the changes
conn.commit()

top_20_companies = [
    'AAPL',   # Apple
    'MSFT',   # Microsoft
    'GOOGL',  # Alphabet (Google)
    'AMZN',   # Amazon
    'NVDA',   # Nvidia
    'TSLA',   # Tesla
    'META',   # Meta Platforms (Facebook)
    'BRK.B',  # Berkshire Hathaway
    'TSM',    # Taiwan Semiconductor
    'V',      # Visa
    'JNJ',    # Johnson & Johnson
    'XOM',    # Exxon Mobil
    'WMT',    # Walmart
    'LVMUY',  # LVMH Moet Hennessy Louis Vuitton
    'PG',     # Procter & Gamble
    'NSRGY',  # Nestlé
    'MA',     # Mastercard
    'UNH',    # UnitedHealth Group
    'HD',     # Home Depot
    'BABA'    # Alibaba
]
for symbol in top_20_companies:
    with open(f'C:/Users/tman0/OneDrive/Documents/Code/Magic Formula Project/Companies Data/{symbol}_overview_sheet.json', 'r') as json_file:
        overview_data = json.load(json_file)
    try:
        EVToEBITDA = float(overview_data["EVToEBITDA"])
        EarningsYield = (1/EVToEBITDA)
        ROE = float(overview_data["ReturnOnEquityTTM"])

        print(f"Earnings Yield (EY) of {symbol}: {EarningsYield:.2%}")
        print(f"Return on Equity (ROE) of {symbol}: {ROE:.2%}")
        company = (symbol,overview_data["Name"], round(EarningsYield*100,2), round(ROE*100,2))

        # Insert multiple rows of data
        cur.execute('''
            INSERT INTO companies (symbol, company_name, earnings_yield, return_on_equity)
            VALUES (?, ?, ?, ?)
        ''', company)
    except:
        pass

# Commit the transaction to save the changes
conn.commit()

cur.execute('SELECT * FROM companies')

# Fetch all rows from the query
rows = cur.fetchall()

# Print the data
for row in rows:
    print(row)

# Close the connection
conn.close()