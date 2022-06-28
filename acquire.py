from cgi import test
from lib2to3.pgen2.pgen import DFAState
from lib2to3.refactor import get_all_fix_names
import numpy as np
import seaborn as sns
import scipy.stats as stats
import pandas as pd
import matplotlib.pyplot as plt
from pydataset import data
import scipy
import os
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')
import requests


def items():
    # setup
    domain = 'https://python.zgulde.net'
    endpoint = '/api/v1/items'
    items = []
    #loop while our endpoint till it hits an end.
    while endpoint != None:
        #create api url
        url = domain + endpoint
        #get data
        response = requests.get(url)
        data = response.json()
        #add data to list
        items.extend(data['payload']['items'])
        #grab new endpoint
        endpoint = data['payload']['next_page']
    items = pd.DataFrame(items)

def stores():
    # setup
    domain = 'https://python.zgulde.net'
    endpoint = '/api/v1/stores'
    stores = []
    #loop while our endpoint isn't none
    while endpoint != None:
        #create api url
        url = domain + endpoint
        #get data
        response = requests.get(url)
        data = response.json()
        #add data to list
        stores.extend(data['payload']['stores'])
        #grab new endpoint
        endpoint = data['payload']['next_page']
    #save dataframe
    stores = pd.DataFrame(stores)

def sales():
    domain = 'https://python.zgulde.net'
    endpoint = '/api/v1/sales'
    sales = []
    # For each page -- until next page is None
    #loop the process of adding pages to database
    while endpoint != None:
        url = domain + endpoint
        response = requests.get(url)
        data = response.json()
        #add data to list
        sales.extend(data['payload']['sales'])
        #grab new end point
        endpoint = data['payload']['next_page']
        #save dataframe
        sales = pd.DataFrame(sales)
        return sales

def get_stores_data():
    if os.path.exists('stores.csv'):
        return pd.read_csv('stores.csv')
    df = stores()
    df.to_csv('stores.csv', index=False)
    return df

def get_items_data():
    if os.path.exists('items.csv'):
        return pd.read_csv('items.csv')
    df = items()
    df.to_csv('items.csv', index=False)
    return df

def get_sales_data():
    if os.path.exists('sales.csv'):
        return pd.read_csv('sales.csv')
    df = sales()
    df.to_csv('sales.csv', index=False)
    return df


def HEB_data():
    """ renaming functions above and merging them together so that we can have one large dataframe"""
    sales = get_sales_data()
    stores = get_stores_data()
    items = get_items_data()

    #merging data 
    sales_and_stores = pd.merge(sales,stores, how="inner", left_on="store", right_on="store_id")
    df = pd.merge(sales_and_stores,items, how="inner", left_on='item',right_on='item_id')
    return df
    
def get_opsd_german_data():
    if os.path.exists('opsd.csv'):
        return pd.read_csv('opsd.csv')
    df = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
    df.to_csv('opsd.csv', index=False)
    return df
