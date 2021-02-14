import csv
import re
import pandas as pd
import numpy as np

def check_link():

    contact_count = 0
    macs = []
    dates = []
    dates_active = []
    devices = []

    df1 = pd.read_csv('./data/active_mac_addresses.txt', header=None)
    df1.columns = ['mac', 'date']

    df2 = pd.read_csv('./data/mac_addresses.txt', header=None)
    df2.columns = ['mac','device','date']

    for index, row in df2.iterrows():
        device = row['device']
        mac1 = row['mac']
        date1 = row['date']
        for index2, row2 in df1.iterrows():
            mac2 = row2['mac']
            date2 = row2['date']
            if mac1 == mac2:
                macs.append(mac1)
                dates.append(date2)
                dates_active.append(date1)
                devices.append(device)
                contact_count = contact_count+1

    list_of_tuples = list(zip(macs,devices, dates,dates_active)) 
    df = pd.DataFrame(list_of_tuples, columns = ['mac','device', 'active_date','contact_date']) 

    dtypes = {'phone': 'str'}
    df2 = pd.read_csv('./data/users.txt',dtype=dtypes)

    df = pd.merge(df2, df, on='mac',how='right')
    df = df.replace(np.nan, 'Unregistered User', regex=True)

    return df,contact_count



