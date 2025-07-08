import streamlit as st
from config import supabase

st.title("Buscar Actividades Deportivas")

if "authenticated" not in st.session_state or not st.session_state["authenticated"] or st.session_state["role"] != "athlete":
    st.warning("Debes iniciar sesión como deportista para acceder.")
    st.stop()

user_id = st.session_state["user_id"]

# En el futuro: aquí se llamará al modelo de recomendación
st.markdown("Aquí aparecerán tus recomendaciones personalizadas en cuanto el modelo esté implementado.")

# Por ahora: mostrar actividades como lista general (modo temporal)
st.subheader("Actividades disponibles (modo exploración)")

activities = supabase.table("activities").select("*").execute().data

if not activities:
    st.info("No hay actividades registradas aún.")
else:
    for act in activities:
        with st.expander(f"{act['day']} - {act['time']}h - {act['category']} ({act['modality']})"):
            st.write(f"🎯 Tipo: {act['type']}")
            st.write(f"🧍 Género: {act['gender']} | Edad: {act['min_age']} - {act['max_age']}")
            st.write(f"📝 {act['description']}")

from utils.session import show_logout
show_logout()
