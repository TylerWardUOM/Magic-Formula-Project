async function handleSubmit(event) {
    event.preventDefault(); // Prevent the default form submission

    // Get input values
    const initialCapital = document.getElementById('capital').value;
    const age = document.getElementById('age').value;
    const riskTolerance = document.getElementById('riskTolerance').value;
    const yearlyContribution = document.getElementById('contribution').value;
    const benchmark = document.getElementById('benchmark').value;

    // Log input values
    console.log('Input values:', { initialCapital, age, riskTolerance, yearlyContribution, benchmark });

    // Create the request payload
    const payload = {
        initialCapital: parseFloat(initialCapital),
        age: parseInt(age),
        riskTolerance: parseInt(riskTolerance),
        yearlyContribution: parseFloat(yearlyContribution),
        benchmark: benchmark
    };

    console.log('Payload:', payload); // Log the payload

    try {
        // Make an API request
        const response = await fetch('http://localhost:3000/api/investment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        console.log('Response:', response); // Log the response object

        // Check if the response is OK
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        // Parse the JSON response
        const data = await response.json();
        console.log('Data received:', data); // Log the data received

        // Display the results
        displayResults(data.estimatedReturn);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('results').innerText = 'An error occurred while calculating projections.';
    }
}
// Function to display results
function displayResults(estimatedReturn) {
    const resultsDiv = document.getElementById('results');

    if (estimatedReturn !== undefined) {
        resultsDiv.innerHTML = `<h3>Estimated Portfolio Value After 5 Years: £${estimatedReturn.toFixed(2)}</h3>`;
    } else {
        resultsDiv.innerHTML = '<h3>Error: Unable to calculate estimated return.</h3>';
    }
}
