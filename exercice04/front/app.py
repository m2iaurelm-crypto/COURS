import streamlit as st
from views.public import render_public_page
from views.login import render_login_page
from views.private import render_private_page

st.set_page_config(page_title="Fréquentation Médiathèques", layout="wide")

if "token" not in st.session_state:
    st.session_state["token"] = None

st.sidebar.title("Navigation")

if st.session_state["token"]:
    st.sidebar.write(f"Connecté en tant que : **{st.session_state.get('username')}**")
    if st.sidebar.button("Se déconnecter"):
        st.session_state["token"] = None
        st.session_state["username"] = None
        st.rerun()

menu = st.sidebar.radio("Pages", ["Fréquentation (Public)", "Bilan (Privé)", "Connexion"])

if menu == "Fréquentation (Public)":
    render_public_page()
elif menu == "Bilan (Privé)":
    render_private_page()
elif menu == "Connexion":
    if st.session_state["token"]:
        st.info("Vous êtes déjà connecté.")
    else:
        render_login_page()