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

def prep_store_data(df):
    df.sale_date = df.sale_date.apply(lambda date: date[:-13])
    df.sale_date = pd.to_datetime(df.sale_date, format='%a, %d %b %Y')
    # make sure we sort by date/time before resampling or doing other time series manipulations
    df = df.set_index('sale_date').sort_index()
    df['month'] = df.index.strftime('%m-%b')
    df['day_of_week'] = df.index.strftime('%w-%a')
    df['sales_total'] = df.sale_amount * df.item_price
    return df

def prep_opsd_data(df):
    #renaming collumns and making then lower case.
    df.columns = ['date', 'consumption', 'wind', 'solar', 'wind_solar']
    df.date = pd.to_datetime(df.date)
    df = df.set_index('date').sort_index()
    df['month'] = df.index.strftime('%m-%b')
    df['year'] = df.index.year
    df = df.fillna(0)
    df['wind_solar'] = df.wind + df.solar
    return df


