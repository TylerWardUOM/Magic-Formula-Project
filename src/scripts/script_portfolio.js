// Define the base URL for the API, which should be set dynamically in your app
let apiBaseUrl = 'http://localhost:80'; // Default value for local development

// Function to fetch the API base URL from the server
async function fetchApiBaseUrl() {
    try {
        const response = await fetch('/api/config'); // Fetch the config from your server
        if (!response.ok) {
            throw new Error('Failed to fetch configuration');
        }
        const config = await response.json(); // Parse the JSON response
        apiBaseUrl = config.apiBaseUrl; // Set the global variable to the fetched API base URL
        console.log(`API Base URL set to: ${apiBaseUrl}`); // Log the API base URL for debugging
    } catch (error) {
        console.error('Error fetching API base URL:', error); // Log any errors
    }
}

// Call the fetchApiBaseUrl function to initialize the base URL
fetchApiBaseUrl();

async function loadPortfolioData() {
    const riskTolerance = document.getElementById('risk-tolerance').value; // Get risk tolerance value

    try {
        // Make a GET request to the portfolio API endpoint, using the risk tolerance as a query parameter
        const response = await fetch(`${apiBaseUrl}/api/portfolio?risk_tolerance=${riskTolerance}`);
        
        // Check if the request was successful
        if (!response.ok) throw new Error(`Failed to fetch portfolio data: ${response.statusText}`);
        
        // Parse the response data (assuming it's JSON)
        const portfolioData = await response.json();
        
        // Reference the table body element and clear any previous data
        const tableBody = document.getElementById('portfolioTableBody');
        tableBody.innerHTML = '';  // Clear previous rows

        // Loop through the portfolio data and add rows to the table
        for (const [ticker, allocation] of Object.entries(portfolioData)) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${ticker}</td>
                <td>${(allocation * 100).toFixed(2)}%</td>
            `;
            tableBody.appendChild(row);  // Append the new row to the table body
        }
    } catch (error) {
        // Log any errors that occur during the fetch
        console.error('Error loading portfolio data:', error);
    }
}

// Call loadPortfolioData function when the risk tolerance input changes
document.getElementById('risk-tolerance').addEventListener('change', loadPortfolioData);
