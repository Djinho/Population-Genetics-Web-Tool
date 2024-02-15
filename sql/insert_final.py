import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect('PopulationGeneticsDB.sqlite')
cursor = conn.cursor()

# Open the CSV file and read its contents
with open('gene_schema_insert.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        insert_stmt = '''INSERT INTO chromosome_data (ID, CHROM, POS, REF, ALT, QUAL, FILTER, FORMAT, ANNOVAR_DATE, 
                        Func_refGene, Gene_refGene, ACB, ASW, BEB, CDX, CEU, CHB, CHS, CLM, ESN, FIN, GBR, GIH, 
                        GWD, IBS, ITU, JPT, KHV, LWK, MSL, MXL, PEL, PJL, PUR, SIB, STU, TSI, YRI, AFR, AMR, 
                        EAS, EUR, SAS) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        row_data = (row['ID'], row['CHROM'], row['POS'], row['REF'], row['ALT'], row['QUAL'], row['FILTER'], 
                    row['FORMAT'], row['ANNOVAR_DATE'], row['Func.refGene'], row['Gene.refGene'], row['ACB'], 
                    row['ASW'], row['BEB'], row['CDX'], row['CEU'], row['CHB'], row['CHS'], row['CLM'], row['ESN'], 
                    row['FIN'], row['GBR'], row['GIH'], row['GWD'], row['IBS'], row['ITU'], row['JPT'], row['KHV'], 
                    row['LWK'], row['MSL'], row['MXL'], row['PEL'], row['PJL'], row['PUR'], row['SIB'], row['STU'], 
                    row['TSI'], row['YRI'], row['AFR'], row['AMR'], row['EAS'], row['EUR'], row['SAS'])
        cursor.execute(insert_stmt, row_data)

# Commit changes and close the connection
conn.commit()
conn.close()
