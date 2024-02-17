import sqlite3

# Path to your database
db_path = "C:\\Users\\Djinh\\Documents\\Population-Genetics-Web-Tool\\sql\\PopulationGeneticsDB.sqlite"

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query to find duplicate SNPID values in the SNP_Information table
query = """
SELECT SNPID, COUNT(SNPID) 
FROM SNP_Information 
GROUP BY SNPID 
HAVING COUNT(SNPID) > 1;
"""

cursor.execute(query)
duplicates = cursor.fetchall()

if duplicates:
    print("Duplicate SNPID values found:")
    for snpid, count in duplicates:
        print(f"SNPID: {snpid}, Count: {count}")
else:
    print("No duplicate SNPID values found.")

# Close the database connection
conn.close()

