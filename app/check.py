import sqlite3

try:
    conn = sqlite3.connect(r'C:\Users\Djinh\Documents\Population-Genetics-Web-Tool\sql\PopulationGeneticsDB.sqlite')
    print("Connected to the database successfully")
    conn.close()
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
