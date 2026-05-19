# import des librairie utiles
import os
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors


# import des données

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df_movies = pd.read_csv(os.path.join(BASE_DIR, "data", "df_final.csv"))
df_ml = pd.read_csv(os.path.join(BASE_DIR, "data", "df_reco_clean.csv"))

st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
    color: white;
}

.movie-card {
    background-color: #161B22;
    padding: 14px;
    border-radius: 16px;
    margin-bottom: 25px;
    transition: 0.3s;
    box-shadow: 0 0 12px rgba(0,0,0,0.4);
}

.movie-card:hover {
    transform: scale(1.03);
    box-shadow: 0 0 22px rgba(30,144,255,0.5);
}

.movie-card img {
    width: 100%;
    border-radius: 14px;
}

.movie-title {
    font-size: 20px;
    font-weight: bold;
    color: white;
    margin-top: 12px;
}

.movie-info {
    color: #B8C1CC;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# import du style css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("assets/style.css")

# Entrainement du modèle de recommandation

df_ml = df_ml.reset_index(drop=True)  # ← ici les index deviennent 0,1,2,3,4...

features = df_ml.drop(columns=['id'])
X = features.values

model = NearestNeighbors(n_neighbors=6, metric='cosine')
model.fit(X)
distances, indices = model.kneighbors(X)

# Fonction de recommandation
def reco_movie(movie: str):
    # On récupère l'id du film depuis df_final
    id_movie = df_movies[df_movies['title'] == movie]['id'].values[0]
    
    # On trouve l'indice dans df_ml via l'id
    indice_ml = df_ml[df_ml['id'] == id_movie].index[0]
    
    # On récupère les ids des voisins depuis df_ml
    ids_voisins = df_ml.iloc[indices[indice_ml, 1:]]['id'].values
    
    # On affiche depuis df_final via les ids
    df_reco = df_movies[df_movies['id'].isin(ids_voisins)]
    return df_reco

st.set_page_config(layout="wide")

# Masquer le menu de pages automatique de Streamlit si vous utilisez un système de navigation personnalisé.
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
st.sidebar.page_link("pages/recherche_film.py", label="Recherche", icon="🔍")  #kk
st.sidebar.page_link("pages/reco.py", label="Recommandation", icon="⭐")
st.sidebar.markdown("---")
st.sidebar.page_link("pages/main.py", label="A propos", icon="ℹ️")

# création de alias container
c = st.container()

# Affichage de la page main

st.markdown(
    """
    <h1 style='margin: 0; font-size: 2.8rem; font-family: "Segoe UI", sans-serif;'>
        <span style='color:#4169E1;'>Bienvenue sur </span>
        <span class='gold-texture'>MOVIE</span><span style='color:#4169E1;'>DEN</span>
    </h1>
    """,
    unsafe_allow_html=True,
)

st.subheader("Le paradis du cinéma")
st.write('___')

# source des images d'affiche de film
source = "https://image.tmdb.org/t/p/original/"

df_first = df_movies.sort_values(by='popularity', ascending=False).head(3)


movie_input = st.selectbox(
    "Quel est le dernier film que vous avez aimé ?",
    options=[""] + sorted(df_movies['title'].tolist()),
    index=0,
    placeholder="Rechercher un film..."
)

with st.container(border=True):
    if movie_input:
        df_reco_clean = reco_movie(movie_input).reset_index(drop=True)
        st.subheader("🎬 Nous vous recommandons :")
        cols = st.columns(5, gap="medium")
        for i, col in enumerate(cols):
            with col:
                st.image(
                    f"{source}{df_reco_clean['poster_path'].iloc[i]}",
                    use_container_width=True
                )
                st.write(f"**{df_reco_clean['title'].iloc[i]}**")
                # Afficher les genres
                genres = eval(df_reco_clean['genres'].iloc[i]) if isinstance(df_reco_clean['genres'].iloc[i], str) else df_reco_clean['genres'].iloc[i]
                st.caption(", ".join(genres) if isinstance(genres, list) else str(genres))
                # Afficher la note avec une étoile
                note = df_reco_clean['vote_average'].iloc[i]
                st.caption(f"⭐ {note:.1f}/10")
    else:
        st.subheader("🔥 Les films les plus populaires :")
        cols = st.columns(3, gap="large")
        for i, col in enumerate(cols):
            with col:
                st.image(
                    f"{source}{df_first['poster_path'].iloc[i]}",
                    use_container_width=True
                )
                st.write(f"**{df_first['title'].iloc[i]}**")
                # Afficher les genres
                genres = eval(df_first['genres'].iloc[i]) if isinstance(df_first['genres'].iloc[i], str) else df_first['genres'].iloc[i]
                st.caption(", ".join(genres) if isinstance(genres, list) else str(genres))
                # Afficher la note avec une étoile
                note = df_first['vote_average'].iloc[i]
                st.caption(f"⭐ {note:.1f}/10")