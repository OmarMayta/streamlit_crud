import streamlit as st
from supabase import create_client, Client

# Conexión a Supabase
SUPABASE_URL = "https://ecxxzxnyakrxabgsnxwo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVjeHh6eG55YWtyeGFiZ3NueHdvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIxODMwODQsImV4cCI6MjA1Nzc1OTA4NH0.hSsJG2AVuMSMpXCzLb31F3nC5_ZoqUeZExDxDSlokz8"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("CRUD con Supabase")

# Función para obtener usuarios
def obtener_usuarios():
    response = supabase.table("usuarios").select("*").execute()
    return response.data if response.data else []

# Función para agregar usuario
def agregar_usuario(nombre, correo, edad):
    datos = {"nombre": nombre, "correo": correo, "edad": edad}
    respuesta = supabase.table("usuarios").insert(datos).execute()
    return respuesta

# Función para actualizar usuario
def actualizar_usuario(usuario_id, nuevo_nombre, nuevo_correo, nueva_edad):
    datos = {"nombre": nuevo_nombre, "correo": nuevo_correo, "edad": nueva_edad}
    respuesta = supabase.table("usuarios").update(datos).eq("id", usuario_id).execute()
    return respuesta

# Función para eliminar usuario
def eliminar_usuario(usuario_id):
    respuesta = supabase.table("usuarios").delete().eq("id", usuario_id).execute()
    return respuesta

# Formulario para agregar usuario
st.header("Agregar Usuario")
nombre = st.text_input("Nombre")
correo = st.text_input("Correo")
edad = st.number_input("Edad", min_value=0, step=1)

if st.button("Agregar Usuario"):
    respuesta = agregar_usuario(nombre, correo, edad)
    if "error" in respuesta:
        st.error(f"Error al agregar usuario: {respuesta['error']}")
    else:
        st.success("Usuario agregado con éxito")
        st.experimental_rerun()

# Mostrar usuarios
st.header("Lista de Usuarios")
usuarios = obtener_usuarios()

if usuarios:
    for usuario in usuarios:
        with st.expander(f"📌 {usuario['nombre']} - {usuario['correo']} - {usuario['edad']} años"):
            nuevo_nombre = st.text_input("Nuevo Nombre", usuario["nombre"], key=f"nombre_{usuario['id']}")
            nuevo_correo = st.text_input("Nuevo Correo", usuario["correo"], key=f"correo_{usuario['id']}")
            nueva_edad = st.number_input("Nueva Edad", min_value=0, step=1, value=usuario["edad"], key=f"edad_{usuario['id']}")

            if st.button("Actualizar", key=f"update_{usuario['id']}"):
                actualizar_usuario(usuario["id"], nuevo_nombre, nuevo_correo, nueva_edad)
                st.success("Usuario actualizado con éxito")
                st.experimental_rerun()

            if st.button("Eliminar", key=f"delete_{usuario['id']}"):
                eliminar_usuario(usuario["id"])
                st.warning("Usuario eliminado")
                st.experimental_rerun()
else:
    st.write("No hay usuarios registrados.")
