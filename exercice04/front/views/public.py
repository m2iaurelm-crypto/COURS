import streamlit as st
from api_client import get_frequentations_api

def render_public_page():
    st.header("Observatoire Public de Fréquentation")
    
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = 1

    page = st.session_state["current_page"]
    page_size = 5

    res = get_frequentations_api(page=page, page_size=page_size)
    if res and res.status_code == 200:
        data = res.json()
        st.write(f"**Page {data['page']} / {data['pages']}** (Total : {data['total']} observations)")
        
        if data["items"]:
            st.table(data["items"])
        else:
            st.info("Aucune donnée sur cette page.")

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Précédent", disabled=(page <= 1)):
                st.session_state["current_page"] -= 1
                st.rerun()
        with col2:
            if st.button("Suivant", disabled=(page >= data["pages"])):
                st.session_state["current_page"] += 1
                st.rerun()
    else:
        st.error("Erreur lors du chargement des données de fréquentation.")