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

# Cargar listas desde Supabase
sports_data = supabase.table("sports").select("sport_id, name").execute().data
types_data = supabase.table("type").select("type_id, name").execute().data
categories_data = supabase.table("category").select("id_sport, category").execute().data

if not sports_data or not types_data or not categories_data:
    st.error("No se pudieron cargar las listas desde Supabase.")
    st.stop()

sports_dict = {item["name"]: item["sport_id"] for item in sports_data}
types_dict = {item["name"]: item["type_id"] for item in types_data}
categories_dict = {item["category"]: item["id_sport"] for item in categories_data}

# Diccionarios fijos
dias = {
    "Lunes": "Monday", "Martes": "Tuesday", "Miércoles": "Wednesday",
    "Jueves": "Thursday", "Viernes": "Friday", "Sábado": "Saturday", "Domingo": "Sunday"
}
modalidades = {"Presencial": "presential", "Virtual": "virtual"}
generos = {"Mixto": "mixed", "Hombre": "male", "Mujer": "female"}

# Mostrar actividades registradas
st.subheader("Tus actividades registradas")

activities = supabase.table("activities").select("*").eq("venue_id", venue_id).execute().data

if not activities:
    st.info("No tienes actividades registradas aún.")
else:
    for act in activities:
        with st.expander(f"🗓 {act['day']} - {act['time']}h | {act['category']} ({act['modality']})"):
            st.write(f"Deporte ID: {act['sport_id']}")
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
    sport_name = st.selectbox("Deporte", list(sports_dict.keys()))
    sport_id = sports_dict[sport_name]

    type_name = st.selectbox("Tipo de actividad", list(types_dict.keys()))
    type_id = types_dict[type_name]

    category_name = st.selectbox("Categoría / Nivel", list(categories_dict.keys()))
    category_id = categories_dict[category_name]

    day_es = st.selectbox("Día", list(dias.keys()), index=0)
    time = st.time_input("Hora de inicio", value=activity_data.get("time"))
    duration = st.number_input("Duración (min)", min_value=15, step=15, value=activity_data.get("duration", 60))
    modality_es = st.selectbox("Modalidad", list(modalidades.keys()), index=0)
    gender_es = st.selectbox("Género", list(generos.keys()), index=0)
    min_age = st.number_input("Edad mínima", min_value=0, max_value=99, value=activity_data.get("min_age", 0))
    max_age = st.number_input("Edad máxima", min_value=1, max_value=99, value=activity_data.get("max_age", 99))
    spots = st.number_input("Plazas disponibles", min_value=1, max_value=100, value=activity_data.get("spots", 10))
    requires_registration = st.checkbox("Requiere registro previo", value=activity_data.get("requires_registration", False))
    description = st.text_area("Descripción de la actividad", value=activity_data.get("description", ""))

    submitted = st.form_submit_button("Guardar actividad")

    if submitted:
        new_data = {
            "venue_id": venue_id,
            "sport_id": sport_id,
            "type": type_id,
            "category": category_id,
            "day": dias[day_es],
            "time": str(time),
            "duration": duration,
            "modality": modalidades[modality_es],
            "gender": generos[gender_es],
            "min_age": min_age,
            "max_age": max_age,
            "spots": spots,
            "requires_registration": requires_registration,
            "description": description
        }

        if "edit_activity" in st.session_state:
            update_data("activities", activity_data["acti_id"], new_data, id_field="acti_id")
            del st.session_state["edit_activity"]
            st.success("Actividad actualizada correctamente.")
        else:
            insert_data("activities", new_data)
            st.success("Actividad creada correctamente.")

        st.rerun()
