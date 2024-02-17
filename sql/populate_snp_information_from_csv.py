import pandas as pd
import sqlite3

# Define the path to your CSV file
csv_file_path = 'snp_annotations.csv'  # Ensure this is the correct path to the CSV file

# Read the CSV file using pandas, specifying the encoding and header explicitly
df = pd.read_csv(csv_file_path, sep=',', encoding='utf-8', header=0)

# Trim whitespace from column names
df.columns = df.columns.str.strip()

# Print the DataFrame head to ensure it's read correctly
print(df.head())

# Connect to your SQLite database
conn = sqlite3.connect('PopulationGeneticsDB.sqlite')
cursor = conn.cursor()

# Iterate through the DataFrame and insert each row into the SNP_Information table
for index, row in df.iterrows():
    chromosome = row['CHROM']
    position = row['POS']
    rs_id = row['ID'].split(';')[0]  # If the ID column needs different processing adjust here
    ref = row['REF']
    alt = row['ALT'] if row['ALT'] != '.' else None  # Handling cases where ALT is '.'

    # Prepare the INSERT statement
    insert_query = """INSERT INTO SNP_Information (Chromosome, Position, ID, REF, ALT) 
                      VALUES (?, ?, ?, ?, ?);"""

    # Execute the INSERT statement
    cursor.execute(insert_query, (chromosome, position, rs_id, ref, alt))

# Commit changes and close the connection
conn.commit()
conn.close()

print("SNP_Information table has been populated.")
