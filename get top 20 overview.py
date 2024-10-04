import requests
import json
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

# Set up API key and symbol
api_key = 'BD15JMZFXKHB6GWG'
for symbol in top_20_companies:
    # API URLs for overview
    overview_url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}'

    # Fetch income statement, balance sheet, and cash flow data
    overview_response = requests.get(overview_url)

    # Convert responses to JSON
    overview_data = overview_response.json()

    with open(f'{symbol}_overview_sheet.json', 'w') as balance_file:
        json.dump(overview_data, balance_file, indent=4)