import yfinance as yf

# Define the company symbol
symbol = input()  # Replace with the desired company's stock symbol

# Create a Ticker object
ticker = yf.Ticker(symbol)

# Fetch the balance sheet
balance_sheet = ticker.quarterly_balance_sheet
financials = ticker.quarterly_financials

# Display available columns in the balance sheet for debugging
# print("Available columns in balance sheet:")
#print(balance_sheet.columns)
# print('Balance Sheet\n')
# print(balance_sheet.info)
# print('financials\n')

# print(financials.info)
#print(ticker.cashflow.info)
#print(ticker.info)

print(financials.loc['Net Income'][0])
tax=0.21
total_equity = balance_sheet.loc['Total Assets'][0] - balance_sheet.loc['Total Liabilities Net Minority Interest'][0] # Adjust according to your data structure
total_debt = balance_sheet.loc['Total Debt'][0]  # Ensure you include all liabilities
invested_capital = balance_sheet.loc['Invested Capital'][0]
NOPAT =  financials.loc['EBIT'][0]*(1-tax)


capital_employed = total_equity #+ total_debt #- balance_sheet.loc['Cash And Cash Equivalents'][0]
print(NOPAT)
print(invested_capital)
print(100*NOPAT/capital_employed)
print(100*NOPAT/invested_capital)