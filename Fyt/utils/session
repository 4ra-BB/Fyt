import streamlit as st

def show_logout():
    if st.session_state.get("authenticated", False):
        with st.sidebar:
            if st.button("Cerrar sesión"):
                st.session_state.clear()
                st.rerun()
