import streamlit as st

def afficher_sidebar(authenticator=None):

    st.sidebar.markdown(
        """
        <h1 style='margin: 0; font-size: 2.8rem; font-family: "Segoe UI", sans-serif;'>
            <span class='gold-texture'>MOVIE</span><span style='color:#4169E1;'>DEN</span>
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("---")

    st.sidebar.page_link("app.py", label="Accueil", icon="🏠")
    st.sidebar.page_link("pages/main.py", label="Recherche", icon="🔍")
    st.sidebar.page_link("pages/reco.py", label="Recommandation", icon="⭐")

    st.sidebar.markdown("---")

    st.sidebar.page_link("pages/connection.py", label="Se connecter", icon="🔐")
    st.sidebar.page_link("pages/creation_compte.py", label="Création de compte", icon="➕")

    st.sidebar.markdown("---")

    st.sidebar.page_link("pages/a_propos.py", label="A propos", icon="ℹ️")

    # Afficher le bouton logout uniquement si connecté
    if st.session_state.get("authentication_status"):

        st.sidebar.markdown("---")

        st.sidebar.write(f"Bienvenue {st.session_state['name']}")

        authenticator.logout("Déconnexion", "sidebar")

    if not st.session_state.get("authentication_status"):
        st.sidebar.page_link("pages/connection.py", label="Se connecter", icon="🔐")
        st.sidebar.page_link("pages/creation_compte.py", label="Création de compte", icon="➕")   

     