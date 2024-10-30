// This script fetches company data from a Google Sheet and displays it in a table format.
// It retrieves the company's name, exchange code, P/E ratio, and ROC from specified columns.

import config from '../../config/config.js'; // Importing configuration for API access

// Define the range of cells to fetch from Google Sheets
const range = 'Sheet4!A1:H100'; // Updated range to include Column G
const sheetURL = `https://sheets.googleapis.com/v4/spreadsheets/${config.sheetID}/values/${range}?key=${config.apiKey}`; // Construct the URL for the API request

// Fetch the data from Google Sheets
fetch(sheetURL)
    .then(response => {
        // Check if the response is OK (status 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`); // Handle any HTTP errors
        }
        return response.json(); // Parse the JSON response
    })
    .then(data => {
        const entries = data.values; // Extract the values from the response
        const tableBody = document.getElementById('tableBody'); // Get the table body element for appending rows

        // Check if the data contains any entries
        if (!entries || entries.length < 1) {
            console.log('No data found.'); // Log a message if no data is present
            return; // Exit the function if there's no data
        }

        // Loop through the rows in the data, starting from the second row to skip headers
        for (let i = 1; i < entries.length; i++) { // Start from index 1 to skip the header row
            const row = entries[i]; // Get the current row of data
            
            // Extract relevant column values from the row
            const companyName = row[6] || ''; // Column G (company name, index 6)
            const exchangeCode = row[7] || ''; // Column H (exchange code, index 7)
            const peRatio = row[1] || ''; // Column B (P/E ratio, index 1)
            const rocValue = row[3] || ''; // Column D (ROC value, index 3)

            // Check for error values in the extracted data
            if (companyName === '#VALUE!' || peRatio === '#VALUE!' || rocValue === 'ROC data not found') {
                continue; // Skip this row if any specified columns have error values
            }

            // Create a new table row to display the data
            const tableRow = document.createElement('tr');

            // Column 1: Company Button with Company Name
            const companyCell = document.createElement('td'); // Create a new cell for the company button
            const companyButton = document.createElement('button'); // Create a button element for the company
            companyButton.textContent = companyName; // Set the button text to the company name

            // Add an event listener to the button to open the company's finance page
            companyButton.addEventListener('click', () => {
                window.open(`https://www.google.com/finance/quote/${companyName}:${exchangeCode}`, '_blank'); // Open the link in a new tab
            });

            companyCell.appendChild(companyButton); // Append the button to the cell
            tableRow.appendChild(companyCell); // Append the cell to the row

            // Column 2: P/E Ratio
            const peCell = document.createElement('td'); // Create a cell for P/E Ratio
            peCell.textContent = peRatio; // Set cell text to P/E Ratio
            tableRow.appendChild(peCell); // Append the cell to the row

            // Column 3: ROC Value
            const rocCell = document.createElement('td'); // Create a cell for ROC Value
            rocCell.textContent = rocValue; // Set cell text to ROC Value
            tableRow.appendChild(rocCell); // Append the cell to the row

            // Append the constructed row to the table body
            tableBody.appendChild(tableRow);
        }
    })
    .catch(error => console.error('Error fetching data from Google Sheets:', error)); // Log any errors that occur during the fetch process
