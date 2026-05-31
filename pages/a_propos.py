# import des librairie utiles
import os
import streamlit as st
from app import afficher_barre_navigation, local_css, BASE_DIR


st.set_page_config(layout="wide")
# import du style css

local_css(os.path.join(BASE_DIR, "assets", "style.css"))  # ← chemin absolu


# Barre de navigation en haut avec bouton connexion à droite
afficher_barre_navigation()


st.header("Application de recommandations de films")
st.subheader("Coordonnées du Cinéma :")
st.write("Adresse : Place Saint Jacques, 23300, LA SOUTERRAINE, Creuse (23)")
st.write("Téléphone : 05 55 89 51 71")
st.write("E-mail : eden@mjclasout.fr")
st.image(os.path.join(BASE_DIR, "assets", "uploads", "Eden.png"))

