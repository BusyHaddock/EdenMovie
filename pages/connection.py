# import des librairie utiles
import os
import streamlit as st
from streamlit_authenticator import Authenticate
import pandas as pd
import numpy as np
import json
from app import afficher_barre_navigation

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

# Charger les comptes depuis le fichier JSON
lesDonneesDesComptes = charger_comptes()

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
        <span class='white'>Movi</span><span style='color:#4169E1;'>EDEN</span>
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

# Affichage de la page connection
st.markdown(
    """
    <h1 style='margin: 0; font-size: 2.8rem; font-family: "Segoe UI", sans-serif;'>
        <span class='white'>Movi</span><span style='color:#4169E1;'>EDEN</span>
    </h1>
    """,
    unsafe_allow_html=True,
)

authenticator = Authenticate(
    lesDonneesDesComptes,  # Les données des comptes
    "cookie name",         # Le nom du cookie, un str quelconque
    "cookie key",          # La clé du cookie, un str quelconque
    30,                    # Le nombre de jours avant que le cookie expire
)

# Affichage sidebar
#afficher_sidebar(authenticator)

# Utiliser la méthode login pour afficher le formulaire de connexion et vérifier les informations d'identification de l'utilisateur
authenticator.login()

# Gérer l'accès en fonction des informations renseignées
def accueil():
      st.title(f"Bonjour {st.session_state['name']}, vous êtes connecté à l'application !")
      
      # Création de 3 colonnes 
      col1, col2 = st.columns(2)

      # Contenu de la première colonne : 
      with col1:
       st.image("assets/uploads/Faire_recherche_film.png")
       if st.button("Faire une recherche"):
        st.switch_page("pages/recherche_film.py")

    # Contenu de la deuxième colonne :
      with col2:
       st.image("assets/uploads/Demander_recommendation.png")
       if st.button("Demander une recommandation"):
        st.switch_page("pages/reco.py")

if st.session_state["authentication_status"]:
  # Le bouton de déconnexion
  authenticator.logout("Déconnexion", "sidebar")
  with st.sidebar:
    st.write(f"Bienvenue {st.session_state['name']}")
  accueil()

elif st.session_state["authentication_status"] is False:
    st.error("L'username ou le password est/sont incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning('Les champs username et mot de passe doivent être remplie')
    st.markdown("")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("""
        <style>
        .create_account_btn {
            display: flex;
            justify-content: center;
            margin-top: 1rem;
        }
        .create_account_btn button {
            background-color: #4169E1;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1.5rem;
            font-weight: bold;
            width: 100%;
        }
        .create_account_btn button:hover {
            background-color: #FFD700;
            color: #1a1a2e;
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("➕ Créer un compte", key="create_account", use_container_width=True):
            st.switch_page("pages/creation_compte.py")


local_css("assets/style.css")

st.markdown("""
<style>

/* Texte saisi dans username/password */
.stTextInput input {
    color: white !important;
}

/* Placeholder */
.stTextInput input::placeholder {
    color: #cccccc !important;
}

/* Fond des champs */
.stTextInput div[data-baseweb="input"] {
    background-color: #1e1e1e !important;
}

/* Label */
.stTextInput label {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)