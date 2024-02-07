import sqlite3

# Connect to the SQLite database
db_connection = sqlite3.connect('PopulationGeneticsDB.sqlite')  # Replace with your database name

# Create a cursor
cursor = db_connection.cursor()

# 1. Retrieve data from the Ancestry table
cursor.execute('SELECT * FROM Ancestry')
table_data = cursor.fetchall()

# 2. Read data from the SQL file
with open('ancestry_insert_statements.sql', 'r') as sql_file:
    sql_file_data = sql_file.read()

# Close the database connection
db_connection.close()

# 3. Compare table data with SQL file data
if table_data == sql_file_data:
    print("Data in the Ancestry table matches the data in the SQL file.")
else:
    print("Data in the Ancestry table does not match the data in the SQL file.")

# Optional: You can also compare the data line by line if needed
# line_by_line_comparison = table_data == sql_file_data.splitlines()
# print("Line-by-line comparison:", line_by_line_comparison)
