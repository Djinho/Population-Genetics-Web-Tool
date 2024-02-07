import sqlite3

# Example of manually populated expected data for illustration purposes
expected_data = [
    # This should be populated with actual data extracted from your INSERT statements
    # (PopulationID, Ancestry0, Ancestry1, ..., Ancestry26)
]

# Database connection setup
conn = sqlite3.connect('PopulationGeneticsDB.sqlite')
cursor = conn.cursor()

# Fetch actual data from the Ancestry table
cursor.execute('SELECT * FROM Ancestry')
actual_data = cursor.fetchall()

# Initial checks for data consistency
if not expected_data:
    print("Inconclusive: Expected data list is empty. Check your INSERT statements parsing.")
elif not actual_data:
    print("Inconclusive: No data found in the Ancestry table in the database.")
else:
    # Assuming data is present in both expected and actual datasets, we proceed with comparison
    data_mismatch_found = False
    for expected_row in expected_data:
        if expected_row not in actual_data:
            print(f"Incorrect: Data mismatch found for expected row {expected_row}.")
            data_mismatch_found = True
            break  # Stop at the first mismatch found for simplicity; remove if you want to find all mismatches
    
    if not data_mismatch_found:
        print("Correct: All expected data matches the actual data in the Ancestry table.")

# Closing the database connection
conn.close()

