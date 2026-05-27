import streamlit as st
import pandas as pd
import os


# Configuration de la page
st.set_page_config(layout="wide")
st.markdown("""
<style>
div[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# Chargement des données
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

df_movies = pd.read_csv(os.path.join(BASE_DIR, "data", "df_final.csv"))

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/style.css")
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

        st.markdown(f"""
            <div class="detail-card">
                <h2>🎬 {movie['title']}</h2>
            </div>
            """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])

        source = "https://image.tmdb.org/t/p/original/"

        with col1:
            st.image(
                f"{source}{movie['poster_path']}",
                use_container_width=True
            )

        with col2:

            st.markdown(f"""
                <div class="movie-detail-info">
                ⭐ <b>Note :</b> {movie['vote_average']:.1f}/10
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class="movie-detail-info">
                📅 <b>Date :</b> {movie['release_date']}
                </div>
                """, unsafe_allow_html=True)

            try:
                genres = eval(movie['genres'])

                if isinstance(genres, list):
                    st.markdown(f"""
                    <div class="movie-detail-info">
                    🎭 <b>Genres :</b> {' • '.join(genres)}
                    </div>
                    """, unsafe_allow_html=True)

            except:
                pass

            if 'overview' in movie:

                st.markdown("""
                <h3 style='margin-top:25px;'>
                📝 Synopsis
                </h3>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="synopsis-box">
                {movie['overview']}
                </div>
                """, unsafe_allow_html=True)

            if "favoris" not in st.session_state:
                st.session_state["favoris"] = []

            if st.button("❤️ Ajouter aux favoris"):
                st.session_state["favoris"].append(movie["title"])
                st.success("Film ajouté aux favoris ❤️")

            if st.button("❌ Fermer les détails"):
                del st.session_state["selected_movie"]
                st.rerun()

    source = "https://image.tmdb.org/t/p/original/"

# Pagination
films_par_page = 20

total_pages = (len(results) - 1) // films_par_page + 1

if "page" not in st.session_state:
    st.session_state["page"] = 1

col_prev, col_page, col_next = st.columns([1, 2, 1])

with col_prev:
    if st.button("⬅️ Précédent") and st.session_state["page"] > 1:
        st.session_state["page"] -= 1
        st.rerun()

with col_page:
    st.markdown(
        f"<h4 style='text-align:center;'>Page {st.session_state['page']} / {total_pages}</h4>",
        unsafe_allow_html=True
    )

with col_next:
    if st.button("Suivant ➡️") and st.session_state["page"] < total_pages:
        st.session_state["page"] += 1
        st.rerun()

page = st.session_state["page"]

start = (page - 1) * films_par_page
end = start + films_par_page

results_page = results.iloc[start:end]

st.write(f"Page {page} / {total_pages}")

cols = st.columns(5)

for index, (_, movie) in enumerate(results_page.iterrows()):

        with cols[index % 5]:
            source = "https://image.tmdb.org/t/p/original/"
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

