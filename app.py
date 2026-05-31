# import des librairie utiles
import os
import base64
import streamlit as st
import pandas as pd
import numpy as np
import ast
import requests
from datetime import datetime, timedelta
from streamlit_authenticator import Authenticate

st.set_page_config(
    layout="wide",
    page_title="MOVIEDEN - Accueil",
    page_icon="🏠")


# import des données

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df_movies = pd.read_csv(os.path.join(BASE_DIR, "data", "df_film.csv"))
df_ml = pd.read_csv(os.path.join(BASE_DIR, "data", "df_reco_clean.csv"))

def afficher_barre_navigation():
    # Masquer sidebar Streamlit par défaut
    st.markdown("""
        <style>
        div[data-testid="stSidebarNav"] { display: none; }
        </style>
    """, unsafe_allow_html=True)

    # Logo sidebar
    st.sidebar.markdown("""
        <h1 style='margin: 0; font-size: 1.5rem; font-family: "Segoe UI", sans-serif; text-align: center;'>
            <span style='color:white;'>MOVI</span><span style='color:#4169E1;'>EDEN</span>
        </h1>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # Navigation
    st.sidebar.page_link("app.py", label="Accueil", icon="🏠")
    st.sidebar.page_link("pages/recherche_film.py", label="Recherche", icon="🔍")
    st.sidebar.page_link("pages/reco.py", label="Recommandation", icon="⭐")
    st.sidebar.markdown("---")
    st.sidebar.page_link("pages/a_propos.py", label="A propos", icon="ℹ️")

    # Footer logo
    logo_path = os.path.join(BASE_DIR, "assets", "uploads", "logo.png")
    footer_html = "<div class='sidebar-footer'><div style='font-size:12px; color:gray;'>Powered by DigData</div>"
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            logo_base64 = base64.b64encode(f.read()).decode('utf-8')
        footer_html += f"<img src='data:image/png;base64,{logo_base64}' width='40' style='border-radius:8px; margin-left:12px;'/>"
    footer_html += "</div>"
    st.sidebar.markdown(footer_html, unsafe_allow_html=True)

    # Barre connexion en haut à droite
    top_bar_cols = st.columns([10, 1.5], gap="medium")
    with top_bar_cols[1]:
        if st.session_state.get("authentication_status"):
            st.write(f"👤 {st.session_state.get('name', 'Utilisateur')}")
            if st.button("🚪 Déconnexion", key="logout_top"):
                st.session_state["authentication_status"] = False
                st.rerun()
        else:
            st.page_link("pages/connection.py", label="🔐 Se connecter")

def parse_genres(val):
    """Safely parse a genres value from the dataframe into a list of strings.

    Handles lists represented as Python lists ("['a','b']"), comma-separated
    strings ("Action,Comedy"), empty values and already-list objects.
    """
    if isinstance(val, list):
        return [str(x) for x in val]
    if pd.isna(val) or val == '':
        return []
    if isinstance(val, str):
        s = val.strip()
        # Try literal_eval first (handles "['a', 'b']" and similar)
        try:
            parsed = ast.literal_eval(s)
            if isinstance(parsed, (list, tuple)):
                return [str(x) for x in parsed]
            if isinstance(parsed, str):
                return [g.strip() for g in parsed.split(',') if g.strip()]
        except Exception:
            # Fallback: treat as comma-separated string
            return [g.strip() for g in s.split(',') if g.strip()]
    # Fallback to string conversion
    return [str(val)]


def get_upcoming_movies_tmdb(headers=None):
    """Fetch upcoming movies from TMDB API for the next 7 days.

    Accepts a headers dict (for Bearer tokens) or falls back to a query API key.
    Returns a list of movies with release dates within the next 7 days.
    """
    if headers is None:
        # Try to read from streamlit secrets
        try:
            headers = st.secrets.get("headers")
        except AttributeError:
            headers = None

    api_key = None
    if not headers:
        try:
            api_key = st.secrets.get("tmdb_api_key")
        except AttributeError:
            api_key = None

    if not headers and not api_key:
        st.warning("⚠️ Clé API TMDB non configurée. Affichage des films du dataset.")
        return None

    try:
        url = "https://api.themoviedb.org/3/movie/upcoming"
        params = {
            "language": "fr-FR",
            "page": 1,
            "region": "FR"
        }
        request_headers = None
        if headers:
            request_headers = headers
        elif api_key:
            params["api_key"] = api_key

        response = requests.get(url, params=params, headers=request_headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Filter for movies releasing within the next 7 days
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        
        upcoming = []
        for movie in data.get('results', []):
            release_date_str = movie.get('release_date', '')
            if release_date_str:
                try:
                    release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
                    if today <= release_date <= next_week:
                        upcoming.append({
                            'title': movie.get('title', 'N/A'),
                            'release_date': release_date_str,
                            'poster_path': movie.get('poster_path', ''),
                            'overview': movie.get('overview', ''),
                            'vote_average': movie.get('vote_average', 0)
                        })
                except ValueError:
                    continue
        
        return upcoming if upcoming else None
    except Exception as e:
        st.warning(f"⚠️ Erreur API TMDB: {str(e)}")
        return None
df_movies = df_movies.drop_duplicates(subset='tconst').reset_index(drop=True)

# import du style css
def local_css(file_name):
    with open(file_name, encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css(os.path.join(BASE_DIR, "assets", "style.css")) 


# Barre de navigation en haut avec bouton connexion à droite
afficher_barre_navigation()

# création de alias container
c = st.container()

# Affichage de la page main
ban_path_eden = os.path.join(BASE_DIR, "assets", "uploads", "ban_eden.png")

if os.path.exists(ban_path_eden):
    with open(ban_path_eden, 'rb') as f:
        ban_base64 = base64.b64encode(f.read()).decode('utf-8')
    st.markdown(
        f"""
        <div class='main-header-banner' style="background-image:url('data:image/png;base64,{ban_base64}')">
            <div class='main-header-banner-overlay'>
                <h1>
                    <span style='color:#4169E1;'>Bienvenue sur </span>
                    <span class='white'>MOVI</span><span style='color:#4169E1;'>EDEN</span>
                </h1>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <h1 style='margin: 0; font-size: 2.8rem; font-family: "Segoe UI", sans-serif;'>
            <span style='color:#4169E1;'>Bienvenue sur </span>
            <span class='white'>MOVI</span><span style='color:#4169E1;'>EDEN</span>
        </h1>
        """,
        unsafe_allow_html=True,
    )

st.subheader("Le paradis du cinéma")
st.write('___')
# source des images d'affiche de film
source = "https://image.tmdb.org/t/p/original/"

df_popular = df_movies[
    (df_movies['startYear'] <= 2026) &
    (df_movies['startYear'] >= 2024) &
    (df_movies['avg_rating_imdb'] > 0) &
    (df_movies['avg_rating_tmdb'] > 0)
].sort_values(by='popularity', ascending=False).reset_index(drop=True)

# Section films à venir
st.subheader("Bientôt en Salle")
upcoming_movies = get_upcoming_movies_tmdb()

if upcoming_movies:
    cols = st.columns(min(3, len(upcoming_movies)), gap="large")
    for i, movie in enumerate(upcoming_movies[:3]):
        with cols[i]:
            poster_url = f"{source}{movie['poster_path']}" if movie['poster_path'] else ""
            if poster_url:
                st.markdown(f"""
                            <div class='upcoming-card'>
                                <div class='upcoming-poster'
                                style="background-image:url('{poster_url}')"></div>
                                <div class='upcoming-card-text'>
                                <div class='upcoming-card-title'>{movie['title']}</div>
                                <div class='upcoming-date'>
                                📅 {movie['release_date']}</div>
                            <p class='overview-clamp'>{movie['overview']}</p>
                             </div>

                            </div>
                            """, unsafe_allow_html=True)      
            else:
                st.markdown(f"""
                    <div class='upcoming-card'>
                        <div class='upcoming-card-overlay'>
                            <div class='upcoming-card-title'>{movie['title']}</div>
                            <div class='upcoming-date'>📅 {movie['release_date']}</div>
                            <p class='overview-clamp'>{movie['overview']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
else:
    today = pd.to_datetime('today').normalize()
    next_week = today + pd.Timedelta(days=7)
    df_movies['release_date_parsed'] = pd.to_datetime(df_movies['startYear'], errors='coerce')
    upcoming = df_movies[(df_movies['release_date_parsed'] > today) & 
                         (df_movies['release_date_parsed'] <= next_week)].sort_values('release_date_parsed').head(3).reset_index(drop=True)
    if not upcoming.empty:
        cols = st.columns(3, gap="large")
        for i, col in enumerate(cols):
            if i < len(upcoming):
                movie = upcoming.iloc[i]
                with col:
                    poster_url = f"{source}{movie['poster_path']}" if pd.notna(movie['poster_path']) and movie['poster_path'] != '' else ''
                    if poster_url:
                        st.markdown(f"""
                            <div class='upcoming-card upcoming-card-bg' style="background-image:url('{poster_url}')">
                                <div class='upcoming-card-overlay'>
                                    <div class='upcoming-card-title'>{movie['title_fr']}</div>
                                    <div class='upcoming-date'>📅 {movie['startYear']}</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class='upcoming-card'>
                                <div class='upcoming-card-overlay'>
                                    <div class='upcoming-card-title'>{movie['title_fr']}</div>
                                    <div class='upcoming-date'>📅 {movie['startYear']}</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ Aucun film à venir cette semaine.")

# Top du moment
st.subheader("Top du moment")
if not df_popular.empty:
    top1 = df_popular.iloc[0]
    banner_src = top1['backdrop_path'] if pd.notna(top1.get('backdrop_path', '')) and top1['backdrop_path'] != '' else top1['poster_path']
    poster_src = top1['poster_path'] if pd.notna(top1.get('poster_path', '')) and top1['poster_path'] != '' else banner_src
    vote_avg_imdb = top1['avg_rating_imdb'] if pd.notna(top1['avg_rating_imdb']) else 0
    vote_avg_tmdb = top1['avg_rating_tmdb'] if pd.notna(top1['avg_rating_tmdb']) else 0
    overview_text = top1['overview'] if pd.notna(top1.get('overview', '')) else ''
 
    st.markdown(f"""
        <div class="top1-banner" style="background-image:url('{source}{banner_src}');">
            <div class="top1-overlay">
                <img src="{source}{poster_src}" class="top1-poster" />
                <div class="top1-details">
                    <h2>{top1['title_fr']}</h2>
                    <div class="rating">⭐ IMDB {vote_avg_imdb:.1f}/10 · ⭐ TMDb {vote_avg_tmdb:.1f}/10 · 📅 {top1['startYear']}</div>
                    <p class="synopsis">{overview_text}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    if st.button(
                "🎬 Voir détails",
            ):
        st.session_state["selected_tconst"] = top1["tconst"]
        st.switch_page("pages/movie_detail.py")
    if "show_trailer" not in st.session_state:
        st.session_state.show_trailer = False


st.markdown("<div class='top-list'>", unsafe_allow_html=True)
for idx, (_, movie) in enumerate(df_popular.iloc[1:5].iterrows(), start=2):
    genres = parse_genres(movie['genres'])
    genres_text = ", ".join(genres) if isinstance(genres, list) else str(genres)
    vote_avg_imdb = movie['avg_rating_imdb'] if pd.notna(movie['avg_rating_imdb']) else 0
    vote_avg_tmdb = movie['avg_rating_tmdb'] if pd.notna(movie['avg_rating_tmdb']) else 0
    banner_src = movie['backdrop_path'] if pd.notna(movie.get('backdrop_path', '')) and movie['backdrop_path'] != '' else movie['poster_path']

    st.markdown(f"""
        <div class="top-list-card" style="--poster: url('{banner_src}');">
                    <div class="top-number">{idx}</div>
                        <div class="top-card-content">
                            <img src="{source}{movie['poster_path']}" class="small-poster" />
                                <div class="top-card-text">
                                <div class="movie-title">{movie['title_fr']}</div>
                                <div class="movie-info">⭐ IMDB : {vote_avg_imdb:.1f}/10 · ⭐ TMDb : {vote_avg_tmdb:.1f}/10</div>
                                <div class="movie-info">📅 {movie['startYear']} · {genres_text}</div>
        """, unsafe_allow_html=True)
    if st.button("🎬 Voir détails", key=f"details_{idx}"):
        st.session_state["selected_tconst"] = movie["tconst"]
        st.switch_page("pages/movie_detail.py")
st.markdown("</div>", unsafe_allow_html=True)
    
if 'show_more' not in st.session_state:
    st.session_state.show_more = False

more_container = st.empty()

if st.session_state.show_more:  # ← plus de .get() avec valeur par défaut
    more = df_popular.iloc[5:10]
    if not more.empty:
        st.markdown("<div class='top-list'>", unsafe_allow_html=True)
        for idx, (_, movie) in enumerate(more.iterrows(), start=6):
            genres = parse_genres(movie['genres'])
            genres_text = ", ".join(genres) if isinstance(genres, list) else str(genres)
            vote_avg_imdb = movie['avg_rating_imdb'] if pd.notna(movie['avg_rating_imdb']) else 0
            vote_avg_tmdb = movie['avg_rating_tmdb'] if pd.notna(movie['avg_rating_tmdb']) else 0
            st.markdown(f"""
                <div class="top-list-card">
                    <div class="top-number">{idx}</div>
                        <div class="top-card-content">
                            <img src="{source}{movie['poster_path']}" class="small-poster" />
                            <div class="top-card-text">
                                <div class="movie-title">{movie['title_fr']}</div>
                                <div class="movie-info">⭐ IMDB : {vote_avg_imdb:.1f}/10 · ⭐ TMDb : {vote_avg_tmdb:.1f}/10</div>
                                <div class="movie-info">📅 {movie['startYear']} · {genres_text}</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            if st.button("🎬 Voir détails", key=f"details_{idx}"):
                st.session_state["selected_tconst"] = movie["tconst"]
                st.switch_page("pages/movie_detail.py")
        st.markdown("</div>", unsafe_allow_html=True)

label = "Afficher moins" if st.session_state.show_more else "Afficher plus"
if st.button(label):
    st.session_state.show_more = not st.session_state.show_more
    st.rerun()
print(len(df_popular))  # combien de films en 2026 ?
if st.session_state.show_trailer:

    @st.dialog("🎬 Bande-annonce", width="large")
    def trailer_popup():
        st.video(
            f"https://www.youtube.com/watch?v={st.session_state['trailer']}",
            width=2000
        )

    trailer_popup()

    st.session_state.show_trailer = False

