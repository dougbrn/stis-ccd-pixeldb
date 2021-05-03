import mysql.connector
import pandas as pd
import numpy as np
from .utils import get_anneals, date_to_anneal_num
import os.path

class PixelDB:
    def __init__(self,host,user,password,database):
        """Define the pixel database connection creates a client connection and a cursor object"""
        self.db = mysql.connector.connect(host=host,user=user,password=password,database=database)
        self.cursor = self.db.cursor()

    def __execute(self, statement):
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

    def query_pixel(self,pixel_row,pixel_col,date=None,anneal_num=None):
        """Return pixel properties for a given pixel and anneal combination"""
        if (not date) and (not anneal_num):
            print("Please provide a date (format YYYY-MM-DD or YYYY-MM-DD HH:MM:SS) or an anneal number to retrieve pixel properties from.")
            return
        elif date and not anneal_num:
            anneal_num = date_to_anneal_num(date)
        sql_statement = f"SELECT * FROM HAS_PROPERTIES_IN \
                        WHERE ROWNUM = {pixel_row} \
                        AND COLUMNNUM = {pixel_col} \
                        AND ANNEALNUMBER = {anneal_num}"
        result = self.__execute(sql_statement)
        return result

    def query_anneal(self, date=None, anneal_num=None, instrument='STIS', detector='CCD'):
        """Return anneal properties for a single anneal, probably want to handle querying for multiple anneals at once"""
        if (not date) and (not anneal_num):
            print("Please provide a date (format YYYY-MM-DD or YYYY-MM-DD HH:MM:SS) or an anneal number to retrieve pixel properties from.")
            return
        elif date and not anneal_num:
            anneal_num = date_to_anneal_num(date)
        sql_statement = f"SELECT * FROM ANNEAL_PERIOD \
                        WHERE ANNEALNUMBER = {anneal_num}"
        result = self.__execute(sql_statement)
        return

    def query_anneal_darks(self, date=None, anneal_num=None, instrument='STIS', detector='CCD'):
        """Return the list of dark names for a given anneal"""
        if (not date) and (not anneal_num):
            print("Please provide a date (format YYYY-MM-DD or YYYY-MM-DD HH:MM:SS) or an anneal number to retrieve pixel properties from.")
            return
        elif date and not anneal_num:
            anneal_num = date_to_anneal_num(date)
        sql_statement = f"SELECT * FROM DARKS \
                        WHERE ANNEALNUMBER = {anneal_num}"
        result = self.__execute(sql_statement)
        return

    def check_for_anneals(self, exclude=[]):
        """Returns a list of anneals not contained in the pixel database"""

        # Read in the tabulated set of available anneals
        anneal_df = get_anneals()

        # Query database for the set of stored anneal numbers
        result = self.__execute("SELECT AnnealNumber FROM ANNEAL_PERIODS")

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
        pix_csv = os.path.join(csv_loc,f'anneal_{anneal_num}.csv')
        
        #Insert Anneal Period
        start_date = str(anneal['start']).split(" ")[0]
        end_date = str(anneal['end']).split(" ")[0]
        statement = f"INSERT INTO ANNEAL_PERIOD ( AnnealNumber, StartDate, EndDate, NumberOfDarks) \
                    VALUES ( {int(anneal_num)}, {start_date}, {end_date}, {int(anneal['num'])})"
        self.__execute(statement)
        self.db.commit() #Needed for confirming the database-altering transaction

        #Insert Darks
        darks = list(anneal['darks'])[0].split(',')
        dark_vals = []
        for dark in darks:
            dark = dark.strip()
            dark_tup = (dark, anneal_num)
            dark_vals.append(dark_tup)
        statement = "INSERT INTO darks ( Darks, AnnealNumber) VALUES (%s, %d)"
        self.__executemany(statement, dark_vals)
        self.db.commit()

        #Insert Pixel Properties
        #self.db.commit()
        
