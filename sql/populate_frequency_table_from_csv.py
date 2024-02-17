import pandas as pd
import sqlite3
import os

"""
This script populates the Frequency table in a population genetics SQLite database with data from a CSV file containing genotype frequencies. It checks for the existence of the database and the populations table, then maps population names to their IDs. It assumes that each row in the CSV corresponds to a SNP record in the database, and the CSV's index corresponds to the SNP ID.
"""

# Define the path to your database file
db_path = 'C:\\Users\\Djinh\\Documents\\Population-Genetics-Web-Tool\\sql\\PopulationGeneticsDB.sqlite'

# Check if the database file exists and is not empty
if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
    print(f"The database file at {db_path} does not exist or is empty.")
    exit(1)

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if the populations table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='populations';")
if cursor.fetchone() is None:
    print("The populations table does not exist in the database.")
    exit(1)

# Load genotype frequencies CSV
genotype_frequencies_df = pd.read_csv('genotype_frequencies.csv')

# Get the population mapping from the database
cursor.execute("SELECT PopulationName, PopulationID FROM populations")
population_mapping = {name: id for name, id in cursor.fetchall()}

# Function to insert frequency data
def insert_frequency_data(cursor, frequencies_df, population_mapping):
    for index, row in frequencies_df.iterrows():
        snp_id = index + 1  # Assuming the index+1 corresponds to SNPID
        for population_name, pop_id in population_mapping.items():
            # Construct column names for frequencies based on the population name
            freq_0_col = f"{population_name}_geno_0_freq"
            freq_1_col = f"{population_name}_geno_1_freq"
            freq_2_col = f"{population_name}_geno_2_freq"
            
            # Insert data into Frequency table
            cursor.execute("""
                INSERT INTO Frequency (SNPID, PopulationID, Genotype0Frequency, Genotype1Frequency, Genotype2Frequency)
                VALUES (?, ?, ?, ?, ?)
            """, (
                snp_id, 
                pop_id, 
                row.get(freq_0_col, None),
                row.get(freq_1_col, None),
                row.get(freq_2_col, None)
            ))

# Insert the frequency data into the database
insert_frequency_data(cursor, genotype_frequencies_df, population_mapping)

# Commit changes and close the connection
conn.commit()
conn.close()

print("The genotype frequencies have been successfully inserted into the database.")
