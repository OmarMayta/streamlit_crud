import streamlit as st
from supabase import create_client, Client
import pandas as pd

# Definir las credenciales directamente en el código
SUPABASE_URL = "https://ecxxzxnyakrxabgsnxwo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVjeHh6eG55YWtyeGFiZ3NueHdvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIxODMwODQsImV4cCI6MjA1Nzc1OTA4NH0.hSsJG2AVuMSMpXCzLb31F3nC5_ZoqUeZExDxDSlokz8"

# Crear cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Título de la aplicación
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
# ---------- 3️⃣ ACTUALIZACIÓN (UPDATE) ----------
st.subheader("Editar Usuario")

# Obtener la lista de usuarios para seleccionar
response = supabase.table("usuarios").select("*").execute()
usuarios = response.data

if usuarios:
    usuario_seleccionado = st.selectbox("Selecciona un usuario:", [f"{u['id']} - {u['nombre']}" for u in usuarios])

    if usuario_seleccionado:
        user_id = int(usuario_seleccionado.split(" - ")[0])  # Extraer el ID del usuario seleccionado
        usuario_data = next((u for u in usuarios if u["id"] == user_id), None)

        if usuario_data:
            with st.form(key="form_editar_usuario"):
                nuevo_nombre = st.text_input("Nombre:", usuario_data["nombre"])
                nuevo_correo = st.text_input("Correo:", usuario_data["correo"])
                nueva_edad = st.number_input("Edad:", min_value=0, max_value=120, step=1, value=usuario_data["edad"])

                # Botón para actualizar
                update_button = st.form_submit_button("Actualizar Usuario")

            if update_button:
                try:
                    update_data = {
                        "nombre": nuevo_nombre,
                        "correo": nuevo_correo,
                        "edad": nueva_edad
                    }
                    response = supabase.table("usuarios").update(update_data).eq("id", user_id).execute()

                    if response.data:
                        st.success("Usuario actualizado correctamente.")
                        st.experimental_rerun()  # Recargar la página para ver los cambios
                    else:
                        st.error("No se pudo actualizar el usuario.")

                except Exception as e:
                    st.error(f"Error al actualizar usuario: {e}")

else:
    st.warning("No hay usuarios registrados para editar.")
