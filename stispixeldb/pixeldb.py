import mysql.connector
import pandas as pd
import numpy as np
from .utils import get_anneals, date_to_anneal_num
import os.path
import datetime

class PixelDB:
    def __init__(self,host,user,password,database):
        """Define the pixel database connection creates a client connection and a cursor object"""
        self.db = mysql.connector.connect(host=host,user=user,password=password,database=database,connection_timeout=3600)
        self.cursor = self.db.cursor()
        self.__prohibited = ["DROP *"]

    def __execute(self, statement, vals=None):
        self.cursor.execute(statement)
        result = []
        for row in self.cursor:
            result.append(row)
        return result

    def __batch_execute(self, statement, values):
        self.cursor.executemany(statement, values)
        result = []
        for row in self.cursor:
            result.append(row)
        return result

    def custom_query(self,statement):
        """execute a general sql query against the database"""
        if statement in self.__prohibited:
            print("Cannot execute, statement prohibited.")
            return
        else:
            result = self.__execute(statement)
            return pd.DataFrame(result)

    def query_pixel(self,pixel_row,pixel_col,date=None,anneal_num=None, columns=['AnnealNumber','RowNum',
                                                                                'ColumnNum','Stability',
                                                                                'Sci_Mean','Err_Mean',
                                                                                'NaN_Count','Readnoise']):
        """Return pixel properties for a given pixel and anneal combination"""
        if (not date) and (not anneal_num):
            print("Please provide a date (format YYYY-MM-DD or YYYY-MM-DD HH:MM:SS) or an anneal number to retrieve pixel properties from.")
            return
        elif date and not anneal_num:
            anneal_num = date_to_anneal_num(date)
        col_string = ','.join(columns)
        sql_statement = f"SELECT {col_string} FROM HAS_PROPERTIES_IN \
                        WHERE RowNum = {pixel_row} \
                        AND ColumnNum = {pixel_col} \
                        AND AnnealNumber = {anneal_num}"
        result = self.__execute(sql_statement)
        return pd.DataFrame(result, columns=columns)

    def query_pixel_region(self,pixel_row_range, pixel_col_range, date=None,anneal_num=None, columns=['AnnealNumber','RowNum',
                                                                                'ColumnNum','Stability',
                                                                                'Sci_Mean','Err_Mean',
                                                                                'NaN_Count','Readnoise']):
        """Return pixel properties for a given pixel and anneal combination"""
        if (not date) and (not anneal_num):
            print("Please provide a date (format YYYY-MM-DD or YYYY-MM-DD HH:MM:SS) or an anneal number to retrieve pixel properties from.")
            return
        elif date and not anneal_num:
            anneal_num = date_to_anneal_num(date)
        col_string = ','.join(columns)

        pixel_row1,pixel_row2 = pixel_row_range
        pixel_col1,pixel_col2 = pixel_col_range
        sql_statement = f"SELECT {col_string} FROM HAS_PROPERTIES_IN \
                        WHERE ( RowNum BETWEEN ({pixel_row1}) AND ({pixel_row2}))\
                        AND (ColumnNum BETWEEN ({pixel_col1}) AND ({pixel_col2}))\
                        AND AnnealNumber = {anneal_num}"
        result = self.__execute(sql_statement)
        return pd.DataFrame(result, columns=columns)


    def query_anneal(self, date=None, anneal_num=None, instrument='STIS', detector='CCD', columns=['AnnealNumber', 'StartDate',
                                                                                                    'EndDate','NumberOfDarks']):
        """Return anneal properties for a single anneal, probably want to handle querying for multiple anneals at once"""
        if (not date) and (not anneal_num):
            print("Please provide a date (format YYYY-MM-DD or YYYY-MM-DD HH:MM:SS) or an anneal number to retrieve pixel properties from.")
            return
        elif date and not anneal_num:
            anneal_num = date_to_anneal_num(date)
        col_string = ','.join(columns)
        sql_statement = f"SELECT {col_string} FROM ANNEAL_PERIOD \
                        WHERE ANNEALNUMBER = {anneal_num}"
        result = self.__execute(sql_statement)
        return pd.DataFrame(result, columns=columns)


    def query_anneal_darks(self, date=None, anneal_num=None, instrument='STIS', detector='CCD', columns=['Darks','AnnealNumber']):
        """Return the list of dark names for a given anneal"""
        if (not date) and (not anneal_num):
            print("Please provide a date (format YYYY-MM-DD or YYYY-MM-DD HH:MM:SS) or an anneal number to retrieve pixel properties from.")
            return
        elif date and not anneal_num:
            anneal_num = date_to_anneal_num(date)
        col_string = ','.join(columns)
        sql_statement = f"SELECT {col_string} FROM DARKS \
                        WHERE ANNEALNUMBER = {anneal_num}"
        
        result = self.__execute(sql_statement)
        return pd.DataFrame(result, columns=columns)


    def load_pixel_mapping(self, csv_loc='.',csv_name='pixel_map.csv'):
        # Prepare Pixel File
        pix_path = os.path.join(csv_loc,csv_name)
        try:
            pix_csv = pd.read_csv(pix_path,header=None)
        except FileNotFoundError:
            print("No Pixel Mapping CSV file found")
            return

        #Insert Pixel Properties
        pix_vals = list(pix_csv.itertuples(index=False, name=None))
        statement = "INSERT INTO PIXEL ( RowNum,ColumnNum, Detector_Name) \
                    VALUES (%s,%s,%s)"
        self.__batch_execute(statement, pix_vals)
        self.db.commit()


    def check_for_anneals(self, exclude=[]):
        """Returns a list of anneals not contained in the pixel database"""

        # Read in the tabulated set of available anneals
        anneal_df = get_anneals()

        # Query database for the set of stored anneal numbers
        result = self.__execute("SELECT AnnealNumber FROM ANNEAL_PERIOD")

        missing_anneals = []
        for anneal in anneal_df['number']:
            if (anneal not in result) and (anneal not in exclude):
                missing_anneals.append(anneal)
        return missing_anneals


    def insert_anneal(self, anneal_num, csv_loc = '.'):
        """Loads anneals and their corresponding pixels and darks into the database"""
        anneal_df = get_anneals() # Load in the list of available anneals
        anneal = anneal_df.loc[anneal_df['number']==anneal_num]
        if len(anneal) == 0:
            print("No Matching Anneal Period Found.")
            return
        
        # Prepare Pixel File
        pix_path = os.path.join(csv_loc,f'anneal_{anneal_num}.csv')
        try:
            pix_csv = pd.read_csv(pix_path)
        except FileNotFoundError:
            print("No Pixel Property CSV file found")
            return
        
        #Insert Anneal Period
        start_year,start_month,start_day = list(anneal['start'])[0].split(" ")[0].split("-")
        start_date = datetime.date(int(start_year), int(start_month), int(start_day))
        start_date.strftime('%Y %m %d')

        end_year,end_month,end_day = list(anneal['end'])[0].split(" ")[0].split("-")
        end_date = datetime.date(int(end_year), int(end_month), int(end_day))
        end_date.strftime('%Y %m %d')

        statement = "INSERT INTO ANNEAL_PERIOD ( AnnealNumber, StartDate, EndDate, NumberOfDarks) VALUES (%s, %s, %s, %s)"
        anneal_vals = (anneal_num, start_date, end_date, int(anneal['num']))
        #self.__execute(statement,anneal_vals)

        self.cursor.execute("INSERT INTO ANNEAL_PERIOD ( AnnealNumber, StartDate, EndDate, NumberOfDarks) VALUES (%s, %s, %s, %s)",
               (anneal_num, start_date, end_date, int(anneal['num'])))
        result = []
        for x in self.cursor:
            print(x)
            result.append(x)
        print(result)
        self.db.commit() #Needed for confirming the database-altering transaction
        
        #Insert Darks
        darks = list(anneal['darks'])[0].split(',')
        dark_vals = []
        for dark in darks:
            dark = dark.strip()
            dark_tup = (dark, anneal_num)
            dark_vals.append(dark_tup)
        statement = "INSERT INTO DARKS ( Darks, AnnealNumber) VALUES (%s, %s)"
        self.__batch_execute(statement, dark_vals)
        self.db.commit()

        #Insert Pixel Properties
        pix_csv.insert(0,'AnnealNumber',anneal_num)
        pix_csv = pix_csv.fillna(0)
        pix_vals = list(pix_csv.itertuples(index=False, name=None))
        first_half = pix_vals[0:int(len(pix_csv)/2)]
        second_half = pix_vals[int(len(pix_csv)/2):]
        print("Starting First Half Insertion")
        statement = "INSERT INTO HAS_PROPERTIES_IN ( AnnealNumber, RowNum, ColumnNum, Stability, Sci_Mean, Err_Mean, NaN_Count, Readnoise) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        self.__batch_execute(statement, first_half)
        self.db.commit()
        print("Starting Second Half Insertion")
        statement = "INSERT INTO HAS_PROPERTIES_IN ( AnnealNumber, RowNum, ColumnNum, Stability, Sci_Mean, Err_Mean, NaN_Count, Readnoise) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        self.__batch_execute(statement, second_half)
        self.db.commit()
        return
        
