import streamlit as st
from utils.queries import insert_data
from config import supabase

st.title("Registro de Centro Deportivo")

# Diccionarios
venue_types = {"Club": "Club", "Tienda": "Shop", "Otro": "Other"}

# Formulario
with st.form("venue_registration_form"):
    st.subheader("Datos de acceso")
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")

    st.subheader("Datos del centro")
    name = st.text_input("Nombre comercial")
    vat = st.text_input("CIF o VAT")
    company = st.text_input("Razón social")
    address = st.text_input("Dirección")
    postal_code = st.text_input("Código postal")
    city = st.text_input("Ciudad")
    lat = st.number_input("Latitud", format="%.6f")
    lon = st.number_input("Longitud", format="%.6f")
    website = st.text_input("Web")
    instagram = st.text_input("Instagram")
    facebook = st.text_input("Facebook")
    twitter = st.text_input("Twitter")
    tiktok = st.text_input("TikTok")
    phone = st.text_input("Teléfono")
    venue_type_es = st.selectbox("Tipo de centro", list(venue_types.keys()))
    accessibility = st.checkbox("¿Tiene accesibilidad física?")
    languages = st.text_input("Idiomas hablados")

    submitted = st.form_submit_button("Registrar")

# Lógica
if submitted:
    try:
        auth_res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {"role": "venue"}
            }
        })

        if auth_res and auth_res.user:
            auth_user_id = auth_res.user.id

            venue_data = {
                "auth_user_id": auth_user_id,
                "name": name,
                "vat_number": vat,
                "company_name": company,
                "address": address,
                "postal_code": postal_code,
                "city": city,
                "latitude": lat,
                "longitude": lon,
                "website": website,
                "instagram": instagram,
                "facebook": facebook,
                "twitter": twitter,
                "tiktok": tiktok,
                "phone": phone,
                "email": email,
                "venue_type": venue_types[venue_type_es],
                "accessibility": accessibility,
                "languages_spoken": languages
            }

            db_res = insert_data("venues", venue_data)
            if "error" not in db_res:
                st.success("Centro registrado correctamente. Ya puedes iniciar sesión.")
            else:
                st.error("Error al guardar el centro. Intenta más tarde.")
        else:
            st.error("No se pudo completar el registro. Intenta con otro correo.")
    except Exception as e:
        st.error(f"Error durante el registro: {e}")
