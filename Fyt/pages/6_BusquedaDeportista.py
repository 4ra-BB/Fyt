import streamlit as st
from config import supabase

st.title("Buscar Actividades Deportivas")

if "authenticated" not in st.session_state or not st.session_state["authenticated"] or st.session_state["role"] != "athlete":
    st.warning("Debes iniciar sesión como deportista para acceder.")
    st.stop()

user_id = st.session_state["user_id"]

# Cargar listas desde Supabase
sports_data = supabase.table("sports").select("sport_id, name").execute().data
types_data = supabase.table("type").select("type_id, name").execute().data
categories_data = supabase.table("category").select("id_sport, category").execute().data

sports_dict = {item["name"]: item["sport_id"] for item in sports_data}
types_dict = {item["name"]: item["type_id"] for item in types_data}
categories_dict = {item["category"]: item["id_sport"] for item in categories_data}

dias = {
    "Lunes": "Monday", "Martes": "Tuesday", "Miércoles": "Wednesday",
    "Jueves": "Thursday", "Viernes": "Friday", "Sábado": "Saturday", "Domingo": "Sunday"
}
modalidades = {"Presencial": "presential", "Virtual": "virtual"}
generos = {"Mixto": "mixed", "Hombre": "male", "Mujer": "female"}

with st.form("busqueda_form"):
    st.markdown("### Filtros de búsqueda (opcional)")

    sport_name = st.selectbox("Deporte", ["(Cualquiera)"] + list(sports_dict.keys()))
    sport_id = sports_dict.get(sport_name)

    type_name = st.selectbox("Tipo de actividad", ["(Cualquiera)"] + list(types_dict.keys()))
    type_id = types_dict.get(type_name)

    category_name = st.selectbox("Categoría / Nivel", ["(Cualquiera)"] + list(categories_dict.keys()))
    category_id = categories_dict.get(category_name)

    day_es = st.selectbox("Día", ["(Cualquiera)"] + list(dias.keys()))
    day = dias.get(day_es)

    time = st.time_input("Hora deseada (opcional)", value=None)
    modality_es = st.selectbox("Modalidad", ["(Cualquiera)"] + list(modalidades.keys()))
    modality = modalidades.get(modality_es)

    gender_es = st.selectbox("Género", ["(Cualquiera)"] + list(generos.keys()))
    gender = generos.get(gender_es)

    submitted = st.form_submit_button("Buscar")

if submitted:
    st.subheader("Resultados (búsqueda flexible)")

    activities = supabase.table("activities").select("*").execute().data
    resultados = []

    for act in activities:
        score = 0

        if sport_id and act["sport_id"] == sport_id:
            score += 3
        if type_id and act["type"] == type_id:
            score += 2
        if category_id and act["category"] == category_id:
            score += 2
        if day and act["day"] == day:
            score += 1
        if modality and act["modality"] == modality:
            score += 1
        if gender and (act["gender"] == gender or act["gender"] == "mixed"):
            score += 1
        if time:
            hora_act = int(str(act["time"]).split(":")[0])
            hora_usr = int(str(time).split(":")[0])
            if abs(hora_act - hora_usr) <= 1:
                score += 1

        resultados.append((score, act))

    resultados.sort(reverse=True, key=lambda x: x[0])
    mejores = [r for r in resultados if r[0] > 0]

    if mejores:
        for score, act in mejores[:10]:
            with st.expander(f"{act['day']} - {act['time']}h - {act['category']} ({act['modality']})"):
                st.write(f"🎯 Tipo: {act['type']} | 🎯 Score: {score}")
                st.write(f"🧍 Género: {act['gender']} | Edad: {act['min_age']} - {act['max_age']}")
                st.write(f"📝 {act['description']}")
    else:
        st.info("No se encontraron coincidencias. Mostrando las más recientes:")
        for act in activities[:5]:
            with st.expander(f"{act['day']} - {act['time']}h - {act['category']} ({act['modality']})"):
                st.write(f"🎯 Tipo: {act['type']}")
                st.write(f"🧍 Género: {act['gender']} | Edad: {act['min_age']} - {act['max_age']}")
                st.write(f"📝 {act['description']}")
