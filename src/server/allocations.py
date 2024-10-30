import sys
import json
import yfinance as yf  # Yahoo Finance library for fetching financial data
import scrapers as scrapers  # Custom scrapers for fetching financial metrics
import sqlite3  # SQLite library for database operations


# Existing code (with database setup, ranking functions, etc.)

# Define a function to allocate portfolio based on Magic Formula rankings
def allocate_portfolio(risk_threshold):
    """Allocate portfolio based on top-ranked companies by combined rank.

    Args:
        num_companies (int): Number of top-ranked companies to include in the portfolio.

    Returns:
        dict: Dictionary with ticker symbols as keys and allocation percentages as values.
    """

     # Determine the number of companies based on risk tolerance
    min_companies = 5    # Minimum number of companies for high risk
    max_companies = 30   # Maximum number of companies for low risk
    num_companies = max_companies - ((risk_threshold - 1) * (max_companies - min_companies) // 9)
    # Connect to SQLite database
    conn = sqlite3.connect('data\companies.db')
    c = conn.cursor()

    # Fetch top-ranked companies from the database
    c.execute('''
        SELECT ticker, exchange, combined_rank
        FROM company_data
        ORDER BY combined_rank ASC  -- Lower combined rank is better
        LIMIT ?
    ''', (num_companies,))

    # Retrieve and close the database connection
    top_companies = c.fetchall()
    conn.close()

    # Calculate weights based on ranking: lower combined_rank gets more weight
    # Use a factor to make allocation proportional to 1/rank (adjust as needed)
    weights = [1 / (i + 1) for i in range(len(top_companies))]
    total_weight = sum(weights)
    allocations = {company[0]: weight / total_weight for company, weight in zip(top_companies, weights)}

    return allocations


# Example usage
if __name__ == '__main__':
    risk_tolerance = int(sys.argv[1])  # Receive risk tolerance as a command-line argument
    portfolio_allocations = allocate_portfolio(risk_tolerance)
    
    # Print allocations as JSON string
    print(json.dumps(portfolio_allocations))