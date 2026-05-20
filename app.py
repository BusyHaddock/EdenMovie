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
st.sidebar.page_link("pages/recherche_film.py", label="Recherche", icon="🔍")  #kk
st.sidebar.page_link("pages/reco.py", label="Recommandation", icon="⭐")
st.sidebar.markdown("---")
st.sidebar.page_link("pages/a_propos.py", label="A propos", icon="ℹ️")

# création de alias container
c = st.container()

# Affichage de la page main
logo_path_eden = os.path.join(BASE_DIR, "assets", "uploads", " ")

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
        st.image(f"{source}{banner_src}", use_container_width=True)
    st.markdown(f"\n### {top1['title']}")
    yt_search = f"https://www.youtube.com/results?search_query={top1['title'].replace(' ', '+')}+bande+annonce"
    st.markdown(f'<a href="{yt_search}" target="_blank" style="float:right; padding:8px 12px; background:#4169E1; color:white; border-radius:6px; text-decoration:none;">Voir la bande annonce</a>', unsafe_allow_html=True)

# Top 10 affiches avec bouton 'Afficher plus'
st.subheader("🔥 Films les plus populaires")
top5 = df_popular.head(5)
if 'show_more' not in st.session_state:
    st.session_state.show_more = False

cols = st.columns(5, gap="medium")
for i, (_, movie) in enumerate(top5.iterrows()):
    with cols[i]:
        genres = eval(movie['genres']) if isinstance(movie['genres'], str) else movie['genres']
        genres_text = ", ".join(genres) if isinstance(genres, list) else str(genres)
        vote_avg = movie['vote_average'] if pd.notna(movie['vote_average']) else 0
        st.markdown(f"""
            <a href="?page=pages/recherche_film.py&movie_id={movie['id']}" style="text-decoration:none; color:inherit;">
            <div class="movie-card">
                <img src="{source}{movie['poster_path']}" />
                <div class="movie-title">{movie['title']}</div>
                <div class="movie-info">⭐ {vote_avg:.1f}/10</div>
                <div class="movie-info">📅 {movie['release_date']}</div>
                <div class="movie-info">🎭 {genres_text}</div>
            </div>
            </a>
            """, unsafe_allow_html=True)

btn_cols = st.columns([1, 1, 1, 1, 1], gap="medium")
with btn_cols[2]:
    label = "Afficher moins" if st.session_state.show_more else "Afficher plus"
    if st.button(label):
        st.session_state.show_more = not st.session_state.show_more
        st.rerun()

if st.session_state.show_more:
    more = df_popular.iloc[5:10]
    for row_start in range(0, len(more), 5):
        cols = st.columns(5, gap="medium")
        for i in range(5):
            idx = row_start + i
            if idx < len(more):
                movie = more.iloc[idx]
                with cols[i]:
                    genres = eval(movie['genres']) if isinstance(movie['genres'], str) else movie['genres']
                    genres_text = ", ".join(genres) if isinstance(genres, list) else str(genres)
                    vote_avg = movie['vote_average'] if pd.notna(movie['vote_average']) else 0
                    st.markdown(f"""
                        <a href="?page=pages/recherche_film.py&movie_id={movie['id']}" style="text-decoration:none; color:inherit;">
                        <div class="movie-card">
                            <img src="{source}{movie['poster_path']}" />
                            <div class="movie-title">{movie['title']}</div>
                            <div class="movie-info">⭐ {vote_avg:.1f}/10</div>
                            <div class="movie-info">📅 {movie['release_date']}</div>
                            <div class="movie-info">🎭 {genres_text}</div>
                        </div>
                        </a>
                        """, unsafe_allow_html=True)

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