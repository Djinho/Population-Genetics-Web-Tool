import sqlite3
import re

"""
This script reads and executes SQL insert statements from a specified file for a SQLite database. It ensures that each 
SNP and Population combination is unique before inserting to prevent duplicates in the database. The script assumes that 
the provided SQL insert statements are correctly formatted and contain valid SNPID and PopulationID values.

Assumptions:
1. SQL insert statements are complete and end with a semicolon ';'.
2. The database and SQL file paths are correctly specified.
3. SNPID and PopulationID are extracted from the insert statements using a regex pattern.
4. The database schema is set up to relate SNPID and PopulationID correctly.
"""

# Path to the SQLite database
database_path = 'C:\\Users\\Djinh\\Documents\\Population-Genetics-Web-Tool\\sql\\PopulationGeneticsDB.sqlite'
# Path to the SQL file with the insert statements
sql_file_path = 'C:\\Users\\Djinh\\Documents\\Population-Genetics-Web-Tool\\sql\\correct_inserts.sql'

def extract_values(statement):
    """
    Extracts the SNPID and PopulationID from the SQL insert statement.
    """
    matches = re.search(r"VALUES\s*\(\s*\(SELECT\s*SNPID\s*FROM\s*SNP_Information\s*WHERE\s*ID\s*=\s*'([^']+)'\),\s*\(SELECT\s*PopulationID\s*FROM\s*populations\s*WHERE\s*PopulationName\s*=\s*'([^']+)'\)", statement)
    if matches:
        return matches.group(1), matches.group(2)
    return None, None

def execute_sql_file(db_path, sql_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    inserted_combinations = set()  # Set to keep track of inserted SNPID and PopulationID combinations

    with open(sql_path, 'r') as sql_file:
        statement = ""
        for line in sql_file:
            # Check if the line is part of a SQL statement
            if not line.strip().endswith(';'):
                statement += line
            else:
                # The line ends a SQL statement; execute it if it's unique
                statement += line
                snpid, population_id = extract_values(statement)
                if snpid and population_id:
                    # Check if the combination is already inserted
                    if (snpid, population_id) not in inserted_combinations:
                        try:
                            cursor.execute(statement)
                            connection.commit()
                            inserted_combinations.add((snpid, population_id))
                            print(f"Inserted unique combination: SNPID = {snpid}, PopulationID = {population_id}")
                        except sqlite3.OperationalError as e:
                            print(f"An error occurred: {e}")
                statement = ""  # Reset for the next statement

    connection.close()

# Execute the function with the specified database and SQL file paths
execute_sql_file(database_path, sql_file_path)
