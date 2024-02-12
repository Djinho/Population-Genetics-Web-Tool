import sqlite3

# Corrected path for SQLite database in WSL
db_path = '/mnt/c/Users/Djinh/Documents/Population-Genetics-Web-Tool/sql/PopulationGeneticsDB.sqlite'

# Corrected path for your SQL file with INSERT statements in WSL
sql_file_path = '/mnt/c/Users/Djinh/Documents/Population-Genetics-Web-Tool/sql/pca_coordinates_inserts_updated.sql'

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
    print("Data inserted successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the database connection
    conn.close()

