import streamlit as st
from supabase import create_client, Client
import pandas as pd

# Obtener las claves desde Streamlit Secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Conectar con Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("CRUD con Streamlit y Supabase")

# ---------- 1️⃣ LECTURA (READ) ----------
st.subheader("Lista de Usuarios")

try:
    response = supabase.table("usuarios").select("*").execute()
    data = response.data

    if data:
        df = pd.DataFrame(data)  # Convertimos los datos en un DataFrame
        st.dataframe(df)  # Mostramos la tabla en Streamlit
    else:
        st.warning("No hay usuarios registrados.")

except Exception as e:
    st.error(f"Error al obtener datos: {e}")

# ---------- 2️⃣ CREACIÓN (CREATE) ----------
st.subheader("Agregar Nuevo Usuario")

# Crear un formulario en Streamlit
with st.form(key="form_nuevo_usuario"):
    nombre = st.text_input("Nombre:")
    correo = st.text_input("Correo:")
    edad = st.number_input("Edad:", min_value=0, max_value=120, step=1)

    # Botón para enviar datos
    submit_button = st.form_submit_button("Agregar Usuario")

# Si el usuario presiona el botón, insertamos en Supabase
if submit_button:
    if nombre and correo and edad:  # Validamos que los campos no estén vacíos
        try:
            data = {
                "nombre": nombre,
                "correo": correo,
                "edad": edad
            }
            response = supabase.table("usuarios").insert(data).execute()

            if response.data:
                st.success("Usuario agregado exitosamente.")
                st.experimental_rerun()  # Recargar la página para actualizar la tabla
            else:
                st.error("No se pudo agregar el usuario.")

        except Exception as e:
            st.error(f"Error al agregar usuario: {e}")

    else:
        st.warning("Por favor, completa todos los campos.")
