import sqlite3
import re

# Define the path to your database and SQL file
database_path = '/mnt/c/Users/Djinh/Documents/Population-Genetics-Web-Tool/sql/PopulationGeneticsDB.sqlite'
sql_file_path = '/mnt/c/Users/Djinh/Documents/Population-Genetics-Web-Tool/sql/ancestry_insert_statements.sql'

# Function to parse SQL insert statements
def parse_sql_inserts(file_path):
    expected_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Match the VALUES part of the SQL statement
            match = re.search(r"VALUES \(([^)]+)\);", line)
            if match:
                values_str = match.group(1)
                # Split values and convert them to appropriate types
                values = values_str.split(', ')
                # Assuming the first value is PopulationID and should be an integer
                population_id = int(float(values[0]))  # Convert to float first to handle any decimal, then to int
                ancestries = tuple(float(val) for val in values[1:])  # Convert the rest to floats
                expected_data[population_id] = ancestries
    return expected_data

# Parse the SQL file to get expected values
expected_values = parse_sql_inserts(sql_file_path)

# Connect to the SQLite database
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Query to select all data from Ancestry table
query = "SELECT * FROM Ancestry"
cursor.execute(query)

# Fetch all records
records = cursor.fetchall()

# Initialize counters
correct = 0
incorrect = 0
inconclusive = 0

# Verification logic
for record in records:
    population_id = record[0]  # Assuming the first column is PopulationID
    actual_values = record[1:]  # Exclude PopulationID for comparison
    
    if population_id in expected_values:
        expected = expected_values[population_id]
        if actual_values == expected:
            correct += 1
        else:
            print(f"PopulationID {population_id}: Incorrect")
            incorrect += 1
    else:
        print(f"PopulationID {population_id}: Inconclusive (no expected values provided)")
        inconclusive += 1

# Close the database connection
conn.close()

# Summary
print(f"\nData verification completed. Correct: {correct}, Incorrect: {incorrect}, Inconclusive: {inconclusive}.")
