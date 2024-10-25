import requests
import json
top_20_companies = [
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

# Set up API key and symbol
api_key = 'BD15JMZFXKHB6GWG'
for symbol in top_20_companies:
    # API URLs for overview
    overview_url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}'

    # Fetch income statement, balance sheet, and cash flow data
    overview_response = requests.get(overview_url)

    # Convert responses to JSON
    overview_data = overview_response.json()

    with open(f'C:/Users/tman0/OneDrive/Documents/Code/Magic Formula Project/Companies Data/{symbol}_overview_sheet.json', 'w') as balance_file:
        json.dump(overview_data, balance_file, indent=4)