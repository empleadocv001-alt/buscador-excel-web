import streamlit as st
import pandas as pd

st.set_page_config(page_title="Buscador Inteligente", layout="wide")

st.title("🔎 Buscador Inteligente de Información")
st.caption("Escribe y presiona Enter (soporta AND / OR)")

@st.cache_data
def cargar_datos():
    df = pd.read_excel("datos.xlsx")
    df["_search"] = (
        df.astype(str)
        .agg(" ".join, axis=1)
        .str.lower()
    )
    return df

df = cargar_datos()

busqueda = st.text_input(
    "Buscar:",
    placeholder="Ej: juan AND quito | maria OR loja"
)

def filtrar(texto):
    texto = texto.lower().strip()

    if " and " in texto:
        terminos = [t.strip() for t in texto.split(" and ")]
        return df[df["_search"].apply(lambda x: all(t in x for t in terminos))]

    if " or " in texto:
        terminos = [t.strip() for t in texto.split(" or ")]
        return df[df["_search"].apply(lambda x: any(t in x for t in terminos))]

    return df[df["_search"].str.contains(texto, regex=False)]

def convertir_links(df):
    df = df.copy()
    for col in df.columns:
        if df[col].astype(str).str.startswith("http").any():
            df[col] = df[col].astype(str).apply(
                lambda x: f'<a href="{x}" target="_blank">{x}</a>' if x.startswith("http") else x
            )
    return df

if busqueda:
    resultados = filtrar(busqueda)

    st.success(f"Resultados encontrados: {len(resultados)}")

    resultados = resultados.drop(columns="_search")
    resultados = convertir_links(resultados)

    st.markdown(
        resultados.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )
else:
    st.info("🔍 Escribe algo y presiona Enter")
