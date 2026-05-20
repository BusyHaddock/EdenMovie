import streamlit as st
import pandas as pd
import os

# Configuration de la page
st.set_page_config(layout="wide")

# Chargement des données
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

df_movies = pd.read_csv(os.path.join(BASE_DIR, "data", "df_final.csv"))
df_movies = df_movies.head(1000)

# Supporter l'ouverture d'un film depuis la page d'accueil via le paramètre URL `movie_id`
params = st.experimental_get_query_params()
if 'movie_id' in params and 'selected_movie' not in st.session_state:
    try:
        movie_id_param = int(params['movie_id'][0])
        movie_row = df_movies[df_movies['id'] == movie_id_param]
        if not movie_row.empty:
            st.session_state['selected_movie'] = movie_row.iloc[0]
            # Nettoyer les query params pour éviter une boucle et recharger la page
            st.experimental_set_query_params()
            st.experimental_rerun()
    except Exception:
        pass

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

    if "selected_movie" in st.session_state:

        movie = st.session_state["selected_movie"]

        st.markdown("---")

        st.subheader(f"🎬 {movie['title']}")

        col1, col2 = st.columns([1, 2])

        source = "https://image.tmdb.org/t/p/original/"

        with col1:
            st.image(
                f"{source}{movie['poster_path']}",
                use_container_width=True
            )

        with col2:

            st.write(f"⭐ Note : {movie['vote_average']:.1f}/10")

            st.write(f"📅 Date : {movie['release_date']}")

            try:
                genres = eval(movie['genres'])

                if isinstance(genres, list):
                    st.write(f"🎭 Genres : {' • '.join(genres)}")

            except:
                pass

            if 'overview' in movie:
                st.write("### 📝 Synopsis")
                st.write(movie['overview'])

            if "favoris" not in st.session_state:
                st.session_state["favoris"] = []

            if st.button("❤️ Ajouter aux favoris"):
                st.session_state["favoris"].append(movie["title"])
                st.success("Film ajouté aux favoris ❤️")

            if st.button("❌ Fermer les détails"):
                del st.session_state["selected_movie"]
                st.rerun()

    source = "https://image.tmdb.org/t/p/original/"
    cols = st.columns(4)

    for index, (_, movie) in enumerate(results.head(100).iterrows()):

        with cols[index % 4]:

            poster = f"{source}{movie['poster_path']}"

            try:
                genres = eval(movie['genres'])
                genres_text = " • ".join(genres) \
                    if isinstance(genres, list) else ""
            except:
                genres_text = ""

            st.markdown(f"""
            <div class="movie-card">
                <img src="{poster}">
                <div class="movie-title">{movie['title']}</div>
                <div class="movie-info">
                    ⭐ {movie['vote_average']:.1f}/10
                </div>
                <div class="movie-info">
                    📅 {movie['release_date']}
                </div>
                <div class="movie-info">
                    🎭 {genres_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                "🎬 Voir détails",
                key=f"details_{index}"
            ):
                st.session_state["selected_movie"] = movie
                st.rerun()










else:
    st.info("Tapez un titre ou choisissez un genre pour commencer la recherche.")

