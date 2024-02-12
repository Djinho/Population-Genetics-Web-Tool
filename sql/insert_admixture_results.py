import sqlite3

# Path to your SQLite database
db_path = 'C:\\Users\\Djinh\\Documents\\Population-Genetics-Web-Tool\\sql\\PopulationGeneticsDB.sqlite'

# Path to your SQL file with INSERT statements for the admixture_results table
sql_file_path = 'C:\\Users\\Djinh\\Documents\\Population-Genetics-Web-Tool\\sql\\admixture_results_inserts_updated.sql'

# Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Read SQL file
with open(sql_file_path, 'r') as file:
    sql_script = file.read()

# Execute SQL script
try:
    cursor.executescript(sql_script)
    conn.commit()
    print("Admixture results data inserted successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the database connection
    conn.close()
