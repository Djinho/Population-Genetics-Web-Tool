import pandas as pd
import sqlite3

# Load and transform the matrix data
fst_matrix_path = 'data/fst_matrix.txt'
fst_matrix = pd.read_csv(fst_matrix_path, sep='\t', index_col=0)
fst_long = fst_matrix.unstack().reset_index()
fst_long.columns = ['population1', 'population2', 'fst_value']
fst_long['ordered_pair'] = fst_long.apply(lambda x: tuple(sorted([x['population1'], x['population2']])), axis=1)
fst_long = fst_long.drop_duplicates(subset=['ordered_pair']).drop('ordered_pair', axis=1)

# Create a new SQLite database
db_path = '/mnt/data/fst_matrix.db'
conn = sqlite3.connect(db_path)

# Create the fst_data table
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS fst_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    population1 TEXT NOT NULL,
    population2 TEXT NOT NULL,
    fst_value REAL NOT NULL
)
''')

# Insert data into the table
data_to_insert = fst_long[['population1', 'population2', 'fst_value']].values.tolist()
cursor.executemany('INSERT INTO fst_data (population1, population2, fst_value) VALUES (?, ?, ?)', data_to_insert)

# Commit the changes and close the connection
conn.commit()
conn.close()

