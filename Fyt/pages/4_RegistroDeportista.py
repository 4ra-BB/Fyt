import streamlit as st
from utils.queries import insert_data
from config import supabase

st.title("Registro de Usuario Deportista")

# Diccionarios de traducción
sex_options = {"Hombre": "male", "Mujer": "female", "Otro": "other"}
frequency_options = {"Diaria": "daily", "Semanal": "weekly", "Ocasional": "occasional", "Otra": "other"}
transport_options = {"A pie": "walk", "Bici": "bike", "Transporte público": "public transport", "Coche": "car"}
time_options = {"Mañana": "morning", "Tarde": "afternoon", "Noche": "evening"}
level_options = {"Principiante": "beginner", "Intermedio": "intermediate", "Avanzado": "advanced"}

# Formulario
with st.form("athlete_registration_form"):
    st.subheader("Datos de acceso")
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")

    st.subheader("Datos personales")
    full_name = st.text_input("Nombre completo")
    age = st.number_input("Edad", min_value=10, max_value=100, step=1)
    sex_es = st.selectbox("Sexo", list(sex_options.keys()))
    disability = st.checkbox("¿Tienes alguna discapacidad física?")
    frequency_es = st.selectbox("Frecuencia deportiva", list(frequency_options.keys()))
    training_goal = st.text_input("¿Cuál es tu objetivo deportivo?")
    preferred_sports = st.multiselect("Deportes que te interesan", ["Yoga", "Fútbol", "Padel", "Running", "Tenis"])
    residence_address = st.text_input("Dirección")
    postal_code = st.text_input("Código postal")
    transport_es = st.selectbox("Transporte habitual", list(transport_options.keys()))
    time_es = st.selectbox("¿En qué horario prefieres entrenar?", list(time_options.keys()))
    level_es = st.selectbox("Nivel de experiencia", list(level_options.keys()))
    phone = st.text_input("Teléfono")

    submitted = st.form_submit_button("Registrar")

# Lógica de registro
if submitted:
    try:
        auth_res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {"role": "athlete"}
            }
        })

        st.write("Resultado completo:", auth_res)

        if auth_res and auth_res.user:
            auth_user_id = auth_res.user.id

            user_data = {
                "user_id": auth_user_id,
                "full_name": full_name,
                "email": email,
                "age": age,
                "sex": sex_options[sex_es],
                "disability": disability,
                "frequency": frequency_options[frequency_es],
                "training_goal": training_goal,
                "preferred_sports": preferred_sports,
                "residence_address": residence_address,
                "postal_code": postal_code,
                "transport_mode": transport_options[transport_es],
                "preferred_time_of_day": time_options[time_es],
                "experience_level": level_options[level_es],
                "phone": phone
            }

            db_res = insert_data("users", user_data)
            if "error" not in db_res:
                st.success("Usuario registrado correctamente. Ya puedes iniciar sesión.")
            else:
                st.error(f"Error al guardar el usuario: {db_res['error']}")
        else:
            st.warning("No se devolvió usuario, aunque no hubo excepción.")

    except Exception as e:
        st.error(f"⚠️ Error real detectado: {e}")
