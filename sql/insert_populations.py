import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('PopulationGeneticsDB.sqlite')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# List of populations to insert
populations = [
    (1, 'SIB'),
    (2, 'GBR'),
    (3, 'FIN'),
    (4, 'CHS'),
    (5, 'PUR'),
    (6, 'CDX'),
    (7, 'CLM'),
    (8, 'IBS'),
    (9, 'PEL'),
    (10, 'PJL'),
    (11, 'KHV'),
    (12, 'ACB'),
    (13, 'GWD'),
    (14, 'ESN'),
    (15, 'BEB'),
    (16, 'MSL'),
    (17, 'STU'),
    (18, 'ITU'),
    (19, 'CEU'),
    (20, 'YRI'),
    (21, 'CHB'),
    (22, 'JPT'),
    (23, 'LWK'),
    (24, 'ASW'),
    (25, 'MXL'),
    (26, 'TSI'),
    (27, 'GIH')
]

# Insert populations into the Populations table
try:
    cursor.executemany('INSERT INTO Populations (PopulationID, PopulationName) VALUES (?, ?)', populations)
    conn.commit()
    print("Populations added successfully.")
except sqlite3.IntegrityError:
    print("PopulationID already exists. No new populations were added.")
except Exception as e:
    print(f"An error occurred: {e}")

# Close the database connection
conn.close()
