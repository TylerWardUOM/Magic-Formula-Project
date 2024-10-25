import config from './config.js';

const range = 'Sheet4!A1:G100';
const sheetURL = `https://sheets.googleapis.com/v4/spreadsheets/${config.sheetID}/values/${range}?key=${config.apiKey}`;


// Fetch the data from Google Sheets
fetch(sheetURL)
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        const entries = data.values; // Get the values from the response
        const tableBody = document.getElementById('tableBody');

        if (!entries || entries.length < 1) {
            console.log('No data found.');
            return;
        }

        // Loop through the rows in the data, starting from the second row (to skip headers)
        for (let i = 1; i < entries.length; i++) { // Start from 1 to skip header
            const row = entries[i];
            const gValue = row[6] || ''; // Column G (index 6)
            const bValue = row[1] || ''; // Column B (index 1)
            const dValue = row[3] || ''; // Column D (index 3)

            // Check for error values
            if (gValue === '#VALUE!' || bValue === '#VALUE!' || dValue === 'ROC data not found') {
            continue; // Skip this row if any of the specified columns have an error
            }

            // Create a new table row and add the cells
            const tableRow = document.createElement('tr');
            
            const gCell = document.createElement('td');
            gCell.textContent = gValue;
            tableRow.appendChild(gCell);

            const bCell = document.createElement('td');
            bCell.textContent = bValue;
            tableRow.appendChild(bCell);

            const dCell = document.createElement('td');
            dCell.textContent = dValue;
            tableRow.appendChild(dCell);

            tableBody.appendChild(tableRow);
        }
    })
    .catch(error => console.error('Error fetching data from Google Sheets:', error));
