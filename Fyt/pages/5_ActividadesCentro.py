import streamlit as st
from config import supabase
from utils.queries import insert_data, update_data, delete_data

st.title("Gestión de Actividades")

if "authenticated" not in st.session_state or not st.session_state["authenticated"] or st.session_state["role"] != "venue":
    st.warning("Debes iniciar sesión como centro deportivo para acceder.")
    st.stop()

user_id = st.session_state["user_id"]

venue_query = supabase.table("venues").select("venue_id").eq("auth_user_id", user_id).execute()
venue_info = venue_query.data[0] if venue_query.data else None

if not venue_info:
    st.error("No se encontró el centro deportivo asociado a este usuario.")
    st.stop()

venue_id = venue_info["venue_id"]

# Diccionarios de traducción
dias = {
    "Lunes": "Monday", "Martes": "Tuesday", "Miércoles": "Wednesday",
    "Jueves": "Thursday", "Viernes": "Friday", "Sábado": "Saturday", "Domingo": "Sunday"
}
modalidades = {"Presencial": "presential", "Virtual": "virtual"}
generos = {"Mixto": "mixed", "Hombre": "male", "Mujer": "female"}
frecuencias = {"Semanal": "weekly", "Quincenal": "biweekly", "Mensual": "monthly", "Puntual": "one-time"}

# Mostrar actividades registradas
st.subheader("Tus actividades registradas")

activities = supabase.table("activities").select("*").eq("venue_id", venue_id).execute().data

if not activities:
    st.info("No tienes actividades registradas aún.")
else:
    for act in activities:
        with st.expander(f"🗓 {act['day']} - {act['time']}h | {act['category']} ({act['modality']})"):
            st.write(f"Deporte ID: {act['sport_id']}")
            st.write(f"Precio: {act['price']} €")
            st.write(f"Descripción: {act['description']}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🗑 Eliminar", key=f"del_{act['acti_id']}"):
                    delete_data("activities", act["acti_id"], id_field="acti_id")
                    st.rerun()
            with col2:
                if st.button(f"✏️ Editar", key=f"edit_{act['acti_id']}"):
                    st.session_state["edit_activity"] = act
                    st.rerun()

# Crear/Editar actividad
if "edit_activity" in st.session_state:
    st.subheader("Editar actividad")
    activity_data = st.session_state["edit_activity"]
else:
    st.subheader("Crear nueva actividad")
    activity_data = {}

with st.form("activity_form"):
    sport_id = st.number_input("ID del deporte", min_value=1, step=1, value=activity_data.get("sport_id", 1))
    day_es = st.selectbox("Día", list(dias.keys()), index=0)
    time = st.time_input("Hora de inicio", value=activity_data.get("time"))
    duration = st.number_input("Duración (min)", min_value=15, step=15, value=activity_data.get("duration", 60))
    modality_es = st.selectbox("Modalidad", list(modalidades.keys()), index=0)
    type_ = st.text_input("Tipo (recreativo, federado, etc)", value=activity_data.get("type", ""))
    category = st.text_input("Categoría / Nivel", value=activity_data.get("category", ""))
    gender_es = st.selectbox("Género", list(generos.keys()), index=0)
    min_age = st.number_input("Edad mínima", min_value=0, max_value=99, value=activity_data.get("min_age", 0))
    max_age = st.number_input("Edad máxima", min_value=1, max_value=99, value=activity_data.get("max_age", 99))
    price = st.number_input("Precio (€)", min_value=0.0, format="%.2f", value=activity_data.get("price", 10.0))
    frequency_es = st.selectbox("Frecuencia", list(frecuencias.keys()), index=0)
    spots = st.number_input("Plazas disponibles", min_value=1, max_value=100, value=activity_data.get("spots", 10))
    requires_registration = st.checkbox("Requiere registro previo", value=activity_data.get("requires_registration", False))
    payment_method = st.text_input("Método de pago", value=activity_data.get("payment_method", ""))
    description = st.text_area("Descripción", value=activity_data.get("description", ""))
    latitude = st.number_input("Latitud", format="%.6f", value=activity_data.get("latitude", 0.0))
    longitude = st.number_input("Longitud", format="%.6f", value=activity_data.get("longitude", 0.0))

    submitted = st.form_submit_button("Guardar actividad")

    if submitted:
        new_data = {
            "venue_id": venue_id,
            "sport_id": sport_id,
            "day": dias[day_es],
            "time": str(time),
            "duration": duration,
            "modality": modalidades[modality_es],
            "type": type_,
            "category": category,
            "gender": generos[gender_es],
            "min_age": min_age,
            "max_age": max_age,
            "price": price,
            "spots": spots,
            "requires_registration": requires_registration,
            "frequency": frecuencias[frequency_es],
            "payment_method": payment_method,
            "description": description,
        }

        if "edit_activity" in st.session_state:
            update_data("activities", activity_data["acti_id"], new_data, id_field="acti_id")
            del st.session_state["edit_activity"]
            st.success("Actividad actualizada correctamente.")
        else:
            insert_data("activities", new_data)
            st.success("Actividad creada correctamente.")

        st.rerun()
