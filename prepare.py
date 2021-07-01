from datetime import datetime
import numpy as np
import pandas as pd

def prep_stores(df):
    ''' Takes in the stores.csv pulled from the zach API. Converts date to datetime
    and sets to index. Adds a day, month, and sales total column.
    '''
    df['sale_date'] = pd.to_datetime(df['sale_date']).drop(columns = 'Unnamed: 0')
    df = df.set_index('sale_date').sort_index()
    df['day'] =  df.index.day_name()
    df['month'] = df.index.month
    df['sales_total'] = df['sale_amount'] * df['item_price']
    return df

def prep_power(df):
    '''Takes in the germany OPSD data and converts the date to a datetime,
    sets date as index, and adds month and day columns. Fills nulls with 0.
    '''
    df = df.drop(columns = 'Unnamed: 0')
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date').sort_index()
    df['day'] =  df.index.day_name()
    df['month'] = df.index.month
    df = df.fillna(0)
    return df