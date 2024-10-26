import requests
from bs4 import BeautifulSoup

def scrape_roc(ticker, exchange):
    # Build the URL using both the ticker and exchange
    url = f'https://www.google.com/finance/quote/{ticker}:{exchange}'
    
    # Fetch the page content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        return "Error fetching the data"

    # Parse the HTML content
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # Try to find the "Return on capital" (ROC) value
    try:
        # Find the table cell containing the ROC value
        roc_label = soup.find(text="Return on capital")
        roc_value = roc_label.find_next('td').text.strip() if roc_label else None

        if roc_value:
            # Remove the percentage sign and convert to a number
            roc_value = float(roc_value.replace('%', '').strip())
            return roc_value  # Return the value as a number
        else:
            return "ROC data not found"
    except Exception as e:
        return f"An error occurred: {str(e)}"


import requests
from bs4 import BeautifulSoup

def scrape_pe_ratio(ticker, exchange):
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
        pe_ratio_element = soup.find(text="P/E ratio")
        
        if pe_ratio_element:
            # Navigate to the element that contains the P/E ratio value
            pe_ratio_value = pe_ratio_element.find_next(class_="P6K39c").text.strip()
            return float(pe_ratio_value)
        else:
            return "P/E Ratio data not found"
    
    except requests.RequestException as e:
        return f"Error fetching data: {e}"
    except (ValueError, AttributeError) as e:
        return "Error parsing P/E Ratio data"

print(scrape_pe_ratio("PDD","NASDAQ"))
print(scrape_roc("PDD","NASDAQ"))