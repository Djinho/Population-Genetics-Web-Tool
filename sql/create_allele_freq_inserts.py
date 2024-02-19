"""This script updates allele frequencies in the Frequency table of the PopulationGeneticsDB.sqlite database.
It assumes that the Frequency table already contains rows with SNPID and PopulationID that need to be updated with new AlleleFrequency values.
The snp_annotations.csv file should have the SNP IDs in a column named 'ID', and the allele_frequencies.csv file should contain allele frequency data for various populations.
The script will iterate through the SNP annotations and allele frequencies, map each population name to its database ID, 
and write SQL UPDATE statements to update the AlleleFrequency in the 'Frequency' table where the SNPID and PopulationID match.
"""

"""
Assumptions of the code:

1. 'PopulationGeneticsDB.sqlite' with correct schema and 'populations', 'SNP_Information', 'Frequency' tables exist.
2. 'snp_annotations.csv' has 'ID' column with SNP identifiers matching the database.
3. 'allele_frequencies.csv' has headers with population names matching those in the database and frequencies aligned with SNPs.
4. The script can read CSVs and write an SQL file in its directory.
5. Python environment has pandas and sqlite3 packages installed.
"""




import pandas as pd
import sqlite3

# Function to map population names to IDs
def map_population_ids(db_path):
    conn = sqlite3.connect(db_path)
    query = "SELECT PopulationID, PopulationName FROM populations;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return {row['PopulationName']: row['PopulationID'] for index, row in df.iterrows()}

# Function to find SNPID based on the unique ID from SNP_Information table
def get_snp_id_mapping(db_path):
    conn = sqlite3.connect(db_path)
    query = "SELECT SNPID, ID FROM SNP_Information;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return {row['ID']: row['SNPID'] for index, row in df.iterrows()}

# Read in the SNP annotations and allele frequencies
snp_annotations = pd.read_csv('snp_annotations.csv')
allele_frequencies = pd.read_csv('allele_frequencies.csv')

# Map the population names and SNP IDs to the database IDs
population_id_map = map_population_ids('PopulationGeneticsDB.sqlite')
snp_id_map = get_snp_id_mapping('PopulationGeneticsDB.sqlite')

# Open the file for writing SQL update statements
with open('update_allele_frequencies.sql', 'w') as file:
    # Iterate over SNP annotations and allele frequencies
    for index, snp_row in snp_annotations.iterrows():
        unique_id = snp_row['ID']
        snp_db_id = snp_id_map.get(unique_id)
        if snp_db_id is not None:
            for population_name, frequency in allele_frequencies.iloc[index].items():
                population_id = population_id_map.get(population_name)
                if population_id is not None and pd.notna(frequency):
                    # Write the SQL update statement
                    file.write(f"UPDATE Frequency SET AlleleFrequency = {frequency} "
                               f"WHERE SNPID = {snp_db_id} AND PopulationID = {population_id};\n")

print("SQL update statements have been written to update_allele_frequencies.sql")
