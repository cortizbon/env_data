import streamlit as st
import pandas as pd
import plotly.express as px
import requests as rq
import geopandas as gpd
import matplotlib.pyplot as plt
st.set_page_config(layout='wide')
st.title("Test")

tab1, tab2 = st.tabs(["Datos históricos", "Solicitud a API"])
TOKEN = st.secrets["TOKEN"]
ID = None
PATH = f"https://att.waqi.info/feed/{ID}/?token={TOKEN}"

df = pd.read_csv("data___env.csv")
info = pd.read_csv('info_locs.csv')


with tab1:
    col1, col2 = st.columns((2, 4))
    with col1:
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

        metric = st.selectbox("Seleccione una métrica", df["subs"].unique())

        location = st.selectbox("Seleccione la ubicación", df["loc"].unique())
        filtro = df[df["loc"] == location]

        date_init = st.date_input(
            "Seleccione la fecha inicial",
            value=filtro["date"].min(),
            min_value=filtro["date"].min(),
            max_value=filtro["date"].max(),
        )
        date_end = st.date_input(
            "Seleccione la fecha final",
            value=filtro["date"].min(),
            min_value=filtro["date"].min(),
            max_value=filtro["date"].max(),
        )
    with col2: 
        if date_init >= date_end:
            st.error("La fecha inicial debe ser menor a la final.")
        else:
            filtro2 = filtro[
                (filtro["date"] >= pd.to_datetime(date_init))
                & (filtro["date"] <= pd.to_datetime(date_end))
                & (filtro["subs"] == metric)
            ].sort_values(by="date")
            fig = px.line(data_frame=filtro2, x="date", y="value")
            st.plotly_chart(fig)

    st.download_button(
                "Descargar datos completos", df.to_csv(index=False), "datos_completos.csv"
            )
    try:
        st.download_button(
                    "Descargar datos filtrados",
                    filtro2.to_csv(index=False),
                    "datos_filtrados.csv",
                )
    except:
        st.write(' ')

with tab2:
    col4, col3 = st.columns((4, 1))
    with col3:
        lista_puntos = ['Todos'] + list(info['name'].unique())
        st.write(f"Son {len(lista_puntos)- 1} puntos de recolección de información.")
        NAME = st.selectbox("Seleccione una ubicación", lista_puntos)

    with col4:
        if NAME == 'Todos':
            st.map(info)
        else:
            ID = info[info["name"] == NAME]["uid"].reset_index(drop=True)[0]
            st.map(info[info["name"] == NAME])
            
            PATH = f"https://att.waqi.info/feed/A{ID}/?token={TOKEN}"
            response = rq.get(PATH)
            if response.json()['status'] != 'error':
                st.write(response.json()['data']['city']['location'])
                st.write(response.json()['data']['attributions'][0]['name'])
                st.write(response.json()['data']['attributions'][0]['url'])
            else:
                PATH = f"https://att.waqi.info/feed/@{ID}/?token={TOKEN}"
                response = rq.get(PATH)
                st.write(response.json()['data']['city']['location'])
                st.write(response.json()['data']['attributions'][0]['name'])
                st.write(response.json()['data']['attributions'][0]['url'])
    





    
