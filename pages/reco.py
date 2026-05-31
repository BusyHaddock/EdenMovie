import os
import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from app import afficher_barre_navigation, BASE_DIR, local_css

st.set_page_config(
    layout="wide",
    page_title="MOVIEDEN - Recommandation",
    page_icon="🎬"
)
local_css(os.path.join(BASE_DIR, "assets", "style.css"))
afficher_barre_navigation()

st.title("Système de recommandation de films")
st.write("Choisissez un film et découvrez des suggestions similaires 🎬")

# =========================
# CHARGEMENT DES DONNÉES
# =========================
df_movies = pd.read_csv(os.path.join(BASE_DIR, 'data', 'df_film.csv'))
X = pd.read_csv(os.path.join(BASE_DIR, "data", "df_reco_clean.csv"))
X= X.reset_index(drop=True)
df_index = pd.read_csv(os.path.join(BASE_DIR, "data", "df_index.csv"))
df_index = df_index.reset_index(drop=True)

# =========================
# MODÈLE
# =========================
model = NearestNeighbors(n_neighbors=6, metric="cosine")
model.fit(X)

# =========================
# FONCTION RECOMMANDATION
# =========================
def reco_movie(titre_film):
    mask = df_index['title_fr'].str.lower() == titre_film.lower()
    if mask.sum() == 0:
        return None

    tconst = df_index[mask]['tconst'].iloc[0]
    # position numérique dans le df_index
    pos = df_index[df_index['tconst'] == tconst].index[0]

    distances, indices = model.kneighbors(X.loc[[pos]])

    resultats = df_index.iloc[indices[0]]
    resultats = resultats[resultats['tconst'] != tconst]

    # Merge pour récupérer poster et infos d'affichage
    resultats = resultats.merge(
        df_movies[['tconst', 'poster_path', 'genres', 'avg_rating_imdb']],
        on='tconst',
        how='left'
    ).head(5).reset_index(drop=True)

    return resultats

# =========================
# INTERFACE
# =========================
movie_input = st.selectbox(
    "🎬 Choisis un film que tu as aimé :",
    [""] + sorted(df_movies["title_fr"].dropna().unique().tolist())
)

source_img = "https://image.tmdb.org/t/p/w500"

# =========================
# AFFICHAGE
# =========================
if movie_input:
    st.subheader("✨ Films recommandés pour toi :")

    results = reco_movie(movie_input)

    if results is None or results.empty:
        st.warning("Aucune recommandation trouvée pour ce film.")
    else:
        cols = st.columns(5)
        for i, col in enumerate(cols):
            if i < len(results):
                with col:
                    poster = results.loc[i, 'poster_path']
                    if pd.notna(poster) and str(poster).strip():
                        st.image(f"{source_img}{poster}", use_container_width=True)

                    st.markdown(f"**{results.loc[i, 'title_fr']}**")
                    st.caption(f"📅 {results.loc[i, 'startYear']}")

                    note = results.loc[i, 'avg_rating_imdb']
                    if pd.notna(note):
                        st.caption(f"⭐ {note:.1f}/10")

                    if st.button("Voir détails", key=f"reco_{i}"):
                        st.session_state["selected_tconst"] = results.loc[i, 'tconst']
                        st.switch_page("pages/movie_detail.py")
else:
    st.info("👉 Sélectionne un film pour obtenir des recommandations.")