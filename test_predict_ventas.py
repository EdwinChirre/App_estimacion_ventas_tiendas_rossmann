import pickle
import pandas as pd
import numpy as np
 
from xgboost import XGBRegressor
from typing import List, Union

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder

from src import utils

#cargando base:

# Cargando el modelo:
model_sales = pickle.load(open('pickles/model.pkl', 'rb'))

#cargando scaler
scaler_model = pickle.load(open('pickles/scaler_model.pkl', 'rb'))

#cargando encoder
encoder_model = pickle.load(open('pickles/encoder.pkl', 'rb'))

store_df = pd.read_csv("data/store.csv")

   

#def predict_sales(input_values: List[float]):
    
def predict(input_values: List[Union[int, float,str,object]]):
    # Creando un numpy array bidimensional
    # Un numpy array es un contenedor eficiente en memoria que permite realizar operaciones numéricas rápidas
    features = [np.array(input_values)]
    
    # Creando un dataframe a partir del array bidimensional
    features_df = pd.DataFrame(features)
    
    input_cols = ['Store', 'Date', 'Promo', 'StateHoliday', 'SchoolHoliday']
        
    features_df.columns = input_cols
 
    
    features_df['Store'] = features_df['Store'].astype(int)
    #features_df['Date'] = pd.to_datetime(features_df['Date'])
    #features_df = pd.DataFrame()
    
     
    
    var_store = ['Store',
             'CompetitionDistance','Promo2', 'StoreType','Assortment',
             'CompetitionOpenSinceYear','CompetitionOpenSinceMonth','Promo2SinceYear',
             'Promo2SinceWeek','PromoInterval']
    
    features_df = features_df.merge(store_df[var_store], how='left', on='Store')
    
     
    utils.split_date(features_df)
    utils.comp_months(features_df)
    utils.promo_cols(features_df)


    
    
    
    numeric_cols = ['Store', 'Promo', 'SchoolHoliday', 
              'CompetitionDistance', 'CompetitionOpen', 'Promo2', 'Promo2Open', 'IsPromo2Month',
              'Day', 'Month', 'Year', 'WeekOfYear']
    
    categorical_cols = ['DayOfWeek', 'StateHoliday', 'StoreType', 'Assortment']
    
    
    
    features_df[numeric_cols] = scaler_model.transform(features_df[numeric_cols])
    
    #features_df['DayOfWeek'] = features_df['DayOfWeek'].astype(int)

    encoded_cols = list(encoder_model.get_feature_names_out(categorical_cols))
    features_df[encoded_cols] = encoder_model.transform(features_df[categorical_cols])
    
    var_final = ['Store', 'Promo', 'SchoolHoliday', 'CompetitionDistance',
       'CompetitionOpen', 'Promo2', 'Promo2Open', 'IsPromo2Month', 'Day',
       'Month', 'Year', 'WeekOfYear', 'DayOfWeek_1', 'DayOfWeek_2',
       'DayOfWeek_3', 'DayOfWeek_4', 'DayOfWeek_5', 'DayOfWeek_6',
       'DayOfWeek_7', 'StateHoliday_0', 'StateHoliday_a', 'StateHoliday_b',
       'StateHoliday_c', 'StoreType_a', 'StoreType_b', 'StoreType_c',
       'StoreType_d', 'Assortment_a', 'Assortment_b', 'Assortment_c']
    
    preds = model_sales.predict(features_df[var_final])
    
    #preds = np.round(preds,2)
    
    print('La venta estimada es: ', preds)
    #print(features_df.columns)
    # print(features_df['DayOfWeek'])
    # print(features_df[['Store', 'Promo', 'SchoolHoliday', 'CompetitionDistance','CompetitionOpen', 'Promo2']])
    # print(features_df[['Promo2Open', 'IsPromo2Month', 'Day',
    #    'Month', 'Year', 'WeekOfYear', 'DayOfWeek_1.0', 'DayOfWeek_2.0']])
    # print(features_df[['DayOfWeek_3.0', 'DayOfWeek_4.0', 'DayOfWeek_5.0', 'DayOfWeek_6.0',
    #    'DayOfWeek_7.0', 'StateHoliday_0', 'StateHoliday_a', 'StateHoliday_b']])
    # print(features_df[['StateHoliday_c', 'StoreType_a', 'StoreType_b', 'StoreType_c',
    #    'StoreType_d', 'Assortment_a', 'Assortment_b', 'Assortment_c']])
    
    
    return preds
  
if __name__ == '__main__':
    venta1 = (1,"2015-07-31",1,'0',1) #5263 - 5388.752930
    venta2 = (2,"2015-07-31",1,'0',1) #6064 - 6054.42431
    venta3 = (3,"2015-07-31",1,'0',1) #8314 - 8427.394531
    
    predict(venta1)
    predict(venta2)
    predict(venta3)
    
