import streamlit as st
import requests
import json

API_URLBASE = "https://predict-sale-store-container-service.e5tasnbtgnsga.us-east-1.cs.amazonlightsail.com"

def execute_prediction_request(Store: int,
    Date: str,
    Promo: int, 
    StateHoliday: str,
    SchoolHoliday: int
                                ):# -> float:

    payload = {
        'Store': Store,
        'Date': Date,
         'Promo': Promo,
        'StateHoliday': StateHoliday,
        'SchoolHoliday': SchoolHoliday
        
    }
    
    response = requests.post(API_URLBASE + '/sales-estimate', data=json.dumps(payload))
    
    #return response
    
    if response.status_code == 201:       
        return response.json().get('Sales')
    else:
        response.raise_for_status()
        
Sales = execute_prediction_request(1,"2015-07-31",1,'0',1)   
print(Sales)     