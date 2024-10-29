import sys
import json

def calculate_projections(initialCapital, age, riskTolerance, yearlyContribution, benchmark):
    if benchmark == "sp500":
        expected_rate_of_return = 0.07  # 7%
    elif benchmark == "gold":
        expected_rate_of_return = 0.02  # 2%
    elif benchmark == "magicFormula":
        expected_rate_of_return = 0.08  # 8%
    else:
        expected_rate_of_return = 0

    years = 5

    # Calculate future value with yearly contributions
    future_value = initialCapital * (1 + expected_rate_of_return) ** years
    for year in range(1, years + 1):
        future_value += yearlyContribution * (1 + expected_rate_of_return) ** (years - year)

    return future_value

if __name__ == "__main__":
    input_data = sys.argv[1]  # The first argument is the JSON string

    try:
        # Ensure that the input_data is correctly formatted JSON
        data = json.loads(input_data)  
        initialCapital = data['initialCapital']
        age = data['age']
        riskTolerance = data['riskTolerance']
        yearlyContribution = data['yearlyContribution']
        benchmark = data['benchmark']
        
        # Log received input for verification
        # Calculate the projections
        estimated_value = calculate_projections(initialCapital, age, riskTolerance, yearlyContribution, benchmark)

        # Return the result as JSON
        result = {'estimatedReturn': estimated_value}
        print(json.dumps(result))  # Output the result as a JSON string

    except (json.JSONDecodeError, KeyError) as e:
        print(json.dumps({'error': 'Invalid input data'}))
