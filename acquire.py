import requests
import pandas as pd
import io
import os

def pull_zach_data(url, endpoint, filename):
    '''Pulls zach data with target endpoints.
       Endpoints: sales, items, stores .Checks for a cached .csv to import.
       If none found, it will import from the api and cache to a df. '''
    if os.path.isfile(filename):
        df = pd.read_csv(filename, index_col=0)
        return df
    else:
        data_list = []
        response = requests.get(url)
        data = response.json()
        n = data['payload']['max_page']
        for i in range(1, n+1):
            new_url = url+"?page="+str(i)
            response = requests.get(new_url)
            data = response.json()
            page_stores = data['payload'][endpoint]
            data_list += page_stores
            df = pd.DataFrame(data_list)
        df.to_csv(filename)
        return df

def store_item_sales(sales_df, item_df, store_df):
    '''Merges sales, item, and store dataframes. You must 
    arange arguments the order sales, items, and stores dataframes.
    returns a composite dataframe'''
    sales_df = sales_df.rename(columns = {'item':'item_id'})
    df = sales_df.merge(items_df, on = 'item_id', how = 'left')
    df = df.rename(columns = {'store':'store_id'})
    df = df.merge(stores_df ,on = 'store_id', how = 'left')
    return df

def get_github_csv(url, filename):
    '''Pulls a .csv from a raw github link. It well check for a cached version first.
    If none found, it will download and decode the content and save it to the passed
    filename. '''
    if os.path.isfile(filename):
        df = pd.read_csv(filename, index_col=0)
        return df
    else:
        download = requests.get(url).content
        df = pd.read_csv(io.StringIO(download.decode('utf-8')))
        df.to_csv(filename)
        return df