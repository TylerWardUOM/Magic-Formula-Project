// server.js
// This file sets up an Express server that interacts with a SQLite database,
// executes Python scripts for investment calculations and scraping, and 
// provides RESTful API endpoints for client requests.

const express = require('express'); // Import Express framework
const sqlite3 = require('sqlite3').verbose(); // Import SQLite3 for database interactions
const cors = require('cors'); // Import CORS middleware to allow cross-origin requests
const { exec } = require('child_process'); // Import exec to run Python scripts
const cron = require('node-cron'); // Import node-cron for scheduling tasks
const path = require('path'); // Import path module for handling file paths
require('dotenv').config(); // Load environment variables from .env file


const app = express(); // Create an Express application
const pycmd = process.env.pycmd || 'python'
const PORT = process.env.PORT || 80; // Use PORT from env or default to 80
const HOST = process.env.HOST || 'localhost'; // Use HOST from env or default to localhost
const dbPath = path.join(__dirname, '../../data/companies.db'); // Path to the SQLite database
const pythonScriptPath = 'src/server/main.py'; // Relative path to the Python script

app.use(cors()); // Enable CORS for all routes
app.use(express.json()); // Middleware to parse JSON request bodies

console.log('Starting server...'); // Log to console when server starts

// Endpoint to get the API base URL
app.get('/api/config', (req, res) => {
    res.json({
        apiBaseUrl: process.env.API_BASE_URL || 'http://localhost:80'
    });
});

// Serve static files from the 'src/views' directory
app.use(express.static(path.join(__dirname, '../../'))); 

// Route to serve index.html on root request
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../views', 'index.html')); // Adjusted path
});

// Schedule to run the Python script at 4:00 PM EST every day
// Note: Based on the server's time zone, this may need adjustment
cron.schedule('00 16 * * *', () => {
    console.log('Running Python script at:', new Date().toLocaleString());

    exec(`${pycmd} ${pythonScriptPath}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return;
        }
        console.log(`stdout: ${stdout}`); // Log the output from the Python script
    });
});

// New endpoint to force run the Python script
app.get('/api/run_script', (req, res) => {
    console.log('Received request to run Python script...');

    exec(`${pycmd} ${pythonScriptPath}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error.message}`);
            return res.status(500).send('Failed to execute script'); // Send error response
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return res.status(500).send('Script executed with errors'); // Send error response
        }
        console.log(`stdout: ${stdout}`); // Log the output from the Python script
        res.send('Python script executed successfully'); // Send success response
    });
});

// Endpoint to calculate investment returns
app.post('/api/investment', (req, res) => {
    console.log('Received request at /api/investment'); // Log when a request is received
    const { initialCapital, age, riskTolerance, yearlyContribution, benchmark } = req.body; // Extract data from request

    // Prepare the data to be sent to the Python script
    const inputData = JSON.stringify({ initialCapital, age, riskTolerance, yearlyContribution, benchmark });

    // Call the Python script
    exec(`${pycmd} src/server/investment_return_calculator.py "${inputData.replace(/"/g, '\\"')}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error.message}`);
            return res.status(500).json({ error: 'Error calculating investment return' }); // Send error response
        }

        // Parse the output from the Python script
        try {
            const result = JSON.parse(stdout); // Parse the JSON output
            console.log('Data retrieved successfully'); // Log when data is retrieved
            res.json(result); // Send the result as JSON response
        } catch (jsonError) {
            console.error('Error parsing JSON:', jsonError);
            return res.status(500).json({ error: 'Error parsing response from Python script' }); // Send error response
        }
    });
});

// Existing endpoint to get company data
app.get('/api/company_data', (req, res) => {
    console.log('Received request at /api/company_data'); // Log when a request is received
    const db = new sqlite3.Database(dbPath, sqlite3.OPEN_READONLY, (err) => {
        if (err) {
            console.error('Error connecting to the database:', err.message);
            res.status(500).send('Database connection failed'); // Send error response if connection fails
            return;
        }
    });

    // SQL query to retrieve company data
    const sql = `SELECT ticker, exchange, pe_ratio, roc FROM company_data ORDER BY combined_rank ASC`; // Adjust table name as needed

    db.all(sql, [], (err, rows) => {
        if (err) {
            console.error('Error querying the database:', err.message);
            res.status(500).send('Failed to retrieve data'); // Send error response if query fails
        } else {
            console.log('Data retrieved successfully'); // Log when data is retrieved
            res.json(rows); // Send the retrieved data as JSON response
        }
    });

    db.close(); // Close the database connection
});

app.get('/api/portfolio', (req, res) => {
    // Get the risk tolerance from query parameters or default to 5
    const riskTolerance = req.query.risk_tolerance || 5;

    // Run the Python script with the risk tolerance as an argument
    exec(`${pycmd} src/server/allocations.py ${riskTolerance}`, (error, stdout, stderr) => {
        if (error) {
            console.error('Error executing Python script:', error);
            return res.status(500).json({ error: 'Error executing Python script' });
        }

        if (stderr) {
            console.error('Python script stderr:', stderr);
            return res.status(500).json({ error: 'Python script returned an error' });
        }

        try {
            // Parse the JSON output from Python script
            const result = JSON.parse(stdout);
            console.log('Data retrieved successfully');
            res.json(result); // Send the result as JSON response
        } catch (jsonError) {
            console.error('Error parsing JSON:', jsonError);
            return res.status(500).json({ error: 'Error parsing response from Python script' });
        }
    });
});

// Start the Express server
app.listen(PORT, () => {
    console.log(`Server running on http://${HOST}:${PORT}`); // Log server running message
});
