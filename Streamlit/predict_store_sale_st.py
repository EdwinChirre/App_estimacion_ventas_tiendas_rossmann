import streamlit as st
import requests
import json

import datetime



API_URLBASE = "https://predict-sale-store-container-service.e5tasnbtgnsga.us-east-1.cs.amazonlightsail.com"

def execute_prediction_request(Store: int,
    Date: str,
    Promo: int,
    StateHoliday: str,
    SchoolHoliday: int
                                ) -> float:

    payload = {
        'Store': Store,
        'Date': Date,
        'Promo': Promo,
        'StateHoliday': StateHoliday,
        'SchoolHoliday': SchoolHoliday
        
    }
    
    response = requests.post(API_URLBASE + '/sales-estimate', data=json.dumps(payload))
    
    if response.status_code == 201:       
        return response.json().get('Sales')
    else:
        response.raise_for_status()
               
        
header_container = st.container()



with header_container:


    html_temp = """
    <div style="background-color:#3E6D9C ;padding:10px">
    <h2 style="color:white;text-align:center;">
    App para la estimacón de venta </h2>
    </div>
    """
    
    st.markdown(html_temp, unsafe_allow_html=True)
    
    st.image(
    "image/store_rossmann4.jpg",use_column_width = True,
    width=50,)
    
    st.write('Llene el siguiente formulario para calcular la venta estimada de su tienda')

    
with st.form(key='sales-estimate-form'):
    col1, col2 = st.columns(2)
    
    Store = col1.text_input(label='Id tienda:')
    #DayOfWeek = col1.slider(label='Día de la semana:', min_value=1, max_value=7)
    Date = col1.date_input('Seleccionar fecha de estimacion:')
    Date =  Date.strftime("%Y-%m-%d")
    #Promo = col1.slider(label='Tiene promoción hoy?:', min_value=0, max_value=1)
    Promo = col2.checkbox('Tiene promoción:', value = False)
    if Promo:
        Promo = 1
    else:
        Promo = 0
        
    SchoolHoliday = col2.checkbox('Feriado estatal:', value = False)
    if SchoolHoliday:
        SchoolHoliday = 1
    else:
        SchoolHoliday = 0


    StateHoliday = col2.selectbox('Tipo de feriado estatal:', 
                                  ['Feriado publico', 'Pascua', 'Navidad', 'Ninguno'], index = 3)
    mapping = {'Feriado publico': 'a', 'Pascua':'b','Navidad':'c', 'Ninguno':'0'}
    StateHoliday = mapping[StateHoliday]
    #SchoolHoliday = col1.slider(label='Le afecta el feriado estatal?:', min_value=0, max_value=1)
    #SchoolHoliday = col2.selectbox('Le afecta el feriado estatal?:',[0,1])
    
    
    customized_button = st.markdown("""
    <style >
    div.stButton > button:first-child {
        background-color: #578a00;
        color:#ffffff;
    }
    div.stButton > button:hover {
        background-color: #00128a;
        color:#ffffff;
        }
    </style>""", unsafe_allow_html=True)
    
    submit = customized_button  # Modified
    
    submit = st.form_submit_button('Estimar Venta')
    
    if submit:
        Sales = execute_prediction_request(Store, Date, Promo, StateHoliday, 
                                           SchoolHoliday)
        st.success(f'La venta estimada para la tienda {Store} es ${Sales:.2f} USD')
        #Sales
        #st.success(Sales)
    #else:
        #st.error('Oops!! Algo salió mal en la comunicación con el servicio de predicción.')
            
    
    
    