import mysql.connector
import pandas as pd
import numpy as np

class PixelDB:
    def __init__(self,host,user,password):
        """Define the pixel database connection creates a client connection and a cursor object"""
        self.db = mysql.connector.connect(host=host,user=user,password=password)
        self.cursor = self.db.cursor()

    def query_pixel(self,pixel_row,pixel_col,date=None,anneal_num=None,instrument='STIS',detector='CCD'):
        """Return pixel properties for a given pixel and anneal combination"""
        if (not date) and (not anneal_num):
            print("Please provide a date or an anneal number to retrieve pixel properties from.")
            return
        self.cursor.execute("[SQL STATEMENT HERE]")
        for row in self.cursor:
            print(row)
        return

    def query_anneal(self, date=None, anneal_num=None, instrument='STIS', detector='CCD'):
        """Return anneal properties for a single anneal, probably want to handle querying for multiple anneals at once"""
        if (not date) and (not anneal_num):
            print(
                "Please provide a date or an anneal number to identify an anneal to retrieve properties from")
            return
        self.cursor.execute("[SQL STATEMENT HERE]")
        for row in self.cursor:
            print(row)
        return

    def query_anneal_darks(self, date=None, anneal_num=None, instrument='STIS', detector='CCD'):
        """Return the list of dark names for a given anneal"""
        if (not date) and (not anneal_num):
            print(
                "Please provide a date or an anneal number to identify an anneal to retrieve dark file names from")
            return
        self.cursor.execute("[SQL STATEMENT HERE]")
        for row in self.cursor:
            print(row)
        return
