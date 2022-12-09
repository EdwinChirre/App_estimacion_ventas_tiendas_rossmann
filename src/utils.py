import pickle
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from typing import List

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
#from dotenv import load_dotenv()

#funciones

#extraer el dia de 


def split_date(df):
    df['Date'] = pd.to_datetime(df['Date'][0])#.strftime('%Y/%m/%d')
    df['Year'] = df.Date.dt.year
    df['Month'] = df.Date.dt.month
    df['Day'] = df.Date.dt.day
    df['WeekOfYear'] = df.Date.dt.isocalendar().week
    df['DayOfWeek'] = df.Date.dt.dayofweek + 1
    df['DayOfWeek'] = df['DayOfWeek'].astype(int)
    
def comp_months(df):
    df['CompetitionOpen'] = 12 * (df.Year - df.CompetitionOpenSinceYear) + (df.Month - df.CompetitionOpenSinceMonth)
    df['CompetitionOpen'] = df['CompetitionOpen'].map(lambda x: 0 if x < 0 else x).fillna(0)
    
def check_promo_month(row):
    month2str = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',              
                 7:'Jul', 8:'Aug', 9:'Sept', 10:'Oct', 11:'Nov', 12:'Dec'}
    try:
        months = (row['PromoInterval'] or '').split(',')
        if row['Promo2Open'] and month2str[row['Month']] in months:
            return 1
        else:
            return 0
    except Exception:
        return 0

def promo_cols(df):
    # Months since Promo2 was open
    df['Promo2Open'] = 12 * (df.Year - df.Promo2SinceYear) +  (df.WeekOfYear - df.Promo2SinceWeek)*7/30.5
    df['Promo2Open'] = df['Promo2Open'].map(lambda x: 0 if x < 0 else x).fillna(0) * df['Promo2']
    # Whether a new round of promotions was started in the current month
    df['IsPromo2Month'] = df.apply(check_promo_month, axis=1) * df['Promo2']    
    
def input_var(df):
    max_distance = 75860

    df['CompetitionDistance'].fillna(max_distance, inplace=True)
 