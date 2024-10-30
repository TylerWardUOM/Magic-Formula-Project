// Asynchronous function to handle form submission
async function handleSubmit(event) {
    event.preventDefault(); // Prevent the default form submission to avoid page reload

    // Get input values from the form fields
    const initialCapital = document.getElementById('capital').value; // Initial investment amount
    const age = document.getElementById('age').value; // Age of the investor
    const riskTolerance = document.getElementById('riskTolerance').value; // Investor's risk tolerance level
    const yearlyContribution = document.getElementById('contribution').value; // Yearly investment contribution
    const benchmark = document.getElementById('benchmark').value; // Benchmark for comparison

    // Log input values for debugging purposes
    console.log('Input values:', { initialCapital, age, riskTolerance, yearlyContribution, benchmark });

    // Create the request payload object to send to the server
    const payload = {
        initialCapital: parseFloat(initialCapital), // Convert initial capital to a float
        age: parseInt(age), // Convert age to an integer
        riskTolerance: parseInt(riskTolerance), // Convert risk tolerance to an integer
        yearlyContribution: parseFloat(yearlyContribution), // Convert yearly contribution to a float
        benchmark: benchmark // Keep benchmark as a string
    };

    console.log('Payload:', payload); // Log the payload for debugging

    // Change the submit button to a loading state during processing
    const submitButton = document.getElementById('submit-button'); // Get the submit button element by ID
    submitButton.disabled = true; // Disable the button to prevent multiple submissions
    submitButton.innerText = 'Loading...'; // Change the button text to indicate processing

    try {
        // Make an API request to submit the investment data
        const response = await fetch('http://localhost:80/api/investment', {
            method: 'POST', // Use POST method for submitting data
            headers: {
                'Content-Type': 'application/json' // Set content type to JSON
            },
            body: JSON.stringify(payload) // Convert payload object to a JSON string
        });

        console.log('Response:', response); // Log the response object for debugging

        // Check if the response is OK (status 200-299)
        if (!response.ok) {
            throw new Error('Network response was not ok'); // Throw an error if the response is not OK
        }

        // Parse the JSON response from the server
        const data = await response.json();
        console.log('Data received:', data); // Log the data received from the server

        // Display the estimated return results to the user
        displayResults(data.estimatedReturn);
    } catch (error) {
        console.error('Error:', error); // Log any errors that occur
        document.getElementById('results').innerText = 'An error occurred while calculating projections.'; // Display an error message
    } finally {
        // Re-enable the button and reset text after processing completes
        submitButton.disabled = false; // Re-enable the button
        submitButton.innerText = 'Submit'; // Reset the button text to its original state
    }
}

// Function to display results in the results div
function displayResults(estimatedReturn) {
    const resultsDiv = document.getElementById('results'); // Get the results display element

    // Check if the estimated return value is defined
    if (estimatedReturn !== undefined) {
        resultsDiv.innerHTML = `<h3>Estimated Portfolio Value After 5 Years: £${estimatedReturn.toFixed(2)}</h3>`; // Display the estimated return
    } else {
        resultsDiv.innerHTML = '<h3>Error: Unable to calculate estimated return.</h3>'; // Display an error message if return is undefined
    }
}
