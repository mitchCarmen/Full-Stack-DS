# DEFINE PROCESSING PIPELINE

import pandas as pd

def feat_eng_datetime(df):
    """Takes a raw airline df and engineers new date time features that will be used for modeling"""
    
    print('Running feature engineering')
    
    df['FlightDate'] = pd.to_datetime(df['FlightDate'])
    df['Year'] = pd.DatetimeIndex(df['FlightDate']).year.astype('category')
    df['Month'] = pd.DatetimeIndex(df['FlightDate']).month.astype('category')
    df['Day'] = pd.DatetimeIndex(df['FlightDate']).day.astype('category')
    df['Hour'] = pd.to_datetime(df['DepTime'], format='%H:%M').dt.hour.astype('category')
    df['Minutes'] = pd.to_datetime(df['DepTime'], format='%H:%M').dt.minute.astype('category')
    df['DepTime'] = pd.to_datetime(df['DepTime'], format='%H:%M').dt.time
    df = df.drop(columns=['FlightDate','DepTime'])
    
    return df