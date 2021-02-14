import pandas as pd
import numpy as np
import os

def users_df():
    df1 = pd.read_csv('./data/mac_addresses.txt', header=None)
    df1.columns = ['mac','device','date']

    dtypes = {'phone': 'str'}
    df2 = pd.read_csv('./data/users.txt',dtype=dtypes)

    df3 = pd.merge(df1, df2, on='mac',how='left')

    file_path = './data/active_mac_addresses.txt'

    if os.stat(file_path).st_size == 0:
        covid_tests=[]
        for index, row in df3.iterrows():
            covid_tests.append('Negative')
        df3['Covid_test']=covid_tests
        df4 = df3.replace(np.nan, 'Unregistered User', regex=True)
        return df4

    else:
        df4 = pd.read_csv('./data/active_mac_addresses.txt', header=None)
        df4.columns = ['mac', 'date']

        covid_tests=[]
        for index, row in df3.iterrows():
            mac = row['mac']
            if mac in df4['mac'].values:
                covid_tests.append('Positive')
            else:
                covid_tests.append(None)

        df3['Covid_test']=covid_tests
        df4 = df3.replace(np.nan, 'Unregistered User', regex=True)


        return df4

