import os
import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors


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



# =========================
# CONFIG PAGE
# =========================
st.set_page_config(page_title="Recommandation", layout="wide")

st.title("Système de recommandation de films")
st.write("Choisissez un film et découvrez des suggestions similaires 🎬")

# =========================
# CHARGEMENT DES DONNÉES
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

df_movies = pd.read_csv(os.path.join(BASE_DIR, "../data/df_final.csv"))
df_ml = pd.read_csv(os.path.join(BASE_DIR, "../data/df_reco_clean.csv"))

df_ml = df_ml.reset_index(drop=True)

# =========================
# MODÈLE 
# =========================
features = df_ml.drop(columns=["id"])
X = features.values

model = NearestNeighbors(n_neighbors=6, metric="cosine")
model.fit(X)

distances, indices = model.kneighbors(X)

# =========================
# FONCTION RECOMMANDATION
# =========================
def reco_movie(movie_title):
    try:
        movie_id = df_movies[df_movies["title"] == movie_title]["id"].values[0]
        idx = df_ml[df_ml["id"] == movie_id].index[0]

        neighbor_ids = df_ml.iloc[indices[idx, 1:]]["id"].values
        recommendations = df_movies[df_movies["id"].isin(neighbor_ids)]

        return recommendations

    except IndexError:
        return pd.DataFrame()

# =========================
# INTERFACE UTILISATEUR
# =========================
movie_input = st.selectbox(
    "🎬 Choisis un film que tu as aimé :",
    [""] + sorted(df_movies["title"].dropna().unique())
)

source_img = "https://image.tmdb.org/t/p/original/"

# =========================
# AFFICHAGE RECOMMANDATIONS
# =========================
if movie_input:

    st.subheader("✨ Films recommandés pour toi :")

    results = reco_movie(movie_input).reset_index(drop=True)

    if results.empty:
        st.warning("Aucune recommandation trouvée pour ce film.")
    else:
        cols = st.columns(5)

        for i, col in enumerate(cols):
            if i < len(results):
                with col:
                    st.image(source_img + results.loc[i, "poster_path"], use_container_width=True)
                    st.markdown(f"**{results.loc[i, 'title']}**")

                    # genres safe
                    genres = results.loc[i, "genres"]
                    try:
                        genres = eval(genres) if isinstance(genres, str) else genres
                        genres = ", ".join(genres) if isinstance(genres, list) else str(genres)
                    except:
                        genres = str(genres)

                    st.caption(genres)
                    st.caption(f"⭐ {results.loc[i, 'vote_average']:.1f}/10")

else:
    st.info("👉 Sélectionne un film pour obtenir des recommandations.")