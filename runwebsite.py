from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Function to fetch data from the SQLite database
def get_companies():
    conn = sqlite3.connect('results.db')  # Connect to your .db file
    cur = conn.cursor()
    
    # Query the data
    cur.execute('SELECT * FROM companies')
    
    # Fetch all the rows from the database
    rows = cur.fetchall()
    
    conn.close()  # Close the connection
    return rows

# Route to display the data on the webpage
@app.route('/')
def index():
    companies = get_companies()  # Get company data from the database
    return render_template('table.html', companies=companies)

if __name__ == '__main__':
    app.run(debug=True)