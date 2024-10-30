// server.js
const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors'); // Import the cors middleware
const { exec } = require('child_process'); // Import exec to run Python script
const cron = require('node-cron'); // Import node-cron for scheduling
const path = require('path');

const app = express();
const PORT = 3000;
const dbPath = path.join(__dirname, '../../data/companies.db');
const pythonScriptPath = 'main.py'; // Relative path to your Python script

app.use(cors()); // Enable CORS for all routes
app.use(express.json()); // This line must be present to parse JSON request bodies


console.log('Starting server...'); // Check if this appears

// Schedule to run the Python script at 4:00 PM EST every day Based on servers times zone so will need to be adjusted
cron.schedule('* 16 * * *', () => {
    console.log('Running Python script...');

    exec(`py ${pythonScriptPath}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return;
        }
        console.log(`stdout: ${stdout}`);
    });
});

// New endpoint to force run the Python script
app.get('/api/run_script', (req, res) => {
    console.log('Received request to run Python script...');

    exec(`py ${pythonScriptPath}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error.message}`);
            return res.status(500).send('Failed to execute script');
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return res.status(500).send('Script executed with errors');
        }
        console.log(`stdout: ${stdout}`);
        res.send('Python script executed successfully');
    });
});


app.post('/api/investment', (req, res) => {
    console.log('Received request at /api/investment'); // Check if this appears
    const { initialCapital, age, riskTolerance, yearlyContribution, benchmark } = req.body;

    // Prepare the data to be sent to the Python script
    const inputData = JSON.stringify({ initialCapital, age, riskTolerance, yearlyContribution, benchmark });


    // Call the Python script
    exec(`py investment_return_calculator.py "${inputData.replace(/"/g, '\\"')}"`, (error, stdout, stderr) => {


        if (error) {
            console.error(`Error executing Python script: ${error.message}`);
            return res.status(500).json({ error: 'Error calculating investment return' });
        }
        
        // Parse the output from the Python script
        try {
            const result = JSON.parse(stdout);
            res.json(result);
        } catch (jsonError) {
            console.error('Error parsing JSON:', jsonError);
            return res.status(500).json({ error: 'Error parsing response from Python script' });
        }
    });
});




// Existing endpoint to get company data
app.get('/api/company_data', (req, res) => {
    console.log('Received request at /api/company_data'); // Check if this appears
    const db = new sqlite3.Database(dbPath, sqlite3.OPEN_READONLY, (err) => {
        if (err) {
            console.error('Error connecting to the database:', err.message);
            res.status(500).send('Database connection failed');
            return;
        }
    });

    const sql = `SELECT ticker, exchange, pe_ratio, roc FROM company_data ORDER BY combined_rank ASC`; // Adjust table name as needed

    db.all(sql, [], (err, rows) => {
        if (err) {
            console.error('Error querying the database:', err.message);
            res.status(500).send('Failed to retrieve data');
        } else {
            console.log('Data retrieved successfully'); // Check if this appears
            res.json(rows);
        }
    });

    db.close();
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
