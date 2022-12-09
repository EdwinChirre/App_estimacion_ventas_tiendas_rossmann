from fastapi import FastAPI
from pydantic import BaseModel

import pickle
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from typing import List, Union

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
import uvicorn

from src import utils


app = FastAPI()

#cargando base:

# Cargando el modelo:
model_sales = pickle.load(open('pickles/model.pkl', 'rb'))

#cargando scaler
scaler_model = pickle.load(open('pickles/scaler_model.pkl', 'rb'))

#cargando encoder
encoder_model = pickle.load(open('pickles/encoder.pkl', 'rb'))

store_df = pd.read_csv("data/store.csv")


class Input(BaseModel):
    Store: int
    Date: object
    Promo: int
    StateHoliday: str
    SchoolHoliday: int
          
class Output(BaseModel):
    Store: int
    Sales: float           
        
@app.post('/sales-estimate', response_model=Output, status_code=201)
async def generate_sales_estimate(input: Input):
    print('Nuevo request para predecir las ventas de una tienda:', input) 
    
    
    input_values = [input.Store,
                    input.Date,
                    input.Promo,
                    input.StateHoliday,
                    input.SchoolHoliday]
    
    features = [np.array(input_values)]
    
    # Creando un dataframe a partir del array bidimensional
    features_df = pd.DataFrame(features)
    
    input_cols = ['Store', 'Date', 'Promo',  'StateHoliday','SchoolHoliday']
    
    features_df.columns = input_cols
 
    
    features_df['Store'] = features_df['Store'].astype(int)
    
    
    
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
    
    preds = np.round(preds,3)
    
    
    return  Output(Store =input.Store, Sales = preds)


if __name__ == '__main__':
    uvicorn.run(app,host="0.0.0.0", port = 3000,debug =True)