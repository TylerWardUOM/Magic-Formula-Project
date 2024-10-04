import json
companies=['AAPL','NVDA','MSFT']
for x in range(0,10):
    for i in companies:
        symbol=i
        with open(f'C:/Users/tman0/OneDrive/Documents/Code/Magic Formula Project/Companies Data/{symbol}_balance_sheet.json', 'r') as json_file:
            balance_data = json.load(json_file)
        with open(f'C:/Users/tman0/OneDrive/Documents/Code/Magic Formula Project/Companies Data/{symbol}_cash_flow_sheet.json', 'r') as json_file:
            cashflow_data = json.load(json_file)
        with open(f'C:/Users/tman0/OneDrive/Documents/Code/Magic Formula Project/Companies Data/{symbol}_income_statement.json', 'r') as json_file:
            income_data = json.load(json_file)
        with open(f'C:/Users/tman0/OneDrive/Documents/Code/Magic Formula Project/Companies Data/{symbol}_overview_sheet.json', 'r') as json_file:
            overview_data = json.load(json_file)        # Extracting the most recent annual report data
        # Income Statement
        net_income = float(income_data['quarterlyReports'][x]['netIncome'])  # Net Income

        # Cash Flow Statement
        dividends_paid = float(cashflow_data['quarterlyReports'][x]['dividendPayout'])  # Dividends paid

        # Balance Sheet
        total_debt = float(balance_data['quarterlyReports'][x]['totalLiabilities'])  # Total Debt
        total_equity = float(balance_data['quarterlyReports'][x]['totalShareholderEquity'])  # Total Equity

        # Calculate ROIC = (Net Income - Dividends) / (Debt + Equity)
        invested_capital = total_debt + total_equity
        roic = (net_income - dividends_paid) / invested_capital

        # Print the ROIC result
        print(f"Return on Invested Capital (ROIC) for {symbol}: {roic:.2%}")

        # Extracting the most recent annual report data
        # Income Statement
        ebit = float(income_data['quarterlyReports'][x]['ebit'])  # Earnings Before Interest and Taxes (EBIT)

        # Balance Sheet
        total_debt = float(balance_data['quarterlyReports'][x]['totalLiabilities'])  # Total Debt (Liabilities)
        total_equity = float(balance_data['quarterlyReports'][x]['totalShareholderEquity'])  # Total Equity

        # Calculate Total Capital Employed (Debt + Equity)
        total_capital_employed = total_debt + total_equity

        # Calculate Return on Capital (ROC)
        roc = ebit / total_capital_employed

        # Print the ROC result
        print(f"Return on Capital (ROC) for {symbol}: {roc:.2%}")
        market_cap = float(overview_data['MarketCapitalization'])
        #total_debt = float(balance_data['currentDebt']) already got
        cash = float(overview_data['CashAndCashEquivalents'])
        
        # Enterprise Value (EV)
        ev = market_cap + total_debt - cash

    # Calculate Earnings Yield (EY) and Return on Capital (ROC)
        
        # Extract necessary data
        ebit = float(income_data['annualReports'][0]['ebit'])  # Most recent year's EBIT
        total_debt = float(balance_data['annualReports'][0]['totalLiabilities'])
        total_equity = float(balance_data['annualReports'][0]['totalShareholderEquity'])
        
        
        # Earnings Yield (EY)
        earnings_yield = ebit / ev
        
        # Return on Capital (ROC)
        total_capital_employed = total_debt + total_equity
        return_on_capital = ebit / total_capital_employed
        
        print(f"Earnings Yield (EY): {earnings_yield:.2%}")
        print(f"Return on Capital (ROC): {roc:.2%}")
    print(balance_data['quarterlyReports'][x]['fiscalDateEnding'])