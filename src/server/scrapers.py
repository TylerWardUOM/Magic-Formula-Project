import requests  # Library for making HTTP requests
from bs4 import BeautifulSoup  # Library for parsing HTML content

# This module contains functions to scrape financial metrics such as 
# Return on Capital (ROC) and Price-to-Earnings (P/E) ratio from Google Finance.

def scrape_roc(ticker, exchange):
    """Fetches the Return on Capital (ROC) for a given stock ticker and exchange."""
    # Build the URL using both the ticker and exchange
    url = f'https://www.google.com/finance/quote/{ticker}:{exchange}'
    
    # Fetch the page content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        return "Error fetching the data"  # Return error message if request fails

    # Parse the HTML content
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # Try to find the "Return on capital" (ROC) value
    try:
        # Find the table cell containing the ROC value
        roc_label = soup.find(text="Return on capital")  # Locate the label
        roc_value = roc_label.find_next('td').text.strip() if roc_label else None  # Get the next td element's text

        if roc_value:
            # Remove the percentage sign and convert to a float
            roc_value = float(roc_value.replace('%', '').strip())
            return roc_value  # Return the value as a number
        else:
            return "ROC data not found"  # Return message if ROC data is not found
    except Exception as e:
        return f"An error occurred: {str(e)}"  # Return error message if exception occurs

def scrape_pe_ratio(ticker, exchange):
    """Fetches the Price-to-Earnings (P/E) ratio for a given stock ticker and exchange."""
    # Build the URL using the ticker and exchange
    url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
    
    try:
        # Fetch the page content
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        html = response.text
        
        # Parse the HTML content
        soup = BeautifulSoup(html, 'html.parser')

        # Find the P/E ratio element
        pe_ratio_element = soup.find(text="P/E ratio")  # Locate the P/E ratio label
        
        if pe_ratio_element:
            # Navigate to the element that contains the P/E ratio value
            pe_ratio_value = pe_ratio_element.find_next(class_="P6K39c").text.strip()  # Get the value
            return float(pe_ratio_value)  # Convert to float and return
        else:
            return None  # Return None if P/E ratio element is not found
    
    except requests.RequestException as e:
        return None  # Return None if request fails
    except (ValueError, AttributeError) as e:
        return None  # Return None if there is an error in value conversion or attribute access
