import os
import streamlit as st
from streamlit_authenticator import Authenticate
import pandas as pd
import numpy as np
from app import afficher_barre_navigation
import json


# import du style css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("assets/style.css")

st.set_page_config(layout="wide")

# Barre de navigation en haut avec bouton connexion à droite
afficher_barre_navigation()

# Fonction pour charger les comptes utilisateurs
def charger_comptes():
    """Charge les comptes utilisateurs depuis le fichier JSON"""
    chemin_comptes = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "comptes.json")
    if os.path.exists(chemin_comptes):
        with open(chemin_comptes, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'usernames': {
            'utilisateur': {
                'name': 'utilisateur',
                'password': 'utilisateurMDP',
                'email': 'utilisateur@gmail.com',
                'failed_login_attemps': 0,
                'logged_in': False,
                'role': 'utilisateur'
            },
            'root': {
                'name': 'root',
                'password': 'rootMDP',
                'email': 'admin@gmail.com',
                'failed_login_attemps': 0,
                'logged_in': False,
                'role': 'administrateur'
            }
        }
    }

# Fonction pour sauvegarder les comptes utilisateurs
def sauvegarder_comptes(comptes):
    """Sauvegarde les comptes utilisateurs dans le fichier JSON"""
    chemin_dossier = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(chemin_dossier, exist_ok=True)
    chemin_comptes = os.path.join(chemin_dossier, "comptes.json")
    with open(chemin_comptes, 'w', encoding='utf-8') as f:
        json.dump(comptes, f, ensure_ascii=False, indent=4)

# Charger les comptes existants
comptes = charger_comptes()

st.markdown(
    """
    <style>
    div[data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
st.sidebar.page_link("pages/recherche_film.py", label="Recherche", icon="🔍")
st.sidebar.page_link("pages/reco.py", label="Recommandation", icon="⭐")
st.sidebar.markdown("---")
st.sidebar.page_link("pages/a_propos.py", label="A propos", icon="ℹ️")

# Affichage de la creation_compte
st.markdown(
    """
    <h1 style='margin: 0; font-size: 2.8rem; font-family: "Segoe UI", sans-serif;'>
        <span style='color:#4169E1;'>Créer un nouveau compte</span>
        <span class='gold-texture'>MOVIE</span><span style='color:#4169E1;'>DEN</span>
    </h1>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# Affichage du formulaire de création de compte
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.subheader("📝 Formulaire d'inscription", divider="blue")
    
    # Initialiser session_state pour le formulaire
    if 'new_username' not in st.session_state:
        st.session_state.new_username = ""
    if 'new_email' not in st.session_state:
        st.session_state.new_email = ""
    if 'new_password' not in st.session_state:
        st.session_state.new_password = ""
    if 'new_password_confirm' not in st.session_state:
        st.session_state.new_password_confirm = ""
    
    new_username = st.text_input("👤 Nom d'utilisateur", value=st.session_state.new_username)
    new_email = st.text_input("📧 Email", value=st.session_state.new_email)
    new_password = st.text_input("🔐 Mot de passe", type="password", value=st.session_state.new_password)
    new_password_confirm = st.text_input("🔐 Confirmer le mot de passe", type="password", value=st.session_state.new_password_confirm)
    
    st.markdown("")
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("✅ Créer un compte", use_container_width=True, key="btn_create"):
            if not new_username:
                st.error("❌ Veuillez entrer un nom d'utilisateur")
            elif not new_email:
                st.error("❌ Veuillez entrer une adresse email")
            elif not new_password:
                st.error("❌ Veuillez entrer un mot de passe")
            elif new_password != new_password_confirm:
                st.error("❌ Les mots de passe ne correspondent pas")
            elif len(new_password) < 6:
                st.error("❌ Le mot de passe doit contenir au moins 6 caractères")
            elif new_username in comptes['usernames']:
                st.error("❌ Ce nom d'utilisateur existe déjà")
            else:
                # Ajouter le nouveau compte
                comptes['usernames'][new_username] = {
                    'name': new_username,
                    'password': new_password,
                    'email': new_email,
                    'failed_login_attemps': 0,
                    'logged_in': False,
                    'role': 'utilisateur'
                }
                # Sauvegarder les comptes
                sauvegarder_comptes(comptes)
                
                st.success("✅ Compte créé avec succès!")
                st.balloons()
                st.info(f"Vous pouvez maintenant vous connecter avec le nom d'utilisateur: **{new_username}**")
                st.session_state.new_username = ""
                st.session_state.new_email = ""
                st.session_state.new_password = ""
                st.session_state.new_password_confirm = ""
    
    with col_btn2:
        if st.button("🚪 Retour à la connexion", use_container_width=True, key="btn_back"):
            st.switch_page("pages/connection.py")

st.markdown("")
st.markdown("""
<div style='text-align: center; color: #FFD700; font-size: 0.9rem; margin-top: 2rem;'>
💡 Astuce: Votre mot de passe doit être sécurisé et différent de votre nom d'utilisateur
</div>
""", unsafe_allow_html=True)