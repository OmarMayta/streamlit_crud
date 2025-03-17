import streamlit as st
from supabase import create_client, Client
import pandas as pd

# Conectar con Supabase
SUPABASE_URL = "TU_SUPABASE_URL"
SUPABASE_KEY = "TU_SUPABASE_API_KEY"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("CRUD con Streamlit y Supabase")
st.subheader("Lista de Usuarios")

# Obtener los datos de la tabla 'usuarios'
try:
    response = supabase.table("usuarios").select("*").execute()
    data = response.data

    if data:  # Si hay datos, los mostramos en una tabla
        df = pd.DataFrame(data)  # Convertimos a DataFrame de Pandas
        st.dataframe(df)
    else:
        st.info("No hay usuarios registrados.")

except Exception as e:
    st.error(f"Error al obtener datos: {e}")
