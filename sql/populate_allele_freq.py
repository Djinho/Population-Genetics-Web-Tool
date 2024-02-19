import sqlite3

# Define the path to the SQL file and the SQLite database
sql_file_path = 'update_allele_frequencies_adjusted.sql'
database_path = 'PopulationGeneticsDB.sqlite'  # Update with the path to your database if necessary

# Connect to the SQLite database
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Read and execute each SQL command from the file
with open(sql_file_path, 'r') as file:
    sql_statements = file.readlines()
    for statement in sql_statements:
        try:
            cursor.execute(statement)
        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("SQL updates have been executed.")
