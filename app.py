import streamlit as st
import pandas as pd
import plotly.express as px
import requests as rq
import geopandas as gpd
import matplotlib.pyplot as plt

st.title("Test")

tab1, tab2 = st.tabs(["Datos históricos", "Solicitud a API"])
TOKEN = st.secrets["TOKEN"]
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
    st.write(f"Son {len(info['name'].unique())} puntos.")
    NAME = st.selectbox("Seleccione una ubicación", info["name"].unique())
    ID = info[info["name"] == NAME]["uid"]

    fig, ax = plt.subplots()
    ax.axis('off')
    base = locs.plot(color='white', edgecolor='black', ax=ax, figsize=(8, 4))
    info[info["name"] == NAME].plot(ax=base, color='red', markersize=5)
    st.pyplot(fig)
    try:
        PATH = f"https://att.waqi.info/feed/A{ID}/?token={TOKEN}"
        response = rq.get(PATH)
        st.write(response.json())
        st.write("test")
        st.write(TOKEN)
    except:
        PATH = f"https://att.waqi.info/feed/@{ID}/?token={TOKEN}"
        response = rq.get(PATH)
        st.write(response.json())
        st.write("test")
        st.write(TOKEN)

    
