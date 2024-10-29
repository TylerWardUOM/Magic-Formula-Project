// Front-end JavaScript

fetch('http://localhost:3000/api/company_data')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(entries => {
        const tableBody = document.getElementById('tableBody');

        if (!entries || entries.length < 1) {
            console.log('No data found.');
            return;
        }

        // Loop through the rows in the data
        entries.forEach(row => {
            const exchange = row.exchange || ''; // Adjust column names as needed
            const ticker = row.ticker || '';
            const pe = row.pe_ratio || '';
            const roc = row.roc || '';

            // Check for error values
            if (ticker === '#VALUE!' || pe === '#VALUE!' || roc === 'ROC data not found') {
                return; // Skip this row if any of the specified columns have an error
            }

            // Create a new table row and add the cells
            const tableRow = document.createElement('tr');

            // Column 1: Company Button
            const companyCell = document.createElement('td');
            const companyButton = document.createElement('button');
            companyButton.textContent = ticker; // Set button text to company name

            // Add event listener to button for opening the link
            companyButton.addEventListener('click', () => {
                window.open(`https://www.google.com/finance/quote/${ticker}:${exchange}`, '_blank'); // Opens the link in a new tab
            });

            companyCell.appendChild(companyButton);
            tableRow.appendChild(companyCell);

            // Column 2: B Value
            const bCell = document.createElement('td');
            bCell.textContent = pe;
            tableRow.appendChild(bCell);

            // Column 3: D Value
            const dCell = document.createElement('td');
            dCell.textContent = roc;
            tableRow.appendChild(dCell);

            // Append the row to the table body
            tableBody.appendChild(tableRow);
        });
    })
    .catch(error => console.error('Error fetching data:', error));
