import numpy as np
import pandas as pd
import requests
import os

def get_items(use_cache = True):
    '''
    This function takes in no arguments. It firsts checks if 'items.csv' exists, and if does, it returns a dataframe
    using this file. If the file does not exist it gathers the data using an API, creates a dataframe and caches it as 
    as a .csv file, then returns the dataframe.
    '''
    filename = 'items.csv'

    #Check for the csv cache
    if os.path.isfile(filename) and use_cache:
        print('Using cached csv...')
        return pd.read_csv(filename)

    else:
        #Gather data from the first page
        print('Gathering data using API...')
        domain = 'https://python.zgulde.net'
        endpoint = '/api/v1/items'
        items = []
        while True:
            url = domain + endpoint
            response = requests.get(url)
            data = response.json()
            print(f'\rGetting page {data["payload"]["page"]} of {data["payload"]["max_page"]}: {url}', end='')
            items.extend(data['payload']['items'])
            endpoint = data['payload']['next_page']
            if endpoint is None:
                break

        # Now cache the dataframe as a .csv
        df = pd.DataFrame(items)
        df.to_csv('items.csv', index = False)

        return df


def get_stores(use_cache = True):
    '''
    This function takes in no arguments. It firsts checks if 'stores.csv' exists, and if does, it returns a dataframe
    using this file. If the file does not exist it gathers the data using an API, creates a dataframe and caches it as 
    as a .csv file, then returns the dataframe.
    '''
    filename = 'stores.csv'

    #Check for the csv cache
    if os.path.isfile(filename) and use_cache:
        print('Using cached csv...')
        return pd.read_csv(filename)

    else:
        #Gather data from the first page
        print('Gathering data using API...')
        domain = 'https://python.zgulde.net'
        endpoint = '/api/v1/stores'
        items = []
        while endpoint is not None:
            url = domain + endpoint
            response = requests.get(url)
            data = response.json()
            print(f'\rGetting page {data["payload"]["page"]} of {data["payload"]["max_page"]}: {url}', end='')
            items.extend(data['payload']['stores'])
            endpoint = data['payload']['next_page']

        # Now cache the dataframe as a .csv
        df = pd.DataFrame(items)
        df.to_csv('stores.csv', index = False)

        return df


def get_sales(use_cache = True):
    '''
    This function takes in no arguments. It firsts checks if 'sales.csv' exists, and if does, it returns a dataframe
    using this file. If the file does not exist it gathers the data using an API, creates a dataframe and caches it as 
    as a .csv file, then returns the dataframe.
    '''
    filename = 'sales.csv'

    #Check for the csv cache
    if os.path.isfile(filename) and use_cache:
        print('Using cached csv...')
        return pd.read_csv(filename)

    else:
        #Gather data from the first page
        print('Gathering data using API...')
        domain = 'https://python.zgulde.net'
        endpoint = '/api/v1/sales'
        items = []
        while endpoint is not None:
            url = domain + endpoint
            response = requests.get(url)
            data = response.json()
            print(f'\rGetting page {data["payload"]["page"]} of {data["payload"]["max_page"]}: {url}', end='')
            items.extend(data['payload']['sales'])
            endpoint = data['payload']['next_page']

        # Now cache the dataframe as a .csv
        df = pd.DataFrame(items)
        df.to_csv('sales.csv', index = False)

        return df


def get_merged_data(use_cache=True):
    '''
    This function takes in no arguments. It firsts checks if 'merged_data.csv' exists, and if does, it returns a dataframe
    using this file. If the file does not exist it gathers the data using an API, creates a dataframe and caches it as 
    as a .csv file, then returns the dataframe.
    '''
    filename = 'merged_data.csv'

    #Check for the csv cache
    if os.path.isfile(filename) and use_cache:
        print('Using cached csv...')
        return pd.read_csv(filename)
    
    else:
        #Get items data
        items = get_items()
        #Get stores data
        stores = get_stores()
        #Get sales data
        sales = get_sales()
        
        #Merge into a singe dataframe
        #First rename columns in stores in order to correctly merge
        sales = sales.rename(columns={'store':'store_id', 'item':'item_id'})
        
        #First merging stores and sales
        df = pd.merge(sales, stores, how='left', on='store_id')
        #Next merge with items
        df = pd.merge(df, items, how='left', on='item_id')
                             
        # Now cache the dataframe as a .csv
        df.to_csv('merged_data.csv', index = False)
                             
        return df
    

def get_power_data(use_cache=True):
    '''
    This function takes in no arguments. It firsts checks if 'german_power.csv' exists, and if does, it returns a dataframe
    using this file. If the file does not exist it gathers the data using an API, creates a dataframe and caches it as 
    as a .csv file, then returns the dataframe.
    '''
    filename = 'german_power.csv'

    #Check for the csv cache
    if os.path.isfile(filename) and use_cache:
        print('Using cached csv...')
        return pd.read_csv(filename)
    
    else:
        #Gather data
        print('Gathering data from website...')
        df = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
        
        #Cache data locally
        df.to_csv('german_power.csv', index=False)
        
        return df