import pandas as pd
import numpy as np
import datetime

def get_anneals():
    """Read in the tabulated set of available anneals"""
    URL = 'http://www.stsci.edu/~STIS/monitors/anneals/anneal_periods.html'
    anneal_df = pd.read_html(URL)[0]
    cols = list(anneal_df.columns)
    cols[0] = "number"
    anneal_df.columns = cols
    return anneal_df

def date_to_anneal_num(date):
    """Retrieve the correct anneal number corresponding to an input date
    date (string): in format YYYY-MM-DD or YYYY-MM-DD HH:MM:SS
    """
    anneal_df = get_anneals()

    if len(date.split(' ')) == 2:
        fmt = '%Y-%m-%d %H:%M:%S'
    elif len(date.split(' ')) == 1:
        fmt = '%Y-%m-%d'
    else:
        print("Did not recognize input date string format.")
        return None
    
    date = datetime.datetime.strptime(date, fmt)

    for anneal in anneal_df.iterrows():
        anneal_start = datetime.datetime.strptime(anneal[1]['start'], '%Y-%m-%d %H:%M:%S')
        anneal_end = datetime.datetime.strptime(anneal[1]['end'], '%Y-%m-%d %H:%M:%S')
        if (date >= anneal_start) and (date < anneal_end):
            return anneal[1]['number']
    print("No Matching Anneal Period Found.")
    return None




