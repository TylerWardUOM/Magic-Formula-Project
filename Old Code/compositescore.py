import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('results.db')

# Create a cursor object
cursor = conn.cursor()

# SQL query to calculate composite score and sort by it
# Higher scores are better, so we order by descending
query = '''
SELECT  symbol,
        company_name,
       earnings_yield,
       return_on_equity,
       (earnings_yield + return_on_equity) AS composite_score
FROM companies
ORDER BY composite_score DESC;
'''

# Execute the query
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Print the sorted results
print("Sorted Companies by Magic Formula:")
print("{:<20} {:<15} {:<20} {:<15}{:<20}".format('Symbol','Company Name', 'Earnings Yield', 'Return on Capital', 'Composite Score'))
for row in results:
    print("{:<20} {:<15} {:<20} {:<15}{:<20}".format(row[0], row[1], row[2], row[3],row[4]))

# Close the cursor and connection
cursor.close()
conn.close()