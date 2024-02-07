import sqlite3
import re

# Database connection
db_path = '/mnt/c/Users/Djinh/Documents/Population-Genetics-Web-Tool/sql/PopulationGeneticsDB.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# File containing SQL INSERT statements
sql_file_path = '/mnt/c/Users/Djinh/Documents/Population-Genetics-Web-Tool/sql/ancestry_insert_statements.sql'

# Function to parse INSERT statements and return a list of tuples representing the rows to be inserted
def parse_insert_statements(file_path):
    with open(file_path, 'r') as file:
        insert_statements = file.read()

    # Extract values from each INSERT statement
    values_pattern = re.compile(r"VALUES\s*\((.*?)\);", re.S)
    values_raw = values_pattern.findall(insert_statements)
    
    # Convert string values to tuples
    values = []
    for value_string in values_raw:
        # Split the string into individual values, convert to the appropriate type, and append to the list
        row = tuple(eval(val) for val in value_string.split(','))
        values.append(row)
    
    return values

# Function to verify the data in the database
def verify_data_in_database(cursor, table_name, values):
    errors = []
    for row in values:
        PopulationID = row[0]
        cursor.execute(f"SELECT * FROM {table_name} WHERE PopulationID = ?", (PopulationID,))
        db_row = cursor.fetchone()
        if db_row:
            if db_row != row:
                errors.append(f"Mismatch for PopulationID {PopulationID}: expected {row}, found {db_row}")
        else:
            errors.append(f"Record with PopulationID {PopulationID} not found in the database.")

    if errors:
        print("Data verification failed with the following errors:")
        for error in errors:
            print(error)
    else:
        print("All data verified successfully. No discrepancies found.")

# Parse INSERT statements
values_to_verify = parse_insert_statements(sql_file_path)

# Verify the data
verify_data_in_database(cursor, 'Ancestry', values_to_verify)

# Close database connection
conn.close()
