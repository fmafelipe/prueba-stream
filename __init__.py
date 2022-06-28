import streamlit as st 
import numpy as np 
import pandas as pd 

# 1 Titulo de la aplicacion 

st.title("Uber pickups en NewYork")

# 2.1 Traer los datos con los que se va a trabajar 

DATE_COLUMN = 'date/time'
URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')


# 2.2 Cargar los datos y los guarda en cache 
@st.cache
def cargar_datos(nrows):
    data = pd.read_csv(URL, nrows=nrows)
    minusculas = lambda x: str(x).lower() # vuelve el texto en minusculas
    data.rename(minusculas, axis='columns', inplace= True) # convierte el nombre de las columnas en minusculas
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN]) # convierte la columna en formato de fecha
    
    return data

data_load_state = st.text('Cargando datos... ')
datos = cargar_datos(10000)
data_load_state = st.text('Datos cargados con exito usando cache')


# 3 Agregar un subtitulo en la applicacion para mostrar los datos

if st.checkbox("mostrar datos sin proocesar"):
    st.subheader('Datos sin procesar')
    st.write("Estos son los datos escogidos")
    st.write(datos)

# 4 histogrma 

st.subheader("Numero de pickups por hora")
hist_value = np.histogram(datos[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.write(hist_value)
st.bar_chart(hist_value)


# 5 Trazar datos en un mapa 
st.subheader("Lugares de mas recolecciones")
st.map(datos[["lat","lon"]])

# Mapa con las recolecciones a las 17:00 hora donde hay mayor recogidas

st.subheader("Pickups de 17:00 a 18:00")
filtered_data = datos[datos[DATE_COLUMN].dt.hour == 17]
st.map(filtered_data)

# Filtrar resultados por hoa con un slider 
st.subheader("Mapa filtrando los datos con slider")
filtro = st.slider('Hora',0,23,17)
filtro2 = datos[datos[DATE_COLUMN].dt.hour == filtro]
st.map(filtro2)
st.write("Cantidad de datos: ", len(filtro2))




