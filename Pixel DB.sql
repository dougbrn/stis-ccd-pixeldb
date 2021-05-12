CREATE DATABASE anneals_pixels;

CREATE TABLE ANNEAL_PERIOD
(
	AnnealNumber INT (4) PRIMARY KEY,
	StartDate DATE,
	EndDate DATE,
	NumberOfDarks INT
);

CREATE TABLE DARKS
(
	Darks VARCHAR (10) PRIMARY KEY,
	AnnealNumber INT (4),
	FOREIGN KEY(AnnealNumber) REFERENCES ANNEAL_PERIOD(AnnealNumber) ON DELETE CASCADE
);

CREATE TABLE INSTRUMENT
(
	IName VARCHAR(10) PRIMARY KEY,
	N_Detectors INT (2),
	Functioning TINYINT(1)
);

CREATE TABLE DETECTOR
(
	DName VARCHAR(8) PRIMARY KEY,
	Annealed TINYINT(1),
	N_Rows INT(4),
    N_Columns INT(4),
	IName VARCHAR(10),
	FOREIGN KEY(IName) REFERENCES INSTRUMENT(IName) ON DELETE SET NULL
);

CREATE TABLE PIXEL
(
	RowNum INT (4),
	ColumnNum INT (4),
	Detector_Name VARCHAR(8),
	PRIMARY KEY   (RowNum, ColumnNum),
	FOREIGN KEY(Detector_Name) REFERENCES DETECTOR(DName) ON DELETE SET NULL
);

CREATE TABLE HAS_PROPERTIES_IN
(
	AnnealNumber INT(3),
	RowNum INT (4),
	ColumnNum INT (4),
	Stability DECIMAL (9,4),
	Sci_Mean DECIMAL (9,4),
	Err_Mean DECIMAL (7,4),
	NaN_Count INT (3),
	Readnoise DECIMAL (6,4),
	PRIMARY KEY (AnnealNumber, Rownum, ColumnNum),
	FOREIGN KEY(AnnealNumber) REFERENCES ANNEAL_PERIOD(AnnealNumber) on delete CASCADE,
	FOREIGN KEY(RowNum, ColumnNum) REFERENCES PIXEL(RowNum, ColumnNum) on delete CASCADE

);

INSERT INTO INSTRUMENT (Iname, N_Detectors, Functioning)
VALUES ('STIS',3,1);

INSERT INTO DETECTOR (Dname, Annealed, N_Rows, N_Columns, IName)
VALUES ('CCD',1, 1024, 1024, 'STIS');
