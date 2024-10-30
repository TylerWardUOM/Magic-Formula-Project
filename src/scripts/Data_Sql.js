// Front-end JavaScript to fetch and display company data in a table

// Fetch the API base URL from the server
fetch('/api/config') // Adjust to match your server endpoint
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch configuration');
        }
        return response.json();
    })
    .then(config => {
        const apiBaseUrl = config.apiBaseUrl; // Extract the API base URL from the config
        console.log(`Fetching data from: ${apiBaseUrl}/api/company_data`);

        return fetch(`${apiBaseUrl}/api/company_data`); // Fetch company data using the API base URL
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`); // Handle HTTP errors
        }
        return response.json(); // Parse the JSON from the response
    })
    .then(companyData => {
        const tableBody = document.getElementById('tableBody'); // Get the table body element

        // Check if data is empty and log a message if no data is found
        if (!companyData || companyData.length < 1) {
            console.log('No data found.'); // No data to display
            return;
        }

        // Loop through the entries in the fetched company data
        companyData.forEach(entry => {
            const exchangeCode = entry.exchange || ''; // Get the exchange code, default to empty string
            const tickerSymbol = entry.ticker || ''; // Get the ticker symbol, default to empty string
            const peRatio = entry.pe_ratio || ''; // Get the Price-to-Earnings (P/E) ratio
            const returnOnCapital = entry.roc || ''; // Get the Return on Capital (ROC) value

            // Check for error values in the data
            if (tickerSymbol === '#VALUE!' || peRatio === '#VALUE!' || returnOnCapital === 'ROC data not found') {
                return; // Skip this entry if any specified columns have error values
            }

            // Create a new table row for displaying company data
            const tableRow = document.createElement('tr');

            // Column 1: Company Button with Ticker Symbol
            const tickerCell = document.createElement('td'); // Create a cell for the ticker symbol
            const tickerButton = document.createElement('button'); // Create a button element for the ticker
            tickerButton.textContent = tickerSymbol; // Set button text to ticker symbol

            // Add event listener to button for opening the link in a new tab
            tickerButton.addEventListener('click', () => {
                window.open(`https://www.google.com/finance/quote/${tickerSymbol}:${exchangeCode}`, '_blank'); // Opens Google Finance link for the company
            });

            tickerCell.appendChild(tickerButton); // Append the button to the cell
            tableRow.appendChild(tickerCell); // Append the cell to the row

            // Column 2: Price-to-Earnings (P/E) Ratio
            const peCell = document.createElement('td'); // Create a cell for P/E ratio
            peCell.textContent = peRatio; // Set cell text to P/E ratio
            tableRow.appendChild(peCell); // Append the cell to the row

            // Column 3: Return on Capital (ROC)
            const rocCell = document.createElement('td'); // Create a cell for ROC value
            rocCell.textContent = returnOnCapital; // Set cell text to ROC value
            tableRow.appendChild(rocCell); // Append the cell to the row

            // Append the constructed row to the table body
            tableBody.appendChild(tableRow);
        });
    })
    .catch(error => console.error('Error fetching data:', error)); // Log any errors that occur during the fetch
