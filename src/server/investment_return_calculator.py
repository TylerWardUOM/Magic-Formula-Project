import sys
import json
import yfinance as yf
from datetime import datetime, timedelta

#IDEAS TO ADD
#saves the data so doesnt need to fetch from y finance every time

def fetch_historical_data(ticker, start_date):
    """Fetch historical data for a given ticker from start_date to today."""
    # Fetch historical market data
    data = yf.download(ticker, start=start_date)
    # Return the closing price on the last available date
    return data['Close'].iloc[-1]

def calculate_current_portfolio_value(initialCapital, age, riskTolerance, yearlyContribution, benchmark):
    if benchmark.lower() == 'sp500':
        symbol = "^GSPC"  # S&P 500
    elif benchmark.lower() == 'gold':
        symbol = "GC=F"  # Gold futures
    else:
        raise ValueError("Invalid benchmark specified. Use 'sp500' or 'gold'.")    
    # Get today's date
    end_date = datetime.today().strftime('%Y-%m-%d')
    
    # Fetch historical data for the S&P 500 for the last 5 years
    start_date = (datetime.today().replace(year=datetime.today().year - 5)).strftime('%Y-%m-%d')
    data = yf.download(symbol, start=start_date, end=end_date, progress=False)
    
    # Calculate the yearly returns
    data['Year'] = data.index.year
    yearly_data = data.groupby('Year')['Close'].last().pct_change().dropna()
    
    # Initialize portfolio value
    portfolio_value = initialCapital
    
    # Calculate portfolio value year by year
    for year, return_rate in yearly_data.items():
        portfolio_value = portfolio_value * (1 + return_rate) + yearlyContribution
        
    return portfolio_value

if __name__ == "__main__":
    input_data = sys.argv[1]  # The first argument is the JSON string

    try:
        # Ensure that the input_data is correctly formatted JSON
        data = json.loads(input_data)  
        initialCapital = data['initialCapital']
        age = data['age']
        riskTolerance = data['riskTolerance']
        yearlyContribution = data['yearlyContribution']
        benchmark = data['benchmark']
        
        # Log received input for verification
        # Calculate the projections
        estimated_value = calculate_current_portfolio_value(initialCapital, age, riskTolerance, yearlyContribution, benchmark)

        # Return the result as JSON
        result = {'estimatedReturn': estimated_value}
        print(json.dumps(result))  # Output the result as a JSON string

    except (json.JSONDecodeError, KeyError) as e:
        print(json.dumps({'error': 'Invalid input data'}))
