#I7VI9ZCYF8E4072X
import requests
import json

# Set up API key and symbol
api_key = 'BD15JMZFXKHB6GWG'
symbol = 'AMZN'  # Apple Inc.

# API URLs for income statement, balance sheet, and cash flow
income_url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={api_key}'
balance_url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={api_key}'
cashflow_url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={api_key}'

# Fetch income statement, balance sheet, and cash flow data
income_response = requests.get(income_url)
balance_response = requests.get(balance_url)
cashflow_response = requests.get(cashflow_url)

# Convert responses to JSON
income_data = income_response.json()
balance_data = balance_response.json()
cashflow_data = cashflow_response.json()

# Dump income statement JSON data into a file
with open(f'{symbol}_income_statement.json', 'w') as income_file:
    json.dump(income_data, income_file, indent=4)  # indent=4 for pretty formatting

# Dump balance sheet JSON data into a file
with open(f'{symbol}_balance_sheet.json', 'w') as balance_file:
    json.dump(balance_data, balance_file, indent=4)

# Dump cash flow sheet JSON data into a file
with open(f'{symbol}_cash_flow_sheet.json', 'w') as balance_file:
    json.dump(cashflow_data, balance_file, indent=4)

# Extracting the most recent annual report data
# Income Statement
net_income = float(income_data['annualReports'][0]['netIncome'])  # Net Income

# Cash Flow Statement
dividends_paid = float(cashflow_data['annualReports'][0]['dividendPayout'])  # Dividends paid

# Balance Sheet
total_debt = float(balance_data['annualReports'][0]['totalLiabilities'])  # Total Debt
total_equity = float(balance_data['annualReports'][0]['totalShareholderEquity'])  # Total Equity

# Calculate ROIC = (Net Income - Dividends) / (Debt + Equity)
invested_capital = total_debt + total_equity
roic = (net_income - dividends_paid) / invested_capital

# Print the ROIC result
print(f"Return on Invested Capital (ROIC) for {symbol}: {roic:.2%}")

# Extracting the most recent annual report data
# Income Statement
ebit = float(income_data['annualReports'][0]['ebit'])  # Earnings Before Interest and Taxes (EBIT)

# Balance Sheet
total_debt = float(balance_data['annualReports'][0]['totalLiabilities'])  # Total Debt (Liabilities)
total_equity = float(balance_data['annualReports'][0]['totalShareholderEquity'])  # Total Equity

# Calculate Total Capital Employed (Debt + Equity)
total_capital_employed = total_debt + total_equity

# Calculate Return on Capital (ROC)
roc = ebit / total_capital_employed

# Print the ROC result
print(f"Return on Capital (ROC) for {symbol}: {roc:.2%}")