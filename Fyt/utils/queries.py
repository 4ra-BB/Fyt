# Librerías necesarias
import streamlit as st
from supabase import create_client, Client
import requests
import datetime
from config import supabase

# Insertar un nuevo registro en una tabla
def insert_data(table_name, data_dict):
    try:
        response = supabase.table(table_name).insert(data_dict).execute()
        return response
    except Exception as e:
        return {"error": str(e)}

# Obtener datos de una tabla con filtros opcionales
def get_data(table_name, filters=None):
    try:
        query = supabase.table(table_name).select("*")
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        response = query.execute()
        return response
    except Exception as e:
        return {"error": str(e)}

# Actualizar un registro por ID
def update_data(table_name, record_id, data_dict, id_field="id"):
    try:
        response = supabase.table(table_name).update(data_dict).eq(id_field, record_id).execute()
        return response
    except Exception as e:
        return {"error": str(e)}

# Eliminar un registro por ID
def delete_data(table_name, record_id, id_field="id"):
    try:
        response = supabase.table(table_name).delete().eq(id_field, record_id).execute()
        return response
    except Exception as e:
        return {"error": str(e)}
