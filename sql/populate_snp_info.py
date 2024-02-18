import sqlite3

# Define the path to your database and SQL file
db_path = 'C:\\Users\\Djinh\\Documents\\Population-Genetics-Web-Tool\\sql\\PopulationGeneticsDB.sqlite'
sql_file_path = 'snp_insert_statements.sql'  # Replace with your actual SQL file path

# Read the SQL file
with open(sql_file_path, 'r') as file:
    sql_script = file.read()

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Execute the SQL script
try:
    cursor.executescript(sql_script)
    conn.commit()
    print("The SNP_Information table has been populated successfully.")
except sqlite3.Error as e:
    print(f"An error occurred: {e}")

# Close the connection
conn.close()
