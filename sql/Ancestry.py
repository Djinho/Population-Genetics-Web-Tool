import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('PopulationGeneticsDB.sqlite')

# Create a cursor
cursor = conn.cursor()

# Read the SQL statements from your file and execute them
with open('ancestry_insert_statements.sql', 'r') as file:
    for line in file:
        if line.strip():  # Check if the line is not empty
            cursor.execute(line)

# Commit changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()

