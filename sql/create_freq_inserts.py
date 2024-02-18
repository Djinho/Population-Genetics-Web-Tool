import pandas as pd

"""
This script generates SQL INSERT statements to populate the Frequency table
with genotype frequency data for various populations based on provided CSV files.

Assumptions:
- 'genotype_frequencies.csv' has columns named '<Population>_geno_<0/1/2>_freq'
  indicating the frequency of genotypes 0, 1, and 2 for each population.
- 'snp_annotations.csv' has an 'ID' column with SNP IDs in the format 'rs#####'.
- Each row in 'genotype_frequencies.csv' corresponds to a SNP ID at the same row in 'snp_annotations.csv'.
- The 'populations' table has a 'PopulationName' column corresponding to the population codes used in 'genotype_frequencies.csv'.
- The 'SNP_Information' table has an 'ID' column that matches the SNP IDs from 'snp_annotations.csv'.

The script generates a file named 'insert_statements.sql' containing the SQL INSERT statements.
"""

# Load the CSV files into DataFrames
geno_freq_df = pd.read_csv('genotype_frequencies.csv')
anno_df = pd.read_csv('snp_annotations.csv')

# Prepare the SQL file with INSERT statements
with open('insert_statements.sql', 'w') as sql_file:
    for index, row in geno_freq_df.iterrows():
        snp_id = anno_df.loc[index, 'ID']  # Assuming the 'ID' column exists in 'snp_annotations.csv'
        for col in row.index:
            if col.endswith('_freq'):
                pop_name = col.split('_geno_')[0]
                geno_0_freq, geno_1_freq, geno_2_freq = row[f'{pop_name}_geno_0_freq'], row[f'{pop_name}_geno_1_freq'], row[f'{pop_name}_geno_2_freq']
                # Generate the INSERT statement
                sql_insert = f"""INSERT INTO Frequency (SNPID, PopulationID, Genotype0Frequency, Genotype1Frequency, Genotype2Frequency) 
VALUES (
  (SELECT SNPID FROM SNP_Information WHERE ID = '{snp_id}'),
  (SELECT PopulationID FROM populations WHERE PopulationName = '{pop_name}'),
  {geno_0_freq}, {geno_1_freq}, {geno_2_freq}
);\n"""
                # Write the INSERT statement to the SQL file
                sql_file.write(sql_insert)

# Confirm completion
print("SQL INSERT statements have been written to 'insert_statements.sql'")
