CREATE TABLE populations (
    PopulationID INTEGER PRIMARY KEY AUTOINCREMENT,
    PopulationName TEXT NOT NULL,
    is_Superpopulation INTEGER NOT NULL CHECK (is_Superpopulation IN (0,1))
);

CREATE TABLE admixture_results (
    ResultID INTEGER PRIMARY KEY AUTOINCREMENT,
    PopulationID INTEGER,
    ancestry_1 REAL,
    ancestry_2 REAL,
    ancestry_3 REAL,
    ancestry_4 REAL,
    ancestry_5 REAL,
    FOREIGN KEY (PopulationID) REFERENCES populations(PopulationID)
);

CREATE TABLE pca_coordinates (
    CoordinateID INTEGER PRIMARY KEY AUTOINCREMENT,
    PopulationID INTEGER,
    pc1 REAL,
    pc2 REAL,
    pc3 REAL,
    pc4 REAL,
    pc5 REAL,
    pc6 REAL,
    pc7 REAL,
    pc8 REAL,
    pc9 REAL,
    pc10 REAL,
    FOREIGN KEY (PopulationID) REFERENCES populations(PopulationID)
);
