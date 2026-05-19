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
        <span class='white'>MOVIE</span><span style='color:#4169E1;'>DEN</span>
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
st.sidebar.page_link("pages/main.py", label="A propos", icon="ℹ️")

# création de alias container
c = st.container()

# Affichage de la page main
logo_path_eden = os.path.join(BASE_DIR, "assets", "uploads", "Logo eden.png")

if os.path.exists(logo_path_eden):
    col_logo, col_title = st.columns([1, 11])
    with col_logo:
        st.image(logo_path_eden, width=100)
    with col_title:
        st.markdown(
            """
            <h1 style='margin: 0; font-size: 2.8rem; font-family: "Segoe UI", sans-serif;'>
                <span style='color:#4169E1;'>Bienvenue sur </span>
                <span class='white'>MOVIE</span><span style='color:#4169E1;'>DEN</span>
            </h1>
            """,
            unsafe_allow_html=True,
        )
else:
    st.markdown(
        """
        <h1 style='margin: 0; font-size: 2.8rem; font-family: "Segoe UI", sans-serif;'>
            <span style='color:#4169E1;'>Bienvenue sur </span>
            <span class='white'>MOVIE</span><span style='color:#4169E1;'>DEN</span>
        </h1>
        """,
        unsafe_allow_html=True,
    )

st.subheader("Le paradis du cinéma")
st.write('___')

# source des images d'affiche de film
source = "https://image.tmdb.org/t/p/original/"

df_popular = df_movies.sort_values(by='popularity', ascending=False).reset_index(drop=True)

# Bannière du film #1 (backdrop si disponible)
if not df_popular.empty:
    top1 = df_popular.iloc[0]
    banner_src = top1['backdrop_path'] if pd.notna(top1.get('backdrop_path', '')) and top1['backdrop_path'] != '' else top1['poster_path']
    if pd.notna(banner_src) and banner_src != '':
        st.image(f"{source}{banner_src}", width=True)
    st.markdown(f"\n### {top1['title']}")
    yt_search = f"https://www.youtube.com/results?search_query={top1['title'].replace(' ', '+')}+bande+annonce"
    st.markdown(f'<a href="{yt_search}" target="_blank" style="float:right; padding:8px 12px; background:#4169E1; color:white; border-radius:6px; text-decoration:none;">Voir la bande annonce</a>', unsafe_allow_html=True)

# Top 10 affiches avec bouton 'Afficher plus'
st.subheader("🔥 Top 10 des films les plus populaires")
top10 = df_popular.head(10)
if 'show_more' not in st.session_state:
    st.session_state.show_more = False

cols_main, col_btn = st.columns([11, 1])
with cols_main:
    for row in range(2):
        cols = st.columns(5, gap="medium")
        for i, col in enumerate(cols):
            idx = row * 5 + i
            if idx < len(top10):
                movie = top10.iloc[idx]
                with col:
                    st.image(f"{source}{movie['poster_path']}", use_container_width=True)
                    st.write(f"**{movie['title']}**")
                    genres = eval(movie['genres']) if isinstance(movie['genres'], str) else movie['genres']
                    st.caption(", ".join(genres) if isinstance(genres, list) else str(genres))
                    note = movie['vote_average']
                    st.caption(f"⭐ {note:.1f}/10")
with col_btn:
    if st.button("Afficher plus"):
        st.session_state.show_more = not st.session_state.show_more

if st.session_state.show_more:
    more = df_popular.iloc[10:20]
    for row_start in range(0, len(more), 5):
        cols = st.columns(5, gap="medium")
        for i in range(5):
            idx = row_start + i
            if idx < len(more):
                movie = more.iloc[idx]
                with cols[i]:
                    st.image(f"{source}{movie['poster_path']}", use_container_width=True)
                    st.write(f"**{movie['title']}**")

# Section films à venir
st.subheader("🎬 Films à venir")
today = pd.to_datetime('today').normalize()
df_movies['release_date_parsed'] = pd.to_datetime(df_movies['release_date'], errors='coerce')
upcoming = df_movies[df_movies['release_date_parsed'] > today].sort_values('release_date_parsed').head(6).reset_index(drop=True)
if not upcoming.empty:
    cols = st.columns(3, gap="large")
    for i, col in enumerate(cols):
        if i < len(upcoming):
            movie = upcoming.iloc[i]
            with col:
                st.image(f"{source}{movie['poster_path']}", use_container_width=True)
                st.write(f"**{movie['title']}**")
                st.caption(movie['release_date'])
else:
    st.write("Aucun film à venir trouvé.")

# Sidebar footer: Powered by DigData + zone  logo
st.sidebar.markdown("---")
st.sidebar.markdown("<div style='font-size:12px; color:gray;'>Powered by DigData</div>", unsafe_allow_html=True)
logo_path = os.path.join(BASE_DIR, "assets", "uploads", "logo.png")

if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=40)