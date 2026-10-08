import streamlit as st
from api_client import get_bilan_api

def render_private_page():
    st.header("Bilan Analytique Métier")

    token = st.session_state.get("token")
    res = get_bilan_api(token)

    if not res:
        st.error("Impossible de contacter l'API backend.")
        return

    if res.status_code == 200:
        bilan = res.json()
        st.success("Accès autorisé au bilan analytique.")
        col1, col2, col3 = st.columns(3)
        col1.metric("Observations", bilan["nb_observations"])
        col2.metric("Total Visiteurs", bilan["total_visiteurs"])
        col3.metric("Moyenne : Visiteurs / Obs", bilan["moyenne_visiteurs"])
    elif res.status_code == 401:
        st.error("401 Non autorisé : Veuillez vous connecter avec des identifiants valides.")
    elif res.status_code == 403:
        st.warning("403 Interdit : Votre compte ne possède pas le rôle 'analyst' pour consulter ce bilan.")