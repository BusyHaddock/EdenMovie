import streamlit as st
import pandas as pd
import os

# EN PREMIER avant tout
st.set_page_config(layout="wide")

# Ensuite seulement les imports locaux
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import afficher_barre_navigation
from app import BASE_DIR

# Import du CSS
from app import local_css

local_css(os.path.join(BASE_DIR, "assets", "style.css"))  # ← chemin absolu

# Masquer sidebar Streamlit par défaut
st.markdown("""
    <style>
    div[data-testid="stSidebarNav"] { display: none; }
    </style>
""", unsafe_allow_html=True)

afficher_barre_navigation()


# Chargement données
@st.cache_data
def load_data():
    df_film = pd.read_csv(os.path.join(BASE_DIR, "data", "df_film.csv"))
    df_intervenants = pd.read_csv(os.path.join(BASE_DIR, "data", "df_intervenant.csv"))
    df_principals = pd.read_csv(os.path.join(BASE_DIR, "data", "df_principals.csv"))
    return df_film, df_intervenants, df_principals

df_film, df_intervenants, df_principals = load_data()

# Récupération du tconst depuis l'URL
tconst = st.session_state.get("selected_tconst", None)

if not tconst:
    st.error("Aucun film sélectionné.")
    if st.button("← Retour à la recherche"):
        st.switch_page("pages/recherche_film.py")
    st.stop()

# Filtrage du film
film_row = df_film[df_film["tconst"] == tconst]

if film_row.empty:
    st.error(f"Film introuvable : {tconst}")
    if st.button("← Retour à la recherche"):
        st.switch_page("pages/recherche_film.py")
    st.stop()

film = film_row.iloc[0]

# --- Affichage ---
st.title(film.get("title_fr") or film.get("primaryTitle"))

# Bouton retour en haut
if st.button("← Retour à la recherche"):
    st.switch_page("pages/recherche_film.py")

# Contenu principal
col1, col2 = st.columns([1, 2])

with col1:
    if pd.notna(film.get("poster_path")):
        st.image(f"https://image.tmdb.org/t/p/w500{film['poster_path']}", use_container_width=True)

with col2:
    st.markdown(f"⭐ **Note :** {film.get('avg_rating_imdb', 'N/A')}/10")
    st.markdown(f"📅 **Année :** {film.get('startYear', 'N/A')}")
    st.markdown(f"⏱️ **Durée :** {film.get('runtimeMinutes', 'N/A')} min")
    st.markdown(f"🎭 **Genres :** {film.get('genres', 'N/A')}")
    st.markdown(f"🔞 **Certification :** - {film.get('certification_fr', 'N/A')} ans")

    if pd.notna(film.get("overview")):
        st.markdown("### 📝 Synopsis")
        st.write(film["overview"])

    # Bande annonce
    if pd.notna(film.get("trailer_key")):
        if st.button("🎬 Voir la bande annonce"):
            
            @st.dialog("🎬 Bande-annonce", width="large")
            def trailer_popup():
                st.video(f"https://www.youtube.com/watch?v={film['trailer_key']}")
            
            trailer_popup()

# --- Casting ---
st.markdown("---")

# Merge principals + intervenants pour ce film
principals_film = df_principals[df_principals["tconst"] == tconst]

casting = principals_film.merge(
    df_intervenants[["nconst", "primaryName", "profile_path"]],
    on="nconst",
    how="left"
)

def get_photo(profile_path):
    if pd.notna(profile_path) and str(profile_path).strip() and str(profile_path) != "\\N":
        return f"https://image.tmdb.org/t/p/w185{profile_path}"
    return os.path.join(BASE_DIR, "assets", "uploads", "unknow_pp.jpg")

casting["image_src"] = casting["profile_path"].apply(get_photo)

# Réalisateur(s)
directors = casting[casting["category"] == "director"]

if not directors.empty:
    st.markdown("### 🎬 Réalisateur(s)")
    dir_cols = st.columns(min(4, len(directors)))
    for idx, (_, director) in enumerate(directors.iterrows()):
        with dir_cols[idx % len(dir_cols)]:
            st.image(director["image_src"], width=150)
            st.markdown(f"**{director.get('primaryName', 'Inconnu')}**")

st.markdown("---")

# Acteurs
actors = casting[casting["category"].isin(["actor", "actress"])]
actors = actors[actors["profile_path"].apply(
    lambda x: pd.notna(x) and str(x).strip() not in ["", "\\N"]
)].head(10)

if not actors.empty:
    st.markdown("### 🎭 Acteurs")
    act_cols = st.columns(5)
    for idx, (_, actor) in enumerate(actors.iterrows()):
        with act_cols[idx % 5]:
            st.image(actor["image_src"], width=150)
            st.markdown(f"**{actor.get('primaryName', 'Inconnu')}**")
            # Personnage joué si disponible
            if pd.notna(actor.get("characters")) and str(actor["characters"]) != "\\N":
                st.caption(str(actor["characters"]).strip('[]"\''))

st.markdown("---")

# Bouton retour en bas
if st.button("← Retour à la recherche", key="retour_bas"):
    st.switch_page("pages/recherche_film.py")
