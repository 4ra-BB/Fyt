import streamlit as st
from utils.auth import login_user
from config import supabase

st.title("Iniciar sesión - Centro Deportivo")

# Verificar si ya hay sesión iniciada
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Estado para mostrar u ocultar formulario de recuperación
if "show_reset" not in st.session_state:
    st.session_state["show_reset"] = False

# FORMULARIO PRINCIPAL
if not st.session_state["authenticated"] and not st.session_state["show_reset"]:
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Entrar"):
            user = login_user(email, password)
            if user and user["role"] == "venue":
                st.session_state["authenticated"] = True
                st.session_state["user_id"] = user["user_id"]
                st.session_state["email"] = user["email"]
                st.session_state["role"] = user["role"]
                st.success("Sesión iniciada correctamente.")
                st.experimental_rerun()
            else:
                st.error("Credenciales incorrectas, por favor, revisa los datos.")

    with col2:
        if st.button("¿Olvidaste tu contraseña?"):
            st.session_state["show_reset"] = True
            st.experimental_rerun()

# FORMULARIO DE RECUPERACIÓN
elif st.session_state["show_reset"]:
    st.markdown("### Recuperar contraseña")
    recovery_email = st.text_input("Introduce tu correo registrado")

    if st.button("Enviar enlace de recuperación"):
        try:
            supabase.auth.reset_password_for_email(recovery_email)
            st.success("Se ha enviado un correo con instrucciones para restablecer tu contraseña.")
        except Exception as e:
            st.error("Hubo un error al enviar el correo.")

    if st.button("Volver al inicio de sesión"):
        st.session_state["show_reset"] = False
        st.experimental_rerun()

# YA LOGUEADO
elif st.session_state["authenticated"]:
    st.markdown(f"Has iniciado sesión como **{st.session_state['email']}**")
    st.page_link("pages/5_ActividadesCentro.py", label="➡️ Ir a gestión de actividades")
