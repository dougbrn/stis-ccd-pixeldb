import mysql.connector
import pandas as pd
import numpy as np

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

    def query_pixel(self,pixel_row,pixel_col,date=None,anneal_num=None,instrument='STIS',detector='CCD'):
        """Return pixel properties for a given pixel and anneal combination"""
        if (not date) and (not anneal_num):
            print("Please provide a date or an anneal number to retrieve pixel properties from.")
            return
        result = self.__execute("[SQL STATEMENT HERE]")
        return

    def query_anneal(self, date=None, anneal_num=None, instrument='STIS', detector='CCD'):
        """Return anneal properties for a single anneal, probably want to handle querying for multiple anneals at once"""
        if (not date) and (not anneal_num):
            print(
                "Please provide a date or an anneal number to identify an anneal to retrieve properties from")
            return
        result = self.__execute("[SQL STATEMENT HERE]")
        return

    def query_anneal_darks(self, date=None, anneal_num=None, instrument='STIS', detector='CCD'):
        """Return the list of dark names for a given anneal"""
        if (not date) and (not anneal_num):
            print(
                "Please provide a date or an anneal number to identify an anneal to retrieve dark file names from")
            return
        result = self.__execute("[SQL STATEMENT HERE]")
        return

    def check_for_anneals(self, exclude=[]):
        """Returns a list of anneals not contained in the pixel database"""

        # Read in the tabulated set of available anneals
        URL = 'http://www.stsci.edu/~STIS/monitors/anneals/anneal_periods.html'
        anneal_df = pd.read_html(URL)[0]
        cols = list(anneal_df.columns)
        cols[0] = "number"
        anneal_df.columns = cols

        # Query database for the set of stored anneal numbers
        result = self.__execute("SELECT AnnealNumber FROM ANNEAL_PERIODS")

        missing_anneals = []
        for anneal in anneal_df['number']:
            if (anneal not in result) and (anneal not in exclude):
                missing_anneals.append(anneal)
        return missing_anneals


    def insert_anneals(self):
        """Loads anneals and their corresponding pixels into the database"""
        pass