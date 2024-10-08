import yfinance as yf

# Function to calculate ROC
def calculate_roc(ticker):
    # Get the stock data
    stock = yf.Ticker(ticker)

    # Fetch financials
    income_statement = stock.quarterly_financials
    balance_sheet = stock.quarterly_balance_sheet

    # Check the latest annual values
    try:
        operating_income = income_statement.loc['Operating Income'][0]  # Most recent value
        total_assets = balance_sheet.loc['Total Assets'][0]  # Most recent value
        current_liabilities = balance_sheet.loc['Current Liabilities'][0]  # Most recent value
        # If you prefer to calculate Capital Employed differently, uncomment the following lines
        # total_equity = balance_sheet.loc['Ordinary Shares Number'][0]  # Adjust according to your data structure
        # total_debt = balance_sheet.loc['Total Debt Net Lease Liab'][0]  # Ensure you include all liabilities
        # capital_employed = total_equity + total_debt
        
        # Assuming a tax rate; adjust according to Apple's effective tax rate
        tax_rate = 0.21  # Example: 21% corporate tax rate

        # Calculate NOPAT
        nopat = operating_income * (1 - tax_rate)

        # Calculate Capital Employed
        capital_employed = total_assets - current_liabilities

        # Calculate ROC
        roc = nopat / capital_employed

        return roc
    
    except KeyError as e:
        print(f"Error retrieving data: {e}")
        return None

# Example usage
ticker_symbol = 'AAPL'
roc = calculate_roc(ticker_symbol)

if roc is not None:
    print(f"Return on Capital (ROC) for {ticker_symbol}: {roc:.2%}")
