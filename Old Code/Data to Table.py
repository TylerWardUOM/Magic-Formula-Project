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
        PERatio REAL NOT NULL,
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
    'BABA',   # Alibaba
    'PDD',
    'MRK',
    'NVS',
    'JPM',
    'BRK.A',
    'PEP',
    'MCD',
    'NVO',
    'SHELL',
    'ACN',
    'BAC',
    'KO',
    'ADBE',
    'CVX',
    'CSCO',
    'TSM',
    'ASML',
    'LLY',
    'IBM',
    'WMT',
    'TMUS',
    'UNH',
    'ABBV',
    'AZN',
    'TMO',
    'COST'
]
companies=[]
for symbol in top_20_companies:
    with open(f'C:/Users/tman0/OneDrive/Documents/Code/Magic Formula Project/Companies Data/{symbol}_overview_sheet.json', 'r') as json_file:
        overview_data = json.load(json_file)
    try:
        PERatio = float(overview_data["PERatio"])
        ROE = float(overview_data["ReturnOnEquityTTM"])
        ROE = float(overview_data["EBITDA"])/float(overview_data["MarketCapitalization"])

        print(f"PE Ratio of {symbol}: {PERatio:.2%}")
        print(f"Return on Equity (ROE) of {symbol}: {ROE:.2%}")
        company = (symbol,overview_data["Name"], round(PERatio,2), round(ROE*100,2))
        companies.append(company)


    except:
        pass

# Commit the transaction to save the changes
        # Insert multiple rows of data
PERatios = sorted(companies, key=lambda x: x[2])
ROEs = sorted(companies, key = lambda x: x[3])
ROEs = ROEs [::-1]

def get_ranks(lst):
    return {item: rank for rank, item in enumerate(lst)}

# Get the ranks for both lists
ranks1 = get_ranks(PERatios)
ranks2 = get_ranks(ROEs)

# Combine the ranks by summing them for each item
combined_ranks = {item: ranks1[item] + ranks2[item] for item in PERatios}

# Sort items by combined rank
companies = sorted(combined_ranks, key=lambda x: combined_ranks[x])
for company in companies:
    cur.execute('''
        INSERT INTO companies (symbol, company_name, PERatio, return_on_equity)
        VALUES (?, ?, ?, ?)
    ''', company)

conn.commit()

cur.execute('SELECT * FROM companies')

# Fetch all rows from the query
rows = cur.fetchall()

# Print the data
for row in rows:
    print(row)

# Close the connection
conn.close()