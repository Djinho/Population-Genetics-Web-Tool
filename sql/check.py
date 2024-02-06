import sqlite3

def check_imported_data(db_path='PopulationGeneticsDB.sqlite'):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to select all data from PCACoordinates
    query = "SELECT * FROM PCACoordinates ORDER BY PopulationID"

    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        # Check if any rows are returned
        if rows:
            print("Data has been imported correctly. Displaying first 5 rows:")
            for row in rows[:5]:  # Display the first 5 rows
                print(row)
        else:
            print("No data found in PCACoordinates table.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        conn.close()

# Specify the path to your SQLite database file if it's different
db_path = 'PopulationGeneticsDB.sqlite'
check_imported_data(db_path)
