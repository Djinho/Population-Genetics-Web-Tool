import sqlite3
import csv
from datetime import datetime

# Connect to the SQLite database
conn = sqlite3.connect('PopulationGeneticsDB.sqlite')
cursor = conn.cursor()

# Create the table and indices
cursor.executescript('''
CREATE TABLE IF NOT EXISTS chromosome_data (
    ID TEXT PRIMARY KEY,
    CHROM TEXT CHECK (CHROM = 'chr1'),
    POS INTEGER,
    REF TEXT,
    ALT TEXT,
    QUAL TEXT,
    FILTER TEXT,
    FORMAT TEXT,
    ANNOVAR_DATE DATE,
    Func_refGene TEXT,
    Gene_refGene TEXT,
    -- Additional columns for other annotations can be added here
    ACB REAL,
    ASW REAL,
    BEB REAL,
    CDX REAL,
    CEU REAL,
    CHB REAL,
    CHS REAL,
    CLM REAL,
    ESN REAL,
    FIN REAL,
    GBR REAL,
    GIH REAL,
    GWD REAL,
    IBS REAL,
    ITU REAL,
    JPT REAL,
    KHV REAL,
    LWK REAL,
    MSL REAL,
    MXL REAL,
    PEL REAL,
    PJL REAL,
    PUR REAL,
    SIB REAL,
    STU REAL,
    TSI REAL,
    YRI REAL,
    AFR REAL,
    AMR REAL,
    EAS REAL,
    EUR REAL,
    SAS REAL
);

CREATE INDEX IF NOT EXISTS idx_chrom ON gene_variants (CHROM);
CREATE INDEX IF NOT EXISTS idx_pos ON gene_variants (POS);
CREATE INDEX IF NOT EXISTS idx_gene_refgene ON gene_variants (Gene_refGene);
''')

# Prepare the INSERT statement
insert_stmt = '''
INSERT INTO gene_variants (ID, CHROM, POS, REF, ALT, QUAL, FILTER, FORMAT, ANNOVAR_DATE, Func_refGene, Gene_refGene, ACB, ASW, BEB, CDX, CEU, CHB, CHS, CLM, ESN, FIN, GBR, GIH, GWD, IBS, ITU, JPT, KHV, LWK, MSL, MXL, PEL, PJL, PUR, SIB, STU, TSI, YRI, AFR, AMR, EAS, EUR, SAS)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
'''

# Open the CSV file and insert each row into the database
with open('gene_schema_insert.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Insert the row into the database only if the chromosome is 'chr1'
        if row['CHROM'] == 'chr1':
            cursor.execute(insert_stmt, (
                row['ID'],
                row['CHROM'],
                int(row['POS']),
                row['REF'],
                row['ALT'],
                row['QUAL'],
                row['FILTER'],
                row['FORMAT'],
                datetime.strptime(row['ANNOVAR_DATE'], '%Y-%m-%d').date(),
                row['Func.refGene'],
                row['Gene.refGene'],
                float(row['ACB']) if row['ACB'] else None,
                float(row['ASW']) if row['ASW'] else None,
                float(row['BEB']) if row['BEB'] else None,
                float(row['CDX']) if row['CDX'] else None,
                float(row['CEU']) if row['CEU'] else None,
                float(row['CHB']) if row['CHB'] else None,
                float(row['CHS']) if row['CHS'] else None,
                float(row['CLM']) if row['CLM'] else None,
                float(row['ESN']) if row['ESN'] else None,
                float(row['FIN']) if row['FIN'] else None,
                float(row['GBR']) if row['GBR'] else None,
                float(row['GIH']) if row['GIH'] else None,
                float(row['GWD']) if row['GWD'] else None,
                float(row['IBS']) if row['IBS'] else None,
                float(row['ITU']) if row['ITU'] else None,
                float(row['JPT']) if row['JPT'] else None,
                float(row['KHV']) if row['KHV'] else None,
                float(row['LWK']) if row['LWK'] else None,
                float(row['MSL']) if row['MSL'] else None,
                float(row['MXL']) if row['MXL'] else None,
                float(row['PEL']) if row['PEL'] else None,
                float(row['PJL']) if row['PJL'] else None,
                float(row['PUR']) if row['PUR'] else None,
                float(row['SIB']) if row['SIB'] else None,
                float(row['STU']) if row['STU'] else None,
                float(row['TSI']) if row['TSI'] else None,
                float(row['YRI']) if row['YRI'] else None,
                float(row['AFR']) if row['AFR'] else None,
                float(row['AMR']) if row['AMR'] else None,
                float(row['EAS']) if row['EAS'] else None,
                float(row['EUR']) if row['EUR'] else None,
                float(row['SAS']) if row['SAS'] else None
            ))
