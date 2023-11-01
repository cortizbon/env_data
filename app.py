import streamlit as st
import pandas as pd
import plotly.express as px
import requests as rq
import geopandas as gpd
import matplotlib.pyplot as plt

st.title("Test")

tab1, tab2 = st.tabs(["Datos históricos", "Solicitud a API"])
TOKEN = "564211daa23309754373f1044fb4453eca26784f"#st.secrets["TOKEN"]
ID = None
PATH = f"https://att.waqi.info/feed/{ID}/?token={TOKEN}"

df = pd.read_csv("data___env.csv")
info = gpd.read_file("info_points.geojson")
locs = gpd.read_file("locs.geojson")


with tab1:
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
        st.download_button(
            "Descargar datos filtrados",
            filtro2.to_csv(index=False),
            "datos_filtrados.csv",
        )

with tab2:
    lista_puntos = ['Todos'] + list(info['name'].unique())
    st.write(f"Son {len(lista_puntos)- 1} puntos.")
    NAME = st.selectbox("Seleccione una ubicación", lista_puntos)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off')
    base = locs.plot(color='white', edgecolor='black', ax=ax, figsize=(8, 4))
    if NAME == 'Todos':
        info.plot(ax=base, color='red', markersize=5, figsize=(8, 4))
    else:
        ID = info[info["name"] == NAME]["uid"].reset_index(drop=True)[0]
        info[info["name"] == NAME].plot(ax=base, color='red', markersize=5, figsize=(8, 4))
        PATH = f"https://att.waqi.info/feed/A{ID}/?token={TOKEN}"
        response = rq.get(PATH)
        if response.json()['status'] != 'error':
            st.write(response.json()['data']['city']['location'])
        else:
            PATH = f"https://att.waqi.info/feed/@{ID}/?token={TOKEN}"
            response = rq.get(PATH)
            st.write(response.json()['data']['city']['location'])
    
    st.pyplot(fig)





    
