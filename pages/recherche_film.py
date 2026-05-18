import streamlit as st
import pandas as pd
import os

# Configuration de la page
st.set_page_config(layout="wide")
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

# Chargement des données
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

df_movies = pd.read_csv(os.path.join(BASE_DIR, "data", "df_final.csv"))
df_movies = df_movies.head(1000)

all_genres = []

for genres in df_movies["genres"].dropna():

    try:
        genres_list = eval(genres)

        if isinstance(genres_list, list):

            all_genres.extend(genres_list)

    except:
        pass

# Supprimer les doublons et trier
all_genres = sorted(list(set(all_genres)))
def movie_has_genre(genres, selected_genre):
    try:
        genres_list = eval(genres)

        if isinstance(genres_list, list):
            return selected_genre in genres_list

    except:
        return False

    return False

# Titre
st.title("🔍 Recherche de films")

st.write("Recherchez vos films préférés")

# Barre de recherche
search = st.text_input(
    "Entrez un nom de film",
    placeholder="Exemple : Batman"
)
# Filtre genre
selected_genre = st.selectbox(
    "🎭 Filtrer par genre",
    ["Tous"] + all_genres
)
# Filtrage
results = df_movies.copy()

if search:
    results = results[
        results["title"].str.contains(search, case=False, na=False)
    ]

if selected_genre != "Tous":
    results = results[
        results["genres"].apply(
            lambda genres: selected_genre in genres
            if pd.notna(genres)
            else False
        )
    ]

# Afficher seulement si l'utilisateur a fait une recherche ou choisi un genre
if search or selected_genre != "Tous":

    st.write(f"{len(results)} résultat(s) trouvé(s)")

    source = "https://image.tmdb.org/t/p/original/"
    cols = st.columns(4)

    for index, (_, movie) in enumerate(results.head(100).iterrows()):

        with cols[index % 4]:

            st.image(
                f"{source}{movie['poster_path']}",
                use_container_width=True
            )

            st.markdown(f"### {movie['title']}")
            st.write(f"⭐ {movie['vote_average']:.1f}/10")
            st.caption(f"📅 {movie['release_date']}")

            try:
                genres = eval(movie['genres'])
                if isinstance(genres, list):
                    st.caption(" • ".join(genres))
            except:
                pass

else:
    st.info("Tapez un titre ou choisissez un genre pour commencer la recherche.")