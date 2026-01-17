import streamlit as st
import pandas as pd

# ---------------- CONFIGURACIÓN ----------------
st.set_page_config(
    page_title="AutoRepuestos Chasi",
    layout="wide"
)

URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTjAIeEgP1pU2y-kg9tq6tyy6O6_RhMdvlvdpE1HTqMj1F59YgZzHkWhcr7bEctDg/pub?output=csv"
COLUMNAS = [0, 6, 8, 7, 2, 11]

# ---------------- CARGA ----------------
@st.cache_data(ttl=600, show_spinner=False)
def cargar_datos():
    df = pd.read_csv(URL_CSV)
    df = df.iloc[:, COLUMNAS]

    df["_search"] = (
        df.astype(str)
        .agg(" ".join, axis=1)
        .str.lower()
    )
    return df

df = cargar_datos()

# ---------------- INTERFAZ ----------------
st.title("🔍 Buscador")

busqueda = st.text_input(
    "Buscar",
    placeholder="Escribe y presiona ENTER",
)

# ---------------- BÚSQUEDA ----------------
if busqueda:
    palabras = busqueda.lower().split()

    if "and" in palabras:
        palabras = [p for p in palabras if p != "and"]
        mask = df["_search"].apply(lambda x: all(p in x for p in palabras))
    elif "or" in palabras:
        palabras = [p for p in palabras if p != "or"]
        mask = df["_search"].apply(lambda x: any(p in x for p in palabras))
    else:
        mask = df["_search"].str.contains(busqueda.lower(), na=False)

    resultados = df[mask].drop(columns="_search").head(500)

    st.write(f"Resultados: {len(resultados)}")

    # Tabla responsive
    st.dataframe(
        resultados,
        use_container_width=True,
        hide_index=True,
        column_config={
            col: st.column_config.LinkColumn(col)
            for col in resultados.columns
            if resultados[col].astype(str).str.startswith("http").any()
        }
    )
else:
    st.info("¡Hoy es el mejor dia¡")
