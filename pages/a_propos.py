# import des librairie utiles
import os
import streamlit as st
from streamlit_authenticator import Authenticate
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
#from sidebar import afficher_sidebar


# import du style css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("assets/style.css")

# Création de la side bar
st.sidebar.markdown(
    """
    <h1 style='margin: 0; font-size: 2.8rem; font-family: "Segoe UI", sans-serif;'>
        <span class='gold-texture'>MOVIE</span><span style='color:#4169E1;'>DEN</span>
    </h1>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("---")

# Navigation personnalisée sans emojis dupliqués
st.sidebar.page_link("app.py", label="Accueil", icon="🏠")
st.sidebar.page_link("pages/main.py", label="Recherche", icon="🔍")
st.sidebar.page_link("pages/reco.py", label="Recommandation", icon="⭐")
st.sidebar.markdown("---")
st.sidebar.page_link("pages/connection.py", label="Se connecter", icon="🔐")
st.sidebar.page_link("pages/creation_compte.py", label="Création de compte", icon="➕")
st.sidebar.markdown("---")
st.sidebar.page_link("pages/a_propos.py", label="A propos", icon="ℹ️")

# Affichage de la page a_propos
st.markdown(
    """
    <h1 style='margin: 0; font-size: 2.8rem; font-family: "Segoe UI", sans-serif;'>
        <span style='color:#4169E1;'>A propos de</span>
        <span class='gold-texture'>MOVIE</span><span style='color:#4169E1;'>DEN</span>
    </h1>
    """,
    unsafe_allow_html=True,
)

st.header("Application de recommandations de films")
st.subheader("Coordonnées du Cinéma :")
st.write("Adresse : Place Saint Jacques, 23300, LA SOUTERRAINE, Creuse (23)")
st.write("Téléphone : 05 55 89 51 71")
st.write("E-mail : eden@mjclasout.fr")
st.image("Eden.png")

