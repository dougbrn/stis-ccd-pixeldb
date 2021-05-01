CREATE TABLE ANNEAL_PERIOD
(
    AnnealNumber INT NOT NULL,
	StartDate DATE,
    EndDate DATE,
    NumberOfDarks INT NOT NULL,
    PRIMARY KEY   (AnnealNumber)
);

CREATE TABLE PIXEL
(
    RowNum INT,
	ColumnNum INT,
    Detector_Name VARCHAR(20),
    PRIMARY KEY   (RowNum, ColumnNum)
);

CREATE TABLE DETECTOR
(
    DName VARCHAR(10),
	Annealed CHAR(10),
    N_Pixels VARCHAR(10),
    IName VARCHAR(10),
    PRIMARY KEY   (DName)
);

CREATE TABLE INSTRUMENT
(
    IName VARCHAR(10),
	N_Detectors INT,
    Functioning VARCHAR(4),
    PRIMARY KEY   (IName)
);

CREATE TABLE HAS_PROPERTIES_IN
(
    AnnealNumber VARCHAR(10),
	RowNum INT,
    ColumnNum INT,
    Stability INT,
    DarkRate INT,
    PRIMARY KEY   (AnnealNumber, Rownum, ColumnNum)
);
