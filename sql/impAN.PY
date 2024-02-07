import sqlite3

# Define the path to your database and the SQL file
database_path = '/mnt/c/Users/Djinh/Documents/Population-Genetics-Web-Tool/sql/PopulationGeneticsDB.sqlite'
sql_file_path = '/mnt/c/Users/Djinh/Documents/Population-Genetics-Web-Tool/sql/ancestry_insert_statements.sql'

# Connect to the SQLite database
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Read and execute the SQL file
with open(sql_file_path, 'r') as sql_file:
    sql_script = sql_file.read()
cursor.executescript(sql_script)

# Commit the changes and close the connection
conn.commit()
conn.close()

print('Data imported successfully into Ancestry table.')
