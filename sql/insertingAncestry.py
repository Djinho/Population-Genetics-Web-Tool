import sqlite3

# Path to your SQLite database
db_path = '/mnt/c/Users/Djinh/Documents/Population-Genetics-Web-Tool/sql/PopulationGeneticsDB.sqlite'

# Path to your SQL file containing the INSERT statements
sql_file_path = '/mnt/c/Users/Djinh/Documents/Population-Genetics-Web-Tool/sql/ancestry_insert_statements.sql'

def execute_sql_from_file(db_path, sql_file_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Read the SQL file
    with open(sql_file_path, 'r') as file:
        sql_script = file.read()

    # Execute each SQL statement from the file
    # Assuming each statement ends with a semicolon
    sql_commands = sql_script.split(';')
    for command in sql_commands:
        try:
            if command.strip() != '':
                cursor.execute(command)
        except Exception as e:
            print(f"An error occurred: {e}")

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("SQL script executed successfully.")

# Execute the function with the given database path and SQL file path
execute_sql_from_file(db_path, sql_file_path)
