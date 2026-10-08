import streamlit as st
from api_client import login_api

def render_login_page():
    st.header("Connexion")
    with st.form("login_form"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submit = st.form_submit_button("Se connecter")

        if submit:
            res = login_api(username, password)
            if res and res.status_code == 200:
                data = res.json()
                st.session_state["token"] = data["access_token"]
                st.session_state["username"] = username
                st.success("Connexion réussie !")
                st.rerun()
            else:
                st.error("Identifiants invalides ou service indisponible.")