import sys
import json
import yfinance as yf  # Yahoo Finance library for fetching financial data
from datetime import datetime, timedelta

# This script calculates the estimated future portfolio value based on user input, 
# historical market data, and specified benchmarks (e.g., S&P 500 or Gold). 
# It takes input as a JSON string via command line arguments, processes it, 
# and returns the estimated return in JSON format.

# Function to fetch historical data for a specific ticker symbol
def fetch_historical_data(ticker, start_date):
    """Fetch historical data for a given ticker from start_date to today."""
    # Fetch historical market data from Yahoo Finance
    data = yf.download(ticker, start=start_date)
    # Return the closing price on the last available date
    return data['Close'].iloc[-1]

# Function to calculate the current portfolio value based on investment parameters
def calculate_current_portfolio_value(initialCapital, age, riskTolerance, yearlyContribution, benchmark):
    # Determine the benchmark symbol based on user input
    if benchmark.lower() == 'sp500':
        symbol = "^GSPC"  # S&P 500 Index
    elif benchmark.lower() == 'gold':
        symbol = "GC=F"  # Gold futures
    else:
        raise ValueError("Invalid benchmark specified. Use 'sp500' or 'gold'.")    
    
    # Get today's date for fetching historical data
    end_date = datetime.today().strftime('%Y-%m-%d')
    
    # Set the start date for fetching historical data (5 years ago)
    start_date = (datetime.today().replace(year=datetime.today().year - 5)).strftime('%Y-%m-%d')
    
    # Fetch historical data for the specified benchmark
    data = yf.download(symbol, start=start_date, end=end_date, progress=False)
    
    # Calculate yearly returns based on closing prices
    data['Year'] = data.index.year  # Add a column for the year
    yearly_data = data.groupby('Year')['Close'].last().pct_change().dropna()  # Calculate yearly percentage change
    
    # Initialize the portfolio value with the initial capital
    portfolio_value = initialCapital
    
    # Calculate portfolio value year by year using the yearly return rates
    for year, return_rate in yearly_data.items():
        portfolio_value = portfolio_value * (1 + return_rate) + yearlyContribution  # Update portfolio value

    return portfolio_value  # Return the estimated portfolio value after 5 years

if __name__ == "__main__":
    input_data = sys.argv[1]  # The first argument is the JSON string passed from the command line

    try:
        # Ensure that the input_data is correctly formatted as JSON
        data = json.loads(input_data)  
        # Extract relevant data from the parsed JSON
        initialCapital = data['initialCapital']
        age = data['age']
        riskTolerance = data['riskTolerance']
        yearlyContribution = data['yearlyContribution']
        benchmark = data['benchmark']
        
        # Calculate the projected portfolio value based on the input data
        estimated_value = calculate_current_portfolio_value(initialCapital, age, riskTolerance, yearlyContribution, benchmark)

        # Return the result as a JSON response
        result = {'estimatedReturn': estimated_value}
        print(json.dumps(result))  # Output the result as a JSON string

    except (json.JSONDecodeError, KeyError) as e:
        print(json.dumps({'error': 'Invalid input data'}))  # Handle any errors in input formatting
